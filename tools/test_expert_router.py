#!/usr/bin/env python3
"""Contract tests for deterministic expert routing precedence."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "tools" / "expert_router.py"
POLICY = ROOT / "routing" / "precedence.json"
SCHEMA = ROOT / "contracts" / "route-decision.schema.json"


def route(problem: dict, catalog: dict) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        problem_path = root / "problem.json"
        catalog_path = root / "catalog.json"
        problem_path.write_text(json.dumps(problem) + "\n", encoding="utf-8")
        catalog_path.write_text(json.dumps(catalog) + "\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(ROUTER),
                "--problem",
                str(problem_path),
                "--catalog",
                str(catalog_path),
                "--json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(f"router failed: stdout={result.stdout} stderr={result.stderr}")
        return json.loads(result.stdout)


def require_artifacts() -> None:
    for path in (ROUTER, POLICY, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")


def test_exact_result_beats_model() -> None:
    require_artifacts()
    payload = route(
        {"problem_id": "p1", "signature": "sig-known"},
        {
            "exact_results": {"sig-known": {"result_ref": "RES-1"}},
            "negative_memos": {},
            "compiled_rules": {},
            "semantic_search": {"available": True, "complete": True},
            "model_fallback": {"available": True},
        },
    )
    assert payload["route"] == "EXACT_RESULT", payload
    assert payload["selected_ref"] == "RES-1", payload
    assert payload["model_invocation_allowed"] is False, payload


def test_negative_memo_beats_semantic_and_model() -> None:
    payload = route(
        {"problem_id": "p2", "signature": "sig-bad"},
        {
            "exact_results": {},
            "negative_memos": {"sig-bad": {"memo_ref": "NEG-9"}},
            "compiled_rules": {},
            "semantic_search": {"available": True, "complete": True},
            "model_fallback": {"available": True},
        },
    )
    assert payload["route"] == "NEGATIVE_MEMO", payload
    assert payload["selected_ref"] == "NEG-9", payload
    assert payload["model_invocation_allowed"] is False, payload


def test_compiled_rule_beats_model() -> None:
    payload = route(
        {"problem_id": "p3", "signature": "sig-rule"},
        {
            "exact_results": {},
            "negative_memos": {},
            "compiled_rules": {"sig-rule": {"rule_ref": "RULE-4"}},
            "semantic_search": {"available": True, "complete": True},
            "model_fallback": {"available": True},
        },
    )
    assert payload["route"] == "COMPILED_RULE", payload
    assert payload["selected_ref"] == "RULE-4", payload
    assert payload["model_invocation_allowed"] is False, payload


def test_incomplete_search_miss_stays_unknown() -> None:
    payload = route(
        {"problem_id": "p4", "signature": "sig-missing"},
        {
            "exact_results": {},
            "negative_memos": {},
            "compiled_rules": {},
            "semantic_search": {"available": True, "complete": False, "hits": []},
            "model_fallback": {"available": True},
        },
    )
    assert payload["route"] == "SEARCH_INCOMPLETE", payload
    assert payload["verdict"] == "UNKNOWN", payload
    assert payload["model_invocation_allowed"] is False, payload


def test_model_only_after_deterministic_miss_and_complete_search() -> None:
    payload = route(
        {"problem_id": "p5", "signature": "sig-novel"},
        {
            "exact_results": {},
            "negative_memos": {},
            "compiled_rules": {},
            "semantic_search": {"available": True, "complete": True, "hits": []},
            "model_fallback": {"available": True},
        },
    )
    assert payload["route"] == "MODEL_CANDIDATE", payload
    assert payload["verdict"] == "UNKNOWN", payload
    assert payload["model_invocation_allowed"] is True, payload
    assert payload["authority_effect"] == "candidate_only", payload


def main() -> int:
    tests = [
        test_exact_result_beats_model,
        test_negative_memo_beats_semantic_and_model,
        test_compiled_rule_beats_model,
        test_incomplete_search_miss_stays_unknown,
        test_model_only_after_deterministic_miss_and_complete_search,
    ]
    failures = []
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
