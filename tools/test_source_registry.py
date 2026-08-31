#!/usr/bin/env python3
"""Contract test for the Rising Sea source registry."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "registry.jsonl"
ALLOWED_DISPOSITIONS = {
    "CURRENT_SOURCE",
    "HISTORICAL_SOURCE",
    "SUPERSEDED_SOURCE",
    "DUPLICATE_SOURCE",
    "EXTERNAL_REFERENCE",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = {
    "source_id",
    "name",
    "origin",
    "sha256",
    "bytes",
    "source_kind",
    "disposition",
    "discovered_at",
    "availability",
}


def load_registry() -> list[dict]:
    assert REGISTRY.exists(), "sources/registry.jsonl must exist"
    rows = []
    for line_no, raw in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSON on line {line_no}: {exc}") from exc
        rows.append(row)
    return rows


def test_registry_contract() -> None:
    rows = load_registry()
    assert rows, "registry must contain at least one source"
    ids = [row.get("source_id") for row in rows]
    assert len(ids) == len(set(ids)), "source_id values must be unique"
    assert ids == sorted(ids), "registry must be sorted by source_id"

    for row in rows:
        missing = REQUIRED - set(row)
        assert not missing, f"{row.get('source_id')}: missing {sorted(missing)}"
        assert row["origin"], f"{row['source_id']}: origin is required"
        assert SHA256_RE.fullmatch(row["sha256"]), f"{row['source_id']}: invalid sha256"
        assert isinstance(row["bytes"], int) and row["bytes"] >= 0
        assert row["disposition"] in ALLOWED_DISPOSITIONS
        assert row["availability"] in {"VENDORED", "REGISTERED_ONLY", "EXTERNAL"}

        if row["availability"] == "VENDORED":
            vendored = ROOT / row["repo_path"]
            assert vendored.is_file(), f"{row['source_id']}: missing vendored bytes"
            payload = vendored.read_bytes()
            assert len(payload) == row["bytes"], f"{row['source_id']}: byte count mismatch"
            assert hashlib.sha256(payload).hexdigest() == row["sha256"], (
                f"{row['source_id']}: vendored hash mismatch"
            )


if __name__ == "__main__":
    test_registry_contract()
    print("PASS: source registry contract")
