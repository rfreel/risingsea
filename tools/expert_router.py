#!/usr/bin/env python3
"""Deterministic routing before semantic/model fallback."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def decide(problem: dict, catalog: dict) -> dict:
    signature = problem.get("signature")
    if not isinstance(signature, str) or not signature:
        return payload("SEARCH_INCOMPLETE", "UNKNOWN", False, "none", None, "Problem lacks an exact signature.")

    exact = catalog.get("exact_results", {})
    if signature in exact:
        return payload("EXACT_RESULT", "PASS", False, "none", exact[signature].get("result_ref"), "Exact reusable result matched.")

    negatives = catalog.get("negative_memos", {})
    if signature in negatives:
        return payload("NEGATIVE_MEMO", "FAIL", False, "none", negatives[signature].get("memo_ref"), "Exact negative memo matched.")

    rules = catalog.get("compiled_rules", {})
    if signature in rules:
        return payload("COMPILED_RULE", "PASS", False, "none", rules[signature].get("rule_ref"), "Compiled deterministic rule matched.")

    search = catalog.get("semantic_search", {})
    available = search.get("available") is True
    complete = search.get("complete") is True
    hits = search.get("hits") if isinstance(search.get("hits"), list) else []

    if available and hits:
        first = hits[0]
        ref = first.get("ref") if isinstance(first, dict) else str(first)
        return payload("SEMANTIC_SEARCH", "UNKNOWN", False, "none", ref, "Bounded semantic retrieval returned a candidate reference.")

    if available and not complete:
        return payload("SEARCH_INCOMPLETE", "UNKNOWN", False, "none", None, "Search miss is not an absence proof because search completeness is false.")

    model = catalog.get("model_fallback", {})
    if available and complete and model.get("available") is True:
        return payload("MODEL_CANDIDATE", "UNKNOWN", True, "candidate_only", None, "Deterministic routes and complete search produced no result; model may propose a candidate only.")

    return payload("SEARCH_INCOMPLETE", "UNKNOWN", False, "none", None, "No sound complete route is available.")


def payload(route: str, verdict: str, model_allowed: bool, authority_effect: str, selected_ref: str | None, reason: str) -> dict:
    return {
        "schema": "risingsea.route-decision.v1",
        "route": route,
        "verdict": verdict,
        "model_invocation_allowed": model_allowed,
        "authority_effect": authority_effect,
        "selected_ref": selected_ref,
        "reason": reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    print(json.dumps(decide(load(args.problem), load(args.catalog)), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
