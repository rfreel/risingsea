#!/usr/bin/env python3
"""Validate bounded repair recipes and referenced verification oracles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "repairs" / "registry.jsonl"
DEFAULT_ORACLES = ROOT / "repairs" / "oracles.jsonl"

RECIPE_REQUIRED = {
    "recipe_id", "match_verdicts", "match_rule_ids", "preconditions", "write_set",
    "verification_oracle_id", "strongest_falsifier", "recovery", "ruin_class",
    "authority_required", "authority_effect",
}
ORACLE_REQUIRED = {"oracle_id", "kind", "command", "success_contract", "failure_contract"}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: expected object")
        rows.append(row)
    return rows


def validate(registry: Path, oracle_path: Path) -> dict:
    issues: list[dict] = []
    try:
        recipes = load_jsonl(registry)
        oracles = load_jsonl(oracle_path)
    except (OSError, ValueError) as exc:
        return {"status": "FAIL", "recipe_count": 0, "oracle_count": 0, "issues": [{"kind": "load", "detail": str(exc)}]}

    oracle_ids: set[str] = set()
    for row in oracles:
        missing = sorted(ORACLE_REQUIRED - set(row))
        if missing:
            issues.append({"kind": "oracle-missing-fields", "oracle_id": row.get("oracle_id"), "fields": missing})
            continue
        oid = row["oracle_id"]
        if oid in oracle_ids:
            issues.append({"kind": "duplicate-oracle", "oracle_id": oid})
        oracle_ids.add(oid)

    recipe_ids: set[str] = set()
    for row in recipes:
        missing = sorted(RECIPE_REQUIRED - set(row))
        if missing:
            issues.append({"kind": "recipe-missing-fields", "recipe_id": row.get("recipe_id"), "fields": missing})
            continue
        rid = row["recipe_id"]
        if rid in recipe_ids:
            issues.append({"kind": "duplicate-recipe", "recipe_id": rid})
        recipe_ids.add(rid)
        if row.get("authority_effect") != "candidate_only":
            issues.append({"kind": "invalid-authority-effect", "recipe_id": rid})
        if not row.get("write_set"):
            issues.append({"kind": "empty-write-set", "recipe_id": rid})
        oracle_id = row.get("verification_oracle_id")
        if oracle_id not in oracle_ids:
            issues.append({"kind": "missing-oracle", "recipe_id": rid, "oracle_id": oracle_id})
        if row.get("ruin_class") != "none" and not row.get("authority_required"):
            issues.append({"kind": "ruin-without-authority", "recipe_id": rid})

    return {
        "status": "PASS" if not issues else "FAIL",
        "recipe_count": len(recipes),
        "oracle_count": len(oracles),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--oracles", default=str(DEFAULT_ORACLES))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = validate(Path(args.registry), Path(args.oracles))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
