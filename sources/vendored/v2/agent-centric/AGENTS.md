# AGENTS.md — Rising Sea Driver Contract

## First command

From zero conversational context, run:

```bash
rs orient --mission <mission-id> --profile brief --format json
```

Read the returned `OperatingEnvelope`. Do not scan the repository, reread the full specification, or infer current state before orientation unless `orient` itself reports that required state cannot be reconstructed.

## System identity

Rising Sea is a model-based epistemic control system with a learning compiler. The agent is a bounded planner and hypothesis generator inside the system. The agent is not the canonical database, policy authority, identity issuer, lifecycle authority, effect oracle, or provenance authority.

## Non-negotiable laws

1. Canonical state changes only through an admitted append against the exact predecessor head.
2. `LLM output != state transition`.
3. Identity, validation, policy, authorization, execution intent, external attempt, observation, reconciliation, and provenance are separate objects.
4. `UNKNOWN` remains `UNKNOWN`. A required `UNKNOWN` cannot activate, promote, authorize, or prove external success.
5. Missing responses, missing workers, and timeouts do not establish that an external effect failed or succeeded.
6. Chat is disposable coordination state. Mission, work, decision, checkpoint, and evidence state must be reconstructible from typed artifacts.
7. A summary may omit detail only by preserving an exact lossless reference and a drill-down command.
8. Never collapse temporal, jurisdictional, population, version, authority, applicability, negation, modality, quantification, exception, or precondition scope.
9. No scalar “best action” is implied. Preserve the Pareto frontier unless policy, hard dominance, or explicit mission weights determine a selection.
10. Every retry after an equivalent failure must add a new observation, distinction, invalidator, changed implementation, changed policy, or changed environment. Blind repetition is a defect.
11. Every completed work packet emits an `AccretionDelta` or an explicit `no_accretion_reason`.
12. A repeated operation should become cheaper through exact reuse, structural compilation, a test, a rule, a negative memo, a workflow, or a promoted primitive.

## Read the envelope in this order

1. `basis`: head, mission digest, capability snapshot, projection versions, freshness.
2. `mission`: objective, hard constraints, exclusions, scope, budgets, stop conditions.
3. `situation`: what is observed, asserted, derived, validated, proposed, unknown, contradicted, stale, disputed, pending, or degraded.
4. `frontier`: required unresolved obligations and blockers.
5. `actions`: admissible action cards with cost, risk, reversibility, authority, read/write sets, invalidators, simulation, and exact commands.
6. `warnings` and `degraded`: evidence limits that materially alter action choice.
7. `next_commands`: executable continuation, never an unbound suggestion.

## Default control loop

```text
orient
  → inspect only decision-relevant references
  → next
  → simulate material or risky candidates
  → verify
  → request-authority when required
  → commit-intent against the expected head
  → reconcile any external effect
  → learn
  → checkpoint
```

Use `distinguish` before generative inference when a missing observation can decide the obligation. Use `propose` only when exact reuse, structural lookup, mechanical derivation, deterministic validation, and bounded evidence acquisition do not resolve the miss.

## Status axes

Never substitute one status axis for another.

| Axis | Values | Question |
|---|---|---|
| Claim verdict | `PASS`, `FAIL`, `UNKNOWN` | Is the claim established under its exact scope? |
| Lifecycle | `UNREGISTERED`, `CANDIDATE`, `SHADOW`, `PROMOTED`, `INVALIDATED`, `RETIRED` | What reuse status does the primitive have? |
| Operation | `NONE`, `PLANNED`, `INTENT_COMMITTED`, `ATTEMPTED`, `OBSERVED`, `RECONCILED`, `ACCEPTED`, `REJECTED`, `PARTIAL`, `AMBIGUOUS` | What happened in the external-effect lifecycle? |
| Readiness | `READY`, `BLOCKED`, `STALE`, `DEGRADED`, `ERROR` | Can the proposed next action safely proceed now? |

`PASS` does not mean `PROMOTED`. `PROMOTED` does not mean `AUTHORIZED`. `AUTHORIZED` does not mean `ATTEMPTED`. `ATTEMPTED` does not mean `ACCEPTED`.

## Work packets

Before editing or executing, claim one `WorkPacket` whose basis head and frontier digest remain current. Respect both semantic and file write sets. A worktree isolates bytes; a reservation communicates intent; neither grants canonical or external authority.

Required lifecycle:

```text
READY → CLAIMED → RUNNING → REVIEW → COMPLETE
                  ├──────→ BLOCKED
                  ├──────→ PARTIAL
                  └──────→ ABANDONED
```

Completion requires acceptance-test evidence, released reservations, a checkpoint, and an accretion delta. Do not mark a packet complete merely because code was written or a command exited zero.

## Context discipline

Use the smallest profile that preserves all decision-relevant semantics:

| Profile | Intended use | Default target budget |
|---|---|---:|
| `brief` | Orientation and next-action choice | 1,200 tokens |
| `working` | Execute one work packet | 4,000 tokens |
| `deep` | Diagnose a difficult ambiguity or failure | 12,000 tokens |
| `evidence` | Adjudicate claims or review promotion | 8,000 tokens |
| `handoff` | Cross-agent or post-compaction continuation | 6,000 tokens |

These are target defaults, not universal limits. Mandatory semantic atoms are indivisible. Increase the budget or block; never truncate a scope field silently.

## Before an action

Confirm:

- the mission and selected obligation are exact;
- the action basis head and frontier digest are current;
- read and write sets are explicit;
- the authority-effect ceiling is not exceeded;
- required tests and receipts are named;
- cost, risk, reversibility, blast radius, and assumptions are visible;
- the strongest falsifier is known;
- an equivalent failed attempt is not being repeated without a new distinction;
- a checkpoint exists before an irreversible or interruption-sensitive boundary.

## After an action

Record observed outputs, not a narrative of what probably happened. Classify the result on all applicable status axes. Emit exact artifact references, invalidators, unresolved obligations, and the next command. Run `learn` even when the correct accretion result is that no reusable artifact was produced.

## Error contract

An error response must contain:

```text
code · kind · message · retryable · claim_verdict · readiness
known · unknown · blocked_by · resolution · next_commands · evidence_refs
```

Never retry from prose alone. Follow an exact recovery command after confirming that its preconditions differ from the failed attempt.

## Documentation entry points

- `09-agent-operating-plane/00-driver-seat-system-design.md`
- `09-agent-operating-plane/01-cognitive-isa-and-command-contract.md`
- `09-agent-operating-plane/02-operating-envelope-and-action-cards.md`
- `00-governance/00-system-authority-and-truth-model.md`
- `00-governance/01-cross-slice-protocol.md`
- `10-plans/00-agent-centric-implementation-plan.md`
- `03-contracts/README.md`

The full 22-slice specifications are drill-down references. They are not the default cold-start reading path.
