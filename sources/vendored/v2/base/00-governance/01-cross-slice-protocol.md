# Rising Sea Cross-Slice and Agent Operating Protocol

## Objective

Define one end-to-end system loop. Internal slices exchange versioned artifacts; the agent interacts through one cognitive ISA and one operating envelope. No component communicates through hidden mutable state or prose-only side channels.

## Synthetic control loop

```text
AUTHORIZED SOURCE INTENT
  → MissionEnvelope
  → ORIENT: canonical head + situation + frontier + capabilities
  → NEXT: reuse / mechanical route / distinction / work packet / residual proposal
  → PLAN or DISTINGUISH when required
  → SIMULATE selected action
  → PROPOSE typed candidate when mechanical routes miss
  → VERIFY separate semantic, static, behavioral, replay, and resource obligations
  → REQUEST-AUTHORITY: policy + identity + human approval when required
  → COMMIT-INTENT against exact head and ActionCard digest
  → EFFECT attempt
  → RECONCILE intended postconditions with observed state
  → append terminal outcome and provenance
  → invalidate affected projections and reusable results
  → LEARN: witness → test/rule/negative memo/primitive candidate
  → CHECKPOINT and emit AccretionDelta
  → ORIENT at the new head
```

The agent does not need to know which slice executes each arrow. The operating envelope provides exact drill-down when internal detail can change the next decision.

## Immutable object chain

```text
MissionEnvelope
  → SituationFrame
  → DecisionFrontier
  → WorkGraph / WorkPacket
  → ContextCapsule
  → ActionCard
  → CounterfactualDelta
  → CandidateDelta or selected mechanical route
  → ValidationReceiptSet
  → AuthorityBindingSet
  → ExecutionIntent
  → AttemptReceipt
  → ObservationSet
  → ReconciliationReceipt
  → AccretionDelta
  → ResumeCapsule
```

Every object binds its predecessor artifacts by identifier and digest. Upper objects are summaries or proposals; only admitted events change canonical history.

## Operating envelope

Every agent command returns one stable outer shape containing:

- request and command identity;
- history, mission, capability, projection, and context basis;
- orthogonal status vector;
- mission summary;
- situation partitions;
- active frontier;
- up to three Pareto-distinct action cards by default;
- command-specific payload;
- receipts, warnings, and degraded modes;
- exact next commands;
- envelope digest.

## Handoff envelope

Every cross-slice and agent handoff contains:

| Field | Requirement |
|---|---|
| `schema_id` | Exact schema identifier and version |
| `artifact_id` | Stable identifier unique in its namespace |
| `content_digest` | Digest over media-type canonical bytes |
| `producer` | Slice, implementation digest, run, and receipt identifier |
| `history_head` | Exact canonical source head when state-dependent |
| `mission_digest` | Exact mission and output-contract basis when task-dependent |
| `frontier_digest` | Exact unresolved-obligation basis when decision-dependent |
| `scope` | Temporal, jurisdictional, population, version, authority, and applicability dimensions |
| `status_vector` | Separate claim, lifecycle, operation, and readiness values |
| `invalidators` | Changes that make reuse or control unsafe |
| `provenance_refs` | Input, process, identity, policy, environment, and output evidence |
| `authority_effect_ceiling` | Maximum effect the producing adapter may exercise |
| `omissions` | Omitted objects, reasons, decision effect, and inspect commands |
| `next_commands` | Exact safe continuation commands |

## Transition gates

| From | To | Required receipts | Explicitly insufficient |
|---|---|---|---|
| Source intent | Mission | SEMIR parse, scope, exclusion, and output-contract receipt | A chat summary or inferred default |
| Mission + head | Operating envelope | Current capability observation and projection freshness | Documentation-only capability or stale dashboard |
| History projection | Closure | Exact head, fold/rule digests, DATALOG receipt | Cached graph without source head |
| Closure | Frontier | Complete residual partition | Text compression or unverified subtraction |
| Frontier | Action card | Mission, head, obligation, cost/risk, authority, read/write set, invalidators | A recommendation string |
| Action card | Simulation | Frozen action digest and declared transition model | Informal “dry run” prose |
| Residual | LLM proposal | Context capsule containing only unresolved work and mandatory premises | Whole repository or history by default |
| Candidate | Verification | Typed IR and exact candidate digest | Model confidence or compile success alone |
| Verification | Shadow | Required SHACL, VERIFY, TEST, scope, and resource receipts | Absence of observed failures |
| Shadow | Promotion | Scoped evidence profile; no blocking required UNKNOWN | Scalar confidence |
| Selected action | Authority binding | Current OPA decision, SPIFFE identity, and human approval when required | Identity alone, policy alone, or old approval |
| Authority binding | Execution intent | Exact action digest, head, read/write set, and durable append | Queue row or worker claim |
| Execution intent | Attempt | Current intent, adapter capability, and delivery lease | Task readiness or message thread |
| Attempt | Terminal outcome | Fresh authoritative observation and reconciliation | Exit zero, 2xx, timeout, or missing error |
| Outcome | Learned candidate | Reconstructible evidence, scope, and generalization contract | Anecdote or raw frequency |
| Session boundary | Resume | Capsule digest, current-head comparison, pending-effect check | Previous chat transcript alone |

## Status preservation

A consumer may change a claim verdict only with new evidence. Lifecycle, operation, and readiness transitions occur through their own events or projections. Forbidden shortcuts include:

```text
UNKNOWN → PASS by default
CANDIDATE → PROMOTED by model confidence
PROMOTED → READY without per-use applicability
IDENTITY_ATTESTED → ALLOW without policy
ALLOW → EXECUTED without intent and enforcement
ATTEMPTED → ACCEPTED without observation
STALE action → intent after head change
message → task completion or authority
context summary → canonical state
```

## Resource-aware route order

```text
exact reusable result
  → exact negative memo
  → finite compiled table/trie/automaton
  → deterministic rule/graph operator
  → incremental derivation
  → cheapest decisive observation
  → bounded semantic retrieval
  → LLM residual proposal
  → human decision
```

The router includes immediate cost, future verification cost, risk, reversibility, invalidation blast radius, and downstream unblock. It preserves incomparable options.

## Local transaction boundary

One local transaction may atomically change:

- canonical event rows;
- current head and sequence;
- Merkle frontier;
- idempotency index;
- outbox obligation tied to an execution intent;
- bounded rebuildable projections.

It cannot atomically change a remote provider, another transaction domain, a human decision, or a physical system.

## External effect boundary

```text
commit exact intent
  → at-least-once delivery under operation identity
  → provider attempt
  → authoritative status or state observation
  → reconcile
  → terminal append
```

Exactly-once may be claimed only under a provider contract that establishes sufficient idempotency and status semantics.

## Correlation identifiers

Mission, obligation, work packet, action, candidate, validation, policy, identity, approval, operation, idempotency, provider, observation, event, and provenance IDs remain distinct. A correlation ID groups them for navigation but does not replace their semantics.

## Interop conformance

Every slice and agent command publishes:

1. JSON Schema or equivalent type contract;
2. canonicalization and digest profile;
3. compatibility and migration policy;
4. typed error envelope with retry safety and next commands;
5. authority effect declaration;
6. deterministic and recorded-input declaration;
7. minimum provenance binding;
8. invalidators and freshness policy;
9. positive, negative, stale, crash, and resume fixtures;
10. capability observation status;
11. brief fields and drill-down commands;
12. accretion output contract.
