#!/usr/bin/env python3
"""Adversarial contract fixtures for the Rising Sea RuinGuard boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "tools" / "ruin_guard.py"
RULES = ROOT / "guard" / "ruin-classes.json"
DONOR = ROOT / "infrastructure" / "donors" / "destructive-command-guard.json"
SCHEMA = ROOT / "contracts" / "ruin-class.schema.json"


def require_artifacts() -> None:
    for path in (GUARD, RULES, DONOR, SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")


def decide(operation: object) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(operation, fh)
        fh.write("\n")
        input_path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(GUARD), "--operation", str(input_path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        input_path.unlink(missing_ok=True)
    if result.returncode not in (0, 2):
        raise AssertionError(f"unexpected guard exit {result.returncode}: {result.stdout}\n{result.stderr}")
    return json.loads(result.stdout)


def assert_not_allow(label: str, operation: object) -> dict:
    payload = decide(operation)
    if payload.get("decision") == "ALLOW":
        raise AssertionError(f"{label}: ruin candidate was allowed: {payload}")
    if payload.get("decision") not in {"BLOCK", "REVIEW_REQUIRED"}:
        raise AssertionError(f"{label}: invalid fail-closed decision: {payload}")
    return payload


def test_destructive_commands_fail_closed() -> None:
    require_artifacts()
    fixtures = {
        "git-reset-hard": {
            "operation_id": "op-git",
            "kind": "shell",
            "command": "git reset --hard HEAD~1"
        },
        "recursive-delete": {
            "operation_id": "op-rm",
            "kind": "shell",
            "command": "rm -rf ./src"
        },
        "database-drop": {
            "operation_id": "op-db",
            "kind": "sql",
            "command": "DROP TABLE users"
        }
    }
    for label, operation in fixtures.items():
        payload = assert_not_allow(label, operation)
        if not payload.get("ruin_classes"):
            raise AssertionError(f"{label}: missing ruin classification: {payload}")


def test_scope_expansion_requires_review() -> None:
    payload = assert_not_allow(
        "scope-explosion",
        {
            "operation_id": "op-scope",
            "kind": "write",
            "declared_write_set": ["specs/a.md"],
            "proposed_write_set": ["specs/a.md", "unrelated/b.md"]
        },
    )
    if "scope_explosion" not in payload.get("ruin_classes", []):
        raise AssertionError(payload)


def test_malformed_input_never_allows() -> None:
    payload = assert_not_allow("malformed", {"unexpected": "shape"})
    if payload.get("decision") != "REVIEW_REQUIRED":
        raise AssertionError(f"malformed input must fail closed to review: {payload}")


def test_safe_reads_are_allowed() -> None:
    safe = [
        {"operation_id": "safe-git", "kind": "shell", "command": "git status --short"},
        {"operation_id": "safe-ls", "kind": "shell", "command": "ls -la"},
        {"operation_id": "safe-read", "kind": "read", "target": "README.md"}
    ]
    for operation in safe:
        payload = decide(operation)
        if payload.get("decision") != "ALLOW":
            raise AssertionError(f"safe read was not allowed: {operation} -> {payload}")
        if payload.get("ruin_classes"):
            raise AssertionError(f"safe read received ruin class: {payload}")


def main() -> int:
    tests = [
        test_destructive_commands_fail_closed,
        test_scope_expansion_requires_review,
        test_malformed_input_never_allows,
        test_safe_reads_are_allowed,
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
