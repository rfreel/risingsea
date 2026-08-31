# Expert-Domain Deterministic Control Plane

## Status

Target architecture for converting novice intent into expert-native problem representations, deterministic diagnostics and guarded repair paths.

This specification does not claim a production runtime exists.

## Objective

A user with no domain background should receive the same decision-relevant distinctions the right expert would use, without first learning the expert vocabulary.

The system must therefore transform user intent into a domain-native representation before asking a model to reason about the problem.

The desired control law is:

```text
user intent
  -> truth / capability observation
  -> ruin classification
  -> domain-machine routing
  -> expert-native representation
  -> deterministic diagnostic where available
  -> explicit defect / evidence gap / blocked state
  -> safe repair route or discovery route
  -> verification
  -> receipt
  -> procedural compilation
```

The path of least resistance must be the path a competent domain expert would take.

## Optimization target

Do not optimize primarily for tokens. Tokens are comparatively cheap.

Optimize for:

1. minimum unverified semantic discretion;
2. minimum repeated inference;
3. minimum irreversible downside;
4. maximum mechanically checkable state;
5. maximum reconstructibility;
6. maximum reuse of mature mechanisms;
7. explicit `PASS / FAIL / UNKNOWN` rather than narrative confidence.

A 20,000-token discovery that compiles into a deterministic 20-line checker is a successful trade when the checker is reusable.

## Non-negotiable laws

1. If a deterministic procedure exists, an LLM may not replace it.
2. If a deterministic representation exists, prose may not replace it as the machine contract.
3. If a deterministic verifier exists, model confidence is irrelevant to the claim verdict.
4. LLM output is candidate material only; it is never a state transition.
5. Security or authority constraints must be encoded in types, protocol, policy, capability, state machine, verifier, or guard—not prompted compliance.
6. `UNKNOWN` remains `UNKNOWN` until new evidence changes it.
7. A missing response never proves an external effect succeeded or failed.
8. Ruin-class operations fail closed unless the exact required authority and evidence are present.
9. Semantic transformations require typed scope, provenance, reconstruction and residual checking before promotion.
10. A recurring expert judgment that can be made mechanical should eventually cease to be a judgment.

## Infrastructure order

The build order is intentionally authority-first rather than UX-first.

### I0 — Canonical truth and receipts

Required capabilities:

- append-only event history;
- exact predecessor/head precondition;
- provenance links;
- distinct claim/lifecycle/operation/readiness axes;
- immutable verification receipts;
- rebuildable projections.

Existing Rising Sea donor: CT + PROV + SQLITE + JCS families.

### I1 — Capability and truth-source observation

Before routing or action, the system must know what is actually available and what kind of truth it can observe.

Required outputs:

```text
capabilities
truth_source_class
readiness
degraded_modes
freshness
repair_command
```

Donors:

- `Dicklesworthstone/flywheel_connectors`: explicit authority, capability typestate, truth hierarchy, default deny;
- `Dicklesworthstone/franken_agent_detection`: deterministic environment/agent probes;
- Rising Sea `SPIFFE`, `OPA`, `ROUTER` contracts.

### I2 — Ruin guard

Ruin protection precedes ordinary action selection.

Ruin classes include at least:

- irreversible data loss;
- destructive Git/history operations;
- destructive infrastructure/database operations;
- credential disclosure;
- privilege escalation;
- unauthorized money movement;
- mass external effects;
- unbounded resource consumption;
- dangerous scope widening.

Donor: `Dicklesworthstone/destructive_command_guard`.

The preferred implementation is adapter/reuse of DCG rule packs and explainable deny semantics, not a new LLM classifier.

### I3 — Domain Machine Registry

A `DomainMachine` is the compiler target for expert practice.

Each machine declares:

```text
domain identity
expert-native representation
required observations
invariants
deterministic diagnostics
admissible repair recipes
verification oracles
ruin boundaries
degraded modes
failure routing
discovery strategy
mechanism donors
```

