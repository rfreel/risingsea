#!/usr/bin/env python3
"""Adversarial contract tests for deterministic expert diagnosis."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSE = ROOT / "tools" / "diagnose.py"
RULES = ROOT / "diagnostics" / "rules.json"
SCHEMA = ROOT / "contracts" / "diagnostic-receipt.schema.json"


def observation(obs_id: str, proposition: str, scope: str, value: object, *, current: bool = True) -> dict:
    return {
        "observation_id": obs_id,
        "proposition": proposition,
        "scope": scope,
        "value": value,
        "source_class": "HOST_OBSERVED",
        "authority": "observation",
        "provenance": {"kind": "fixture", "ref": obs_id, "digest": f"sha256:{obs_id}"},
        "freshness": "CURRENT" if current else "STALE",
        "observed_at": "2026-08-31T23:00:00Z",
        "current_for_decision": current,
        "digest": f"sha256:{obs_id.zfill(64)[:64]}"
    }


def invoke(problem: dict, accepted: list[dict], contradictions: list[dict] | None = None) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        p_problem = base / "problem.json"
        p_obs = base / "observations.json"
        p_problem.write_text(json.dumps(problem) + "\n", encoding="utf-8")
        p_obs.write_text(json.dumps({
            "schema": "risingsea.accepted-observation-set.v1",
            "accepted": accepted,
            "rejected": [],
            "contradictions": contradictions or []
        }) + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(DIAGNOSE), "--problem", str(p_problem), "--observations", str(p_obs), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        raise AssertionError(f"diagnose failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def test_required_false_is_defect() -> None:
    for path in (DIAGNOSE, RULES, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    payload = invoke(
        {"problem_id": "p1", "domain": "build", "rule_ids": ["build.api.compiles"]},
        [observation("o1", "build.target.api compiles", "build.target.api", False)],
    )
    assert payload["verdict"] == "DEFECT", payload
    assert payload["rule_ids"] == ["build.api.compiles"], payload
    assert payload["observation_ids"] == ["o1"], payload


def test_required_true_is_satisfied() -> None:
    payload = invoke(
        {"problem_id": "p2", "domain": "build", "rule_ids": ["build.api.compiles"]},
        [observation("o2", "build.target.api compiles", "build.target.api", True)],
    )
    assert payload["verdict"] == "SATISFIED", payload


def test_missing_required_observation_is_evidence_gap() -> None:
    payload = invoke({"problem_id": "p3", "domain": "build", "rule_ids": ["build.api.compiles"]}, [])
    assert payload["verdict"] == "EVIDENCE_GAP", payload
    assert payload["missing"] == ["build.target.api compiles@build.target.api"], payload


def test_contradiction_dominates_satisfaction() -> None:
    obs = [
        observation("o3a", "build.target.api compiles", "build.target.api", True),
        observation("o3b", "build.target.api compiles", "build.target.api", False),
    ]
    contradiction = [{"scope": "build.target.api", "proposition": "build.target.api compiles", "observation_ids": ["o3a", "o3b"]}]
    payload = invoke({"problem_id": "p4", "domain": "build", "rule_ids": ["build.api.compiles"]}, obs, contradiction)
    assert payload["verdict"] == "CONTRADICTED", payload


def test_blocking_rule_produces_blocked() -> None:
    payload = invoke(
        {"problem_id": "p5", "domain": "build", "rule_ids": ["build.api.compiles", "build.toolchain.available"]},
        [
            observation("o4", "build.target.api compiles", "build.target.api", True),
            observation("o5", "build.toolchain available", "build.toolchain", False),
        ],
    )
    assert payload["verdict"] == "BLOCKED", payload
    assert "build.toolchain.available" in payload["rule_ids"], payload


def test_no_deciding_rule_is_unknown() -> None:
    payload = invoke({"problem_id": "p6", "domain": "novel", "rule_ids": []}, [])
    assert payload["verdict"] == "UNKNOWN", payload


def test_model_candidate_cannot_override_defect() -> None:
    payload = invoke(
        {
            "problem_id": "p7",
            "domain": "build",
            "rule_ids": ["build.api.compiles"],
            "model_candidates": [{"verdict": "SATISFIED", "reason": "looks fine"}]
        },
        [observation("o7", "build.target.api compiles", "build.target.api", False)],
    )
    assert payload["verdict"] == "DEFECT", payload
    assert payload["model_candidates_considered"] == 0, payload


def test_stale_true_observation_cannot_satisfy_current_rule() -> None:
    payload = invoke(
        {"problem_id": "p8", "domain": "build", "rule_ids": ["build.api.compiles"]},
        [observation("o8", "build.target.api compiles", "build.target.api", True, current=False)],
    )
    assert payload["verdict"] == "EVIDENCE_GAP", payload


def test_unknown_rule_id_does_not_synthesize_semantics() -> None:
    payload = invoke({"problem_id": "p9", "domain": "build", "rule_ids": ["invented.rule"]}, [])
    assert payload["verdict"] == "UNKNOWN", payload
    assert payload["unknown_rule_ids"] == ["invented.rule"], payload


def main() -> int:
    tests = [
        test_required_false_is_defect,
        test_required_true_is_satisfied,
        test_missing_required_observation_is_evidence_gap,
        test_contradiction_dominates_satisfaction,
        test_blocking_rule_produces_blocked,
        test_no_deciding_rule_is_unknown,
        test_model_candidate_cannot_override_defect,
        test_stale_true_observation_cannot_satisfy_current_rule,
        test_unknown_rule_id_does_not_synthesize_semantics,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failures.append(f"{test.__name__}: {exc}")
            print(f"FAIL {test.__name__}: {exc}", file=sys.stderr)
    if failures:
        print(f"FAILED {len(failures)}/{len(tests)}", file=sys.stderr)
        return 1
    print(f"PASS {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
