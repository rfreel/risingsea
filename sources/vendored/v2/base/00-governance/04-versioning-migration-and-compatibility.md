# Versioning, Migration, and Compatibility

## Versioned objects

Every schema, semantic vocabulary, canonicalization profile, rule bundle, shapes graph, policy bundle, trust bundle, primitive version, implementation, test corpus, route registry, observation adapter, and fold function has an immutable identity and digest.

## Compatibility classes

| Class | Rule |
|---|---|
| `IDENTICAL` | Same bytes/digest and version |
| `BACKWARD_READ_COMPATIBLE` | New reader accepts old object without semantic loss; proven by fixtures |
| `FORWARD_READ_COMPATIBLE` | Old reader safely ignores only explicitly optional fields; proven by fixtures |
| `MIGRATABLE_LOSSLESS` | Deterministic transform preserves every protected semantic field; round-trip/equivalence receipt required |
| `MIGRATABLE_LOSSY` | Transform has an explicit loss report; cannot satisfy obligations requiring lost fields |
| `INCOMPARABLE` | No authorized transform or semantic comparison exists |
| `REJECTED` | Version is unsafe, revoked, malformed, or outside policy |

Unknown versions are rejected by default. A reader may preserve an opaque object for forwarding only when doing so cannot grant authority or misrepresent validation.

## Migration event protocol

1. Register migration implementation as a candidate primitive.
2. Define source and target version domains and protected semantic fields.
3. Create positive, negative, and adversarial fixture corpus.
4. Run lossless/lossy classification and round-trip tests.
5. Shadow on historical data.
6. Promote the migration primitive for an exact source/target pair.
7. Append a migration-intent event.
8. Produce new immutable objects; never rewrite old bytes.
9. Verify target objects and source-to-target provenance.
10. Change routing/read preference by an explicit event after coverage reaches policy threshold.

## Hash and canonicalization agility

Commitments include algorithm and profile identifiers. Migration from one digest/canonicalization algorithm to another uses dual commitments over the same retained source bytes or a verified correspondence artifact. The system never compares bare digest strings without algorithm/profile context.

## Rule and ontology changes

A rule or semantic-schema change may:

- derive new facts;
- invalidate prior derivations;
- change residual classification;
- change primitive applicability;
- require candidate retesting;
- enlarge or shrink the unresolved set.

Therefore, closure and residual artifacts bind exact rule and semantic-schema digests. Historical evidence remains valid only for its recorded semantics.

## Projection migration

Projection schemas may be replaced freely when:

- source history remains unchanged;
- new fold is versioned;
- full rebuild is possible;
- old/new comparison receipt is retained;
- consumers identify the fold version;
- cutover does not alter canonical event semantics.

## External-provider version drift

Provider adapters record API version, endpoint identity, request/response schema, idempotency semantics, consistency/freshness model, and observation authority. Unannounced drift produces adapter UNKNOWN/FAIL and blocks unsafe writes; it does not trigger permissive parsing by default.

## Agent interface versioning

The cognitive ISA, operating envelope, action card, work packet, context capsule, resume capsule, capability catalog, and error envelope are versioned independently from internal adapter implementations.

A command response states:

- requested and realized schema version;
- adapter and projection versions used;
- unsupported fields or downgraded behavior;
- migration or retry command;
- whether the result remains safe for read-only use;
- whether any action card is invalidated by the version difference.

Unknown major versions fail closed. Minor additive fields may be ignored only when the schema declares them optional and the consumer proves they cannot affect authority, scope, semantics, cost, or risk.

## Capsule migration

A resume or handoff capsule is migrated by producing a new capsule that cites the source capsule and a migration receipt. The source bytes remain unchanged. Migration must preserve mission, exclusions, scope, status axes, pending effects, read/write sets, and invalidators. A field that cannot be preserved becomes explicit `UNKNOWN` and may block resumption.
