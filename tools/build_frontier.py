#!/usr/bin/env python3
"""Build deterministic, compact flywheel triage projections from work/items.jsonl."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work" / "items.jsonl"
OUT = ROOT / "generated"


def load_items() -> list[dict]:
    items = []
    for line_no, raw in enumerate(WORK.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            items.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{WORK}:{line_no}: invalid JSON: {exc}") from exc
    return items


def ready_projection(item: dict) -> dict:
    return {
        "id": item["id"],
        "title": item["title"],
        "priority": item.get("priority"),
        "next_action": item.get("next_action"),
    }


def blocked_projection(item: dict) -> dict:
    return {
        "id": item["id"],
        "title": item["title"],
        "depends_on": item.get("depends_on", []),
    }


def partial_projection(item: dict) -> dict:
    return {
        "id": item["id"],
        "title": item["title"],
        "partial_reason": item.get("partial_reason"),
        "next_action": item.get("next_action"),
    }


def top_projection(item: dict | None) -> dict | None:
    if item is None:
        return None
    return {
        "id": item["id"],
        "title": item["title"],
        "objective": item["objective"],
        "acceptance": item.get("acceptance", []),
        "strongest_falsifier": item.get("strongest_falsifier"),
        "next_action": item.get("next_action"),
    }


def main() -> int:
    items = load_items()
    ready = sorted(
        (item for item in items if item.get("status") == "READY"),
        key=lambda item: (item.get("priority", 10**9), item["id"]),
    )
    blocked = sorted(
        (item for item in items if item.get("status") == "BLOCKED"),
        key=lambda item: (item.get("priority", 10**9), item["id"]),
    )
    partial = sorted(
        (item for item in items if item.get("status") == "PARTIAL"),
        key=lambda item: (item.get("priority", 10**9), item["id"]),
    )
    complete = [item for item in items if item.get("status") == "COMPLETE"]
    classified = {"READY", "BLOCKED", "PARTIAL", "COMPLETE"}
    other = [item for item in items if item.get("status") not in classified]

    top = ready[0] if ready else None
    triage = {
        "schema": "risingsea.triage.v2",
        "source": "work/items.jsonl",
        "counts": {
            "total": len(items),
            "ready": len(ready),
            "blocked": len(blocked),
            "partial": len(partial),
            "complete": len(complete),
            "other": len(other),
        },
        "top_ready": top_projection(top),
        "ready": [ready_projection(item) for item in ready],
        "blocked": [blocked_projection(item) for item in blocked],
        "partial": [partial_projection(item) for item in partial],
        "next_command": top.get("next_action") if top else None,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "triage.json").write_text(
        json.dumps(triage, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# Current Frontier",
        "",
        "> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.",
        "",
    ]
    if top:
        lines.extend(
            [
                "## Highest-value ready item",
                "",
                f"**{top['id']} — {top['title']}**",
                "",
                top["objective"],
                "",
                "Acceptance:",
                "",
                *[f"- {criterion}" for criterion in top.get("acceptance", [])],
                "",
                f"Strongest falsifier: {top.get('strongest_falsifier', 'not recorded')}",
                "",
                f"Next action: `{top.get('next_action', '')}`",
                "",
            ]
        )
    else:
        lines.extend(["No READY work items.", ""])

    if blocked:
        lines.extend(["## Blocked", ""])
        for item in blocked:
            deps = ", ".join(item.get("depends_on", [])) or "none recorded"
            lines.append(f"- `{item['id']}` — {item['title']} — blocked by: {deps}")
        lines.append("")

    if partial:
        lines.extend(["## Partial", ""])
        for item in partial:
            reason = item.get("partial_reason") or "partial state recorded"
            lines.append(f"- `{item['id']}` — {item['title']} — {reason}")
        lines.append("")

    (OUT / "frontier.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
