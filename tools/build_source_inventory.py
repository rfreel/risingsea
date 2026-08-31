#!/usr/bin/env python3
"""Build deterministic source inventory from sources/registry.jsonl."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "registry.jsonl"
OUT = ROOT / "generated" / "source-inventory.json"


def git_blob_id(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def load_rows() -> list[dict]:
    return [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    payload = REGISTRY.read_bytes()
    rows = load_rows()
    source_ids = [row["source_id"] for row in rows]
    if source_ids != sorted(source_ids):
        raise SystemExit("sources/registry.jsonl must be sorted by source_id")

    inventory = {
        "schema": "risingsea.source-inventory.v1",
        "source": "sources/registry.jsonl",
        "source_git_blob": git_blob_id(payload),
        "counts": {
            "total": len(rows),
            "by_disposition": dict(sorted(Counter(row["disposition"] for row in rows).items())),
            "by_availability": dict(sorted(Counter(row["availability"] for row in rows).items())),
            "by_kind": dict(sorted(Counter(row["source_kind"] for row in rows).items())),
        },
        "source_ids": source_ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
