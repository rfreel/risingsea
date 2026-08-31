# Accretion, Learning, and Resource-Economic Control

## Objective

Make each completed unit of work reduce the expected cost or risk of future work without allowing anecdote, model confidence, or raw frequency to become authority.

## Accretion definition

An interaction is accretive when it leaves behind a reusable, scoped, invalidatable artifact whose future use is cheaper than reconstructing the same knowledge or behavior from scratch.

Accretive artifacts include:

- canonical observations;
- regression and property tests;
- minimized counterexamples;
- semantic distinctions;
- derivation rules;
- static or policy rule candidates;
- negative memos;
- reusable action results;
- dependency edges and invalidators;
- context-packing rules;
- deterministic workflows;
- promoted primitives;
- provider/effect reconciliation knowledge;
- decision and authority patterns.

A long explanation alone is not accretion unless it is compiled into a retrievable, scoped artifact with provenance and reuse conditions.

## Accretion delta

Every work packet and session checkpoint emits:

```json
{
  "schema": "rising-sea.accretion-delta.v2",
  "mission_id": "mission-...",
  "history_head_before": "sha256:...",
  "history_head_after": "sha256:...",
  "new_observations": [],
  "new_tests": [],
  "new_rules": [],
  "new_negative_memos": [],
  "new_cache_entries": [],
  "new_distinctions": [],
  "primitive_candidates": [],
  "promotions": [],
  "invalidators": [],
  "retirements": [],
  "unresolved": [],
  "estimated_future_savings": {},
  "no_accretion_reason": null,
  "receipt_refs": []
}
```

`estimated_future_savings` is a derived forecast with assumptions. It cannot justify promotion by itself.

## The learning ratchet

```text
WITNESS
  → CLASSIFY
  → MINIMIZE
  → TEST
  → COMPILE CANDIDATE
  → REPLAY
  → SHADOW
  → PROMOTE WITH SCOPE
  → USE
  → OBSERVE
  → RECEIPT
  → REENTER
```

### Failures

A repeated failure should become, in order of preference:

1. a reproducible fixture;
2. a property or invariant;
3. a static validation rule when sound;
4. a negative memo when the failure is scope-specific;
5. a routing guardrail;
6. a new distinction request when the failure cannot yet be generalized.

The system stops an equivalent retry loop when inputs, implementation, policy, and evidence have not materially changed.

### Successes

A repeated success may become:

1. a cache entry for exact semantics;
2. a parameterized deterministic workflow;
3. a finite lookup/table/trie/automaton;
4. a rule or graph operator;
5. a candidate primitive;
6. a promoted primitive after scoped evidence.

A single success is evidence, not a universal rule.

## Evidence profile, not scalar confidence

Primitive confidence is represented as a vector:

- positive case count and weighted severity;
- negative case count and weighted severity;
- independent reproduction count;
- scope coverage;
- recency and drift;
- shadow cohort coverage;
- mutation score;
- property/test coverage;
- unresolved obligations;
- known invalidators;
- effect ambiguity rate;
- fallback and rollback evidence.

A scalar may be derived for ranking under a declared policy. It cannot erase a severe counterexample, unresolved safety obligation, or scope gap.

## Resource objective

The system minimizes total expected future resource expenditure subject to hard safety, authority, truth, and scope constraints.

The resource vector includes:

- model input and output tokens;
- deterministic compute;
- wall-clock latency;
- monetary cost;
- human attention;
- network and storage;
- opportunity cost from blocked downstream work;
- risk-weighted expected loss;
- invalidation and rework cost;
- future verification cost.

The system does not silently collapse this vector. It uses dominance and declared mission policy. Uncalibrated probabilities are represented as intervals or unknowns.

## Route economics

The default route order is:

```text
exact result
  → exact negative memo
  → finite table/trie/automaton
  → deterministic rule/graph operator
  → incremental derivation
  → targeted source observation
  → bounded semantic retrieval
  → LLM residual proposal
  → human decision
```

The router may skip a cheaper route only when its applicability is false, unknown under a blocking obligation, stale, unavailable, or expected to cost more after verification and invalidation are included.

## Verification economics

Every reusable artifact stores the smallest witness needed to verify it again. The next verification should become cheaper through:

- stable action keys;
- cached canonicalization;
- incremental closure;
- dependency-directed invalidation;
- minimal counterexamples;
- proof/derivation slices;
- scoped test selection;
- observed provider idempotency/status behavior;
- reusable policy and identity validations within validity bounds.

A speedup claim requires a benchmark receipt. A cache hit without a complete material input closure is not a saving; it is an integrity risk.

## Accretion debt

The system reports accretion debt when:

- the same issue was solved repeatedly without a reusable artifact;
- a human correction was not captured as a distinction or constraint;
- a failure was not minimized or reproducible;
- a manual command bypassed the normal receipt path;
- a context capsule repeatedly includes the same irrelevant material;
- an ambiguous external effect lacks a provider-specific reconciliation adapter;
- a promoted primitive has no current invalidation monitor;
- an agent repeatedly rereads a large plan because work packets are incomplete.

Debt is a planning input, not an automatic authority to refactor.

## Core metrics

| Metric | Definition | Guardrail |
|---|---|---|
| Verified inference displacement | Required decisions safely answered by promoted mechanical paths rather than LLM inference | Must exclude unsafe, stale, or unknown activations |
| Cost per satisfied obligation | Total resource vector divided by newly satisfied required obligations | No scalar total without declared weights |
| Reverification ratio | Cost of repeated verification divided by first verification cost | Compare within exact scope and workload |
| Repeat-work rate | Equivalent tasks reconstructed without reusable evidence | Equivalence must be explicit |
| Accretion yield | Reusable artifacts admitted per completed packet | Quantity does not imply quality |
| Distinction yield | Decisive observations divided by distinction attempts | Preserve no-solution cases |
| Ambiguous-effect rate | Attempts without terminal observed classification | Provider and operation scoped |
| Human attention saved | Baseline attention minus observed attention under matched workflow | Requires matched baseline evidence |

Metrics remain projections. Optimizing a metric may not override truth or safety constraints.
