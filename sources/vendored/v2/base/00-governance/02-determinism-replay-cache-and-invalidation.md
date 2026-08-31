# Determinism, Replay, Cache, and Invalidation

## Determinism classes

| Class | Meaning | Required receipt |
|---|---|---|
| `deterministic` | Identical complete input closure produces byte-equivalent canonical output | Input/output digests, implementation/version, deterministic ordering profile |
| `deterministic_given_recorded_inputs` | Runtime may observe clocks, schedules, or state, but replay is deterministic after those values are captured as inputs | Recorded nondeterministic values and replay command |
| `nondeterministic_with_receipts` | External or stochastic outcomes may differ; each realized outcome is observed and retained | Attempt, observation, seed/sampling, environment, and reconciliation receipts |

“Deterministic” never means independent of version, platform, semantic schema, policy, locale, collation, floating-point mode, or environment. A deterministic claim must state the closure.

## Replay hierarchy

1. **Byte replay:** canonical bytes and digests reproduce.
2. **Projection replay:** deleting derived state and folding history reproduces projection content/digests.
3. **Decision replay:** fixed inputs and policy reproduce the same decision and reasons.
4. **Behavior replay:** candidate run under the same fixture/environment reproduces behavior.
5. **Effect reconciliation replay:** retained attempt and observation evidence reproduces the terminal classification; it does not replay the real-world effect.

A higher level does not follow automatically from a lower level.

## Cache admission

A result may enter a reusable cache only after:

- complete material input closure is declared;
- action definition is canonicalized and hashed;
- execution terminates with a cache-eligible status;
- all output digests verify;
- provenance and implementation identity are available;
- scope, environment, policy, model, and semantic versions are included when material;
- nondeterminism is absent or represented as fixed recorded input;
- invalidators are registered.

## Negative memo admission

A failure or miss may be cached only when the memo records:

- exact proposition/action/request key;
- status: FAIL or UNKNOWN, never generic “no result”;
- evidence or missing-evidence reason;
- scope and version;
- creation and expiry policy;
- dependency invalidators;
- authority class;
- whether retry is safe.

An UNKNOWN memo cannot become a denial rule without separate evidence and primitive promotion.

## Invalidation algorithm

Let `D = (V,E)` be the material dependency graph. When a set of inputs `C ⊆ V` changes, invalidate:

\[
I = \{v \mid \exists c \in C .\ c \leadsto_D v\}
\]

Only material edges participate. An implementation must return reason paths from each invalidated output to at least one changed input. Full global invalidation is permitted only when the dependency model itself is invalid, absent, or changed globally; the reason must be explicit.

## Nondeterministic observations

Before any observed value influences policy, promotion, routing, confidence, or canonical state, record:

- source mechanism and identity;
- request or sampling contract;
- start/end time;
- freshness and consistency semantics;
- raw/normalized value digests;
- uncertainty, missing fields, and errors;
- environment and implementation version.

A cached observation remains an observation from its original time. Reuse does not make it current.

## Replay acceptance tests

| Test | Expected result |
|---|---|
| Delete projections | Rebuild from history with matching declared digests |
| Shuffle input storage order | Canonical deterministic outputs remain stable |
| Change one material input | Exact transitive dependents invalidate |
| Change nonmaterial metadata | Reuse remains valid only if contract proves nonmateriality |
| Omit an ambient input from key | Hermeticity/conformance test fails |
| Corrupt cache output | Digest check rejects and quarantines |
| Replay stochastic run with recorded seed | Same deterministic computational trace within declared platform semantics |
| Replay external effect evidence | Same classification from retained evidence; no second external write |

## Agent context and control determinism

A context capsule is deterministic only for a complete basis:

- history head;
- mission digest;
- frontier digest;
- capability snapshot;
- projection, packer, ranker, tokenizer, and schema versions;
- context profile and budget;
- recorded nondeterministic inputs.

The capsule digest changes when any mandatory semantic atom, omission decision, ordering rule, or material basis changes.

An action key commits to:

```text
mission + head + frontier + action semantics + read set + write set
+ implementation + policy/identity requirements + scope + environment
```

A cache hit is safe only when the complete material action key matches and no invalidator has fired.

## Reorientation rule

After any canonical append:

1. mark dependent operating envelopes and action cards stale;
2. compute changed inputs and transitive invalidation paths;
3. preserve unaffected work only with an explicit non-impact proof;
4. rebuild the frontier and next actions;
5. refresh authority bindings when any bound semantic changed.

## Resume replay

At the same head and versions, a resume capsule must reconstruct the same mission, active frontier, work packet, selected action, read/write sets, pending effects, and next commands. At a different head, it must return a semantic diff rather than pretending continuity.
