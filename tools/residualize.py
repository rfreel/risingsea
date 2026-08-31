#!/usr/bin/env python3
"""Partition finite obligations and emit only proven UNSATISFIED TODO candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

STATES = ["SATISFIED", "UNSATISFIED", "CONTRADICTED", "UNKNOWN", "NOT_APPLICABLE"]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must be object")
    return value


def blocked(reason: str) -> dict:
    return {
        "schema": "risingsea.obligation-residual.v1",
        "status": "BLOCKED",
        "reason": reason,
        "partitions": {state: [] for state in STATES},
        "todo_candidates": [],
        "blocked_frontier": {"UNKNOWN": [], "CONTRADICTED": []},
        "equivalence_groups": [],
    }


def compile_residual(source: dict) -> dict:
    obligations = source.get("obligations", [])
    witnesses = source.get("equivalence_witnesses", [])
    if not isinstance(obligations, list) or not isinstance(witnesses, list):
        return blocked("MALFORMED_INPUT")

    by_id: dict[str, dict] = {}
    partitions = {state: [] for state in STATES}
    for row in obligations:
        if not isinstance(row, dict):
            return blocked("MALFORMED_OBLIGATION")
        oid = row.get("obligation_id")
        state = row.get("state")
        if not isinstance(oid, str) or not oid or oid in by_id:
            return blocked("INVALID_OBLIGATION_ID")
        if state not in STATES:
            return blocked("INVALID_OBLIGATION_STATE")
        if not row.get("proposition") or not row.get("scope") or not row.get("basis_ids"):
            return blocked("MALFORMED_OBLIGATION")
        by_id[oid] = row
        partitions[state].append(oid)

    for state in STATES:
        partitions[state].sort()

    collapsed: dict[str, str] = {}
    groups: list[dict] = []
    for witness in sorted((w for w in witnesses if isinstance(w, dict)), key=lambda w: str(w.get("witness_id", ""))):
        witness_id = witness.get("witness_id")
        members = witness.get("obligation_ids", [])
        scope = witness.get("scope")
        proposition = witness.get("proposition")
        basis_ids = witness.get("basis_ids")
        if not isinstance(witness_id, str) or not witness_id or not isinstance(members, list) or len(members) < 2 or not basis_ids:
            return blocked("INVALID_EQUIVALENCE_WITNESS")
        unique = sorted(set(str(x) for x in members))
        if len(unique) != len(members) or any(member not in by_id for member in unique):
            return blocked("INVALID_EQUIVALENCE_WITNESS")
        rows = [by_id[member] for member in unique]
        if any(row["scope"] != scope or row["proposition"] != proposition for row in rows):
            return blocked("INVALID_EQUIVALENCE_WITNESS")
        if len({row["state"] for row in rows}) != 1:
            return blocked("INVALID_EQUIVALENCE_WITNESS")
        canonical = unique[0]
        for member in unique[1:]:
            if member in collapsed:
                return blocked("OVERLAPPING_EQUIVALENCE_WITNESS")
            collapsed[member] = canonical
        groups.append({"canonical_id": canonical, "member_ids": unique, "witness_id": witness_id})

    todo = sorted(
        oid for oid in partitions["UNSATISFIED"]
        if oid not in collapsed
    )
    return {
        "schema": "risingsea.obligation-residual.v1",
        "status": "PASS",
        "reason": None,
        "partitions": partitions,
        "todo_candidates": todo,
        "blocked_frontier": {
            "UNKNOWN": partitions["UNKNOWN"],
            "CONTRADICTED": partitions["CONTRADICTED"],
        },
        "equivalence_groups": groups,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        payload = compile_residual(load(Path(args.input)))
    except (OSError, ValueError, json.JSONDecodeError):
        payload = blocked("MALFORMED_INPUT")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
