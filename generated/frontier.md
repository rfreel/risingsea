# Current Frontier

> GENERATED from `fold(work/items.jsonl, work/events.jsonl)` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W013 — Implement frontier-resolved WorkPacket lowering**

Lower residual obligations into packets a simple executor can run without architecture, scope, test or recovery decisions.

Acceptance:

- Packets with unresolved design alternatives are rejected
- Reasoning-debt vector is below release threshold
- Execution grammar is READ-CHECK-CHANGE-VERIFY-RECEIPT-STOP

Strongest falsifier: A worker must make an undeclared design, scope or verification decision during packet execution.

Next action: `Write adversarial WorkPacket-lowering mutations for missing oracle, unresolved strategy, widened write set, stale head, missing failure route, authority ambiguity, and undefined semantic terms before implementing lowering.`

## Blocked

- `RS-W014` — Implement external-effect reconciliation adapter — blocked by: RS-W007, RS-W010, RS-W013
- `RS-W015` — Implement procedural expertise compiler — blocked by: RS-W011, RS-W014
- `RS-W016` — Implement novice expert-control surface — blocked by: RS-W005, RS-W009, RS-W010, RS-W011, RS-W013
- `RS-W017` — Run adversarial expert-control benchmark — blocked by: RS-W006, RS-W007, RS-W008, RS-W009, RS-W010, RS-W011, RS-W012, RS-W013, RS-W014, RS-W015, RS-W016
- `RS-W002` — Compile imported corpus into canonical current specs — blocked by: RS-W001B
- `RS-W003` — Compile dependency-aware implementation work graph — blocked by: RS-W002, RS-W013
- `RS-W004` — Run matched cold-agent flywheel navigation benchmark — blocked by: RS-W003, RS-W017

## Partial

- `RS-W001` — Import complete Rising Sea planning corpus with provenance — Source registration and current agent-layer vendoring are established; base-system vendoring remains incomplete.
