# Expert-Domain Control Plane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic-first expert-domain control substrate that converts novice intent into expert-native representations, guarded diagnostics, repair/discovery routes, residual obligations and executable WorkPackets.

**Architecture:** Rising Sea remains authority-first. Mature Doodlestein mechanisms are reused through explicit donor/adaptor contracts; custom code is limited to the residual integration layer. The first executable layer is a machine-readable `DomainMachine` registry plus deterministic validation. Later tasks add truth/capability observation, ruin guarding, routing, diagnosis, recipes, discovery, residualization and simple-executor WorkPacket lowering.

**Tech Stack:** Python 3.12 standard library, JSON/JSONL machine contracts, JSON Schema-shaped validation implemented without new runtime dependencies initially, GitHub Actions, existing Rising Sea source/receipt/work-graph infrastructure.

**Spec:** `specs/expert-domain-control-plane.md`

## Global Constraints

- `LLM output != state transition`.
- Prefer existing catalogued mechanisms over custom implementations.
- Deterministic mechanisms outrank semantic/model inference when applicable.
- Security and authority constraints are mechanically enforced, never prompt-only.
- `PASS`, `FAIL`, and `UNKNOWN` remain distinct.
- Ruin prevention is lexicographically prior to convenience and token cost.
- Search absence is not proof of non-existence without a complete search contract.
- Generated projections are rebuildable and non-authoritative.
- Every completed work item has an evidence receipt.
- No learned rule or primitive self-promotes.

---

## Dependency order

```text
P0 contracts / receipts already present
  |
  +-> P1 DomainMachine contract + validator
  |      |
  |      +-> P2 capability / truth-source adapter contract
  |      +-> P3 ruin-guard adapter contract
  |              |
  |              +-> P4 deterministic router
  |                     |
  |                     +-> P5 diagnostic compiler
  |                            |
  |                            +-> P6 repair recipe + verification oracle
  |                                   |
  |                                   +-> P7 discovery engine
  |                                          |
  |                                          +-> P8 obligation / residual compiler
  |                                                 |
  |                                                 +-> P9 WorkPacket lowering + scheduler
  |                                                        |
  |                                                        +-> P10 effect/reconciliation adapter
  |                                                               |
  |                                                               +-> P11 procedural memory compiler
  |                                                                      |
  |                                                                      +-> P12 novice control surface
  |                                                                             |
  |                                                                             +-> P13 adversarial/fault/novice benchmark
  |
  +-> existing RS-W001B source retrieval continues independently
```

The new control-plane contracts do not claim the source-import task is finished. `RS-W001B` remains independently valid work.

---

### Task 1: DomainMachine contract and deterministic registry validation

**Files:**
- Create: `contracts/domain-machine.schema.json`
- Create: `domain-machines/registry.jsonl`
- Create: `domain-machines/planning.json`
- Create: `domain-machines/external-effect.json`
- Create: `domain-machines/security.json`
- Create: `tools/validate_domain_machines.py`
- Create: `tools/test_domain_machines.py`
- Modify: `.github/workflows/flywheel-integrity.yml`

**Interfaces:**
- Consumes: target contract in `specs/expert-domain-control-plane.md`.
- Produces: `DomainMachine` records keyed by stable `domain_id`; `validate_domain_machines.py --json` returns `{schema,status,count,issues}` and exits nonzero on invalid registry state.

- [ ] **Step 1: Write the failing registry test**

Test must require:

```python
REQUIRED = {
    "domain_id",
    "title",
    "representation",
    "required_observations",
    "invariants",
    "diagnostics",
    "repair_recipes",
    "verification_oracles",
    "ruin_boundaries",
    "failure_routes",
    "discovery_strategy",
    "donors",
}
```

It must fail when `domain-machines/registry.jsonl` or any referenced machine file is absent, when an ID is duplicated, when a donor is missing a repository/mechanism/adoption mode, or when a machine omits an unresolved route.

