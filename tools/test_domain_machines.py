#!/usr/bin/env python3
"""Contract tests for the expert DomainMachine registry.

This file intentionally depends only on the Python standard library so it can
run in a fresh checkout and in the repository integrity workflow.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "domain-machines" / "registry.jsonl"
VALIDATOR = ROOT / "tools" / "validate_domain_machines.py"

REQUIRED_MACHINE_FIELDS = {
    "schema",
    "domain_id",
    "title",
    "representation",
    "required_observations",
    "invariants",
    "diagnostics",
    "repair_recipes",
    "verification_oracles",
    "ruin_boundaries",
    "failure_routes",
    "discovery_strategy",
    "donors",
}

REQUIRED_DONOR_FIELDS = {
    "repository",
    "mechanism",
    "adoption",
    "claim_boundary",
}

ALLOWED_ADOPTION = {"REUSE", "ADAPT", "REFERENCE"}
REQUIRED_SEEDS = {"planning", "external-effect", "security"}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_registry() -> list[dict]:
    if not REGISTRY.exists():
        fail(f"missing registry: {REGISTRY.relative_to(ROOT)}")
    rows: list[dict] = []
    for line_no, raw in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(f"registry line {line_no}: invalid JSON: {exc}")
        rows.append(row)
    if not rows:
        fail("domain machine registry is empty")
    return rows


def test_registry_and_machines() -> None:
    if not VALIDATOR.exists():
        fail(f"missing validator: {VALIDATOR.relative_to(ROOT)}")

    rows = load_registry()
    ids = [row.get("domain_id") for row in rows]
    if len(ids) != len(set(ids)):
        fail(f"duplicate domain_id in registry: {ids}")

    missing_seeds = REQUIRED_SEEDS - set(ids)
    if missing_seeds:
        fail(f"missing required seed domains: {sorted(missing_seeds)}")

    for row in rows:
        domain_id = row.get("domain_id")
        path_value = row.get("path")
        if not isinstance(path_value, str) or not path_value:
            fail(f"{domain_id}: registry row missing path")
        machine_path = ROOT / path_value
        if not machine_path.exists():
            fail(f"{domain_id}: missing machine file {path_value}")
        machine = json.loads(machine_path.read_text(encoding="utf-8"))
        missing = REQUIRED_MACHINE_FIELDS - set(machine)
        if missing:
            fail(f"{domain_id}: missing machine fields {sorted(missing)}")
        if machine["domain_id"] != domain_id:
            fail(f"{domain_id}: registry/machine domain_id mismatch")

        failure_routes = machine.get("failure_routes", {})
        if "UNRESOLVED" not in failure_routes:
            fail(f"{domain_id}: missing UNRESOLVED failure route")

        diagnostics = machine.get("diagnostics", [])
        if not diagnostics:
            fail(f"{domain_id}: no diagnostics declared")
        if diagnostics[-1].get("kind") != "MODEL_CANDIDATE":
            fail(f"{domain_id}: final diagnostic route must be MODEL_CANDIDATE fallback")
        if not any(d.get("kind") != "MODEL_CANDIDATE" for d in diagnostics):
            fail(f"{domain_id}: requires at least one non-model diagnostic")

        donors = machine.get("donors", [])
        if not donors:
            fail(f"{domain_id}: no mechanism donors declared")
        for donor in donors:
            missing_donor = REQUIRED_DONOR_FIELDS - set(donor)
            if missing_donor:
                fail(f"{domain_id}: donor missing {sorted(missing_donor)}")
            if donor["adoption"] not in ALLOWED_ADOPTION:
                fail(f"{domain_id}: invalid donor adoption {donor['adoption']!r}")


def test_validator_cli() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"validator failed:\nstdout={result.stdout}\nstderr={result.stderr}")
    payload = json.loads(result.stdout)
    if payload.get("status") != "PASS":
        fail(f"validator status is not PASS: {payload}")
    if payload.get("count") != 3:
        fail(f"expected 3 seed domain machines, got {payload.get('count')}")


def main() -> int:
    tests = [test_registry_and_machines, test_validator_cli]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # contract harness should report all failures
            failures.append(f"{test.__name__}: {exc}")
            print(f"FAIL {test.__name__}: {exc}", file=sys.stderr)
    if failures:
        print(f"FAILED {len(failures)}/{len(tests)}", file=sys.stderr)
        return 1
    print(f"PASS {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
