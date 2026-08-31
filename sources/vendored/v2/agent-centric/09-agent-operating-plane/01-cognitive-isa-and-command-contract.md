# Cognitive ISA and Agent Command Contract

## Objective

Define one small instruction set through which an agent can sense, decide, act, verify, recover, and learn without knowing which internal vertical slice performs the work.

The command surface is an **agent cognitive instruction set architecture**. It is not another authority. Each command compiles into one or more existing slice operations and returns one stable `OperatingEnvelope`.

## Entry rule

From zero conversational context, the agent runs:

```text
rs orient --mission <mission-id> --format json
```

A bare `rs --robot` is equivalent to `orient` for the current workspace and mission selection policy. Interactive human interfaces may differ, but agent mode is non-interactive.

## Command families

### Sense

| Command | Purpose | Canonical effect |
|---|---|---|
| `orient` | Produce a bounded, complete driver envelope | None |
| `diff` | Show material changes between heads/checkpoints | None |
| `inspect` | Retrieve one referenced object | None |
| `explain` | Return downward witness, scope, invalidators, and falsifier | None |

### Decide

| Command | Purpose | Canonical effect |
|---|---|---|
| `next` | Compute Pareto-undominated next actions | None |
| `plan` | Compile obligations into a work graph and packets | Candidate only |
| `distinguish` | Plan the minimum decisive observation | Candidate only |
| `simulate` | Produce a no-authority counterfactual | None |
| `verify` | Produce scoped validation/test receipts | Validation only |

### Change

| Command | Purpose | Canonical effect |
|---|---|---|
| `propose` | Register a typed candidate delta or primitive | Candidate event only when explicitly appended |
| `request-authority` | Evaluate exact policy and identity prerequisites | Admission evidence only |
| `commit-intent` | Append one exact authorized execution intent | Canonical append and execution-intent effect |
| `reconcile` | Observe and classify an attempted external effect | Terminal event only after canonical append |

### Improve and recover

| Command | Purpose | Canonical effect |
|---|---|---|
| `learn` | Create candidate reusable artifacts from evidence | Candidate only unless separately promoted |
| `checkpoint` | Persist a reconstruction point and resume capsule | Canonical append only when checkpoint retention requires it |
| `resume` | Reconstruct current work without chat memory | None |
| `handoff` | Produce a self-contained work packet and transfer proposal | Candidate/coordination only |

### Meta

| Command | Purpose | Canonical effect |
|---|---|---|
| `capabilities` | Report observed implementations and schemas | None |
| `doctor` | Compare required and observed runtime posture | None |
| `robot-docs` | Expose command and schema documentation | None |

## Command request contract

Every agent command request includes:

```json
{
  "schema": "rising-sea.agent-command-request.v2",
  "request_id": "req-...",
  "verb": "orient",
  "mission_id": "mission-...",
  "expect_history_head": "sha256:...",
  "expect_envelope_digest": null,
  "arguments": {},
  "context_profile": "brief",
  "budgets": {
    "tokens": 1200,
    "wall_time_ms": 5000,
    "compute_units": 100,
    "money_microunits": 0,
    "human_attention_seconds": 0,
    "external_effects": 0
  },
  "authority_request": null
}
```

`expect_history_head` is required for any head-dependent action and for all commands that may lead to mutation. `expect_envelope_digest` is required when selecting an action card from a prior envelope.

## Output mode

Agent mode obeys these stream rules:

- structured output only on stdout;
- diagnostics, progress, and human-readable warnings on stderr;
- exit status distinguishes successful response production from transport/process failure;
- domain `FAIL` and `UNKNOWN` remain inside the structured response and are not encoded only as process exit codes;
- JSON is the normative interchange format;
- TOON or another token-optimized representation may be offered only as a lossless alternative with declared schema identity and round-trip tests.

## Command response contract

Every command returns an `OperatingEnvelope`. Command-specific data lives under `payload`; the surrounding fields remain stable:

```json
{
  "schema": "rising-sea.operating-envelope.v2",
  "request_id": "req-...",
  "command": "orient",
  "response_status": "READY",
  "basis": {},
  "mission": {},
  "situation": {},
  "frontier": {},
  "actions": [],
  "payload": {},
  "receipts": [],
  "warnings": [],
  "degraded": [],
  "next_commands": [],
  "envelope_digest": "sha256:..."
}
```

## Universal command semantics

### `orient`

`orient` must be sufficient to start safe work. It returns:

- exact mission and exclusions;
- current head and projection freshness;
- changes since last checkpoint;
- observed, derived, validated, proposed, stale, and unknown facts;
- active obligations and blockers;
- pending effects requiring reconciliation;
- available capabilities and degraded subsystems;
- up to three Pareto-distinct next actions by default;
- an accretion opportunity;
- exact next commands.

### `next`

`next` applies this precedence:

```text
required safety and authority gates
  → exact reusable result
  → compiled structural/mechanical route
  → cheapest decisive observation
  → independent work packet
  → bounded semantic retrieval
  → LLM proposal
  → human decision when no authorized machine route exists
```

