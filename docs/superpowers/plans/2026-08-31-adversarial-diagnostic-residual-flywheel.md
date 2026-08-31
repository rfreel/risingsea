# Adversarial Diagnostic and Residual Flywheel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Compile expert diagnosis, unresolved discovery, residualization, and WorkPacket lowering so accepted state is reconstructible from typed observations and deterministic contracts, while model output remains candidate-only.

**Architecture:** Insert an Accepted Observation Algebra between routing and diagnosis. Diagnostics consume only admitted observations plus versioned DomainMachine rules. Repairs consume accepted diagnostic states, discovery consumes only unresolved states, and TODOs consume only proven UNSATISFIED obligations. Every transition emits a receipt and every unknown/contradiction remains explicit.

**Tech Stack:** Python 3.12 standard library, JSON/JSONL contracts, deterministic CLI tools, GitHub Actions, existing Rising Sea DomainMachine/RuinGuard/router machinery.

**Spec:** `specs/expert-domain-control-plane.md`

## Global Constraints

- LLM output is candidate material only; it is never a state transition.
- UNKNOWN remains UNKNOWN until new evidence changes it.
- Ruin-class operations fail closed.
- Search absence is not evidence of non-existence unless completeness is established.
- Generated projections are disposable and reproducible from canonical inputs.
- Prefer catalogued mature donor mechanisms; custom code implements only the residual.
- Every accepted verdict identifies its observation basis and deterministic rule.
- Every task is TDD red -> green -> receipt -> work-graph reentry.

---

## Prewalk: competing decompositions

### Rival A — one general diagnostic engine

`problem + domain machine + model -> verdict`

Rejected: too much semantic discretion in one boundary; hard to prove that model content did not influence accepted state.

### Rival B — domain-specific diagnostic scripts

`planning_diag.py`, `effect_diag.py`, `security_diag.py`, ...

Preserved as later adapters, not the kernel. It gives strong domain fidelity but duplicates admission, provenance, UNKNOWN, contradiction, and evidence-gap logic.

### Rival C — observation algebra + deterministic rule evaluation + domain adapters

Selected.

```text
raw evidence
 -> ObservationCandidate
 -> admission / normalization
 -> AcceptedObservation[]
 -> deterministic rule evaluation
 -> DiagnosticReceipt
```

Domain-specific logic is data/contracts where possible. New domains can add rules without gaining authority over observation admission.

### Strongest falsifier

A model-supplied proposition, stale observation, or observation without provenance can cause an accepted `SATISFIED` or `DEFECT` verdict without a deterministic rule identifying the exact basis.

---

## Infrastructure order

```text
RS-W005 DomainMachine                 COMPLETE
RS-W006 Capability truth              COMPLETE
RS-W007 RuinGuard                     COMPLETE
RS-W008 Deterministic router          COMPLETE

RS-W009A Accepted Observation Algebra   <- FIRST
RS-W009  Expert Diagnostic Compiler
RS-W010  Repair Recipe + Oracle Registry
RS-W011  Unresolved Discovery Engine
RS-W012  Obligation Residual Compiler
RS-W013  WorkPacket Lowering
RS-W014  External Effect Reconciliation
RS-W015  Procedural Expertise Compiler
RS-W016  Novice Control Surface
RS-W017  Adversarial Benchmark
```

`RS-W001B` source-corpus closure remains an independent ready lane and must not be conflated with expert-control completion.

---

### Task 1: Accepted Observation Algebra

**Files:**
- Create: `contracts/accepted-observation.schema.json`
- Create: `diagnostics/observation-rules.json`
- Create: `tools/admit_observations.py`
- Create: `tools/test_observation_algebra.py`
- Modify: `.github/workflows/flywheel-integrity.yml`

**Interfaces:**
- Consumes: raw observation candidate JSON objects.
- Produces: `risingsea.accepted-observation-set.v1` containing accepted/rejected observations with provenance, freshness, source class, scope, digest, and rejection reason.

- [ ] Write failing tests for valid deterministic observation admission.
- [ ] Write failing tests rejecting model assertion as authoritative observation.
- [ ] Write failing tests rejecting missing provenance.
- [ ] Write failing tests separating stale from current evidence.
- [ ] Write failing tests preserving contradictory observations rather than picking one.
- [ ] Observe RED in CI with prior gates green.
- [ ] Implement minimal deterministic normalization/admission.
- [ ] Require stable IDs/digests and sorted output.
- [ ] Observe GREEN in full CI.
- [ ] Emit `RS-W009A` receipt and reenter work graph.

### Task 2: Expert Diagnostic Compiler

**Files:**
- Create: `contracts/diagnostic-receipt.schema.json`
- Create: `diagnostics/rules.json`
- Create: `tools/diagnose.py`
- Create: `tools/test_diagnostic_compiler.py`
- Modify: `.github/workflows/flywheel-integrity.yml`

**Interfaces:**
- Consumes: accepted observation set + DomainMachine ID + deterministic diagnostic rules.
- Produces: `SATISFIED | DEFECT | EVIDENCE_GAP | BLOCKED | CONTRADICTED | UNKNOWN` plus exact rule/basis IDs.

