# Context Capsules, Progressive Disclosure, Compaction, and Resume

## Objective

Make chat context disposable while preserving exact mission, semantic, evidentiary, and operational state. The agent should receive the smallest context that permits a correct next decision, with lossless drill-down by reference.

## Context is a derived execution artifact

A context capsule is generated from canonical history and versioned projections. It is not memory authority. The same head, mission, packing profile, budget, and packer version must reproduce the same capsule digest.

```text
history head + mission + frontier + capabilities + profile + budget
  → deterministic context selection
  → ContextCapsule
```

## Context profiles

The v2 default profiles are policy values, not universal limits:

| Profile | Default token ceiling | Use |
|---|---:|---|
| `brief` | 1,200 | Cold orientation, routing, supervisory checks |
| `working` | 4,000 | Execute one bounded work packet |
| `deep` | 12,000 | Complex semantic repair, design, or adversarial review |
| `evidence` | 8,000 | Proof and receipt inspection with minimal narrative |
| `handoff` | 6,000 | Transfer one task between agents or providers |

The capsule records the tokenizer or estimator identity. Token ceilings can be overridden only through the mission or explicit command arguments. Hard constraints are not truncated to satisfy a budget.

## Mandatory packing order

Mandatory content is packed before any relevance-ranked content:

1. mission objective and source-intent digest;
2. hard constraints, exclusions, negation, modality, exceptions, and scope;
3. output obligations and acceptance criteria;
4. current head, freshness, and authority posture;
5. selected work packet and action card;
6. active blockers, contradictions, and required unknowns;
7. pending effects that can make new action unsafe;
8. prior equivalent failures and negative memos;
9. required verification and recovery commands.

Optional content is then selected by marginal decision value:

- direct witnesses for current obligations;
- reusable prior results;
- closest counterexamples;
- implementation context within declared read set;
- material alternatives;
- explanatory narrative.

## Lossless-by-reference rule

Omission is allowed only when the capsule records:

- omitted artifact ID and digest;
- why it was omitted;
- whether omission can affect the next decision;
- exact inspect command;
- size estimate;
- source classification and scope.

A summary that cannot be traced to the omitted object is not a valid compression artifact.

## Semantic atomicity

The packer may not split or truncate:

- a negated proposition from its negation;
- a qualifier from the proposition it scopes;
- an exception from the rule it limits;
- an authority requirement from the action it gates;
- an acceptance criterion from its obligation;
- a failure from its reproduction witness;
- a risk statement from its affected action;
- an observed value from its freshness and source.

When a semantic atom cannot fit, the capsule returns `BUDGET_INSUFFICIENT` and the minimum required budget. It does not silently omit the atom.

## Instruction/data separation

Untrusted source content is never concatenated into the instruction channel. A context capsule has distinct fields:

- `control_instructions`: authenticated system, mission, and policy instructions;
- `trusted_facts`: admitted or validated data with source classification;
- `untrusted_content`: documents, messages, web pages, code comments, logs, and model outputs to analyze as data;
- `tool_results`: typed outputs with provenance and authority ceiling;
- `candidate_reasoning_material`: hypotheses and proposed transformations;
- `forbidden_effects`: explicit authority boundary.

Strings inside `untrusted_content` cannot add commands, alter the mission, change authority, or redefine the schema.

## Read-set and write-set packing

For one work packet, the capsule includes:

- exact read-set manifest;
- allowed write-set manifest;
- file or semantic leases;
- expected outputs;
- acceptance commands;
- known nearby work owned by other agents;
- material diffs since the packet was created.

This allows the agent to operate locally without scanning the entire repository or colliding with another worker.

## Checkpoint capsule

A checkpoint records:

```json
{
  "mission_ref": "mission:...",
  "history_head": "sha256:...",
  "operating_envelope_digest": "sha256:...",
  "active_work_packet": "work:...",
  "selected_action": "action:...",
  "read_set_digest": "sha256:...",
  "write_set_digest": "sha256:...",
  "decisions": [],
  "open_obligations": [],
  "pending_effects": [],
  "produced_artifacts": [],
  "accretion_delta_ref": null,
  "next_commands": [],
  "capsule_digest": "sha256:..."
}
```

The checkpoint is created at task boundaries, before risky actions, before context compaction, before agent handoff, and before planned interruption.

## Resume protocol

1. Load the resume capsule.
2. Verify its digest and schema.
3. Read the current canonical head.
4. If heads match, rebuild the operating envelope from declared versions.
5. If heads differ, compute a semantic and invalidation diff.
6. Preserve unaffected work only with a non-impact proof.
7. Recompute stale action cards and authority bindings.
8. Surface pending or ambiguous effects before new execution.
9. Return exact next commands.

A resumed agent does not need the previous chat transcript. The transcript may be searched as evidence, but it is not a precondition for correctness.

## Cross-provider handoff

A handoff capsule uses provider-neutral schemas. It contains no provider-specific hidden state. Provider-native session conversion may improve convenience but cannot replace:

- mission and scope;
- canonical head;
- work packet;
- evidence and decisions;
- pending effects;
- next commands;
- authority limits.

Read-back verification is required after converting a handoff into a provider-native session format.

## Context quality metrics

Metrics are derived and non-authoritative:

- tokens to first safe action;
- mandatory-content coverage;
- irrelevant-context ratio;
- drill-down rate;
- repeated-read rate;
- stale-capsule rejection rate;
- post-resume divergence rate;
- number of hidden prerequisites discovered after action selection;
- semantic atoms omitted due to budget;
- context reuse savings.

The strongest quality criterion is not minimum token count. It is minimum total resource cost subject to preserving every material distinction needed for a correct decision.
