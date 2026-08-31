# Rising Sea System Authority and Truth Model

## Status

This document defines the normative authority boundary for the repaired Rising Sea target architecture. Every vertical-slice specification inherits it. A slice may narrow these rules but may not widen its own authority.

## Canonical object

The canonical object is an ordered sequence of admitted immutable events:

\[
H_n = \langle e_1, e_2, \ldots, e_n \rangle
\]

Each event binds:

- exact predecessor head;
- event type and schema version;
- canonical payload digest and canonicalization profile;
- temporal, jurisdictional, population, version, authority, and applicability scope digests where material;
- identity, policy, evidence, and provenance references required by the event type;
- idempotency identity;
- event digest and sequence.

The current semantic graph, task state, primitive registry, confidence values, pending work, caches, dashboards, and metrics are projections:

\[
P_i(n) = \operatorname{fold}_i(H_n, v_i)
\]

where `v_i` is the exact fold implementation/version. A projection is authoritative only as a statement about what that fold produced at the named head. A projection cannot alter history and cannot outrank it.

## Agent operating plane

The agent operating plane is a deterministic or recorded-input-deterministic projection over canonical history, mission state, capability observations, and the other declared projections. It compiles internal slice complexity into one `OperatingEnvelope`.

The operating plane may:

- summarize mission, state, uncertainty, changes, work, and action options;
- rank or preserve a Pareto frontier of candidate actions;
- generate context, checkpoint, resume, and handoff capsules;
- issue exact read-only drill-down commands;
- request validation, policy, identity, or human decisions from the owning authorities.

The operating plane may not:

- append canonical events except by invoking the canonical append contract;
- convert a recommendation into authority;
- turn documentation into observed capability;
- treat chat context as state;
- hide required unknowns, stale inputs, pending effects, or degraded telemetry;
- reuse an action card after a material head or dependency change.

Every envelope binds the exact history head, mission digest, frontier digest, capability snapshot, context profile, packer/ranker versions, and output digest. Any authority-bearing action selected from an envelope also binds the envelope digest.

## Authority is not one scalar

Authority classes describe distinct effects. They are not interchangeable levels in one universal hierarchy.

| Effect class | Permitted effect |
| --- | --- |
| none | Produces information or derived state only; cannot change lifecycle, canonical history, or the external world. |
| candidate | May create or rank a typed proposal; cannot accept, promote, append, authorize, or execute it. |
| validation | May issue scoped PASS/FAIL/UNKNOWN evidence under a declared contract; cannot authorize or execute. |
| admission | May permit a named next transition when every precondition is satisfied; does not itself perform the transition unless combined with the canonical append boundary. |
| execution_intent | May commit an authorized intent and durable delivery obligation; does not prove external completion. |
| external_attempt | May perform the exact external operation named by a valid committed intent. Attempt authority does not imply observed completion. |
| canonical_append | May advance the canonical history head through exact-predecessor admission. This is the only canonical state mutation effect. |

Important separations:

```text
identity evidence          != policy decision
policy decision            != enforcement
validation PASS            != lifecycle promotion
promotion                  != per-use applicability
execution intent           != external attempt
external attempt           != observed completion
provenance                 != correctness
projection                 != canonical history
model output               != state transition
```

The only internal canonical mutation is exact-predecessor append. External attempts occur only through an EFFECT adapter after an execution-intent event. External completion is a conclusion of RECONCILE over authoritative observations, not a power granted to the effect worker.

## Truth-source taxonomy

| Source class | Meaning | May establish | Cannot establish alone |
|---|---|---|---|
| `OBSERVED` | Directly captured state from a named observation mechanism | The observation payload within its freshness, scope, and sensor/provider authority | Causal explanation, global validity, future persistence |
| `SOURCE_ASSERTED` | A source states a proposition | That the source made the assertion | Truth of the assertion |
| `DERIVED` | Mechanical rule application from accepted facts | Consequence under exact rule semantics and scope | Validity outside the rule closure |
| `VALIDATED` | A checker emits PASS/FAIL/UNKNOWN | Conformance to its declared contract | Policy allowance, identity, or external outcome |
| `POLICY_DECIDED` | Policy decision point evaluates exact request | ALLOW/DENY/INDETERMINATE under exact policy/data/input | Enforcement or effect completion |
| `IDENTITY_ATTESTED` | Trust system validates workload identity/selectors | Identity within validity and revocation bounds | Operation authorization |
| `MODEL_PROPOSED` | Generative model emits a candidate | Existence of the proposal | Truth, conformance, admission, authority, or execution |
| `PROJECTED` | Deterministic fold/index/cache emits a view | View contents at source head/version | Independent state authority |
| `UNKNOWN` | Required evidence does not decide | The evidence gap and unresolved alternatives | Safe default in either direction |

## Orthogonal status semantics

Rising Sea does not use one scalar status for claims, lifecycle, operations, and readiness. These axes remain independent.

### Claim verdict

| Value | Normative meaning |
|---|---|
| `PASS` | Every required obligation for one exact claim, scope, version, and evidence contract has a valid witness. |
| `FAIL` | A valid required counterexample, contradiction, or invariant violation exists. |
| `UNKNOWN` | Available evidence does not establish PASS or FAIL; the missing witness or processor limitation is explicit. |

For a finite set of required obligations `O`:

- aggregate `PASS` iff every `o ∈ O` passes;
- aggregate `FAIL` iff at least one required `o ∈ O` has a valid failure witness;
- aggregate `UNKNOWN` otherwise.