- [ ] Test invariant violation -> `DEFECT`.
- [ ] Test all required invariants witnessed -> `SATISFIED`.
- [ ] Test missing required observation -> `EVIDENCE_GAP`.
- [ ] Test contradictory accepted observations -> `CONTRADICTED`.
- [ ] Test known prerequisite block -> `BLOCKED`.
- [ ] Test no deciding deterministic rule -> `UNKNOWN`.
- [ ] Mutation: model candidate says PASS while deterministic evidence says DEFECT; verdict remains DEFECT.
- [ ] Mutation: remove rule ID from receipt; schema/contract fails.
- [ ] Mutation: stale evidence substituted for current; cannot satisfy freshness-bound invariant.
- [ ] Observe RED, implement minimal rule evaluator, observe GREEN, receipt, reenter.

### Task 3: Repair Recipe + Verification Oracle Registry

**Files:**
- Create: `contracts/repair-recipe.schema.json`
- Create: `contracts/verification-oracle.schema.json`
- Create: `repairs/registry.jsonl`
- Create: `tools/validate_repairs.py`
- Create: `tools/test_repairs.py`

**Interfaces:**
- Consumes: accepted diagnostic receipt.
- Produces: zero or more applicable bounded repair recipes; never an effect.

Adversarial tests:
- unknown precondition cannot select recipe;
- missing oracle rejects recipe;
- write outside declared write set rejects recipe;
- ruin-class recipe without authority contract rejects recipe;
- repair cannot turn UNKNOWN diagnosis into solved state.

### Task 4: Unresolved Discovery Engine

**Files:**
- Create: `contracts/unresolved.schema.json`
- Create: `tools/discover.py`
- Create: `tools/test_discovery.py`

**Interfaces:**
- Consumes: `UNKNOWN`, `EVIDENCE_GAP`, or explicit rival set.
- Produces: typed unresolved object and next discriminating witness candidate.

Adversarial tests:
- one rival may not disappear without evidence;
- exact prior case searched before model generation;
- incomplete search cannot establish novelty;
- APR/reviewer agreement cannot establish truth;
- unsafe experiment rejected by RuinGuard.

### Task 5: Obligation Residual Compiler

**Files:**
- Create: `contracts/obligation.schema.json`
- Create: `tools/residualize.py`
- Create: `tools/test_residualize.py`

**Partition:**

```text
SATISFIED
UNSATISFIED
CONTRADICTED
UNKNOWN
NOT_APPLICABLE
```

Adversarial tests:
- total partition;
- disjoint partition;
- UNKNOWN never appears in executable TODOs;
- CONTRADICTED never appears in executable TODOs;
- duplicate obligations collapse only with an explicit equivalence witness;
- changed scope invalidates prior satisfaction.

### Task 6: Frontier-Resolved WorkPacket Lowering

**Files:**
- Create: `contracts/work-packet.schema.json`
- Create: `tools/lower_work_packet.py`
- Create: `tools/test_work_packet_lowering.py`

Release gate requires zero unresolved fields in:

```text
design_choice
scope
read_set
write_set
verification_oracle
failure_route
authority
```

Adversarial mutations:
- delete verification oracle;
- introduce second implementation strategy;
- widen write set;
- stale history head;
- missing failure route;
- unresolved semantic term.

Every mutation must reject or produce a typed BLOCKED/STALE result.

### Task 7: Effect State Machine

Keep `intent`, `attempt`, `observation`, `reconciliation` distinct. Mutation campaign must reject attempt-before-intent, timeout-as-success, retry-after-ambiguous without observation, and stale authorization.

### Task 8: Procedural Accretion

Compile repeated verified reasoning into candidate rules/recipes/checkers. One catastrophic failure immediately creates a negative memo/guard candidate. No candidate self-promotes.

### Task 9: Novice Projection

Project only:

```text
Problem
Why
Known
Missing
Do not
Next
Proof
If unresolved
```

Expert representation and receipts remain drillable. Compact mode may not hide ruin warnings, UNKNOWN, contradiction, or authority requirements.

### Task 10: Cross-Domain Adversarial Tournament

Fixture domains:
- planning dependency failure;
- external-effect ambiguity;
- destructive security operation;
- database missing constraint;
- contradictory knowledge claim;
- reliability/recovery ambiguity;
- stale deployment observation.

Compete:
1. direct frontier-model baseline;
2. compiled control + frontier fallback;
3. compiled control + simple executor.

Report separately:
- correctness;
- catastrophic-policy violations;
- UNKNOWN preservation;
- deterministic-route rate;
- model fallback rate;
- recovery correctness;
- context/tokens;
- repeated-task marginal cost.

No scalar winner unless weights are explicitly supplied.

---

## Accretion law

After every task:

```text
witness
 -> regression test
 -> deterministic contract/code
 -> fresh verification receipt
 -> work-graph transition
 -> generated frontier rebuild
 -> next packet
```

If a failure reveals a reusable distinction, add it to the earliest layer that can enforce it mechanically. Do not patch a later layer with prose.
