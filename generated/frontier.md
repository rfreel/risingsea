# Current Frontier

> GENERATED from `fold(work/items.jsonl, work/events.jsonl)` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W012 — Implement obligation residual compiler**

Partition obligations totally and disjointly, sending only UNSATISFIED obligations into executable TODO candidates.

Acceptance:

- Partition is total and disjoint
- Only UNSATISFIED enters TODO candidates
- CONTRADICTED and UNKNOWN remain separate frontier classes

Strongest falsifier: An UNKNOWN or contradicted obligation is emitted as an executable TODO.

Next action: `Write adversarial residual-partition tests proving total/disjoint classification and that only UNSATISFIED obligations can become executable TODO candidates.`

## Blocked

- `RS-W013` — Implement frontier-resolved WorkPacket lowering — blocked by: RS-W010, RS-W012
- `RS-W014` — Implement external-effect reconciliation adapter — blocked by: RS-W007, RS-W010, RS-W013
- `RS-W015` — Implement procedural expertise compiler — blocked by: RS-W011, RS-W014
- `RS-W016` — Implement novice expert-control surface — blocked by: RS-W005, RS-W009, RS-W010, RS-W011, RS-W013
- `RS-W017` — Run adversarial expert-control benchmark — blocked by: RS-W006, RS-W007, RS-W008, RS-W009, RS-W010, RS-W011, RS-W012, RS-W013, RS-W014, RS-W015, RS-W016
- `RS-W002` — Compile imported corpus into canonical current specs — blocked by: RS-W001B
- `RS-W003` — Compile dependency-aware implementation work graph — blocked by: RS-W002, RS-W013
- `RS-W004` — Run matched cold-agent flywheel navigation benchmark — blocked by: RS-W003, RS-W017

## Partial

- `RS-W001` — Import complete Rising Sea planning corpus with provenance — Source registration and current agent-layer vendoring are established; base-system vendoring remains incomplete.
