#!/usr/bin/env python3
"""Contract tests for append-only work-state transitions."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK_STATE = ROOT / "tools" / "work_state.py"
EVENTS = ROOT / "work" / "events.jsonl"


def main() -> int:
    if not WORK_STATE.exists():
        print(f"FAIL missing {WORK_STATE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    if not EVENTS.exists():
        print(f"FAIL missing {EVENTS.relative_to(ROOT)}", file=sys.stderr)
        return 1

    result = subprocess.run(
        [sys.executable, str(WORK_STATE), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1
    payload = json.loads(result.stdout)
    by_id = {row["id"]: row for row in payload["items"]}

    w010_next = str(by_id["RS-W010"].get("next_action", ""))
    checks = [
        (by_id["RS-W007"]["status"] == "COMPLETE", "RS-W007 not COMPLETE"),
        (by_id["RS-W008"]["status"] == "COMPLETE", "RS-W008 not COMPLETE"),
        (by_id["RS-W009A"]["status"] == "COMPLETE", "RS-W009A not COMPLETE"),
        (by_id["RS-W009"]["status"] == "COMPLETE", "RS-W009 not COMPLETE"),
        ("RS-W009A" in by_id["RS-W009"]["depends_on"], "RS-W009 missing RS-W009A dependency"),
        (by_id["RS-W010"]["status"] == "READY", "RS-W010 not READY"),
        (bool(w010_next), "RS-W010 READY without next_action"),
        ("blocked until" not in w010_next.lower(), "RS-W010 READY with blocked next_action"),
        (payload["event_count"] >= 6, "expected append-only transition events"),
    ]
    failed = [message for ok, message in checks if not ok]
    if failed:
        for message in failed:
            print(f"FAIL {message}", file=sys.stderr)
        return 1

    seqs = [json.loads(line)["seq"] for line in EVENTS.read_text(encoding="utf-8").splitlines() if line.strip()]
    if seqs != list(range(1, len(seqs) + 1)):
        print(f"FAIL non-contiguous event sequence: {seqs}", file=sys.stderr)
        return 1

    print("PASS: append-only work event fold contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
