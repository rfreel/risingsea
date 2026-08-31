#!/usr/bin/env python3
"""Select a bounded repair candidate from a deterministic registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "repairs" / "registry.jsonl"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def load_registry() -> list[dict]:
    rows = [json.loads(line) for line in REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip()]
    return sorted(rows, key=lambda row: row["recipe_id"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--facts", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    diagnostic = load_json(Path(args.diagnostic))
    facts = load_json(Path(args.facts))
    verdict = diagnostic.get("verdict")
    if verdict not in {"DEFECT", "BLOCKED"}:
        print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "NO_REPAIR", "reason": "DIAGNOSTIC_NOT_REPAIRABLE", "recipe": None}, indent=2, sort_keys=True))
        return 0

    rule_ids = set(diagnostic.get("rule_ids", []))
    candidates = [
        row for row in load_registry()
        if verdict in row.get("match_verdicts", []) and rule_ids.intersection(row.get("match_rule_ids", []))
    ]
    if not candidates:
        print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "NO_REPAIR", "reason": "NO_MATCHING_RECIPE", "recipe": None}, indent=2, sort_keys=True))
        return 0

    recipe = candidates[0]
    missing = sorted(name for name in recipe.get("preconditions", []) if name not in facts)
    if missing:
        print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "BLOCKED", "reason": "PRECONDITION_UNKNOWN", "missing_preconditions": missing, "recipe": None}, indent=2, sort_keys=True))
        return 0

    false_preconditions = sorted(name for name in recipe.get("preconditions", []) if facts.get(name) is not True)
    if false_preconditions:
        print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "BLOCKED", "reason": "PRECONDITION_FALSE", "false_preconditions": false_preconditions, "recipe": None}, indent=2, sort_keys=True))
        return 0

    allowed_write_set = facts.get("allowed_write_set")
    if allowed_write_set is not None:
        allowed = set(allowed_write_set)
        outside = sorted(path for path in recipe.get("write_set", []) if path not in allowed)
        if outside:
            print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "BLOCKED", "reason": "WRITE_SET_OUTSIDE_ALLOWED_SCOPE", "outside_write_set": outside, "recipe": None}, indent=2, sort_keys=True))
            return 0

    authority_required = recipe.get("authority_required")
    if authority_required and facts.get("authority") != authority_required:
        print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "BLOCKED", "reason": "AUTHORITY_REQUIRED", "authority_required": authority_required, "recipe": None}, indent=2, sort_keys=True))
        return 0

    print(json.dumps({"schema": "risingsea.repair-selection.v1", "status": "SELECTED", "reason": "MATCHED_BOUNDED_RECIPE", "recipe": recipe}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
