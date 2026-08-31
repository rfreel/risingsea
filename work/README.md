# Work Graph

`items.jsonl` is the canonical planning work graph for this repository.

Each line is one self-contained work packet. Generated triage/frontier views derive from it.

## Rules

- Exactly one highest-value READY packet is the default next item.
- `BLOCKED` packets name their dependencies.
- `COMPLETE` requires a receipt under `evidence/receipts/`.
- Work status is independent from claim, lifecycle, and operation status.
- A packet should be executable without rereading the full source corpus.

## Minimum fields

```json
{
  "id": "RS-W001",
  "title": "...",
  "status": "READY",
  "priority": 1,
  "objective": "...",
  "depends_on": [],
  "specs": ["specs/current-system.md"],
  "acceptance": ["..."],
  "strongest_falsifier": "...",
  "authority_ceiling": "candidate",
  "expected_accretion": ["..."],
  "next_action": "..."
}
```