- [ ] **Step 2: Run the test and observe RED**

Run:

```bash
python tools/test_domain_machines.py
```

Expected: nonzero because the registry/validator does not yet exist.

- [ ] **Step 3: Add the minimal contract and validator**

The validator must use only the Python standard library, parse every JSONL row, load each referenced machine file, enforce stable unique IDs and required fields, and verify every donor record has:

```text
repository
mechanism
adoption = REUSE | ADAPT | REFERENCE
claim_boundary
```

- [ ] **Step 4: Seed three real machines**

Seed:

1. `planning` — obligation/dependency graph representation; donors Beads/BV + Rising Sea RESIDUALIZE.
2. `external-effect` — intent/attempt/observation/reconciliation; donor Rising Sea EFFECT + FCP.
3. `security` — principals/capabilities/trust boundaries/ruin classes; donors FCP + DCG.

Each must include a deterministic diagnostic list before an LLM fallback.

- [ ] **Step 5: Run GREEN verification**

```bash
python tools/test_domain_machines.py
python tools/validate_domain_machines.py --json
```

Expected: both exit 0; validator status `PASS`, count `3`.

- [ ] **Step 6: Add CI gate and commit**

Add before doctor:

```yaml
- name: Validate domain machine registry
  run: python tools/test_domain_machines.py && python tools/validate_domain_machines.py --json
```

Commit message: `feat: add expert domain machine contract`

---

### Task 2: Capability and truth-source observation contract

**Files:**
- Create: `contracts/capability-observation.schema.json`
- Create: `infrastructure/donors/capability-truth.json`
- Create: `tools/observe_capabilities.py`
- Create: `tools/test_capability_observation.py`
- Modify: `domain-machines/*.json`

**Interfaces:**
- Consumes: deterministic filesystem/environment probes plus donor metadata.
- Produces: `{capabilities,truth_sources,readiness,degraded,repair_commands}`. No field may claim runtime availability from documentation alone.

- [ ] Write tests that distinguish `OBSERVED`, `DOCUMENTED`, `UNAVAILABLE`, and `UNKNOWN` capability states.
- [ ] Observe RED before implementation.
- [ ] Implement deterministic local probes; do not add semantic inference.
- [ ] Add donor contract referencing `Dicklesworthstone/flywheel_connectors` and `Dicklesworthstone/franken_agent_detection`.
- [ ] Verify an unavailable donor tool degrades explicitly instead of becoming assumed available.
- [ ] Commit `feat: add capability truth observation`.

---

### Task 3: RuinGuard donor adapter and fail-closed classification

**Files:**
- Create: `contracts/ruin-class.schema.json`
- Create: `infrastructure/donors/destructive-command-guard.json`
- Create: `guard/ruin-classes.json`
- Create: `tools/ruin_guard.py`
- Create: `tools/test_ruin_guard.py`

**Interfaces:**
- Consumes: exact candidate operation and current capability/authority state.
- Produces: `ALLOW`, `BLOCK`, or `REVIEW_REQUIRED`; never silently allows on classifier failure.

- [ ] Write failing fixtures for destructive Git, recursive deletion, database destruction, privilege escalation, mass effect and an ordinary safe read.
- [ ] Require `BLOCK` or `REVIEW_REQUIRED` on malformed/unknown ruin classification.
- [ ] Implement adapter-first rule lookup; record DCG as the preferred mature donor.
- [ ] Keep custom rules to Rising Sea-specific residual classes such as scope explosion and unknown-effect retry.
- [ ] Verify safe reads are not blocked by unrelated ruin rules.
- [ ] Commit `feat: add ruin guard boundary`.

---

### Task 4: Deterministic expert router

**Files:**
- Create: `contracts/route-decision.schema.json`
- Create: `router/route-order.json`
- Create: `tools/route_problem.py`
- Create: `tools/test_route_problem.py`

