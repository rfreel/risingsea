# Current Frontier

> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W001 — Import complete Rising Sea planning corpus with provenance**

Ingest the existing Rising Sea planning artifacts as immutable source material without turning historical documents into current authority.

Acceptance:

- Every imported source has path or URI, SHA-256, source kind, and disposition
- Current and historical planning artifacts remain distinguishable
- No source is silently rewritten during import
- A source inventory can be regenerated deterministically

Strongest falsifier: An imported document cannot be traced back to its exact original bytes or external reference.

Next action: `Create sources/registry.jsonl from the available planning artifacts and retain exact hashes.`

## Blocked

- `RS-W002` — Compile imported corpus into canonical current specs — blocked by: RS-W001
- `RS-W003` — Compile dependency-aware implementation work graph — blocked by: RS-W002
- `RS-W004` — Run matched cold-agent flywheel navigation benchmark — blocked by: RS-W003
