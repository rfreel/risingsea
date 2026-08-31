# Start Here

## Mission

Rising Sea exists to make repeated reasoning cheaper without sacrificing correctness, scope, provenance, or independent authority.

The operating loop is:

```text
source → spec → work packet → execute one item → witness → verify → receipt → learn → next
```

## Current status

- Repository architecture: flywheel-first bootstrap.
- Production runtime: not yet established in this repository.
- Current implementation frontier: establish the canonical current spec and import the existing Rising Sea planning corpus without losing provenance.
- Generated projections are non-authoritative.
- UNKNOWN must never be silently upgraded to PASS.

## What is canonical here?

1. `specs/` contains the current intended system contracts.
2. `work/items.jsonl` contains the current work graph.
3. `evidence/` contains receipts and witnesses.
4. `memory/` contains promoted procedural lessons and anti-patterns.
5. `generated/` is derived and rebuildable.

## What should happen next?

Read [`generated/frontier.md`](generated/frontier.md). It is a projection of `work/items.jsonl` and should identify exactly one highest-value ready item.

## What not to do

- Do not recursively ingest the whole repository by default.
- Do not execute work directly from historical source documents.
- Do not treat a plan as implementation evidence.
- Do not treat a successful command as proof of the intended semantic outcome.
- Do not create duplicate concepts because a search returned no result without checking canonical specs and work items first.

## Drill-down order

```text
START-HERE
→ generated/frontier.md
→ selected work packet
→ referenced spec(s)
→ required evidence
→ source material only if needed
```
