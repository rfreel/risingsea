#!/usr/bin/env python3
"""Contract tests for deterministic capability and truth-source observation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVER = ROOT / "tools" / "observe_capabilities.py"
SCHEMA = ROOT / "contracts" / "capability-observation.schema.json"
DONOR_CONTRACT = ROOT / "infrastructure" / "donors" / "capability-truth.json"


def require(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")


def run_observer(catalog: Path, path_env: str) -> dict:
    env = dict(os.environ)
    env["PATH"] = path_env
    result = subprocess.run(
        [sys.executable, str(OBSERVER), "--catalog", str(catalog), "--json"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"observer failed:\nstdout={result.stdout}\nstderr={result.stderr}")
    return json.loads(result.stdout)


def test_truth_and_readiness_axes() -> None:
    require(OBSERVER)
    require(SCHEMA)
    require(DONOR_CONTRACT)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        observed = bin_dir / "fake-observed-tool"
        observed.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        observed.chmod(0o755)

        catalog = tmp_path / "catalog.json"
        catalog.write_text(
            json.dumps(
                {
                    "schema": "risingsea.capability-catalog.v1",
                    "capabilities": [
                        {
                            "capability_id": "observed-tool",
                            "command": "fake-observed-tool",
                            "documentation_uri": "https://example.invalid/observed",
                            "repair_command": "install observed-tool"
                        },
                        {
                            "capability_id": "documented-missing",
                            "command": "definitely-not-installed-risingsea-tool",
                            "documentation_uri": "https://example.invalid/documented",
                            "repair_command": "install documented-missing"
                        },
                        {
                            "capability_id": "unknown-tool",
                            "command": null,
                            "documentation_uri": null,
                            "repair_command": null
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        payload = run_observer(catalog, str(bin_dir))
        if payload.get("schema") != "risingsea.capability-observation.v1":
            raise AssertionError(payload)
        by_id = {item["capability_id"]: item for item in payload["capabilities"]}

        observed_row = by_id["observed-tool"]
        assert observed_row["truth_state"] == "OBSERVED", observed_row
        assert observed_row["readiness"] == "READY", observed_row
        assert observed_row["truth_source_class"] == "HOST_OBSERVED", observed_row
        assert observed_row["observed_path"].endswith("fake-observed-tool"), observed_row

        missing_row = by_id["documented-missing"]
        assert missing_row["truth_state"] == "DOCUMENTED", missing_row
        assert missing_row["readiness"] == "UNAVAILABLE", missing_row
        assert missing_row["truth_source_class"] == "DOCUMENTATION_ONLY", missing_row
        assert missing_row["observed_path"] is None, missing_row
        assert missing_row["repair_command"] == "install documented-missing", missing_row

        unknown_row = by_id["unknown-tool"]
        assert unknown_row["truth_state"] == "UNKNOWN", unknown_row
        assert unknown_row["readiness"] == "UNKNOWN", unknown_row
        assert unknown_row["truth_source_class"] == "UNKNOWN", unknown_row
        assert unknown_row["observed_path"] is None, unknown_row

        degraded = {item["capability_id"]: item for item in payload["degraded"]}
        assert "documented-missing" in degraded, payload
        assert degraded["documented-missing"]["repair_command"] == "install documented-missing"
        assert "observed-tool" not in degraded, payload


def test_documentation_never_implies_ready() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        catalog = tmp_path / "catalog.json"
        catalog.write_text(
            json.dumps(
                {
                    "schema": "risingsea.capability-catalog.v1",
                    "capabilities": [
                        {
                            "capability_id": "documented-only",
                            "command": "not-present-anywhere-risingsea",
                            "documentation_uri": "https://example.invalid/tool",
                            "repair_command": "install it"
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        payload = run_observer(catalog, str(tmp_path))
        row = payload["capabilities"][0]
        if row["truth_state"] == "OBSERVED" or row["readiness"] == "READY":
            raise AssertionError(f"documentation was promoted to runtime observation: {row}")


def main() -> int:
    tests = [test_truth_and_readiness_axes, test_documentation_never_implies_ready]
    failures = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failures.append(f"{test.__name__}: {exc}")
            print(f"FAIL {test.__name__}: {exc}", file=sys.stderr)
    if failures:
        print(f"FAILED {len(failures)}/{len(tests)}", file=sys.stderr)
        return 1
    print(f"PASS {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
