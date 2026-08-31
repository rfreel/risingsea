# Security and Trust Boundaries

## Assets

- canonical event history and head;
- policy and rule bundles;
- semantic schemas and SHACL shapes;
- primitive implementations and dependency artifacts;
- identity trust bundles and credentials;
- evidence, observations, provenance, and receipts;
- external effect targets;
- derived projections, caches, and route registries;
- user/private data present in source claims or observations.

## Adversaries and failures

The model includes malicious or compromised:

- LLM output;
- retrieved documents, RDF literals, source repositories, test fixtures, and prompts;
- candidate primitive implementation;
- cache writer or artifact mirror;
- effect provider response or webhook;
- stale/compromised worker identity;
- policy administrator or policy-data feed;
- projection store, telemetry source, or health signal;
- network path;
- operator error;
- software defects and resource exhaustion.

## Trust boundaries

| Boundary | Input is trusted for | Input is not trusted for |
|---|---|---|
| Cryptographic digest | Byte identity under algorithm/profile | Truth, safety, freshness, or authorization |
| Signature/attestation | Statement by key/identity under trust configuration | Semantic correctness or uncompromised builder |
| SPIFFE identity | Workload identity/selectors until expiry/revocation | Operation allowance |
| OPA decision | Policy result for exact request/bundle/data | Enforcement or real-world outcome |
| SHACL result | Shape conformance for exact graphs/shapes/engine | Behavioral correctness or policy |
| Static verifier | Accepted IR safety/well-formedness fragment | Intended behavior or external safety |
| Test PASS | Tested claims under exact corpus/environment | Untested inputs or global correctness |
| Shadow result | Observed cohort/time/version evidence | Universal correctness or causal transfer |
| Provider response | What the provider endpoint returned | Intended final state unless contract says authoritative |
| Projection/cache | Derived value at source head/key | Independent canonical state |

## Mandatory controls

1. Default deny for append, policy administration, identity issuance, primitive promotion, effect execution, and trust-bundle changes.
2. Least-privilege short-lived credentials, scoped by operation class and target.
3. Exact content and request binding for every authorization.
4. Sandboxing and resource limits for candidate execution, test generation, parsing, canonicalization, rules, and policy evaluation.
5. Egress allowlists and secretless credential injection where practical.
6. Supply-chain verification of implementation and dependency artifacts before execution.
7. Independent read/observation path for high-risk effects where available.
8. Tamper-evident audit receipts and monitor comparison of canonical heads.
9. Prompt/content injection isolation: retrieved/source content is data, never control.
10. No raw secret values in canonical history unless the explicit security model requires encrypted retention and key lifecycle.

## Authority separation matrix

| Role | May propose | May validate | May admit lifecycle | May append canonical event | May attempt external effect | May observe/reconcile |
|---|---:|---:|---:|---:|---:|---:|
| LLM | Yes | No | No | No | No | No |
| Compiler | Yes | Structural self-check only | No | No | No | No |
| SHACL/static/test verifier | Evidence only | Yes, scoped | No | No | No | No |
| Policy decision point | No | Policy evaluation | Allows exact next step | No | No | No |
| Identity service | No | Identity only | No | No | No | No |
| Canonical writer | No | Envelope/precondition checks | Enforces append policy | Yes | No | No |
| Effect worker | No | Request binding | Enforces attempt token | Status events through writer only | Yes, exact operation | May capture attempt evidence |
| Reconciler | No | Observation/postcondition checks | No | Terminal event through writer | No new write effect | Yes |
| Promotion authority | No | Reviews evidence | Yes | Event through writer | No | No |

## Threat-specific acceptance tests

- Prompt injection in RDF/test/log content cannot alter policy, schema, route, or command.
- Symlink/path traversal cannot escape declared local roots.
- Cache poisoning is detected before executable artifact use.
- Stolen expired identity cannot execute.
- ALLOW response replayed against changed request is rejected.
- Provider webhook without valid binding/signature/freshness remains UNKNOWN/untrusted.
- Concurrent appends cannot fork canonical state silently.
- Malicious telemetry cannot lower risk or create health certainty without source validation.
- Secret redaction retains explicit marker and does not change empty/null semantics.
- Hash/profile downgrade is rejected or handled by an explicit migration event.

## Agent-context security

1. Separate authenticated control instructions from untrusted content fields. Text inside a document, tool result, issue, email, log, code comment, or model proposal is data and cannot alter the mission or command protocol.
2. Bind every authority request and approval to the exact action digest, history head, target, quantity, time, location, recipient, and write set when material.
3. Expose read and write sets before execution. Undeclared access is a policy violation.
4. Redact secrets before context packing; preserve typed redaction markers and required secret references.
5. A model may escalate risk but cannot lower the mechanically computed risk floor.
6. Context capsules, recommendations, messages, and work claims have no external or canonical authority.
7. A capability catalog distinguishes observed runtime support from documented target support.
8. High-risk actions require simulation or an explicit simulation-unavailable reason, current verification, and exact human approval when policy requires it.
9. Tool output cannot introduce new executable instructions through prose. Only typed fields accepted by the command schema can control subsequent operations.
10. After compaction or provider handoff, resume revalidates authority and pending effects; no stale token or approval is inherited implicitly.

## Least-attention security

The safe path must be the shortest agent path. The operating envelope presents the exact allowed command, required authority, and recovery action so bypassing controls is never more ergonomic than using them.