The user never needs to know this schema. The novice surface projects it into:

```text
WHAT IS WRONG
WHY IT MATTERS
WHAT PROVES IT
WHAT FIXES IT
WHAT COULD GO WRONG
WHAT HAPPENS NEXT
```

### I4 — Retrieval and routing

Routing order:

```text
exact reusable result
-> exact negative memo
-> finite table / trie / automaton
-> schema / type checker
-> graph algorithm
-> state machine
-> rule engine
-> static analyzer
-> property / conformance test
-> solver / model checker
-> bounded experiment
-> bounded semantic retrieval
-> LLM residual proposal
-> human judgment
```

Donors:

- CASS for lexical-first authoritative history and rebuildable enrichment;
- Beads/BV for deterministic dependency/frontier analysis;
- Rising Sea `ROUTER`.

Search absence is not evidence of non-existence unless the search contract establishes completeness for the relevant scope.

### I5 — Expert diagnostic compiler

Input: a typed problem instance plus a `DomainMachine`.

Output:

```text
SATISFIED
DEFECT
EVIDENCE_GAP
BLOCKED
CONTRADICTED
UNKNOWN
```

A diagnostic must identify the exact violated invariant or missing witness where possible.

The model may propose a candidate diagnostic only when no deterministic diagnostic can decide the case.

### I6 — Repair recipe and verification oracle

A repair recipe is not prose advice. It is a bounded transition contract:

```text
preconditions
read_set
write_set
forbidden_writes
ordered actions
expected state delta
verification oracle
strongest falsifier
rollback / recovery
ruin class
authority required
```

Donors:

- DCG for safe alternatives and guarded destructive classes;
- cross-agent-session-resumer for canonical IR -> target write -> read-back verification;
- UBS for recurring defect -> deterministic scanner;
- Rising Sea `TEST`, `VERIFY`, `EFFECT`.

### I7 — Discovery engine

When normal diagnosis/repair cannot resolve the problem, do not improvise.

Create a typed unresolved object:

```text
missing_distinction
rival_hypotheses
known_evidence
missing_evidence
cheapest_discriminating_witness
safe_experiments
forbidden_actions
```

Discovery loop:

```text
recover exact prior cases
-> recover domain exemplars
-> preserve rival hypotheses
-> find smallest discriminating witness
-> run safe observation / experiment
-> eliminate or refine rivals
-> repeat
```

If still unresolved:

```text
broaden exemplar search
-> APR-style adversarial review rounds
-> synthetic / differential experiment
-> formalize the new distinction
-> compile new checker / rule / representation
-> reenter normal resolution
```

Donor: `Dicklesworthstone/automated_plan_reviser_pro` for iterative proposal refinement. APR convergence metrics are advisory; they do not establish truth.

### I8 — Obligation and residual compiler

Represent requirements as atomic obligations:

```text
id
proposition
scope
source_basis
status
owner
dependencies
acceptance_witness
strongest_falsifier
implementation_state
```

Partition exactly into:

```text
SATISFIED
UNSATISFIED
CONTRADICTED
UNKNOWN
NOT_APPLICABLE
```

Only `UNSATISFIED` obligations become executable TODO candidates.

`CONTRADICTED` and `UNKNOWN` remain separate work classes.

Donor: Rising Sea `RESIDUALIZE`.

### I9 — WorkPacket lowering and scheduler

A WorkPacket should require as little interpretation as possible.

Execution grammar:

```text
READ
CHECK
CHANGE
VERIFY
RECEIPT
STOP
```

The scheduler chooses the packet; the worker does not reprioritize the project.

Donors:

- Beads / Beads Viewer for dependency graph, ready frontier, critical path and graph triage;
- local agentic flywheel for claims, leases, receipts and evidence-gated completion;
- MCP Agent Mail only for coordination, never task authority.

### I10 — Effect execution and reconciliation

