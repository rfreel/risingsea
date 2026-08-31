# Current Frontier

> GENERATED from `fold(work/items.jsonl, work/events.jsonl)` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W011 — Implement unresolved discovery engine**

When normal repair cannot resolve a problem, preserve rivals and mechanically seek discriminating evidence instead of improvising.

Acceptance:

- Prior exact cases and exemplars are searched before new generation
- At least two live rivals are preserved until evidence dominates
- APR convergence does not upgrade truth
- New distinctions can emit checker/rule/representation/recipe candidates

Strongest falsifier: The discovery engine collapses an unresolved rival set to one answer without new evidence.

Next action: `Write adversarial discovery tests that preserve rivals, search exact prior cases first, keep incomplete-search novelty UNKNOWN, and route unsafe experiments through RuinGuard.`

## Blocked

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
