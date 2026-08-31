#!/usr/bin/env python3
"""Adversarial tests for unresolved discovery and discriminating-witness selection."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCOVER = ROOT / "tools" / "discover.py"
SCHEMA = ROOT / "contracts" / "unresolved.schema.json"


def invoke(payload: dict) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(payload, fh)
        fh.write("\n")
        path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(DISCOVER), "--input", str(path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    if result.returncode != 0:
        raise AssertionError(f"discover failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def unresolved(**overrides: object) -> dict:
    value = {
        "unresolved_id": "u-1",
        "problem_id": "p-1",
        "state": "UNKNOWN",
        "rivals": [
            {"rival_id": "r-a", "claim": "dependency missing", "status": "LIVE"},
            {"rival_id": "r-b", "claim": "compiler regression", "status": "LIVE"},
        ],
        "exact_cases": [],
        "search_complete": True,
        "reviewer_consensus": None,
        "witness_candidates": [],
    }
    value.update(overrides)
    return value


def test_exact_prior_case_preempts_generation() -> None:
    for path in (DISCOVER, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    payload = invoke(unresolved(exact_cases=[{"case_id": "case-7", "outcome": "dependency missing", "receipt": "receipt-7"}]))
    assert payload["status"] == "EXACT_CASE", payload
    assert payload["route"] == "EXACT_PRIOR_CASE", payload
    assert payload["case_id"] == "case-7", payload
    assert payload["model_candidate_allowed"] is False, payload


def test_incomplete_search_cannot_establish_novelty() -> None:
    payload = invoke(unresolved(search_complete=False))
    assert payload["status"] == "UNKNOWN", payload
    assert payload["reason"] == "SEARCH_INCOMPLETE", payload
    assert payload["novelty_established"] is False, payload
    assert payload["model_candidate_allowed"] is False, payload


def test_reviewer_consensus_does_not_collapse_rivals() -> None:
    payload = invoke(unresolved(reviewer_consensus={"selected_rival_id": "r-a", "reviewers": 12}))
    assert payload["status"] == "UNKNOWN", payload
    assert payload["live_rival_ids"] == ["r-a", "r-b"], payload
    assert payload["consensus_used_as_evidence"] is False, payload


def test_unsafe_witness_is_rejected_by_ruin_guard() -> None:
    payload = invoke(unresolved(witness_candidates=[
        {
            "witness_id": "w-danger",
            "distinguishes": ["r-a", "r-b"],
            "cost_rank": 0,
            "operation": {"operation_id": "danger", "kind": "shell", "command": "rm -rf ./src"}
        },
        {
            "witness_id": "w-safe",
            "distinguishes": ["r-a", "r-b"],
            "cost_rank": 1,
            "operation": {"operation_id": "safe", "kind": "shell", "command": "git status --short"}
        }
    ]))
    assert payload["status"] == "WITNESS_SELECTED", payload
    assert payload["witness_id"] == "w-safe", payload
    assert payload["rejected_witnesses"] == [{"witness_id": "w-danger", "reason": "RUIN_GUARD"}], payload


def test_live_rival_may_not_disappear_without_evidence() -> None:
    payload = invoke(unresolved(rivals=[{"rival_id": "r-a", "claim": "dependency missing", "status": "LIVE"}]))
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "INSUFFICIENT_RIVALS", payload


def test_safe_witness_selected_by_explicit_rank_not_model_preference() -> None:
    payload = invoke(unresolved(witness_candidates=[
        {
            "witness_id": "w-2",
            "distinguishes": ["r-a", "r-b"],
            "cost_rank": 2,
            "operation": {"operation_id": "safe-2", "kind": "read", "target": "README.md"}
        },
        {
            "witness_id": "w-1",
            "distinguishes": ["r-a", "r-b"],
            "cost_rank": 1,
            "operation": {"operation_id": "safe-1", "kind": "shell", "command": "git status --short"}
        }
    ]))
    assert payload["status"] == "WITNESS_SELECTED", payload
    assert payload["witness_id"] == "w-1", payload


def test_no_witness_after_complete_search_allows_candidate_only_generation() -> None:
    payload = invoke(unresolved())
    assert payload["status"] == "UNKNOWN", payload
    assert payload["reason"] == "NO_DECISIVE_WITNESS", payload
    assert payload["model_candidate_allowed"] is True, payload
    assert payload["allowed_candidate_outputs"] == ["checker", "representation", "recipe", "rule", "witness"], payload


def main() -> int:
    tests = [
        test_exact_prior_case_preempts_generation,
        test_incomplete_search_cannot_establish_novelty,
        test_reviewer_consensus_does_not_collapse_rivals,
        test_unsafe_witness_is_rejected_by_ruin_guard,
        test_live_rival_may_not_disappear_without_evidence,
        test_safe_witness_selected_by_explicit_rank_not_model_preference,
        test_no_witness_after_complete_search_allows_candidate_only_generation,
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
