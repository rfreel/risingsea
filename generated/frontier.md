# Current Frontier

> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W005 — Implement DomainMachine contract and registry validator**

Create the machine contract that encodes expert-native representations, diagnostics, repair/oracle routes, ruin boundaries and donors for each domain.

Acceptance:

- DomainMachine schema and registry exist
- Three real domain machines validate: planning, external-effect, security
- Every donor declares repository, mechanism, adoption mode and claim boundary
- Every machine has an unresolved/discovery route
- CI rejects duplicate IDs, missing machine files and incomplete donor contracts

Strongest falsifier: A domain machine can validate while omitting the representation or route needed to handle an unresolved case.

Next action: `Write and observe the failing domain-machine test before adding the registry and validator.`

## Blocked

- `RS-W006` — Implement capability and truth-source observation — blocked by: RS-W005
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