**Interfaces:**
- Consumes: problem facts, capability observation, domain registry.
- Produces: realized route plus reason and degraded modes.

- [ ] Encode exact precedence from the spec.
- [ ] Test that finite deterministic routes beat model fallback.
- [ ] Test search miss remains `UNKNOWN` when search completeness is not established.
- [ ] Test unavailable semantic enrichment falls back to lexical/structural retrieval with explicit degradation.
- [ ] Commit `feat: add deterministic expert router`.

---

### Task 5: Expert diagnostic compiler

**Files:**
- Create: `contracts/problem-state.schema.json`
- Create: `diagnostics/README.md`
- Create: `tools/diagnose.py`
- Create: `tools/test_diagnose.py`

**Interfaces:**
- Consumes: `DomainMachine`, typed observations and route decision.
- Produces one of `SATISFIED | DEFECT | EVIDENCE_GAP | BLOCKED | CONTRADICTED | UNKNOWN`, with invariant/witness references.

- [ ] Test deterministic invariant violation yields `DEFECT` without model use.
- [ ] Test absent required observation yields `EVIDENCE_GAP`, not guessed state.
- [ ] Test contradictory observations remain `CONTRADICTED`.
- [ ] Model fallback may emit only a `candidate_diagnostic` field while verdict remains `UNKNOWN` until verified.
- [ ] Commit `feat: compile expert diagnostics`.

---

### Task 6: Repair recipes and verification oracles

**Files:**
- Create: `contracts/repair-recipe.schema.json`
- Create: `recipes/registry.jsonl`
- Create: `tools/select_recipe.py`
- Create: `tools/test_recipes.py`

**Interfaces:**
- Produces bounded recipes containing preconditions, read/write sets, forbidden writes, ordered actions, expected delta, oracle, falsifier, recovery, ruin class and authority.

- [ ] Seed recipes for planning dependency defect, ambiguous external effect, and destructive-change protection.
- [ ] Require every recipe to name an exact verification oracle.
- [ ] Block recipe selection when preconditions are unknown.
- [ ] Commit `feat: add verified repair recipes`.

---

### Task 7: Unresolved discovery engine

**Files:**
- Create: `contracts/unresolved-problem.schema.json`
- Create: `discovery/strategy.json`
- Create: `tools/discover.py`
- Create: `tools/test_discovery.py`

**Interfaces:**
- Produces rivals, known evidence, missing evidence, discriminating witness, safe experiments and forbidden actions.

- [ ] Test exact prior-case retrieval precedes new model generation.
- [ ] Preserve at least two live rivals until evidence dominates one.
- [ ] Record APR as iterative review donor, CASS as history retrieval donor.
- [ ] Ensure convergence scores never upgrade verdicts.
- [ ] Compile successful new distinctions as candidates for checker/rule/representation/recipe creation.
- [ ] Commit `feat: add deterministic discovery escalation`.

---

### Task 8: Obligation partition and residual compiler

**Files:**
- Create: `contracts/obligation.schema.json`
- Create: `tools/residualize.py`
- Create: `tools/test_residualize.py`

**Interfaces:**
- Partitions obligations into exactly one of `SATISFIED`, `UNSATISFIED`, `CONTRADICTED`, `UNKNOWN`, `NOT_APPLICABLE`.

- [ ] Test total/disjoint partition.
- [ ] Test only `UNSATISFIED` enters executable TODO candidate output.
- [ ] Keep contradictions and unknowns as separate frontier classes.
- [ ] Commit `feat: compile residual obligations`.

---

### Task 9: Frontier-resolved WorkPacket lowering

**Files:**
- Create: `contracts/work-packet-v2.schema.json`
- Create: `tools/lower_work_packet.py`
- Create: `tools/test_work_packet_lowering.py`
- Modify: `work/README.md`

**Interfaces:**
- Produces packets with one selected path, exact inputs/read/write sets, preconditions, acceptance, verifier, failure routing and authority ceiling.

