#!/usr/bin/env python3
"""Fold immutable work declarations plus append-only events into current work state."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "work" / "items.jsonl"
EVENTS = ROOT / "work" / "events.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected object")
        rows.append(value)
    return rows


def load_current_items() -> tuple[list[dict], list[dict]]:
    base = load_jsonl(ITEMS)
    events = load_jsonl(EVENTS)
    by_id: dict[str, dict] = {}
    for item in base:
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            raise ValueError("base work item missing id")
        if item_id in by_id:
            raise ValueError(f"duplicate base work id: {item_id}")
        by_id[item_id] = copy.deepcopy(item)

    expected_seq = 1
    seen_event_ids: set[str] = set()
    for event in events:
        if event.get("seq") != expected_seq:
            raise ValueError(f"work event seq expected {expected_seq}, got {event.get('seq')}")
        expected_seq += 1
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id or event_id in seen_event_ids:
            raise ValueError(f"invalid/duplicate event_id: {event_id!r}")
        seen_event_ids.add(event_id)

        event_type = event.get("type")
        if event_type == "ITEM_DEFINED":
            item = event.get("item")
            if not isinstance(item, dict):
                raise ValueError(f"{event_id}: ITEM_DEFINED missing item")
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id:
                raise ValueError(f"{event_id}: defined item missing id")
            if item_id in by_id:
                raise ValueError(f"{event_id}: item already exists: {item_id}")
            by_id[item_id] = copy.deepcopy(item)
        elif event_type == "ITEM_STATUS_SET":
            item_id = event.get("item_id")
            if item_id not in by_id:
                raise ValueError(f"{event_id}: unknown item: {item_id}")
            status = event.get("status")
            if not isinstance(status, str) or not status:
                raise ValueError(f"{event_id}: missing status")
            by_id[item_id]["status"] = status
            if status == "COMPLETE":
                by_id[item_id]["next_action"] = f"Read {event.get('receipt', f'evidence/receipts/{item_id}.json')}"
        elif event_type == "DEPENDENCY_ADDED":
            item_id = event.get("item_id")
            dependency = event.get("dependency")
            if item_id not in by_id:
                raise ValueError(f"{event_id}: unknown item: {item_id}")
            if not isinstance(dependency, str) or not dependency:
                raise ValueError(f"{event_id}: missing dependency")
            deps = list(by_id[item_id].get("depends_on", []))
            if dependency not in deps:
                deps.append(dependency)
            by_id[item_id]["depends_on"] = sorted(deps)
        else:
            raise ValueError(f"{event_id}: unknown event type {event_type!r}")

    return [by_id[item_id] for item_id in sorted(by_id)], events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        items, events = load_current_items()
    except ValueError as exc:
        if args.json:
            print(json.dumps({"schema": "risingsea.work-state.v1", "status": "FAIL", "error": str(exc)}, indent=2, sort_keys=True))
        else:
            print(f"FAIL: {exc}")
        return 1
    payload = {
        "schema": "risingsea.work-state.v1",
        "source": ["work/items.jsonl", "work/events.jsonl"],
        "event_count": len(events),
        "items": items,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
