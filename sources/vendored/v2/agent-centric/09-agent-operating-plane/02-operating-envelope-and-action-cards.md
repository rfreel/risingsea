# Operating Envelope, Situation Frames, Frontiers, and Action Cards

## Objective

Specify the one object an agent reads on each control turn and the typed cards from which the agent selects work. The design optimizes for accurate situation understanding, low context cost, stale-state resistance, and explicit control consequences.

## Operating envelope

An `OperatingEnvelope` is an immutable, head-bound projection. It is not a session transcript and not canonical state.

### Required top-level fields

| Field | Function |
|---|---|
| `schema` | Stable machine contract version |
| `request_id` | Correlates one command request and response |
| `command` | Verb that produced the envelope |
| `response_status` | Agent readiness: READY, BLOCKED, STALE, DEGRADED, or ERROR |
| `basis` | History head, projection versions, mission digest, capability snapshot, context profile, and freshness |
| `mission` | Exact objective, exclusions, output contract, budgets, authority, and stop conditions |
| `situation` | Current facts, unknowns, conflicts, changes, pending effects, and health |
| `frontier` | Active obligations, blockers, decision distinctions, and work graph summary |
| `actions` | Pareto-distinct `ActionCard` objects |
| `payload` | Command-specific data |
| `receipts` | Evidence and provenance references |
| `warnings` | Non-blocking limitations with scope |
| `degraded` | Missing or stale capabilities and their consequences |
| `next_commands` | Exact machine commands that continue safely |
| `envelope_digest` | Digest over canonical envelope semantics |

## Mission envelope

The mission is compiled from authorized source intent. It prevents the agent from inventing a new objective, silently broadening scope, or forgetting exclusions.

A mission contains:

- stable mission ID and version;
- source-intent reference and verbatim preservation where required;
- normalized objective;
- finite output contract and acceptance obligations;
- hard constraints;
- explicit exclusions and non-goals;
- temporal, jurisdictional, population, version, applicability, and authority scope;
- budget vector;
- risk posture;
- permitted side-effect classes;
- human-approval policy;
- stop conditions;
- escalation conditions;
- success, failure, and partial-completion semantics.

The mission compiler emits ambiguities rather than selecting defaults with material effect.

## Situation frame

The situation frame is the agent’s state estimate. It separates source class and status axis.

### Fact card

Every fact appears as a typed card:

```json
{
  "fact_id": "fact-...",
  "proposition_ref": "semir:...",
  "truth_source": "OBSERVED",
  "claim_verdict": "PASS",
  "scope": {},
  "freshness": {"status": "current", "as_of": "observation:..."},
  "evidence_grade": "E3",
  "evidence_refs": ["receipt:..."],
  "invalidators": ["dependency:..."],
  "why_relevant": "Blocks obligation O-17 if absent."
}
```

The same proposition may have multiple evidence cards. The system does not collapse disagreement into one scalar confidence value. It exposes the conflict set and the adjudication rule.

### Situation frame partitions

- `observed`: direct captured state within source authority and freshness;
- `source_asserted`: statements made by identified sources;
- `derived`: mechanical consequences with derivation receipts;
- `validated`: checker conclusions under exact contracts;
- `model_proposed`: candidates only;
- `unknown`: required propositions without decisive evidence;
- `contradicted`: propositions with explicit negative evidence;
- `stale`: once-usable facts invalidated by time or dependency change;
- `disputed`: materially conflicting evidence not yet adjudicated;
- `pending_effects`: committed intents without terminal reconciliation;
- `degraded`: missing capabilities or telemetry and their operational effect.

## Decision frontier

The frontier contains only currently decision-relevant unresolved work.

Each obligation records:

- obligation ID and proposition;
- required or optional status;
- acceptance criterion;
- current claim verdict;
- dependencies;
- scope and invalidators;
- cheapest known decisive observation;
- reusable evidence candidates;
- responsible work packet if planned;
- blocking effect on mission completion;
- terminal conditions.

The frontier digest changes when any material obligation, basis, scope, or action set changes.

## Action card

An action card is a frozen, inspectable control proposal. It is the unit of selection, simulation, authorization, and intent commitment.

### Required fields

| Field | Meaning |
|---|---|
| `action_id` | Stable candidate action identifier |
| `verb` | Cognitive ISA action class |
| `mission_id` | Mission served |
| `history_head` | Exact state basis |
| `frontier_digest` | Exact unresolved frontier basis |
| `addresses_obligations` | Required obligations expected to change |
| `objective` | Concrete intended information or state delta |
| `preconditions` | Typed facts and receipts required before action |
| `predicted_delta` | Expected semantic, obligation, dependency, lifecycle, and effect changes |
| `evidence_gain` | Which uncertainty or claim verdict the action may resolve |
| `cost_vector` | Tokens, compute, wall time, money, human attention, storage, network, and external effects |
| `risk_vector` | Safety, security, privacy, irreversibility, blast radius, and ambiguity risk |
| `reversibility` | Reversible, compensatable, irreversible, or unknown with mechanism |
| `authority` | Required policy, identity, human approval, and capability bindings |
| `read_set` | Data/artifacts the action may inspect |
| `write_set` | Canonical, derived, repository, or external surfaces it may affect |
| `invalidators` | Changes that make the card stale |
| `simulation` | Whether and how a no-authority simulation can run |
| `exact_command` | Canonical command for execution of the next stage |
| `why_ranked` | Explicit comparison basis |
| `alternatives` | Materially distinct rival action IDs |

### No hidden scalarization

Action selection is constrained before optimized:

1. eliminate actions that violate hard mission constraints;
2. eliminate stale, unauthorized, unverified, or capability-infeasible actions;
3. identify exact reuse and compiled deterministic routes;
4. compute cost, risk, evidence gain, downstream unblock, accretion value, and reversibility vectors;
5. remove Pareto-dominated actions;
6. recommend a single action only if one dominates or the mission provides an explicit ranking policy;
7. otherwise present at least three materially distinct paths when three exist.

A model may propose risk escalation. It may not lower a mechanically computed risk tier.

## Counterfactual simulation

Before any costly, destructive, privacy-sensitive, or external action, the agent should be able to inspect a simulation card:

```text
current frame
  + action card
  + declared transition model
  → predicted next frame
  + assumptions
  + divergence risks
  + invalidation blast radius
  + rollback/compensation plan
```

Simulation results are model-based candidates. They do not establish external reality. The action card must state which effects the simulation cannot reproduce.

## Recommended action semantics

A recommendation includes:

- comparison set;
- hard filters applied;
- dominance or policy basis;
- evidence used;
- unavailable comparison dimensions;
- sensitivity to changed assumptions;
- strongest reason an expert might reject the recommendation;
- exact next command;
- safe fallback if the command cannot run.

When the system cannot justify one recommendation, the correct output is a preserved frontier, not a synthetic winner.

## Change-of-head behavior

Any canonical append triggers:

1. mark the current operating envelope stale;
2. recompute dependent situation and frontier projections;
3. invalidate action cards whose read sets or assumptions intersect the change;
4. preserve unaffected work packets only with an explicit non-impact proof;
5. require new policy/identity bindings when the action digest or head binding changes;
6. return a semantic diff to the agent.

## Agent-facing completeness rule

The operating envelope is complete only when it tells the agent:

- whether it is safe to act;
- what would make acting unsafe;
- which evidence is missing;
- what changed;
- what can be reused;
- what the next actions cost and risk;
- which action requires human authority;
- how to recover from failure or staleness;
- what reusable artifact may be created by the work.
