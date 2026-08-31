# Agent-Centric v2 Verification Report

Overall: **PASS_WITH_UNKNOWN**

| Result | Count |
|---|---:|
| PASS | 18 |
| FAIL | 0 |
| UNKNOWN | 1 |

## Checks

- **PASS — required_files**: required=18 missing=0
- **PASS — json_integrity**: parsed=231 errors=0
- **PASS — schema_meta_validation**: schemas=26
- **PASS — schema_examples**: examples=24
- **PASS — family_manifests**: families=22 expected=22
- **PASS — spo_registry**: rows=133 unique=133
- **PASS — spo_row_parity**: row_files=133
- **PASS — spo_csv_parity**: csv_rows=133
- **PASS — cognitive_isa**: commands=20 slices=22 designs=10
- **PASS — slice_agent_contracts**: slice_docs=22
- **PASS — markdown_parse**: markdown_files=57
- **PASS — draft_marker_scan**: hits=0
- **PASS — internal_links**: broken=0
- **PASS — html_parse**: html_files=1
- **PASS — graphviz_render**: dot_files=6
- **PASS — agent_control_model**: base_pass=True mutants=6
- **PASS — base_safety_model**: retained v1 bounded safety model
- **UNKNOWN — tlc_execution**: TLA+ source retained, but java/tla2tools.jar is unavailable in this environment.
- **PASS — artifact_manifest**: listed=310

## Evidence boundary

Structural and bounded-model verification only; live runtime and empirical ergonomics are not established.
