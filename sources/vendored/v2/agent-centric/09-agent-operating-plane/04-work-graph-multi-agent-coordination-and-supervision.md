# Work Graph, Multi-Agent Coordination, and Supervision

## Objective

Compile mission obligations into self-contained, dependency-aware work so one or many agents can make parallel progress without rereading the original plan, overwriting each other, or inventing task authority.

## Work graph

The work graph is a derived projection. Nodes are `WorkPacket` objects; edges are typed dependencies.

Dependency types include:

- `requires_output`;
- `requires_decision`;
- `requires_authority`;
- `requires_observation`;
- `requires_resource`;
- `conflicts_write_set`;
- `invalidates`;
- `supersedes`;
- `review_of`;
- `reproduction_of`.

A generic edge named only `depends_on` is insufficient when the dependency type changes readiness or invalidation semantics.

## Work packet contract

A work packet contains everything required to execute one bounded task:

- packet ID, mission ID, and source obligations;
- exact objective and non-goals;
- current history head and frontier digest;
- material background and rationale;
- typed dependencies and blockers;
- input artifacts and read set;
- output artifacts and write set;
- acceptance tests and strongest falsifier;
- required tools and observed capabilities;
- authority effect ceiling;
- risk and resource budgets;
- file, graph, or effect-surface reservations;
- expected accretion output;
- checkpoint and handoff rules;
- completion, partial, blocked, and abandoned semantics;
- exact start, verify, close, and release commands.

A worker should not need the original prose plan to understand or verify the packet.

## Ready, claimed, running, and complete are distinct

| State | Meaning |
|---|---|
| `READY` | Dependencies and preconditions currently permit work; no owner implied |
| `CLAIMED` | One worker has an acknowledged claim; execution may not have started |
| `RUNNING` | Worker has started and owns a bounded attempt |
| `BLOCKED` | A named dependency, authority, distinction, or resource prevents progress |
| `REVIEW` | Output exists but acceptance has not been adjudicated |
| `COMPLETE` | Required acceptance receipts passed and outputs were admitted as appropriate |
| `PARTIAL` | Some required outputs remain explicit |
| `ABANDONED` | Attempt ended without completing; outputs and residual are retained |

A file modification, commit, message, or worker process is not sufficient evidence of completion.

## Claims and reservations

Task claim, communication, file reservation, worktree, and canonical authority are separate objects.

```text
work claim          → who intends to execute a packet
message thread      → coordination and decisions
file/semantic lease → edit-surface intent and conflict prevention
worktree            → filesystem isolation
canonical event     → admitted state transition
```

A lease is advisory or enforced according to its contract. It never grants production or canonical authority.

## Agent assignment

The scheduler uses observed capability and resource state, not model stereotypes alone. Assignment inputs include:

- required tools and environment;
- model/provider capability catalog;
- task risk and authority ceiling;
- context size and modality;
- active account or quota posture;
- current host resources;
- write-set conflicts;
- prior evidence for similar work;
- cancellation and recovery support;
- human supervision requirements.

The assignment receipt states why a worker was selected and which alternatives were rejected or unavailable.

## Parallel planning

Work may run in parallel only when:

- dependency edges permit it;
- write sets do not conflict or isolation exists;
- shared external rate/resource budgets are allocated;
- authority requests do not create incompatible actions;
- completion order is not allowed to alter canonical semantics;
- each packet has independent acceptance tests.

Graph metrics may identify bottlenecks and critical paths, but a score is advisory. The scheduler exposes reason paths and does not equate centrality with priority.

## Agent-to-agent communication

Messages are durable coordination artifacts linked to packet IDs. A message can carry:

- start or completion notice;
- decision request;
- blocker;
- interface contract;
- discovered invalidator;
- review result;
- handoff capsule;
- effect ambiguity alert.

Messages do not mutate task status, release authority, or canonical state. Those transitions require their owning events.

## Peer review

Review packets are generated with:

- exact candidate/diff digest;
- original acceptance obligations;
- known implementation rationale;
- excluded assumptions;
- prior test receipts;
- requested adversarial frames;
- files and semantic surfaces in scope;
- authority to propose fixes, if any.

The reviewer should be able to challenge the candidate without inheriting the producing agent’s conclusions as facts.

## Supervisor envelope

A human or agent supervisor receives a fleet view containing:

- mission progress by satisfied obligation, not prose percentage;
- ready and blocked packets;
- active workers and leases;
- stale or conflicting work;
- pending authority requests;
- ambiguous external effects;
- resource pressure;
- repeated-failure loops;
- accretion produced per packet;
- exact interventions available.

Missing telemetry appears as `UNKNOWN` or `DEGRADED`, not as healthy idle state.

## Interruption and cancellation

An interrupt has explicit phases:

```text
request
  → acknowledge
  → stop new effects
  → checkpoint local work
  → drain owned children
  → release or transfer leases
  → publish terminal attempt receipt
```

A killed process is not evidence that the effect stopped. Pending operations remain visible until reconciled.

## Merge and integration

Worktree or branch merge requires:

- packet acceptance receipts;
- current target-head check;
- semantic diff and scope-preservation check;
- conflict classification;
- invalidation impact analysis;
- review decision;
- exact integration event.

Automated merge is permitted only for a declared low-risk class with complete tests and no unresolved semantic or authority obligations.

## Recovery

After crash or provider loss:

1. reconstruct active packets from canonical and coordination state;
2. identify abandoned claims and leases;
3. inspect worktrees and uncommitted outputs;
4. query external operation status before retry;
5. generate resume or handoff capsules;
6. reassign only after conflict and staleness checks;
7. retain all partial artifacts and failure witnesses.

## Accretive work completion

Closing a packet requires an `AccretionDelta` stating which reusable artifacts were created or why none were justified. Examples include:

- a passing test;
- a minimized failure fixture;
- a new derivation or rule candidate;
- a reusable cache entry;
- a negative memo;
- a new distinction;
- a promoted primitive;
- an invalidator;
- a better context-packing rule;
- a decision record.

This prevents high-volume agent work from producing only transient code and prose.
