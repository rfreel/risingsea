#!/usr/bin/env python3
"""Contract test for the generated source inventory projection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "registry.jsonl"
INVENTORY = ROOT / "generated" / "source-inventory.json"


def load_rows() -> list[dict]:
    return [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    assert INVENTORY.exists(), "generated/source-inventory.json must exist"
    rows = load_rows()
    observed = json.loads(INVENTORY.read_text(encoding="utf-8"))
    expected_digest = hashlib.sha256(REGISTRY.read_bytes()).hexdigest()

    assert observed["schema"] == "risingsea.source-inventory.v1"
    assert observed["source"] == "sources/registry.jsonl"
    assert observed["source_digest"] == expected_digest
    assert observed["counts"]["total"] == len(rows)
    assert sum(observed["counts"]["by_disposition"].values()) == len(rows)
    assert sum(observed["counts"]["by_availability"].values()) == len(rows)
    assert observed["source_ids"] == [row["source_id"] for row in rows]
    assert observed["source_ids"] == sorted(observed["source_ids"])
    print("PASS: deterministic source inventory contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
