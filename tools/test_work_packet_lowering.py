#!/usr/bin/env python3
"""Adversarial tests for frontier-resolved WorkPacket lowering."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "tools" / "lower_work_packet.py"
SCHEMA = ROOT / "contracts" / "work-packet.schema.json"


def base_input() -> dict:
    return {
        "current_head": "head-001",
        "obligation": {
            "obligation_id": "obl-1",
            "state": "UNSATISFIED",
            "objective": "Make the API build invariant true.",
            "basis_ids": ["diag-1"]
        },
        "recipe": {
            "recipe_id": "repair.build.api.compile",
            "selected_strategy": "repair-build-api",
            "strategy_options": ["repair-build-api"],
            "write_set": ["src/api.py", "tests/api_test.py"],
            "verification_oracle_id": "oracle.build.api.compile",
            "recovery": "Revert declared write set and return failing oracle output.",
            "authority_required": None,
            "authority_effect": "candidate_only"
        },
        "execution_contract": {
            "basis_head": "head-001",
            "read_set": ["src/api.py", "tests/api_test.py"],
            "allowed_write_set": ["src/api.py", "tests/api_test.py"],
            "failure_route": "STOP_AND_EMIT_FAILURE_RECEIPT",
            "authority": "candidate",
            "undefined_terms": []
        }
    }


def invoke(payload: dict) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(payload, fh)
        fh.write("\n")
        path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(LOWER), "--input", str(path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    if result.returncode != 0:
        raise AssertionError(f"lowering failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def assert_rejected(mutator, status: str, reason: str) -> None:
    payload = base_input()
    mutator(payload)
    out = invoke(payload)
    assert out["status"] == status, out
    assert out["reason"] == reason, out
    assert out.get("packet") is None, out


def test_complete_contract_lowers_to_simple_executor_packet() -> None:
    for path in (LOWER, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")
    out = invoke(base_input())
    assert out["status"] == "READY", out
    packet = out["packet"]
    assert packet["history_head"] == "head-001", packet
    assert packet["obligation_id"] == "obl-1", packet
    assert packet["selected_strategy"] == "repair-build-api", packet
    assert packet["verification_oracle_id"] == "oracle.build.api.compile", packet
    assert packet["execution_grammar"] == ["READ", "CHECK", "CHANGE", "VERIFY", "RECEIPT", "STOP"], packet
    assert all(value == 0 for value in packet["reasoning_debt"].values()), packet


def test_unknown_obligation_never_lowers() -> None:
    assert_rejected(lambda p: p["obligation"].update(state="UNKNOWN"), "BLOCKED", "OBLIGATION_NOT_EXECUTABLE")


def test_missing_oracle_rejected() -> None:
    assert_rejected(lambda p: p["recipe"].pop("verification_oracle_id"), "BLOCKED", "MISSING_VERIFICATION_ORACLE")


def test_multiple_strategy_options_rejected() -> None:
    assert_rejected(lambda p: p["recipe"].update(strategy_options=["a", "b"]), "BLOCKED", "UNRESOLVED_STRATEGY")


def test_widened_write_set_rejected() -> None:
    assert_rejected(lambda p: p["recipe"]["write_set"].append("unrelated/config.py"), "BLOCKED", "WRITE_SET_OUTSIDE_ALLOWED_SCOPE")


def test_stale_head_rejected() -> None:
    assert_rejected(lambda p: p["execution_contract"].update(basis_head="head-old"), "STALE", "HISTORY_HEAD_CHANGED")


def test_missing_failure_route_rejected() -> None:
    assert_rejected(lambda p: p["execution_contract"].pop("failure_route"), "BLOCKED", "MISSING_FAILURE_ROUTE")


def test_missing_authority_rejected() -> None:
    def mutate(p: dict) -> None:
        p["recipe"]["authority_required"] = "human_exact_action"
        p["execution_contract"]["authority"] = "candidate"
    assert_rejected(mutate, "BLOCKED", "AUTHORITY_REQUIRED")


def test_undefined_semantic_term_rejected() -> None:
    assert_rejected(lambda p: p["execution_contract"].update(undefined_terms=["safe-enough"]), "BLOCKED", "UNRESOLVED_SEMANTIC_TERMS")


def test_missing_read_set_rejected() -> None:
    assert_rejected(lambda p: p["execution_contract"].pop("read_set"), "BLOCKED", "MISSING_READ_SET")


def test_input_permutation_is_deterministic() -> None:
    first = invoke(base_input())
    value = base_input()
    value["execution_contract"]["read_set"].reverse()
    value["execution_contract"]["allowed_write_set"].reverse()
    value["recipe"]["write_set"].reverse()
    second = invoke(value)
    assert first == second, (first, second)


def main() -> int:
    tests = [
        test_complete_contract_lowers_to_simple_executor_packet,
        test_unknown_obligation_never_lowers,
        test_missing_oracle_rejected,
        test_multiple_strategy_options_rejected,
        test_widened_write_set_rejected,
        test_stale_head_rejected,
        test_missing_failure_route_rejected,
        test_missing_authority_rejected,
        test_undefined_semantic_term_rejected,
        test_missing_read_set_rejected,
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