The command must not select a single action when two or more actions are materially incomparable and no ranking policy is authorized. It returns the frontier and explains the unresolved comparison.

### `inspect`

`inspect` retrieves one exact object and never performs broad semantic search unless the caller explicitly requests it. The response names:

- object schema and digest;
- canonical or derived status;
- producing head and freshness;
- provenance and invalidators;
- related objects by typed relation;
- safe drill-down commands.

### `explain`

`explain` answers:

1. What claim or decision is being explained?
2. Which lower-layer facts and rules support it?
3. Which source classes are present?
4. What scope and freshness apply?
5. What would falsify or invalidate it?
6. What was excluded from the explanation due to budget?
7. Which raw witnesses are available?

### `diff`

`diff` is semantic before textual. It separates:

- canonical event changes;
- proposition and scope changes;
- obligation changes;
- authority and policy changes;
- dependency invalidations;
- lifecycle changes;
- pending-effect transitions;
- derived presentation-only changes.

### `plan`

`plan` compiles an output contract into a dependency-aware graph. Every task becomes a `WorkPacket` that can be executed without rereading the source plan. A task packet includes acceptance tests, exact inputs, allowed read/write sets, authority ceiling, budget, blockers, and handoff protocol.

### `distinguish`

`distinguish` returns either:

- a sufficient observation plan with cost, risk, authority, and expected partition effect; or
- a scoped no-solution witness containing at least two worlds consistent with current knowledge that yield different decisions and no allowed query that separates them.

### `simulate`

`simulate` must not acquire production authority. It returns a `CounterfactualDelta`:

- predicted fact, obligation, lifecycle, dependency, and effect-state changes;
- expected evidence gain;
- invalidation blast radius;
- resource cost vector;
- risk and reversibility;
- assumptions and model uncertainty;
- rollback or compensation feasibility;
- differences between simulation and live execution contracts.

### `propose`

`propose` creates an immutable candidate bound to the exact residual, mission, head, and context capsule. The candidate records all semantics it could not preserve or prove. It cannot mark itself accepted, promoted, authorized, or executed.

### `verify`

`verify` keeps separate receipts for:

- schema and semantic shape;
- static admissibility;
- behavioral conformance;
- replay and determinism;
- scope and invalidator completeness;
- authority ceiling;
- security and resource limits.

An aggregate result is `PASS` only when every required receipt passes. Processor failure is not domain `FAIL`.

### `request-authority`

This command evaluates, without executing:

- OPA or equivalent policy decision;
- SPIFFE or equivalent identity evidence;
- exact action and head binding;
- expiry and revocation;
- required human approval;
- capability and data-access scope.

### `commit-intent`

`commit-intent` requires the exact `ActionCard` digest, current head, validation receipts, policy decision, identity validation, and any human approval receipt. The appended intent is the sole source for effect delivery.

### `reconcile`

`reconcile` reads the committed intent, attempts, provider identifiers, observations, and compensation state. It never infers success from exit zero, timeout, missing error, or absent worker. It returns `ACCEPTED`, `REJECTED`, `PARTIAL`, or `AMBIGUOUS` with remaining postconditions.

### `learn`

`learn` compiles evidence into candidate artifacts:

- regression or property tests;
- static or policy rule candidates;
- negative memos;
- context-packing rules;
- deterministic workflows;
- primitive candidates;
- invalidators;
- new distinction queries.

No learned artifact acquires lifecycle or execution authority through this command alone.

### `checkpoint`, `resume`, and `handoff`

These commands make conversational memory disposable. A checkpoint records the mission, head, frontier, active work, pending effects, decisions, read/write sets, and next commands. Resume revalidates the capsule against current history and either reconstructs the envelope or returns a semantic diff requiring re-orientation. Handoff transfers a work packet, not hidden mental state.

## Error envelope

Every error uses one shape:

```json
{
  "code": "RS-STALE-HEAD",
  "kind": "stale-input",
  "message": "The action was compiled against a previous canonical head.",
  "retryable": false,
  "claim_verdict": "UNKNOWN",
  "readiness": "STALE",
  "blocked_by": ["head:sha256:new"],
  "known": ["No intent was committed."],
  "unknown": [],
  "resolution": "Re-orient and recompute the action frontier.",
  "next_commands": ["rs orient --mission mission-123 --format json"],
  "evidence_refs": ["receipt:..."]
}
```

No error may force the agent to infer whether work happened, whether retry is safe, or which command restores progress.

## Self-description

`capabilities` and `robot-docs` expose:

- command schemas and examples;
- observed implementation versions and health;
- authority effects;
- supported determinism classes;
- output profiles and limits;
- error kinds and retry semantics;
- degraded and unavailable features;
- exact schema locations;
- migration compatibility.

Documentation presence is not runtime capability evidence. The catalog labels each entry `observed`, `configured`, `documented_only`, `degraded`, or `unavailable`.
