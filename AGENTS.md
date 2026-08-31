# AGENTS.md — Rising Sea

## Cold start

1. Read `START-HERE.md`.
2. Read `generated/frontier.md`.
3. Select exactly one ready work packet from `work/items.jsonl` unless an explicit parallel plan authorizes more.
4. Load only the specs and evidence referenced by that packet.

## Flywheel law

```text
SOURCE → SPEC → WORK → WITNESS → VERIFY → RECEIPT → LEARN → REENTER
```

Every substantive iteration must either reduce the unresolved frontier or produce a reusable artifact that makes a future iteration cheaper.

## Authority rules

- `LLM OUTPUT != STATE TRANSITION`.
- A proposal is a candidate only.
- Validation, promotion, authorization, execution intent, attempt, observation, reconciliation, and acceptance are distinct.
- `UNKNOWN` remains `UNKNOWN`.
- A timeout or missing response does not prove external success or failure.
- Generated files never become canonical merely because they are easier to read.

## Work selection

Prefer this order:

```text
exact verified reuse
→ structural lookup
→ deterministic rule/table/automaton
→ mechanical closure/validation
→ bounded retrieval
→ evidence acquisition / distinction
→ LLM only on unresolved residual
```

Work exactly one highest-value ready packet per loop. Before starting, verify dependencies are closed and acceptance criteria are explicit.

## Completion protocol

A packet is not complete because prose or code exists. Completion requires:

1. acceptance witness;
2. verification receipt;
3. updated work status;
4. any new procedural lesson, anti-pattern, test, rule, or negative memo captured under `memory/` or `evidence/`;
5. regenerated frontier/triage projection.

If no reusable learning was produced, record `no_accretion_reason` in the receipt.

## Search discipline

Before creating a durable concept or work item:

```text
exact ID/title
→ canonical specs
→ current work graph
→ evidence/memory
→ broader repository search
```

Search absence is not proof of non-existence. If duplicate risk remains, mark the candidate explicitly rather than silently forking the concept.

## Editing discipline

- Prefer updating the canonical object over creating `-v2`, `-final`, or `-revised` copies.
- Preserve history through Git and explicit supersession notes.
- Do not edit files under `generated/` by hand unless repairing the generator and regenerating immediately.
- Never fabricate receipts, tests, implementation state, or external observations.

## Status axes

Keep these independent:

- claim: `PASS | FAIL | UNKNOWN`
- lifecycle: `CANDIDATE | SHADOW | PROMOTED | RETIRED`
- work: `READY | CLAIMED | RUNNING | BLOCKED | REVIEW | COMPLETE | PARTIAL | ABANDONED`
- operation: `PROPOSED | AUTHORIZED | INTENDED | ATTEMPTED | OBSERVED | ACCEPTED | REJECTED | PARTIAL | UNKNOWN`

Do not alias one axis to another.