- [ ] Reject packets containing unresolved design alternatives.
- [ ] Add a `reasoning_debt` vector and reject release when hidden design/scope/test/recovery choices remain.
- [ ] Verify simple executor grammar `READ -> CHECK -> CHANGE -> VERIFY -> RECEIPT -> STOP`.
- [ ] Commit `feat: lower frontier-resolved work packets`.

---

### Task 10: Effect/reconciliation adapter

**Files:**
- Create: `contracts/effect-operation.schema.json`
- Create: `tools/effect_state.py`
- Create: `tools/test_effect_state.py`

**Interfaces:**
- Encodes `intent -> attempt -> observation -> reconciliation` independently.

- [ ] Seed mutant tests for retry after unknown outcome, success from HTTP/exit status alone and attempt without intent.
- [ ] Require current authority before intent.
- [ ] Commit `feat: enforce external effect reconciliation`.

---

### Task 11: Procedural memory compiler

**Files:**
- Create: `contracts/procedural-memory.schema.json`
- Create: `memory/rules.jsonl`
- Create: `tools/compile_memory.py`
- Create: `tools/test_memory_compiler.py`

**Interfaces:**
- Candidate rules retain source evidence, scope, helpful/harmful feedback and lifecycle.

- [ ] Harmful evidence demotes faster than helpful evidence promotes.
- [ ] Catastrophic failure immediately emits guard/negative-memo candidate.
- [ ] No memory self-promotes.
- [ ] Commit `feat: compile procedural expertise`.

---

### Task 12: Novice control projection

**Files:**
- Create: `tools/orient_problem.py`
- Create: `contracts/novice-envelope.schema.json`
- Create: `tools/test_novice_envelope.py`

**Interfaces:**
- Machine fields preserve exact domain/receipt IDs; human projection contains `Problem`, `Why it matters`, `Known`, `Missing`, `Do not`, `Next`, `Proof`, `If unresolved`.

- [ ] Test expert terminology is optional in the default human surface.
- [ ] Test drill-down preserves exact domain representation.
- [ ] Test ruin warning cannot be omitted by compact mode.
- [ ] Commit `feat: add novice expert-control surface`.

---

### Task 13: Adversarial and novice benchmark

**Files:**
- Create: `tests/fixtures/expert-control/`
- Create: `tools/run_expert_control_benchmark.py`
- Create: `evidence/expert-control-benchmark.json`

**Interfaces:**
- Matched baseline vs compiled-control run.

- [ ] Include build, database, security, planning, external-effect, knowledge-conflict and reliability cases.
- [ ] Include malformed input, stale state, missing tool, contradictory evidence and ruin attempts.
- [ ] Measure correctness, recovery, semantic mistakes, deterministic route rate, model fallback rate, human attention and catastrophic-policy violations separately.
- [ ] Do not scalarize without explicit weights.
- [ ] Commit `test: benchmark expert control plane`.

---

## Plan self-review

### Spec coverage

- Authority/truth first: Tasks 2–3 plus existing Rising Sea authority contracts.
- Expert-native representation: Task 1.
- Deterministic routing: Task 4.
- Diagnosis: Task 5.
- Repair/oracles: Task 6.
- Unresolved discovery: Task 7.
- Residual obligations: Task 8.
- Simple executor lowering: Task 9.
- External effects: Task 10.
- Learning/accretion: Task 11.
- Novice ergonomics: Task 12.
- Empirical falsification: Task 13.

### Deliberately not reimplemented

- DCG rule-pack engine;
- FCP capability protocol;
- CASS search/index engine;
- Beads/BV dependency graph engine;
- APR review engine;
- CASS Memory/Eidetic full memory store.

Rising Sea defines adapters/contracts around these donors and implements custom machinery only where the catalogued mechanisms leave a residual.

### First execution packet

Start Task 1 now. It is independent of unfinished source vendoring and provides the machine contract needed by every later expert-domain component.