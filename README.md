# Rising Sea

Rising Sea is a planning and execution flywheel for turning recurring inference into verified, reusable deterministic substrate.

This repository is not a document dump. Planning documents compile into current specifications; specifications compile into self-contained work packets; work produces verification receipts; receipts compile back into specifications, tests, rules, negative memos, and procedural memory so the next loop is cheaper.

```text
SOURCE CORPUS
    ↓
CURRENT SPEC
    ↓
SELF-CONTAINED WORK
    ↓
HIGHEST-VALUE READY ITEM
    ↓
EXECUTE ONE ITEM
    ↓
VERIFY WITH WITNESS
    ↓
RECEIPT
    ↓
COMPILE LEARNING BACK
    ↓
CHEAPER NEXT LOOP
```

## Start

Human: read [`START-HERE.md`](START-HERE.md).

Agent: read [`AGENTS.md`](AGENTS.md), then [`generated/frontier.md`](generated/frontier.md).

## Repository surfaces

- `specs/` — canonical current planning/specification state.
- `work/` — self-contained dependency-aware work packets.
- `evidence/` — verification receipts, witnesses, experiments, and claim evidence.
- `memory/` — procedural rules, anti-patterns, negative memos, and reusable lessons.
- `sources/` — original/imported planning material and provenance.
- `generated/` — rebuildable triage/frontier/index projections. Never authoritative.
- `tools/` — deterministic repository checks and projection builders.

## Core law

`LLM OUTPUT != STATE TRANSITION`.

PASS, PROMOTED, AUTHORIZED, ATTEMPTED, OBSERVED, and ACCEPTED are separate states. UNKNOWN remains UNKNOWN.
