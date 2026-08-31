#!/usr/bin/env python3
"""Adversarial tests for total/disjoint obligation residualization."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDUALIZE = ROOT / "tools" / "residualize.py"
SCHEMA = ROOT / "contracts" / "obligation.schema.json"

STATES = ["SATISFIED", "UNSATISFIED", "CONTRADICTED", "UNKNOWN", "NOT_APPLICABLE"]


def invoke(payload: dict) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(payload, fh)
        fh.write("\n")
        path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(RESIDUALIZE), "--input", str(path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    if result.returncode != 0:
        raise AssertionError(f"residualize failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def obligation(oid: str, state: str, *, scope: str | None = None, proposition: str | None = None) -> dict:
    return {
        "obligation_id": oid,
        "proposition": proposition or f"proposition {oid}",
        "scope": scope or f"scope.{oid}",
        "state": state,
        "basis_ids": [f"basis-{oid}"],
    }


def test_partition_is_total_and_disjoint() -> None:
    for path in (RESIDUALIZE, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    rows = [obligation(f"o-{state.lower()}", state) for state in STATES]
    payload = invoke({"obligations": rows, "equivalence_witnesses": []})
    seen: list[str] = []
    for state in STATES:
        ids = payload["partitions"][state]
        assert len(ids) == 1, payload
        seen.extend(ids)
    assert sorted(seen) == sorted(row["obligation_id"] for row in rows), payload
    assert len(seen) == len(set(seen)), payload


def test_only_unsatisfied_becomes_todo_candidate() -> None:
    rows = [obligation(f"o{i}", state) for i, state in enumerate(STATES)]
    payload = invoke({"obligations": rows, "equivalence_witnesses": []})
    assert payload["todo_candidates"] == ["o1"], payload
    assert "o2" not in payload["todo_candidates"], payload
    assert "o3" not in payload["todo_candidates"], payload


def test_unknown_and_contradicted_never_executable() -> None:
    payload = invoke({
        "obligations": [
            obligation("u", "UNKNOWN"),
            obligation("c", "CONTRADICTED"),
            obligation("x", "UNSATISFIED"),
        ],
        "equivalence_witnesses": [],
    })
    assert payload["todo_candidates"] == ["x"], payload
    assert payload["blocked_frontier"]["UNKNOWN"] == ["u"], payload
    assert payload["blocked_frontier"]["CONTRADICTED"] == ["c"], payload


def test_duplicate_claims_do_not_merge_without_equivalence_witness() -> None:
    a = obligation("a", "UNSATISFIED", scope="same", proposition="same claim")
    b = obligation("b", "UNSATISFIED", scope="same", proposition="same claim")
    payload = invoke({"obligations": [a, b], "equivalence_witnesses": []})
    assert payload["todo_candidates"] == ["a", "b"], payload
    assert payload["equivalence_groups"] == [], payload


def test_explicit_equivalence_witness_collapses_duplicate_residual() -> None:
    a = obligation("a", "UNSATISFIED", scope="same", proposition="same claim")
    b = obligation("b", "UNSATISFIED", scope="same", proposition="same claim")
    payload = invoke({
        "obligations": [a, b],
        "equivalence_witnesses": [{
            "witness_id": "eq-1",
            "obligation_ids": ["a", "b"],
            "scope": "same",
            "proposition": "same claim",
            "basis_ids": ["proof-eq-1"]
        }]
    })
    assert payload["todo_candidates"] == ["a"], payload
    assert payload["equivalence_groups"] == [{"canonical_id": "a", "member_ids": ["a", "b"], "witness_id": "eq-1"}], payload


def test_equivalence_witness_cannot_merge_changed_scope() -> None:
    a = obligation("a", "UNSATISFIED", scope="scope.a", proposition="same claim")
    b = obligation("b", "UNSATISFIED", scope="scope.b", proposition="same claim")
    payload = invoke({
        "obligations": [a, b],
        "equivalence_witnesses": [{
            "witness_id": "bad-eq",
            "obligation_ids": ["a", "b"],
            "scope": "scope.a",
            "proposition": "same claim",
            "basis_ids": ["proof"]
        }]
    })
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "INVALID_EQUIVALENCE_WITNESS", payload
    assert payload["todo_candidates"] == [], payload


def test_invalid_state_blocks_instead_of_guessing_partition() -> None:
    payload = invoke({"obligations": [obligation("bad", "MAYBE")], "equivalence_witnesses": []})
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "INVALID_OBLIGATION_STATE", payload
    assert payload["todo_candidates"] == [], payload


def test_input_permutation_is_deterministic() -> None:
    a = obligation("a", "UNSATISFIED")
    b = obligation("b", "UNKNOWN")
    first = invoke({"obligations": [a, b], "equivalence_witnesses": []})
    second = invoke({"obligations": [b, a], "equivalence_witnesses": []})
    assert first == second, (first, second)


def main() -> int:
    tests = [
        test_partition_is_total_and_disjoint,
        test_only_unsatisfied_becomes_todo_candidate,
        test_unknown_and_contradicted_never_executable,
        test_duplicate_claims_do_not_merge_without_equivalence_witness,
        test_explicit_equivalence_witness_collapses_duplicate_residual,
        test_equivalence_witness_cannot_merge_changed_scope,
        test_invalid_state_blocks_instead_of_guessing_partition,
        test_input_permutation_is_deterministic,
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
