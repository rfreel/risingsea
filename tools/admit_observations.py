#!/usr/bin/env python3
"""Deterministically admit observation candidates into accepted evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "diagnostics" / "observation-rules.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def reject(row: dict, reason: str) -> dict:
    return {"observation_id": str(row.get("observation_id", "")), "reason": reason}


def validate_candidate(row: object, rules: dict) -> tuple[dict | None, dict | None]:
    if not isinstance(row, dict):
        return None, {"observation_id": "", "reason": "MALFORMED_CANDIDATE"}

    obs_id = row.get("observation_id")
    required = ["observation_id", "proposition", "scope", "value", "source_class", "authority", "provenance", "freshness", "observed_at"]
    if any(key not in row for key in required):
        if "provenance" not in row:
            return None, reject(row, "MISSING_PROVENANCE")
        return None, reject(row, "MALFORMED_CANDIDATE")

    if not isinstance(obs_id, str) or not obs_id:
        return None, reject(row, "MALFORMED_CANDIDATE")

    source_class = row.get("source_class")
    if source_class == "MODEL_CANDIDATE":
        return None, reject(row, "MODEL_CANDIDATE_NOT_OBSERVATION")
    if source_class not in rules["accepted_source_classes"]:
        return None, reject(row, "SOURCE_CLASS_NOT_OBSERVATION")

    if row.get("authority") != rules["authority_required"]:
        return None, reject(row, "INVALID_OBSERVATION_AUTHORITY")

    provenance = row.get("provenance")
    if not isinstance(provenance, dict):
        return None, reject(row, "MISSING_PROVENANCE")
    for field in rules["required_provenance_fields"]:
        if not provenance.get(field):
            return None, reject(row, "MISSING_PROVENANCE")

    freshness = row.get("freshness")
    if freshness not in rules["freshness_preserved_values"]:
        return None, reject(row, "INVALID_FRESHNESS")

    normalized = {
        "observation_id": row["observation_id"],
        "proposition": row["proposition"],
        "scope": row["scope"],
        "value": row["value"],
        "source_class": source_class,
        "authority": row["authority"],
        "provenance": {
            "kind": provenance["kind"],
            "ref": provenance["ref"],
            "digest": provenance["digest"],
        },
        "freshness": freshness,
        "observed_at": row["observed_at"],
        "current_for_decision": freshness in rules["freshness_current_values"],
    }
    normalized["digest"] = digest(normalized)
    return normalized, None


def build_payload(candidates: list[object], rules: dict) -> dict:
    accepted: list[dict] = []
    rejected: list[dict] = []
    for candidate in candidates:
        good, bad = validate_candidate(candidate, rules)
        if good is not None:
            accepted.append(good)
        if bad is not None:
            rejected.append(bad)

    accepted.sort(key=lambda row: row["observation_id"])
    rejected.sort(key=lambda row: (row["observation_id"], row["reason"]))

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in accepted:
        groups[(row["scope"], row["proposition"])].append(row)

    contradictions: list[dict] = []
    for (scope, proposition), rows in sorted(groups.items()):
        distinct_values = {canonical_bytes(row["value"]) for row in rows}
        if len(distinct_values) > 1:
            contradictions.append(
                {
                    "scope": scope,
                    "proposition": proposition,
                    "observation_ids": sorted(row["observation_id"] for row in rows),
                }
            )

    return {
        "schema": "risingsea.accepted-observation-set.v1",
        "accepted": accepted,
        "rejected": rejected,
        "contradictions": contradictions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    candidates = source.get("candidates", []) if isinstance(source, dict) else []
    payload = build_payload(candidates, rules)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