### Primitive lifecycle

| Value | Meaning |
|---|---|
| `UNREGISTERED` | No immutable primitive version exists. |
| `CANDIDATE` | A typed proposal exists without promotion or execution authority. |
| `SHADOW` | The candidate may run without production authority to collect evidence. |
| `PROMOTED` | One immutable version is admitted for an exact supported scope; each use still requires applicability and authority. |
| `INVALIDATED` | A material dependency, scope, policy, evidence, or outcome no longer supports use. |
| `RETIRED` | New routing is disabled by an admitted decision; history remains. |

### External-operation lifecycle

| Value | Meaning |
|---|---|
| `NONE` | No operation exists. |
| `PLANNED` | An action card exists; no intent is committed. |
| `INTENT_COMMITTED` | Exact authorized intent and delivery obligation are canonical. |
| `ATTEMPTED` | An external adapter attempted the exact operation. |
| `OBSERVED` | One or more relevant external observations exist. |
| `RECONCILED` | Intended postconditions and observations were compared. |
| `ACCEPTED` | Required postconditions were authoritatively observed. |
| `REJECTED` | Provider or observation establishes non-completion or denial. |
| `PARTIAL` | Some required postconditions hold and the residual is explicit. |
| `AMBIGUOUS` | Evidence cannot decide whether the effect occurred or completed. |

### Agent readiness

| Value | Meaning |
|---|---|
| `READY` | The named next step has all required preconditions. |
| `BLOCKED` | A named dependency, distinction, authority, or resource prevents progress. |
| `STALE` | The artifact or action is bound to an invalidated head, scope, version, or dependency. |
| `DEGRADED` | Work can continue with explicit capability or evidence limitations. |
| `ERROR` | The operating surface failed to produce a valid response. |

Confidence, evidence grade, freshness, authority, risk, and priority are separate fields. None may overwrite one of these axes.

### Status transition discipline

- `UNKNOWN` changes only through new decisive evidence or a corrected contract.
- `FAIL` is not edited into `PASS`; a repaired candidate receives a new identity.
- `PROMOTED` does not imply `READY` for a particular use.
- `INTENT_COMMITTED` does not imply `ATTEMPTED` or `ACCEPTED`.
- `ATTEMPTED` does not imply `OBSERVED`.
- `DEGRADED` does not imply unsafe; it names which guarantees are unavailable.

## Append protocol

1. Build canonical payload bytes using the media-type-specific canonicalizer.
2. Build JCS event-envelope bytes binding payload digest and all authority/evidence references.
3. Authenticate caller and evaluate append policy.
4. Compare expected predecessor to current head.
5. Check idempotency-key binding.
6. Atomically insert event, update head, update Merkle frontier, and write any bounded projection/outbox rows.
7. Return a durable head receipt.
8. On ambiguous client failure, query by idempotency key or event digest before retry.

Exactly one successful event may name a given predecessor. Concurrent losers receive a stale-head result and recompute against the new head.

## Corrections, deletion, and redaction

Canonical events are not edited. A correction, invalidation, supersession, retirement, legal redaction, or tombstone is a later event. A redaction event must state:

- legal/policy authority;
- affected event/artifact fields;
- whether bytes were destroyed, access-restricted, encrypted-key-erased, or merely hidden from projections;
- which verification operations become impossible;
- remaining commitments and limitations.

The system may not claim complete replay after authorized destruction of required bytes. It reports the exact replay boundary as `UNKNOWN` or intentionally unavailable.

## Root invariants

1. `LLM OUTPUT != STATE TRANSITION`.
2. No `UNKNOWN` required obligation activates a primitive or effect.
3. No external attempt occurs without a valid exact execution intent.
4. No exact execution intent is committed without current policy allowance and valid identity.
5. No terminal external success is emitted without an observation satisfying the effect contract.
6. No projection, cache, index, dashboard, metric, or worker lease is canonical authority.
7. No semantic scope field is silently broadened or defaulted.
8. No accepted event changes an earlier event’s bytes.
9. No stale predecessor, policy, identity, candidate, rule, or dependency version is reused after invalidation.
10. Every public claim is bounded by its evidence, scope, version, and freshness.
11. Every agent-facing recommendation binds mission, head, frontier, cost, risk, reversibility, authority, and invalidators.
12. Chat history, context capsules, dashboards, work graphs, and operating envelopes remain derived state.
13. No repeated equivalent attempt follows a failure without a new distinction or material invalidator.
14. Every context omission is lossless by reference and may not drop a hard constraint or semantic qualifier.
15. Every completed work packet emits an AccretionDelta or an explicit no-accretion reason.
16. Every context-loss, handoff, or interruption boundary has a verifiable resume capsule.

## Required system tests

| Test | Witness |
|---|---|
| Concurrent append | Exactly one successor per predecessor; loser is stale, not silently rebased |
| Projection erasure | Delete all projections and rebuild byte-equivalent declared views from history |
| UNKNOWN activation mutant | Model checker and runtime gate both reject |
| Identity/policy cross-product | Only valid identity plus ALLOW plus exact binding can reach intent |
| Ambiguous effect | Timeout after provider application remains UNKNOWN until observation distinguishes it |
| Scope mutation | Changing time, jurisdiction, population, applicability, or version changes semantic digest and invalidates reuse |
| Model proposal injection | Proposal cannot invoke append/effect channels directly |
| Provenance overclaim | Receipt presence cannot satisfy a behavioral correctness obligation |
