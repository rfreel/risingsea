# Current Frontier

> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W006 — Implement capability and truth-source observation**

Observe capabilities, truth-source class, readiness and degradation without inferring live state from documentation.

Acceptance:

- OBSERVED, DOCUMENTED, UNAVAILABLE and UNKNOWN remain distinct
- Missing donor tool degrades explicitly
- Every degradation includes a repair command where known

Strongest falsifier: The system reports a capability as available solely because a document says it exists.

Next action: `Write and observe the failing capability/truth-source contract test before implementing deterministic probes.`

## Blocked

- `RS-W007` — Implement RuinGuard adapter boundary — blocked by: RS-W005, RS-W006
- `RS-W008` — Implement deterministic expert router — blocked by: RS-W005, RS-W006, RS-W007
- `RS-W009` — Implement expert diagnostic compiler — blocked by: RS-W008
- `RS-W010` — Implement repair recipe and verification-oracle registry — blocked by: RS-W009
- `RS-W011` — Implement unresolved discovery engine — blocked by: RS-W008, RS-W009, RS-W010
- `RS-W012` — Implement obligation residual compiler — blocked by: RS-W009, RS-W011
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
