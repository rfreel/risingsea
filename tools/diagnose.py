#!/usr/bin/env python3
"""Compile accepted observations into a deterministic diagnostic receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "diagnostics" / "rules.json"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"expected object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True)
    parser.add_argument("--observations", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    problem = load_json(Path(args.problem))
    observations = load_json(Path(args.observations))
    rules_doc = load_json(RULES_PATH)
    rules = {row["rule_id"]: row for row in rules_doc.get("rules", [])}

    requested = list(problem.get("rule_ids", []))
    unknown_rule_ids = sorted(rule_id for rule_id in requested if rule_id not in rules)
    selected = [rules[rule_id] for rule_id in requested if rule_id in rules]

    accepted = list(observations.get("accepted", []))
    contradictions = list(observations.get("contradictions", []))

    relevant_keys = {(r["scope"], r["proposition"]) for r in selected}
    relevant_contradictions = [
        row for row in contradictions
        if (row.get("scope"), row.get("proposition")) in relevant_keys
    ]

    by_key: dict[tuple[str, str], list[dict]] = {}
    for row in accepted:
        key = (row.get("scope"), row.get("proposition"))
        by_key.setdefault(key, []).append(row)

    used_observation_ids: set[str] = set()
    missing: list[str] = []
    blocked = False
    defect = False

    for rule in selected:
        key = (rule["scope"], rule["proposition"])
        candidates = by_key.get(key, [])
        if rule.get("requires_current", False):
            candidates = [row for row in candidates if row.get("current_for_decision") is True]
        if not candidates:
            missing.append(f"{rule['proposition']}@{rule['scope']}")
            continue

        for row in candidates:
            used_observation_ids.add(str(row.get("observation_id", "")))

        values = {json.dumps(row.get("value"), sort_keys=True) for row in candidates}
        if len(values) > 1:
            continue
        value = candidates[0].get("value")
        if value is False:
            if rule.get("kind") == "prerequisite_true" or rule.get("false_verdict") == "BLOCKED":
                blocked = True
            elif rule.get("false_verdict") == "DEFECT":
                defect = True

    if relevant_contradictions:
        verdict = "CONTRADICTED"
        for row in relevant_contradictions:
            used_observation_ids.update(str(x) for x in row.get("observation_ids", []))
    elif unknown_rule_ids:
        verdict = "UNKNOWN"
    elif not selected:
        verdict = "UNKNOWN"
    elif blocked:
        verdict = "BLOCKED"
    elif defect:
        verdict = "DEFECT"
    elif missing:
        verdict = "EVIDENCE_GAP"
    else:
        verdict = "SATISFIED"

    receipt = {
        "schema": "risingsea.diagnostic-receipt.v1",
        "problem_id": str(problem.get("problem_id", "")),
        "domain": str(problem.get("domain", "")),
        "verdict": verdict,
        "rule_ids": sorted(rule["rule_id"] for rule in selected),
        "observation_ids": sorted(x for x in used_observation_ids if x),
        "missing": sorted(set(missing)),
        "unknown_rule_ids": unknown_rule_ids,
        "model_candidates_considered": 0,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
