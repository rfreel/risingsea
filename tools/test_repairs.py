#!/usr/bin/env python3
"""Adversarial tests for bounded repair recipes and verification oracles."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "tools" / "validate_repairs.py"
SELECT = ROOT / "tools" / "select_repair.py"
RECIPES = ROOT / "repairs" / "registry.jsonl"
RECIPE_SCHEMA = ROOT / "contracts" / "repair-recipe.schema.json"
ORACLE_SCHEMA = ROOT / "contracts" / "verification-oracle.schema.json"


def require_artifacts() -> None:
    for path in (VALIDATE, SELECT, RECIPES, RECIPE_SCHEMA, ORACLE_SCHEMA):
        if not path.exists():
            raise AssertionError(f"missing required artifact: {path.relative_to(ROOT)}")


def diagnostic(verdict: str = "DEFECT", *, rule_ids: list[str] | None = None, observation_ids: list[str] | None = None) -> dict:
    return {
        "schema": "risingsea.diagnostic-receipt.v1",
        "problem_id": "problem-1",
        "domain": "build",
        "verdict": verdict,
        "rule_ids": rule_ids if rule_ids is not None else ["build.api.compiles"],
        "observation_ids": observation_ids if observation_ids is not None else ["obs-1"],
        "missing": [],
        "unknown_rule_ids": [],
        "model_candidates_considered": 0,
    }


def select(diag: dict, facts: dict | None = None) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        dpath = base / "diag.json"
        fpath = base / "facts.json"
        dpath.write_text(json.dumps(diag) + "\n", encoding="utf-8")
        fpath.write_text(json.dumps(facts or {}) + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SELECT), "--diagnostic", str(dpath), "--facts", str(fpath), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        raise AssertionError(f"selector failed: stdout={result.stdout!r} stderr={result.stderr!r}")
    return json.loads(result.stdout)


def test_registry_validates_and_every_recipe_has_oracle() -> None:
    require_artifacts()
    result = subprocess.run([sys.executable, str(VALIDATE), "--json"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, (result.stdout, result.stderr)
    payload = json.loads(result.stdout)
    assert payload["status"] == "PASS", payload
    assert payload["recipe_count"] >= 1, payload
    assert payload["oracle_count"] >= 1, payload


def test_matching_defect_selects_candidate_only_recipe() -> None:
    payload = select(diagnostic(), {"toolchain_available": True})
    assert payload["status"] == "SELECTED", payload
    recipe = payload["recipe"]
    assert recipe["recipe_id"] == "repair.build.api.compile", payload
    assert recipe["authority_effect"] == "candidate_only", payload
    assert recipe["verification_oracle_id"], payload
    assert recipe["write_set"], payload
    assert recipe["strongest_falsifier"], payload
    assert recipe["recovery"], payload


def test_unknown_diagnosis_cannot_select_repair() -> None:
    payload = select(diagnostic("UNKNOWN"), {"toolchain_available": True})
    assert payload["status"] == "NO_REPAIR", payload
    assert payload["reason"] == "DIAGNOSTIC_NOT_REPAIRABLE", payload


def test_unknown_precondition_blocks_selection() -> None:
    payload = select(diagnostic(), {})
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "PRECONDITION_UNKNOWN", payload
    assert payload["missing_preconditions"] == ["toolchain_available"], payload


def test_false_precondition_blocks_selection() -> None:
    payload = select(diagnostic(), {"toolchain_available": False})
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "PRECONDITION_FALSE", payload


def test_recipe_write_set_cannot_exceed_declared_scope() -> None:
    payload = select(diagnostic(), {"toolchain_available": True, "allowed_write_set": ["src/api.py"]})
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "WRITE_SET_OUTSIDE_ALLOWED_SCOPE", payload


def test_ruin_class_requires_authority_contract() -> None:
    payload = select(
        diagnostic(rule_ids=["security.destructive.operation"]),
        {"operator_confirmed": True, "allowed_write_set": ["guard/policy.json"]},
    )
    assert payload["status"] == "BLOCKED", payload
    assert payload["reason"] == "AUTHORITY_REQUIRED", payload


def test_registry_rejects_missing_oracle_mutant() -> None:
    rows = [json.loads(line) for line in RECIPES.read_text(encoding="utf-8").splitlines() if line.strip()]
    mutant = dict(rows[0])
    mutant.pop("verification_oracle_id", None)
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", encoding="utf-8", delete=False) as fh:
        fh.write(json.dumps(mutant) + "\n")
        path = Path(fh.name)
    try:
        result = subprocess.run([sys.executable, str(VALIDATE), "--registry", str(path), "--json"], cwd=ROOT, text=True, capture_output=True, check=False)
    finally:
        path.unlink(missing_ok=True)
    assert result.returncode != 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "FAIL", payload


def main() -> int:
    tests = [
        test_registry_validates_and_every_recipe_has_oracle,
        test_matching_defect_selects_candidate_only_recipe,
        test_unknown_diagnosis_cannot_select_repair,
        test_unknown_precondition_blocks_selection,
        test_false_precondition_blocks_selection,
        test_recipe_write_set_cannot_exceed_declared_scope,
        test_ruin_class_requires_authority_contract,
        test_registry_rejects_missing_oracle_mutant,
    ]
    failures: list[str] = []
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