External effects use:

```text
selected action
-> authority binding
-> exact durable intent
-> attempt
-> authoritative observation
-> reconcile
-> terminal receipt
```

Donor: Rising Sea `EFFECT` plus FCP capability enforcement.

### I11 — Procedural memory compiler

Learning levels:

```text
one success -> evidence
repeated success -> candidate rule
validated repeated success -> deterministic recipe
repeated identical reasoning -> compiler pass
one catastrophic failure -> immediate negative memo / guard candidate
```

Harmful evidence has asymmetric weight because ruin is asymmetric.

Donors: CASS Memory / Eidetic Engine / local flywheel procedural memory.

No learned rule self-promotes.

### I12 — Novice control surface

Only after the machinery above exists should the user-facing projection be finalized.

Primary surface:

```text
Problem
Why it matters
Known
Missing
Do not
Next
Proof of completion
If unresolved
```

The surface should hide expert jargon by default while retaining drill-down to the exact domain representation and receipts.

## Domain-machine examples

| Domain | Expert-native representation | Typical deterministic mechanisms |
|---|---|---|
| Build/dependency | dependency DAG + compiler diagnostics + target graph | Bazel-style invalidation, graph algorithms |
| Concurrency | state machine / Petri net / happens-before graph | model checking, invariant checking |
| Database | schema + constraints + transactions + query plan | SQL constraints, EXPLAIN, transaction tests |
| Security | principals + capabilities + trust boundaries + effects | policy engine, typestate, DCG/FCP |
| Deployment | desired/observed state + rollout state machine + health probes | reconciliation loop, probes |
| Code correctness | invariants + dependency/change surface | static analysis, property/conformance tests |
| Planning | obligations + dependency DAG + acceptance witnesses | Beads/BV, residualization |
| External effect | intent + attempt + observation + reconciliation | outbox/idempotency/read-back |
| Knowledge conflict | scoped claims + provenance + contradiction witnesses | typed IR, validation, retrieval |
| Performance | resource profile + critical path + bottleneck attribution | profiling, graph/queue metrics |
| Reliability | fault model + durability boundary + recovery state machine | fault injection, replay |

## Contract selection policy

For every capability request:

1. Search the Rising Sea/Doodlestein catalog for an existing mechanism.
2. Inspect the current upstream implementation when the mechanism is material to safety or correctness.
3. Prefer adapter/reuse over reimplementation.
4. If the mechanism fits incompletely, preserve the gap explicitly.
5. Create custom machinery only for the residual not covered by mature donors.
6. Every custom mechanism must name its falsifier and migration path to a mature donor if one appears.

## Ruin policy

Ruin prevention is lexicographically prior to convenience and token cost.

A ruin-class action may not be selected only because expected value is positive.

The action must satisfy the applicable mechanical guard, authority, reversibility/containment and verification requirements.

When uncertainty concerns whether an irreversible external action already occurred, the default is observation/reconciliation before retry.

## Acceptance tests

The control plane is not accepted until all of these are demonstrated:

1. A novice can submit an unfamiliar-domain problem and receive the correct expert-native problem shape without knowing the terminology.
2. A deterministic mechanism is preferred over an LLM when both can solve the same case.
3. A ruin-class operation is blocked mechanically before model execution authority.
4. A missing deterministic route produces a typed unresolved object rather than improvisation.
5. Discovery can compile a newly learned distinction into a reusable machine contract, test, rule, guard or recipe.
6. WorkPackets contain no unresolved architecture choice.
7. A simple executor can either complete a packet correctly or stop with a typed receipt.
8. The same canonical state regenerates the same domain registry, frontier and machine-facing outputs.
9. No success, authority or external-effect claim is established from model confidence alone.

## Evidence boundary

This file is a target-state contract. It does not establish that any listed donor is installed, integrated, or operational in Rising Sea. Each adoption requires an explicit adapter/integration receipt.