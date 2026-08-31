# Human Supervision and Exact Authority User Experience

## Objective

Give a human supervisor precise control without requiring the human to understand internal slice composition or restate context. Human attention is reserved for materially ambiguous, value-laden, high-risk, or irreversible decisions.

## Authority card

Every human approval request is bound to an immutable action card and shows:

- exact action and target;
- mission and obligation served;
- current canonical head;
- read and write surfaces;
- external side effects;
- risk tier and blast radius;
- reversibility or compensation mechanism;
- expected result and falsifier;
- evidence already collected;
- required unknowns that remain;
- why automation cannot decide;
- expiry and one-time or reusable scope;
- approve, reject, hold, request-more-evidence, and narrow-scope choices.

Approval binds to the action digest. Editing the command, scope, target, version, or write set invalidates the approval.

## Human choices remain data, not hidden instruction

A human decision becomes a canonical decision event with:

- alternatives considered;
- selected action;
- rejected alternatives when material;
- rationale or explicit no-rationale marker;
- authority identity;
- scope and expiry;
- assumptions;
- strongest known rejection reason;
- reversibility and migration impact.

The event does not imply the human’s rationale is globally true. It establishes the authorized decision.

## Friction policy

The system should not ask for approval when:

- the action is read-only;
- the action is mechanically reversible and within an already authorized scope;
- policy explicitly allows it;
- identity and version bindings are current;
- the mission permits it;
- the risk tier does not require human approval.

The system must ask when:

- a required value judgment or unresolved preference exists;
- the action is irreversible or has material external impact;
- legal, privacy, financial, safety, or authority scope is ambiguous;
- no safe reconciliation path exists;
- the action exceeds budget;
- policy requires independent approval;
- the agent proposes widening mission scope.

## Minimal supervisor view

The default approval card should fit one phone-sized screen. Detail remains available through drill-down. Compactness may not hide:

- target;
- side effect;
- irreversibility;
- amount/quantity;
- recipient;
- time;
- location;
- authority;
- unresolved risk;
- changed scope.

## Interrupt and stop

A supervisor can:

- pause new scheduling;
- cancel a candidate or simulation;
- request checkpoint and drain;
- revoke a lease or authority token;
- reject an intent before attempt;
- stop further retries;
- require reconciliation;
- retire or invalidate a primitive;
- narrow mission scope.

The interface must distinguish “stop requested” from “all effects stopped.”

## No approval laundering

An approval may not be reused for:

- a changed action digest;
- a different recipient or target;
- a different amount, time, location, or jurisdiction;
- a different history head when the change is material;
- a wider write set;
- a different primitive version;
- a different provider with materially different semantics;
- an operation after expiry or revocation.

## Human attention receipts

The system records:

- why attention was requested;
- time to decision;
- evidence inspected;
- decision and scope;
- later outcome;
- whether the same class can be compiled into a safer reusable rule.

This turns repeated supervision into a candidate guardrail without automating a preference that has not been generalized and approved.
