#!/usr/bin/env python3
"""Adversarial contract tests for accepted observation admission."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIT = ROOT / "tools" / "admit_observations.py"
SCHEMA = ROOT / "contracts" / "accepted-observation.schema.json"
RULES = ROOT / "diagnostics" / "observation-rules.json"


def invoke(candidates: list[dict]) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump({"candidates": candidates}, fh)
        fh.write("\n")
        path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(ADMIT), "--input", str(path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    if result.returncode != 0:
        raise AssertionError(f"admitter failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def base_candidate(**overrides: object) -> dict:
    row = {
        "observation_id": "obs-001",
        "proposition": "build.target.api compiles",
        "scope": "build.target.api",
        "value": True,
        "source_class": "HOST_OBSERVED",
        "authority": "observation",
        "provenance": {"kind": "command", "ref": "cargo check -p api", "digest": "sha256:abc"},
        "freshness": "CURRENT",
        "observed_at": "2026-08-31T23:00:00Z",
    }
    row.update(overrides)
    return row


def test_valid_observation_is_accepted_and_digest_bound() -> None:
    for path in (ADMIT, SCHEMA, RULES):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    payload = invoke([base_candidate()])
    assert payload["schema"] == "risingsea.accepted-observation-set.v1", payload
    assert len(payload["accepted"]) == 1, payload
    row = payload["accepted"][0]
    assert row["observation_id"] == "obs-001"
    assert row["digest"].startswith("sha256:")
    assert payload["rejected"] == []


def test_model_assertion_never_becomes_authoritative_observation() -> None:
    payload = invoke([
        base_candidate(
            observation_id="model-001",
            source_class="MODEL_CANDIDATE",
            authority="candidate",
            provenance={"kind": "model", "ref": "proposal-7", "digest": "sha256:model"},
        )
    ])
    assert payload["accepted"] == [], payload
    assert payload["rejected"][0]["reason"] == "MODEL_CANDIDATE_NOT_OBSERVATION", payload


def test_missing_provenance_is_rejected() -> None:
    row = base_candidate(observation_id="obs-no-prov")
    row.pop("provenance")
    payload = invoke([row])
    assert payload["accepted"] == [], payload
    assert payload["rejected"][0]["reason"] == "MISSING_PROVENANCE", payload


def test_stale_evidence_remains_explicit_not_current() -> None:
    payload = invoke([base_candidate(observation_id="obs-stale", freshness="STALE")])
    assert len(payload["accepted"]) == 1, payload
    row = payload["accepted"][0]
    assert row["freshness"] == "STALE", row
    assert row["current_for_decision"] is False, row


def test_contradictory_observations_are_preserved() -> None:
    yes = base_candidate(observation_id="obs-yes", value=True)
    no = base_candidate(observation_id="obs-no", value=False, provenance={"kind": "command", "ref": "cargo check -p api # second host", "digest": "sha256:def"})
    payload = invoke([yes, no])
    assert len(payload["accepted"]) == 2, payload
    assert payload["contradictions"] == [{"scope": "build.target.api", "proposition": "build.target.api compiles", "observation_ids": ["obs-no", "obs-yes"]}], payload


def test_output_is_deterministic_under_input_permutation() -> None:
    a = base_candidate(observation_id="obs-a", proposition="a", scope="a")
    b = base_candidate(observation_id="obs-b", proposition="b", scope="b")
    first = invoke([a, b])
    second = invoke([b, a])
    assert first == second, (first, second)


def main() -> int:
    tests = [
        test_valid_observation_is_accepted_and_digest_bound,
        test_model_assertion_never_becomes_authoritative_observation,
        test_missing_provenance_is_rejected,
        test_stale_evidence_remains_explicit_not_current,
        test_contradictory_observations_are_preserved,
        test_output_is_deterministic_under_input_permutation,
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
