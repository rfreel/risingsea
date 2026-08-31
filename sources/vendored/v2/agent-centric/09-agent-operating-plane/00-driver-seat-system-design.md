# Rising Sea Agent Operating Plane — Driver-Seat System Design

## Status and authority

This document specifies a target-state **agent operating plane** over the Rising Sea authority kernel. The operating plane is a rebuildable projection. It has no independent canonical, policy, identity, lifecycle, or external-effect authority.

The operating plane exists to make the whole system legible as one coherent control loop. An agent should not need to memorize 22 vertical slices, inspect hundreds of files, or reconstruct state from conversational memory. The operating plane compiles those internals into one small, typed, self-describing control surface.

## System thesis

Rising Sea is best understood as a **model-based epistemic control system with a learning compiler**.

- The append-only history supplies the observed and admitted trajectory.
- The semantic graph supplies the current typed state estimate.
- Validation and closure supply the proof state.
- Residualization supplies the unresolved decision surface.
- Distinguish supplies the next evidence acquisition problem.
- The router supplies the admissible action set and reuse opportunities.
- The agent supplies bounded synthesis only where the mechanical system has a miss.
- Policy, identity, and exact intent bind any authorized action.
- Effect reconciliation compares intended postconditions with observed reality.
- Primitive promotion compiles repeated success and failure into cheaper future behavior.

The large language model is therefore neither the database nor the actuator. It is a bounded planner, hypothesis generator, semantic repairer, and system-identification instrument inside a larger verified loop.

## The three coupled loops

### 1. Epistemic loop

```text
observe
  → append evidence
  → fold semantic state
  → derive closure
  → partition obligations
  → expose unresolved frontier
  → acquire a distinction
  → update evidence
```

The epistemic loop reduces uncertainty without treating absence as negation or confidence as authority.

### 2. Operational loop

```text
mission
  → admissible action set
  → counterfactual simulation
  → validation
  → policy and identity binding
  → commit exact intent
  → attempt
  → observe
  → reconcile
```

The operational loop controls real effects while preserving stale-head, cancellation, partial-effect, and ambiguous-outcome distinctions.

### 3. Accretion loop

```text
witness
  → regression/property test
  → candidate rule or primitive
  → shadow evidence
  → scoped promotion
  → reuse
  → cheaper next verification
```

The accretion loop converts successful work, failures, corrections, and human decisions into durable artifacts rather than leaving them trapped in a chat transcript.

The loops share one event history, one scope model, one identifier graph, and one receipt discipline. They are not separate products.

## The abstraction tower

Each layer has a strict lower-layer basis and a downward witness path.

| Layer | Canonical or derived object | Agent question | Downward basis |
|---:|---|---|---|
| 0 | Canonical admitted events | What actually entered system history? | Exact event bytes, predecessor, head receipt |
| 1 | Typed semantic state | What do the events mean under explicit scope? | SEMIR records, RDF dataset, canonical digests |
| 2 | Proof state | What is entailed, contradicted, validated, stale, or unknown? | Shapes, rules, derivations, verifier and test receipts |
| 3 | Decision frontier | What remains unresolved and decision-relevant? | Output contract and residual partition |
| 4 | Work graph | Which independent obligations can be executed, in what dependency order? | Frontier obligations, dependencies, work-packet compiler |
| 5 | Action model | What can be done, at what cost, risk, authority, and expected evidence gain? | Action cards and simulations |
| 6 | Execution state | What exact intent, attempt, observation, and outcome exists? | Policy, identity, intent, provider, observation, reconciliation receipts |
| 7 | Procedural substrate | What can be reused mechanically next time? | Promoted primitives, rules, caches, negative memos, invalidators |
| 8 | Agent operating envelope | What should I attend to now? | Deterministic projection over layers 0–7 at one head |

### Tower laws

1. **No upward assertion without a downward witness.** Every summary, recommendation, status, and action links to the lower-layer evidence that supports it.
2. **No downward mutation from an upper projection.** An operating envelope, dashboard, plan, or context capsule cannot edit canonical history or external state.
3. **No hidden cross-layer state.** Handoffs use versioned artifacts and identifiers rather than ambient memory.
4. **No loss by compression.** A compact layer may omit detail only by retaining exact references and omission reasons.
5. **No authority inheritance.** A higher layer does not acquire the authority of a lower or adjacent layer merely by composing its output.
6. **No unscoped reuse.** Every reusable result carries the versions, scope, freshness, and invalidators that make reuse valid.
7. **No stale control.** Any canonical-head change makes head-bound action cards stale until re-oriented or explicitly proven unaffected.

## The single driver object

The agent should receive one immutable `OperatingEnvelope` for each control turn. The envelope references, rather than duplicates, the underlying system objects:

```text
OperatingEnvelope
  ├── MissionEnvelope
  ├── SituationFrame
  ├── DecisionFrontier
  ├── WorkGraph summary
  ├── ActionCard[]
  ├── Authority posture
  ├── Pending effect posture
  ├── Accretion posture
  ├── receipts and evidence references
  └── exact next commands
```

