# Agent-Centric Implementation Plan

## Objective

Implement Rising Sea as one agent-legible control system rather than a collection of individually callable subsystems. Preserve all authority boundaries while making the default agent experience a single zero-context orientation, a finite decision frontier, exact action cards, resumable work packets, and mandatory accretion.

## Implementation policy

- Write tests and machine contracts before production paths.
- Every task below is a self-contained work packet with an exact predecessor revision and acceptance witness.
- Machine-readable envelopes are canonical for the interface; CLI, TUI, web, and chat renderings are projections.
- No task is complete until its evidence, invalidators, and accretion delta are recorded.
- Parallel tracks may proceed only when they do not invent private status, task, authority, or checkpoint representations.

## Work graph

| ID | Task | Dependencies | Acceptance witness | Track |
| --- | --- | --- | --- | --- |
| AP-001 | Freeze v2 schemas and status axes | — | Schemas validate; no status aliasing | foundation |
| AP-002 | Implement exact-head event store | AP-001 | Concurrent append test has exactly one winner | authority |
| AP-003 | Implement deterministic projection runtime | AP-002 | Delete projections and reproduce digests | state |
| AP-004 | Implement capability catalogue and doctor | AP-001, AP-003 | Observed/documented/degraded states are distinct | introspection |
| AP-005 | Implement MissionEnvelope compiler | AP-001, AP-003 | Round-trip preserves every source constraint and exclusion | semantics |
| AP-006 | Implement SituationFrame projector | AP-003, AP-005 | Every material fact has one source class and scope | state |
| AP-007 | Implement closure and DecisionFrontier | AP-006 | Obligation partition is total and disjoint | reasoning |
| AP-008 | Implement ActionCard compiler | AP-004, AP-007 | All actions show cost, risk, authority, read/write sets, invalidators | control |
| AP-009 | Implement `rs orient` | AP-004, AP-005, AP-006, AP-007, AP-008 | Cold agent returns valid brief envelope | driver |
| AP-010 | Implement progressive ContextCapsule packer | AP-007, AP-009 | Mandatory semantics survive every budget test | context |
| AP-011 | Implement lossless inspect/explain/diff | AP-003, AP-010 | Every compact statement drills to exact witnesses | legibility |
| AP-012 | Implement WorkGraph and WorkPacket | AP-007, AP-008 | Ready, claimed, running, blocked, review, complete remain distinct | work |
| AP-013 | Implement reservations and worktree adapters | AP-012 | Conflicts are detected without treating leases as authority | coordination |
| AP-014 | Implement checkpoint/resume/handoff | AP-010, AP-012 | Chat deletion and cross-agent resume reconstruct state | continuity |
| AP-015 | Implement deterministic router and reuse | AP-003, AP-007, AP-008 | Exact→structural→mechanical→retrieval→distinguish→LLM order is explicit | economy |
| AP-016 | Implement `DISTINGUISH` evidence planner | AP-007, AP-015 | Returns decisive query or bounded no-solution witness | epistemics |
| AP-017 | Implement candidate-only LLM bridge | AP-010, AP-015, AP-016 | No LLM output can reach append or effect interfaces | generation |
| AP-018 | Implement static and behavioral verifier broker | AP-017 | Static, behavior, scope, and evidence receipts remain separate | verification |
| AP-019 | Implement simulation and counterfactual diff | AP-008, AP-018 | No-authority predicted deltas are reproducible | control |
| AP-020 | Implement policy/identity/exact binding | AP-004, AP-008, AP-018 | Identity without allow and allow without identity cannot execute | authority |
| AP-021 | Implement execution-intent/outbox transaction | AP-002, AP-020 | Intent and outbox append atomically against exact head | effects |
| AP-022 | Implement effect adapters and reconciliation | AP-021 | Crash at each boundary yields recoverable state, never inferred success | effects |
| AP-023 | Implement AccretionDelta and learning compiler | AP-011, AP-018, AP-022 | Every completed packet produces reusable output or no-accretion reason | learning |
| AP-024 | Implement primitive lifecycle and invalidation | AP-015, AP-023 | Promotion, per-use checks, invalidation, retirement are event-driven | learning |
| AP-025 | Implement multi-agent scheduler | AP-012, AP-013, AP-014, AP-024 | Dependency, lease, authority, and evidence blockers all respected | coordination |
| AP-026 | Implement human exact-approval surface | AP-008, AP-020 | Approval binds action digest, head, scope, expiration | supervision |
| AP-027 | Implement agent-experience benchmark corpus | AP-009, AP-010, AP-011, AP-012, AP-013, AP-014, AP-015, AP-016, AP-017, AP-018, AP-019, AP-020, AP-021, AP-022, AP-023, AP-024, AP-025, AP-026 | Matched baselines cover accuracy, tokens, compute, recovery, accretion | verification |
| AP-028 | Implement bounded control-model and fault campaigns | AP-021, AP-022, AP-023, AP-024, AP-025, AP-026, AP-027 | Seeded authority, stale, unknown, retry, and context mutants are detected | verification |
| AP-029 | Run shadow pilot | AP-027, AP-028 | No-authority real workload observations retained | promotion |
| AP-030 | Promote first end-to-end driver profile | AP-029 | Cold start→work→effect→learn→resume demonstrated under fixed scope | release |

## Critical path

```text
AP-001 → AP-002 → AP-003 → AP-005 → AP-006 → AP-007 → AP-008 → AP-009
      → AP-010 → AP-014 → AP-015 → AP-016 → AP-017 → AP-018 → AP-020
      → AP-021 → AP-022 → AP-023 → AP-024 → AP-027 → AP-028 → AP-029 → AP-030
```

## First executable vertical slice

The first slice intentionally avoids external effects:

```text
mission source
  → MissionEnvelope
  → SituationFrame
  → DecisionFrontier
  → ActionCard
  → ContextCapsule
  → candidate-only proposal
  → static + behavioral verification
  → AccretionDelta
  → ResumeCapsule
```

Acceptance requires a fresh agent to begin from only a mission identifier, resolve one finite unknown, produce a verified reusable artifact, delete its conversational context, and resume without reconstructing state manually.

## Second executable vertical slice

Add exact authority and one reversible local effect:

```text
verified ActionCard
  → policy + identity
  → exact authorization binding
  → execution intent + outbox
  → idempotent local attempt
  → independent observation
  → reconciliation
  → terminal event
```

The fault campaign kills the process before and after every boundary. Every restart must classify the operation from durable evidence rather than retry blindly.

## Third executable vertical slice

Add two agents on isolated worktrees and shared semantic reservations. One agent implements, the second verifies. Task status remains in the work graph; messages remain coordination records; Git branches remain byte-isolation mechanisms; canonical admission remains a separate append.

## Release gates

1. Structural: schemas, examples, docs, links, and manifests pass.
2. Semantic: scope round-trips and frontier partition properties pass.
3. Control: stale, UNKNOWN, authority, and external-effect invariants pass.
4. Ergonomic: cold-start, next-action, interruption, and handoff tasks pass.
5. Economic: matched workload uses no more total resource vector without an explicit trade-off.
6. Accretive: the second matched execution reuses a verified artifact or explains why reuse is invalid.
7. Shadow: no-authority real workload evidence meets the declared cohort and duration.
8. Promotion: exact version and scope are admitted through the primitive lifecycle.
