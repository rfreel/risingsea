#!/usr/bin/env python3
"""Regression contract for compact, decision-relevant flywheel triage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "generated" / "triage.json"
BUILDER = ROOT / "tools" / "build_frontier.py"

TOP_KEYS = {
    "schema",
    "source",
    "counts",
    "top_ready",
    "ready",
    "blocked",
    "partial",
    "next_command",
}
TOP_READY_KEYS = {
    "id",
    "title",
    "objective",
    "acceptance",
    "strongest_falsifier",
    "next_action",
}
READY_KEYS = {"id", "title", "priority", "next_action"}
BLOCKED_KEYS = {"id", "title", "depends_on"}
PARTIAL_KEYS = {"id", "title", "partial_reason", "next_action"}


def assert_keys(label: str, value: dict, expected: set[str]) -> None:
    actual = set(value)
    if actual != expected:
        raise AssertionError(f"{label}: expected keys {sorted(expected)}, got {sorted(actual)}")


def main() -> int:
    subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    payload = json.loads(TRIAGE.read_text(encoding="utf-8"))

    assert_keys("triage", payload, TOP_KEYS)
    if payload["schema"] != "risingsea.triage.v2":
        raise AssertionError(f"unexpected schema {payload['schema']!r}")

    top = payload["top_ready"]
    if top is not None:
        assert_keys("top_ready", top, TOP_READY_KEYS)

    for item in payload["ready"]:
        assert_keys(f"ready:{item.get('id')}", item, READY_KEYS)
    for item in payload["blocked"]:
        assert_keys(f"blocked:{item.get('id')}", item, BLOCKED_KEYS)
    for item in payload["partial"]:
        assert_keys(f"partial:{item.get('id')}", item, PARTIAL_KEYS)

    counts = payload["counts"]
    expected_count_keys = {"total", "ready", "blocked", "complete", "partial", "other"}
    if set(counts) != expected_count_keys:
        raise AssertionError(f"unexpected count keys: {sorted(counts)}")
    if counts["total"] != counts["ready"] + counts["blocked"] + counts["complete"] + counts["partial"] + counts["other"]:
        raise AssertionError(f"status partition does not cover current work graph: {counts}")

    forbidden = {"specs", "expected_accretion", "authority_ceiling"}
    encoded = json.dumps(payload, sort_keys=True)
    for key in forbidden:
        if f'"{key}"' in encoded:
            raise AssertionError(f"triage leaked non-decision field {key}")

    print("PASS: compact frontier projection contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
