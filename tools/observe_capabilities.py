#!/usr/bin/env python3
"""Observe local capability truth without promoting documentation to runtime state."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "infrastructure" / "donors" / "capability-truth.json"


def load_catalog(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "risingsea.capability-catalog.v1":
        raise ValueError(f"unsupported catalog schema: {data.get('schema')!r}")
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list):
        raise ValueError("catalog capabilities must be a list")
    return data


def observe(entry: dict) -> dict:
    capability_id = entry.get("capability_id")
    if not isinstance(capability_id, str) or not capability_id:
        raise ValueError("capability_id must be a non-empty string")

    command = entry.get("command")
    documentation_uri = entry.get("documentation_uri")
    repair_command = entry.get("repair_command")
    observed_path = shutil.which(command) if isinstance(command, str) and command else None

    if observed_path:
        truth_state = "OBSERVED"
        truth_source_class = "HOST_OBSERVED"
        readiness = "READY"
    elif documentation_uri:
        truth_state = "DOCUMENTED"
        truth_source_class = "DOCUMENTATION_ONLY"
        readiness = "UNAVAILABLE"
    else:
        truth_state = "UNKNOWN"
        truth_source_class = "UNKNOWN"
        readiness = "UNKNOWN"

    return {
        "capability_id": capability_id,
        "truth_state": truth_state,
        "truth_source_class": truth_source_class,
        "readiness": readiness,
        "observed_path": observed_path,
        "documentation_uri": documentation_uri,
        "repair_command": repair_command,
    }


def build_observation(catalog_path: Path) -> dict:
    catalog = load_catalog(catalog_path)
    capabilities = [observe(entry) for entry in catalog["capabilities"]]
    capabilities.sort(key=lambda item: item["capability_id"])

    degraded = []
    for item in capabilities:
        if item["readiness"] == "READY":
            continue
        if item["readiness"] == "UNAVAILABLE":
            reason = "Capability is documented but no executable was observed on PATH."
        else:
            reason = "Capability availability is unknown because neither an executable nor authoritative local evidence was observed."
        degraded.append(
            {
                "capability_id": item["capability_id"],
                "readiness": item["readiness"],
                "reason": reason,
                "repair_command": item["repair_command"],
            }
        )

    try:
        catalog_name = str(catalog_path.relative_to(ROOT))
    except ValueError:
        catalog_name = str(catalog_path)

    return {
        "schema": "risingsea.capability-observation.v1",
        "catalog": catalog_name,
        "capabilities": capabilities,
        "degraded": degraded,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        payload = build_observation(args.catalog)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if args.json:
            print(
                json.dumps(
                    {
                        "schema": "risingsea.capability-observation-error.v1",
                        "status": "FAIL",
                        "error": str(exc),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(f"FAIL: {exc}")
        return 1

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for item in payload["capabilities"]:
            print(
                f"{item['capability_id']}: {item['truth_state']} / {item['readiness']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
