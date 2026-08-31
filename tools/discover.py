#!/usr/bin/env python3
"""Preserve unresolved rivals and select the cheapest safe discriminating witness."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUIN_GUARD = ROOT / "tools" / "ruin_guard.py"
CANDIDATE_OUTPUTS = ["checker", "representation", "recipe", "rule", "witness"]


def load_input(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("unresolved input must be an object")
    return value


def guard(operation: object) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        json.dump(operation, fh)
        fh.write("\n")
        path = Path(fh.name)
    try:
        result = subprocess.run(
            [sys.executable, str(RUIN_GUARD), "--operation", str(path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    if result.returncode not in (0, 2):
        return {"decision": "REVIEW_REQUIRED", "reason": "GUARD_FAILURE"}
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"decision": "REVIEW_REQUIRED", "reason": "GUARD_MALFORMED_OUTPUT"}
    return value if isinstance(value, dict) else {"decision": "REVIEW_REQUIRED", "reason": "GUARD_MALFORMED_OUTPUT"}


def common(base: dict, live_ids: list[str]) -> dict:
    return {
        "schema": "risingsea.discovery-decision.v1",
        "unresolved_id": str(base.get("unresolved_id", "")),
        "problem_id": str(base.get("problem_id", "")),
        "live_rival_ids": live_ids,
        "consensus_used_as_evidence": False,
    }


def decide(value: dict) -> dict:
    rivals = value.get("rivals", [])
    if not isinstance(rivals, list):
        rivals = []
    live = sorted(
        (row for row in rivals if isinstance(row, dict) and row.get("status") == "LIVE"),
        key=lambda row: str(row.get("rival_id", "")),
    )
    live_ids = [str(row.get("rival_id", "")) for row in live if row.get("rival_id")]
    out = common(value, live_ids)

    if len(live_ids) < 2:
        return {
            **out,
            "status": "BLOCKED",
            "reason": "INSUFFICIENT_RIVALS",
            "model_candidate_allowed": False,
        }

    exact_cases = value.get("exact_cases", [])
    if isinstance(exact_cases, list) and exact_cases:
        cases = sorted(
            (row for row in exact_cases if isinstance(row, dict) and row.get("case_id")),
            key=lambda row: str(row["case_id"]),
        )
        if cases:
            case = cases[0]
            return {
                **out,
                "status": "EXACT_CASE",
                "route": "EXACT_PRIOR_CASE",
                "case_id": str(case["case_id"]),
                "model_candidate_allowed": False,
            }

    if value.get("search_complete") is not True:
        return {
            **out,
            "status": "UNKNOWN",
            "reason": "SEARCH_INCOMPLETE",
            "novelty_established": False,
            "model_candidate_allowed": False,
        }

    witness_candidates = value.get("witness_candidates", [])
    if not isinstance(witness_candidates, list):
        witness_candidates = []
    candidates = sorted(
        (row for row in witness_candidates if isinstance(row, dict) and row.get("witness_id")),
        key=lambda row: (row.get("cost_rank", 10**9), str(row["witness_id"])),
    )
    rejected: list[dict] = []
    live_set = set(live_ids)
    for candidate in candidates:
        distinguishes = set(candidate.get("distinguishes", []))
        witness_id = str(candidate["witness_id"])
        if not live_set.issubset(distinguishes):
            rejected.append({"witness_id": witness_id, "reason": "INSUFFICIENT_DISCRIMINATION"})
            continue
        verdict = guard(candidate.get("operation", {}))
        if verdict.get("decision") != "ALLOW":
            rejected.append({"witness_id": witness_id, "reason": "RUIN_GUARD"})
            continue
        return {
            **out,
            "status": "WITNESS_SELECTED",
            "witness_id": witness_id,
            "rejected_witnesses": rejected,
            "model_candidate_allowed": False,
        }

    return {
        **out,
        "status": "UNKNOWN",
        "reason": "NO_DECISIVE_WITNESS",
        "rejected_witnesses": rejected,
        "novelty_established": False,
        "model_candidate_allowed": True,
        "allowed_candidate_outputs": CANDIDATE_OUTPUTS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        payload = decide(load_input(Path(args.input)))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({
            "schema": "risingsea.discovery-decision.v1",
            "status": "BLOCKED",
            "reason": "MALFORMED_INPUT",
            "detail": str(exc),
            "model_candidate_allowed": False,
        }, indent=2, sort_keys=True))
        return 0
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
