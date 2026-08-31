#!/usr/bin/env python3
"""Read-only structural doctor for the Rising Sea planning flywheel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from work_state import load_current_items

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "evidence" / "receipts"
ALLOWED_STATUS = {"READY", "CLAIMED", "RUNNING", "BLOCKED", "REVIEW", "COMPLETE", "PARTIAL", "ABANDONED"}
REQUIRED_FIELDS = {"id", "title", "status", "priority", "objective", "depends_on", "specs", "acceptance", "strongest_falsifier", "authority_ceiling", "expected_accretion", "next_action"}


def check() -> dict:
    issues: list[dict] = []
    try:
        items, events = load_current_items()
    except ValueError as exc:
        return {
            "schema": "risingsea.doctor.v2",
            "status": "FAIL",
            "checks": {"work_items": 0, "events": 0, "issues": 1, "ready": 0},
            "top_ready": None,
            "issues": [{"kind": "work-fold-failure", "detail": str(exc)}],
        }

    by_id: dict[str, dict] = {}
    for item in items:
        item_id = item.get("id")
        missing = sorted(REQUIRED_FIELDS - set(item))
        if missing:
            issues.append({"kind": "missing-fields", "id": item_id, "fields": missing})
        if item.get("status") not in ALLOWED_STATUS:
            issues.append({"kind": "invalid-status", "id": item_id, "status": item.get("status")})
        if item_id in by_id:
            issues.append({"kind": "duplicate-id", "id": item_id})
        elif item_id:
            by_id[item_id] = item

    for item in items:
        for dep in item.get("depends_on", []):
            if dep not in by_id:
                issues.append({"kind": "missing-dependency", "id": item.get("id"), "dependency": dep})
        for spec in item.get("specs", []):
            if not (ROOT / spec).exists():
                issues.append({"kind": "missing-spec", "id": item.get("id"), "path": spec})
        if item.get("status") == "COMPLETE":
            receipt = RECEIPTS / f"{item.get('id')}.json"
            if not receipt.exists():
                issues.append({"kind": "complete-without-receipt", "id": item.get("id"), "path": str(receipt.relative_to(ROOT))})

    ready = sorted((item for item in items if item.get("status") == "READY"), key=lambda item: (item.get("priority", 10**9), item.get("id", "")))
    return {
        "schema": "risingsea.doctor.v2",
        "status": "PASS" if not issues else "FAIL",
        "checks": {"work_items": len(items), "events": len(events), "issues": len(issues), "ready": len(ready)},
        "top_ready": ready[0]["id"] if ready else None,
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
        print(f"{result['status']}: {result['checks']['work_items']} work items; {result['checks']['issues']} issue(s)")
        for issue in result["issues"]:
            print(f"- {issue}")
        if result["top_ready"]:
            print(f"next: {result['top_ready']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
