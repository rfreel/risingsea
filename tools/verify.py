#!/usr/bin/env python3
"""Run the same native integrity gates locally and in GitHub Actions."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (ROOT / ".python-version").read_text().strip()
if ".".join(map(str, sys.version_info[:3])) != EXPECTED:
    raise SystemExit(f"Use Python {EXPECTED}; current interpreter is {sys.version.split()[0]}")

COMMANDS = [['python', 'tools/test_source_registry.py'],
 ['python', 'tools/test_source_inventory.py'],
 ['python', 'tools/check_compile_inputs.py', '--json'],
 ['python', 'tools/test_domain_machines.py'],
 ['python', 'tools/test_capability_observation.py'],
 ['python', 'tools/test_ruin_guard.py'],
 ['python', 'tools/test_expert_router.py'],
 ['python', 'tools/test_observation_algebra.py'],
 ['python', 'tools/test_diagnostic_compiler.py'],
 ['python', 'tools/test_work_event_fold.py'],
 ['python', 'tools/test_repairs.py'],
 ['python', 'tools/test_discovery.py'],
 ['python', 'tools/test_residualize.py'],
 ['python', 'tools/test_work_packet_lowering.py'],
 ['python', 'tools/test_frontier_projection.py'],
 ['python', 'tools/doctor.py', '--json'],
 ['python', 'tools/build_source_inventory.py'],
 ['python', 'tools/build_frontier.py'],
 ['git', 'diff', '--exit-code', '--', 'generated/']]

for command in COMMANDS:
    print("+ " + " ".join(command), flush=True)
    if command[0] == "python":
        command = [sys.executable, *command[1:]]
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
