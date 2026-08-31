# Error, Adjudication, and Recovery Contract

## Canonical error classes

| Class | Meaning | Required response |
| --- | --- | --- |
| USAGE_OR_SCHEMA | Input is malformed, incomplete, or outside accepted schemas. | FAIL request; no side effect. |
| NONCONFORMANCE | A valid input violates a declared shape, invariant, behavior, policy, or lifecycle rule. | FAIL or REJECT according to the owning authority. |
| UNKNOWN_EVIDENCE | A required witness is absent, unavailable, stale, conflicting, or outside scope. | UNKNOWN; no activation. |
| STALE_VERSION | Predecessor, rule, policy, identity, dependency, or candidate version changed. | Reject reuse/activation and recompute. |
| PROCESSOR_FAILURE | The mechanism could not complete because of internal error or unsupported input. | No semantic verdict; retain diagnostics. |
| RESOURCE_LIMIT | Declared time, memory, row, state, or network budget ended processing. | UNKNOWN or contract-specific FAIL; never synthetic PASS. |
| CANCELLED | An authorized cancellation interrupted work. | Distinct terminal/transition state; drain and cleanup receipts required where promised. |
| AMBIGUOUS_EFFECT | An external attempt may have occurred but evidence cannot distinguish outcome. | UNKNOWN; status lookup or human adjudication before unsafe retry. |
| INTEGRITY | Digest, signature, Merkle proof, canonicalization, or replay mismatch. | Block affected authority path and investigate. |
| AUTHORITY | Identity, policy, capability, scope, or enforcement check failed. | DENY/REJECT; no effect. |

## Machine error envelope

```json
{
  "schema": "rising-sea.error.v1",
  "code": "STALE_HEAD",
  "class": "STALE_VERSION",
  "message": "Expected canonical head does not match current head.",
  "retryable": true,
  "retry_precondition": "recompute against returned current_head",
  "current_head": "sha256:...",
  "evidence_refs": [],
  "partial_effect": false,
  "unknown_fields": []
}
```

Required rules:

- `retryable=true` must name the condition under which retry is safe.
- A retry that changes semantic request data creates a new operation ID and authorization.
- `partial_effect=true` requires EFFECT reconciliation; generic retry is forbidden.
- Processor errors cannot be reported as domain FAIL unless the contract explicitly defines resource/termination failure as a failed requirement.
- Missing error detail remains UNKNOWN; it is not filled from likely causes.

## Recovery hierarchy

1. Reopen canonical history and verify head/event chain.
2. Rebuild or verify projections.
3. Enumerate PENDING intents, outbox obligations, test runs, migrations, and lifecycle decisions.
4. For local atomic operations, resume or retry by exact idempotency identity.
5. For external operations, query status/observe before retry.
6. Append recovered terminal evidence or retain UNKNOWN/dead-letter state.
7. Run consistency and invariant checks before accepting new authority-bearing work.

## Repeated correction loop interruption

When the same candidate or operation fails repeatedly without producing a new distinction, the system stops automatic retries and emits:

- repeated failure signature;
- unchanged premises/implementation;
- attempts and resource cost;
- missing discriminating evidence;
- recommended DISTINGUISH plan or human decision;
- prohibition on another equivalent retry until an invalidator changes.

## Agent error completeness

Every error response includes:

- error code and stable kind;
- separate claim verdict and readiness status;
- what is known to have happened;
- what remains unknown;
- whether canonical or external work may already have occurred;
- retry safety;
- blockers and invalidators;
- exact recovery or inspection commands;
- evidence references.

The agent must never infer retry safety from an HTTP status, process exit, timeout, or missing log line.

## Context-loss recovery

Conversational context loss is not a domain failure. Recovery uses the latest valid resume capsule, compares its head to the current head, computes semantic and invalidation deltas, identifies pending effects, and reconstructs the operating envelope. Missing chat history does not justify reopening completed decisions or repeating external attempts.

## No-progress loop gate

An equivalent action may not be scheduled after repeated failure when mission, head, inputs, implementation, policy, and evidence are unchanged. The system must produce a new distinction plan, implementation change, scope change, or human decision before another equivalent attempt.
