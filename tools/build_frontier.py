#!/usr/bin/env python3
"""Build deterministic flywheel triage projections from work/items.jsonl."""

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
    complete = [item for item in items if item.get("status") == "COMPLETE"]

    top = ready[0] if ready else None
    triage = {
        "schema": "risingsea.triage.v1",
        "source": "work/items.jsonl",
        "counts": {
            "total": len(items),
            "ready": len(ready),
            "blocked": len(blocked),
            "complete": len(complete),
        },
        "top_ready": top,
        "ready": ready,
        "blocked": blocked,
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

    (OUT / "frontier.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
