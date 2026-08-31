#!/usr/bin/env python3
"""Lower one UNSATISFIED obligation and bounded repair into a simple-executor WorkPacket."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXECUTION_GRAMMAR = ["READ", "CHECK", "CHANGE", "VERIFY", "RECEIPT", "STOP"]
REASONING_DEBT = {
    "design_choice": 0,
    "scope": 0,
    "read_set": 0,
    "write_set": 0,
    "verification_oracle": 0,
    "failure_route": 0,
    "authority": 0,
    "semantic_terms": 0,
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def blocked(status: str, reason: str) -> dict:
    return {"schema": "risingsea.work-packet-lowering.v1", "status": status, "reason": reason, "packet": None}


def lower(source: dict) -> dict:
    obligation = source.get("obligation")
    recipe = source.get("recipe")
    contract = source.get("execution_contract")
    current_head = source.get("current_head")
    if not isinstance(obligation, dict) or not isinstance(recipe, dict) or not isinstance(contract, dict) or not isinstance(current_head, str) or not current_head:
        return blocked("BLOCKED", "MALFORMED_INPUT")

    if obligation.get("state") != "UNSATISFIED":
        return blocked("BLOCKED", "OBLIGATION_NOT_EXECUTABLE")

    basis_head = contract.get("basis_head")
    if not isinstance(basis_head, str) or not basis_head:
        return blocked("BLOCKED", "MISSING_HISTORY_HEAD")
    if basis_head != current_head:
        return blocked("STALE", "HISTORY_HEAD_CHANGED")

    read_set = contract.get("read_set")
    if not isinstance(read_set, list) or not read_set or any(not isinstance(x, str) or not x for x in read_set):
        return blocked("BLOCKED", "MISSING_READ_SET")

    oracle_id = recipe.get("verification_oracle_id")
    if not isinstance(oracle_id, str) or not oracle_id:
        return blocked("BLOCKED", "MISSING_VERIFICATION_ORACLE")

    strategies = recipe.get("strategy_options")
    selected_strategy = recipe.get("selected_strategy")
    if not isinstance(strategies, list) or len(strategies) != 1 or strategies[0] != selected_strategy or not isinstance(selected_strategy, str) or not selected_strategy:
        return blocked("BLOCKED", "UNRESOLVED_STRATEGY")

    undefined_terms = contract.get("undefined_terms")
    if not isinstance(undefined_terms, list):
        return blocked("BLOCKED", "UNRESOLVED_SEMANTIC_TERMS")
    if undefined_terms:
        return blocked("BLOCKED", "UNRESOLVED_SEMANTIC_TERMS")

    failure_route = contract.get("failure_route")
    if not isinstance(failure_route, str) or not failure_route:
        return blocked("BLOCKED", "MISSING_FAILURE_ROUTE")

    write_set = recipe.get("write_set")
    allowed_write_set = contract.get("allowed_write_set")
    if not isinstance(write_set, list) or not write_set or any(not isinstance(x, str) or not x for x in write_set):
        return blocked("BLOCKED", "MISSING_WRITE_SET")
    if not isinstance(allowed_write_set, list):
        return blocked("BLOCKED", "MISSING_ALLOWED_WRITE_SET")
    if any(path not in set(allowed_write_set) for path in write_set):
        return blocked("BLOCKED", "WRITE_SET_OUTSIDE_ALLOWED_SCOPE")

    authority = contract.get("authority")
    if not isinstance(authority, str) or not authority:
        return blocked("BLOCKED", "MISSING_AUTHORITY")
    required = recipe.get("authority_required")
    if required is not None and authority != required:
        return blocked("BLOCKED", "AUTHORITY_REQUIRED")
    if recipe.get("authority_effect") != "candidate_only":
        return blocked("BLOCKED", "INVALID_AUTHORITY_EFFECT")

    obligation_id = obligation.get("obligation_id")
    objective = obligation.get("objective")
    basis_ids = obligation.get("basis_ids")
    recipe_id = recipe.get("recipe_id")
    recovery = recipe.get("recovery")
    if not isinstance(obligation_id, str) or not obligation_id or not isinstance(objective, str) or not objective:
        return blocked("BLOCKED", "MALFORMED_OBLIGATION")
    if not isinstance(basis_ids, list) or not basis_ids or any(not isinstance(x, str) or not x for x in basis_ids):
        return blocked("BLOCKED", "MISSING_BASIS")
    if not isinstance(recipe_id, str) or not recipe_id or not isinstance(recovery, str) or not recovery:
        return blocked("BLOCKED", "MALFORMED_RECIPE")

    packet_body = {
        "history_head": current_head,
        "obligation_id": obligation_id,
        "objective": objective,
        "basis_ids": sorted(set(basis_ids)),
        "recipe_id": recipe_id,
        "selected_strategy": selected_strategy,
        "read_set": sorted(set(read_set)),
        "write_set": sorted(set(write_set)),
        "verification_oracle_id": oracle_id,
        "recovery": recovery,
        "failure_route": failure_route,
        "authority": authority,
        "authority_effect": "candidate_only",
        "execution_grammar": EXECUTION_GRAMMAR,
        "reasoning_debt": dict(REASONING_DEBT),
    }
    packet = {"packet_id": "wp:sha256:" + hashlib.sha256(canonical(packet_body)).hexdigest(), **packet_body}
    return {"schema": "risingsea.work-packet-lowering.v1", "status": "READY", "reason": "ZERO_REASONING_DEBT", "packet": packet}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        value = json.loads(Path(args.input).read_text(encoding="utf-8"))
        payload = lower(value if isinstance(value, dict) else {})
    except (OSError, json.JSONDecodeError):
        payload = blocked("BLOCKED", "MALFORMED_INPUT")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
