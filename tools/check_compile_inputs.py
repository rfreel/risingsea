#!/usr/bin/env python3
"""Validate the source closure required by RS-W002.

Default mode is read-only progress validation: missing planned files are reported
but do not fail. --require-complete is the promotion gate for RS-W001B.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "compile-inputs.json"
REGISTRY = ROOT / "sources" / "registry.jsonl"


def registry_rows() -> dict[str, dict]:
    rows = {}
    for raw in REGISTRY.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        row = json.loads(raw)
        rows[row["source_id"]] = row
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = registry_rows()
    errors: list[str] = []

    agent_ids = manifest["groups"]["agent_centric_layer"]["source_ids"]
    for source_id in agent_ids:
        row = registry.get(source_id)
        if row is None:
            errors.append(f"{source_id}: missing from registry")
        elif row.get("availability") != "VENDORED":
            errors.append(f"{source_id}: expected VENDORED, got {row.get('availability')}")

    planned = manifest["groups"]["base_system_layer"]["planned_sources"]
    planned_ids = [row["planned_source_id"] for row in planned]
    if len(planned_ids) != len(set(planned_ids)):
        errors.append("duplicate planned_source_id")

    missing: list[str] = []
    verified: list[str] = []
    for row in planned:
        path = ROOT / row["repo_path"]
        if not path.is_file():
            missing.append(row["planned_source_id"])
            continue
        payload_len = path.stat().st_size
        digest = sha256(path)
        if payload_len != row["bytes"]:
            errors.append(
                f"{row['planned_source_id']}: bytes {payload_len} != expected {row['bytes']}"
            )
        if digest != row["sha256"]:
            errors.append(f"{row['planned_source_id']}: sha256 mismatch")
        registered = registry.get(row["planned_source_id"])
        if registered is None:
            errors.append(f"{row['planned_source_id']}: vendored file exists but registry row is missing")
        elif registered.get("availability") != "VENDORED":
            errors.append(
                f"{row['planned_source_id']}: vendored file exists but registry availability is {registered.get('availability')}"
            )
        else:
            verified.append(row["planned_source_id"])

    if args.require_complete and missing:
        errors.append(f"retrieval closure incomplete: {len(missing)} planned source(s) missing")

    report = {
        "schema": "risingsea.compile-input-check.v1",
        "work_id": manifest["work_id"],
        "consumer": manifest["consumer"],
        "agent_source_count": len(agent_ids),
        "base_planned": len(planned),
        "base_verified": len(verified),
        "base_missing": len(missing),
        "missing_source_ids": missing,
        "errors": errors,
        "complete": not missing and not errors,
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"compile inputs: agent={len(agent_ids)} base_verified={len(verified)} "
            f"base_missing={len(missing)} errors={len(errors)}"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