The envelope is deterministic for fixed:

- canonical history head;
- mission digest;
- projection and ranking versions;
- observed capability catalog;
- context profile and token budget;
- policy configuration used only for ranking or visibility;
- recorded nondeterministic inputs.

The envelope digest is bound into any action selected from it. A stale envelope cannot silently control a newer head.

## The seven-question driver contract

A zero-context `orient` response must answer these questions directly:

1. **Mission:** What exact outcome is requested, and what is excluded?
2. **Truth:** What is observed, source-asserted, mechanically derived, validated, or model-proposed?
3. **Uncertainty:** What is unknown, contradicted, stale, disputed, degraded, or awaiting observation?
4. **Change:** What materially changed since the last checkpoint or selected head?
5. **Agency:** Which actions are currently available, blocked, or forbidden?
6. **Consequences:** What would each action cost, risk, invalidate, enable, and require from authority?
7. **Next move:** Which actions are Pareto-undominated, and why is one recommended—or why does the system preserve multiple paths?

An envelope that omits a required question is incomplete. The agent should never need a second broad query merely to discover a hidden prerequisite that the system already knew.

## Orthogonal status dimensions

A single overloaded status is not legible enough. The operating plane carries four independent axes:

| Axis | Values | Question answered |
|---|---|---|
| Claim verdict | `PASS`, `FAIL`, `UNKNOWN` | Is the exact claim established under its contract? |
| Lifecycle | `UNREGISTERED`, `CANDIDATE`, `SHADOW`, `PROMOTED`, `INVALIDATED`, `RETIRED` | Where is the primitive or rule in its reuse lifecycle? |
| Operation | `NONE`, `PLANNED`, `INTENT_COMMITTED`, `ATTEMPTED`, `OBSERVED`, `RECONCILED`, `ACCEPTED`, `REJECTED`, `PARTIAL`, `AMBIGUOUS` | What happened in the effect lifecycle? |
| Readiness | `READY`, `BLOCKED`, `STALE`, `DEGRADED`, `ERROR` | Can the next named control step proceed? |

Confidence, evidence grade, freshness, authority, and risk are separate fields. None may be substituted for a status axis.

## Agent attention model

The agent’s context window is a scarce execution resource. The default operating envelope contains only decision-relevant material:

1. constitutional constraints and authority ceilings;
2. mission and acceptance obligations;
3. active changes and invalidators;
4. unresolved frontier and blockers;
5. reusable exact or structural results;
6. the top Pareto-distinct actions;
7. pending external effects or required reconciliations;
8. one concise accretion opportunity;
9. exact references for drill-down.

Historical narrative, raw logs, full graphs, complete proofs, and unrelated closed work remain available by reference. They do not enter the default context pack.

## Agent control invariants

1. An action card always names the mission, history head, frontier digest, and obligations it addresses.
2. A recommended action is not executable merely because it is recommended.
3. No action with a required `UNKNOWN` applicability, version, policy, or identity obligation may commit intent.
4. No repeated equivalent attempt is recommended after failure unless a material invalidator changed or a new distinction was acquired.
5. No external success appears without observation and reconciliation.
6. No context truncation may drop a hard constraint, exclusion, negation, exception, authority boundary, or acceptance criterion.
7. No action selection scalarizes incomparable cost, risk, and evidence dimensions without a declared policy.
8. A canonical-head change invalidates all dependent envelopes, work packets, simulations, and authority bindings.
9. Every error response includes what is known, what remains unknown, whether retry is safe, and at least one exact recovery command when a recovery exists.
10. Every session checkpoint yields a resume capsule that does not depend on chat memory.
11. Every completed work packet yields an `AccretionDelta`, including an explicit `NO_ACCRETION` reason when nothing reusable was produced.
12. Every agent-facing assertion remains traceable to a source classification and evidence reference.

## What the agent should never have to do

- Read the complete combined specification before taking a bounded action.
- Infer current state from file timestamps, worker artifacts, or prose summaries.
- Guess which command or slice owns an operation.
- Reconstruct the mission from prior messages after context compaction.
- Parse human-formatted tables when a stable machine schema exists.
- Retry an ambiguous external effect blindly.
- Compare raw scores from different scales without normalization or policy.
- remember which files another agent is editing without a lease record.
- decide whether a cache is safe without an action-key and invalidation witness.
- treat a model’s confidence as evidence or authority.

## Synthetic system result

The agent experiences one loop:

```text
ORIENT
  → choose or preserve a decision frontier
  → REUSE / DISTINGUISH / PLAN / PROPOSE
  → SIMULATE
  → VERIFY
  → REQUEST AUTHORITY
  → COMMIT INTENT
  → RECONCILE
  → LEARN
  → CHECKPOINT
  → ORIENT at the new head
```

The 22 internal slices are replaceable implementation boundaries underneath that loop. Their complexity is compiled away from ordinary operation but remains available for exact inspection.
