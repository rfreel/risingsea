# Current Frontier

> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W007 — Implement RuinGuard adapter boundary**

Fail closed on ruin-class operations using DCG/FCP-style mechanical enforcement before ordinary action selection.

Acceptance:

- Destructive Git/filesystem/database and scope-explosion fixtures are blocked or require review
- Safe reads remain allowed
- Malformed classification never silently allows

Strongest falsifier: An unclassified potentially catastrophic operation reaches execution as allowed.

Next action: `Write and observe failing ruin-guard fixtures for destructive Git/filesystem/database operations, scope explosion, malformed input, and safe reads before adding guard rules.`

## Blocked

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
