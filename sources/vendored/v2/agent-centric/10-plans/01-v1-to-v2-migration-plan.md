# Migration Plan — Repaired v1 to Agent-Centric v2

## Migration invariant

The migration changes presentation, orchestration, context, work, and learning contracts. It does not rewrite or reinterpret admitted v1 events. Every v1 object remains addressable by its original digest and schema identifier.

## Compatibility classes

| Class | Meaning | Treatment |
|---|---|---|
| `IDENTICAL` | Bytes and semantics unchanged | Reuse directly |
| `LOSSLESS_ADAPTER` | v1 can be represented in v2 without invented information | Generate v2 projection with provenance to v1 |
| `PARTIAL_ADAPTER` | v1 lacks a v2 field whose absence is non-blocking | Emit explicit `UNKNOWN` or degraded field |
| `BLOCKED` | v1 lacks a field required for safe action | Refuse action; acquire evidence or human repair |
| `SEMANTIC_CONFLICT` | v1 and v2 meanings disagree | Preserve both; append adjudication event |

## Migration steps

1. Freeze the v1 package and generator by digest.
2. Register all v2 schemas and command catalogue without changing runtime behavior.
3. Project v1 mission-like inputs into `MissionEnvelope`; absent scope remains explicit.
4. Project current state into `SituationFrame`, preserving source classification.
5. Compute `DecisionFrontier`; do not infer closed obligations from missing data.
6. Wrap existing commands behind `AgentCommandRequest` and `OperatingEnvelope` adapters.
7. Introduce `ActionCard` as the only agent-facing action representation.
8. Introduce context and resume capsules; keep old session summaries as untrusted inputs until converted.
9. Convert existing tasks into `WorkPacket` records; preserve task IDs and dependencies.
10. Add `agent_route` to every target SPO row as a derived presentation field.
11. Add `agent_interface` to every family manifest; preserve family authority ceilings.
12. Begin emitting `AccretionDelta`; old completed work receives `no_accretion_reason = legacy-unmeasured` unless evidence supports a richer conversion.
13. Run dual projections from the same history and compare v1/v2 shared fields.
14. Shadow the v2 router and compare recommendations without granting authority.
15. Promote individual commands only after matched-task and recovery evidence passes.

## Rollback

Rollback selects the previous presentation/runtime version. It does not delete v2 events or rewrite v1 history. Any v2-only event remains in history and is ignored or rendered as unsupported by the v1 projection. External effects are not rolled back by changing software versions; compensation requires the effect protocol.

## Migration acceptance

- All 133 rows preserve subject, predicate, object, target status, original family, repaired slice, and authority ceiling.
- All 22 family manifests preserve their existing adapter semantics and add only agent-interface metadata.
- Every v1 history head folds under the v2 projection without fabricated scope.
- The v1 and v2 projections agree on shared canonical fields.
- A v1 client cannot accidentally invoke a v2 authority path.
- Downgrade reports unsupported v2 state rather than discarding it.
