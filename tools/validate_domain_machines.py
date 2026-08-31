#!/usr/bin/env python3
"""Deterministically validate Rising Sea DomainMachine registry records.

This validator intentionally uses only the Python standard library. It checks
Rising Sea's contract-critical subset directly; the JSON Schema is the portable
contract for external validators.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "domain-machines" / "registry.jsonl"
SCHEMA_PATH = ROOT / "contracts" / "domain-machine.schema.json"

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
REQUIRED_DONOR_FIELDS = {"repository", "mechanism", "adoption", "claim_boundary"}
ALLOWED_ADOPTION = {"REUSE", "ADAPT", "REFERENCE"}


def issue(kind: str, **detail: object) -> dict:
    return {"kind": kind, **detail}


def load_registry(issues: list[dict]) -> list[dict]:
    if not REGISTRY.exists():
        issues.append(issue("missing-registry", path=str(REGISTRY.relative_to(ROOT))))
        return []
    rows: list[dict] = []
    for line_no, raw in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            issues.append(issue("invalid-registry-json", line=line_no, detail=str(exc)))
            continue
        if not isinstance(row, dict):
            issues.append(issue("invalid-registry-row", line=line_no))
            continue
        rows.append(row)
    return rows


def validate_machine(row: dict, issues: list[dict]) -> None:
    domain_id = row.get("domain_id")
    path_value = row.get("path")
    if not isinstance(domain_id, str) or not domain_id:
        issues.append(issue("invalid-domain-id", value=domain_id))
        return
    if not isinstance(path_value, str) or not path_value:
        issues.append(issue("missing-machine-path", domain_id=domain_id))
        return
    path = ROOT / path_value
    if not path.exists():
        issues.append(issue("missing-machine", domain_id=domain_id, path=path_value))
        return
    try:
        machine = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(issue("invalid-machine-json", domain_id=domain_id, detail=str(exc)))
        return

    missing = sorted(REQUIRED_MACHINE_FIELDS - set(machine))
    if missing:
        issues.append(issue("missing-machine-fields", domain_id=domain_id, fields=missing))
    if machine.get("schema") != "risingsea.domain-machine.v1":
        issues.append(issue("invalid-machine-schema", domain_id=domain_id, value=machine.get("schema")))
    if machine.get("domain_id") != domain_id:
        issues.append(issue("domain-id-mismatch", domain_id=domain_id, machine=machine.get("domain_id")))

    representation = machine.get("representation")
    if not isinstance(representation, dict):
        issues.append(issue("invalid-representation", domain_id=domain_id))
    else:
        for key in ("kind", "fields", "novice_projection"):
            if not representation.get(key):
                issues.append(issue("incomplete-representation", domain_id=domain_id, field=key))

    invariants = machine.get("invariants")
    if not isinstance(invariants, list) or not invariants:
        issues.append(issue("missing-invariants", domain_id=domain_id))

    diagnostics = machine.get("diagnostics")
    if not isinstance(diagnostics, list) or len(diagnostics) < 2:
        issues.append(issue("insufficient-diagnostics", domain_id=domain_id))
    else:
        non_model = [d for d in diagnostics if isinstance(d, dict) and d.get("kind") != "MODEL_CANDIDATE"]
        if not non_model:
            issues.append(issue("no-deterministic-diagnostic", domain_id=domain_id))
        last = diagnostics[-1]
        if not isinstance(last, dict) or last.get("kind") != "MODEL_CANDIDATE":
            issues.append(issue("model-fallback-not-last", domain_id=domain_id))

    oracles = machine.get("verification_oracles")
    if not isinstance(oracles, list) or not oracles:
        issues.append(issue("missing-verification-oracle", domain_id=domain_id))

    failure_routes = machine.get("failure_routes")
    if not isinstance(failure_routes, dict) or "UNRESOLVED" not in failure_routes:
        issues.append(issue("missing-unresolved-route", domain_id=domain_id))

    discovery = machine.get("discovery_strategy")
    if not isinstance(discovery, dict) or not discovery:
        issues.append(issue("missing-discovery-strategy", domain_id=domain_id))

    donors = machine.get("donors")
    if not isinstance(donors, list) or not donors:
        issues.append(issue("missing-donors", domain_id=domain_id))
    else:
        for index, donor in enumerate(donors):
            if not isinstance(donor, dict):
                issues.append(issue("invalid-donor", domain_id=domain_id, index=index))
                continue
            missing_donor = sorted(REQUIRED_DONOR_FIELDS - set(donor))
            if missing_donor:
                issues.append(issue("missing-donor-fields", domain_id=domain_id, index=index, fields=missing_donor))
            if donor.get("adoption") not in ALLOWED_ADOPTION:
                issues.append(issue("invalid-donor-adoption", domain_id=domain_id, index=index, value=donor.get("adoption")))


def check() -> dict:
    issues: list[dict] = []
    if not SCHEMA_PATH.exists():
        issues.append(issue("missing-schema", path=str(SCHEMA_PATH.relative_to(ROOT))))
    rows = load_registry(issues)
    seen: set[str] = set()
    for row in rows:
        domain_id = row.get("domain_id")
        if domain_id in seen:
            issues.append(issue("duplicate-domain-id", domain_id=domain_id))
        if isinstance(domain_id, str):
            seen.add(domain_id)
        validate_machine(row, issues)
    return {
        "schema": "risingsea.domain-machine-validation.v1",
        "status": "PASS" if not issues else "FAIL",
        "count": len(rows),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = check()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result['count']} domain machine(s), {len(result['issues'])} issue(s)")
        for item in result["issues"]:
            print(f"- {item}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
