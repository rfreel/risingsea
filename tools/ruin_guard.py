#!/usr/bin/env python3
"""Minimal fail-closed RuinGuard boundary.

This is an adapter-shaped integration boundary, not a replacement for DCG.
It handles only the residual fixtures required by RS-W007.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "guard" / "ruin-classes.json"


def load_rules() -> dict[str, dict]:
    payload = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    return {row["id"]: row for row in payload["classes"]}


def classify(operation: object) -> dict:
    rules = load_rules()
    if not isinstance(operation, dict):
        return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Operation must be a JSON object.")

    kind = operation.get("kind")
    operation_id = operation.get("operation_id")
    if not isinstance(kind, str) or not isinstance(operation_id, str) or not operation_id:
        return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Operation lacks required kind or operation_id.")

    if kind == "read":
        target = operation.get("target")
        if isinstance(target, str) and target:
            return decision("ALLOW", [], "Read-only operation has no matched ruin class.")
        return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Read operation lacks a target.")

    if kind == "write":
        declared = operation.get("declared_write_set")
        proposed = operation.get("proposed_write_set")
        if not isinstance(declared, list) or not isinstance(proposed, list):
            return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Write operation lacks explicit write sets.")
        declared_set = set(declared)
        proposed_set = set(proposed)
        if not all(isinstance(x, str) for x in declared_set | proposed_set):
            return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Write-set entries must be strings.")
        unexpected = sorted(proposed_set - declared_set)
        if unexpected:
            return decision(
                rules["scope_explosion"]["decision"],
                ["scope_explosion"],
                "Proposed writes exceed the declared write set.",
                details={"unexpected_writes": unexpected},
            )
        return decision("ALLOW", [], "Proposed writes stay within the declared write set.")

    if kind in {"shell", "sql"}:
        command = operation.get("command")
        if not isinstance(command, str) or not command.strip():
            return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Executable operation lacks a command.")
        normalized = " ".join(command.strip().split())
        lowered = normalized.lower()

        if kind == "shell":
            if re.search(r"(^|\s)git\s+reset\s+--hard(?:\s|$)", lowered):
                return decision(
                    rules["destructive_git_history"]["decision"],
                    ["destructive_git_history"],
                    "Destructive Git history/worktree operation matched.",
                )
            if re.search(r"(^|\s)rm\s+-[^\s]*r[^\s]*f[^\s]*(?:\s|$)", lowered) or re.search(
                r"(^|\s)rm\s+-[^\s]*f[^\s]*r[^\s]*(?:\s|$)", lowered
            ):
                return decision(
                    rules["irreversible_data_loss"]["decision"],
                    ["irreversible_data_loss"],
                    "Recursive forced deletion matched.",
                )
            if lowered.startswith("git status") or lowered == "ls" or lowered.startswith("ls "):
                return decision("ALLOW", [], "Known read-only shell operation.")
            return decision("REVIEW_REQUIRED", ["unclassified_operation"], "Shell operation is outside the currently compiled safe/ruin subset.")

        if kind == "sql":
            if re.search(r"\bdrop\s+(table|database|schema)\b", lowered) or re.search(r"\btruncate\s+table\b", lowered):
                return decision(
                    rules["irreversible_data_loss"]["decision"],
                    ["irreversible_data_loss"],
                    "Destructive database operation matched.",
                )
            return decision("REVIEW_REQUIRED", ["unclassified_operation"], "SQL operation is outside the currently compiled safe/ruin subset.")

    return decision("REVIEW_REQUIRED", ["unclassified_operation"], f"Unsupported operation kind: {kind!r}.")


def decision(result: str, ruin_classes: list[str], reason: str, details: dict | None = None) -> dict:
    payload = {
        "schema": "risingsea.ruin-decision.v1",
        "decision": result,
        "ruin_classes": ruin_classes,
        "reason": reason,
        "authority_effect": "guard_only",
    }
    if details:
        payload["details"] = details
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        operation = json.loads(Path(args.operation).read_text(encoding="utf-8"))
        payload = classify(operation)
    except Exception as exc:
        payload = decision("REVIEW_REQUIRED", ["unclassified_operation"], f"Guard input could not be classified: {exc}")

    print(json.dumps(payload, sort_keys=True))
    return 0 if payload["decision"] == "ALLOW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
