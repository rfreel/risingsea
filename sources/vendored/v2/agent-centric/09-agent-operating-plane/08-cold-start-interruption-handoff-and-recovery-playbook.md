# Cold-Start, Interruption, Handoff, and Recovery Playbook

## Cold start

The agent begins with no conversational memory.

```text
1. rs capabilities --format json
2. rs doctor --profile brief --format json
3. rs orient --mission <mission-id> --profile brief --format json
4. follow next_commands[0] only after inspecting its ActionCard
```

The agent does not read the complete specification by default. It drills into one referenced object when the operating envelope says that detail can change the next decision.

## Start-work protocol

1. Inspect the selected action card.
2. Verify history head and frontier digest.
3. Claim the work packet if ownership is required.
4. Reserve the declared write surface.
5. Create or enter the isolated workspace.
6. Load the working context capsule.
7. Execute the exact start command.
8. Checkpoint before any authority-bearing or external action.

## Before a risky action

```text
rs simulate <action-id>
rs verify <candidate-or-action-id>
rs request-authority <action-id>
rs checkpoint --reason before-intent
rs commit-intent <action-id> --expect-head <head>
```

A missing or stale result stops the sequence. The agent does not infer that the later step is safe because an earlier step once passed.

## Interruption

On interrupt:

1. stop scheduling new side effects;
2. acknowledge the interrupt;
3. checkpoint local work;
4. record in-flight commands and child processes;
5. release or transfer edit leases;
6. preserve uncommitted outputs;
7. mark external attempts as pending until reconciled;
8. emit a resume capsule.

## Resume

```text
rs resume <capsule-id> --format json
```

If the head changed, inspect the returned semantic diff. Do not continue an old action card unless the envelope includes a non-impact proof and a current action digest.

## Handoff

```text
rs handoff <work-packet-id> --to <agent-capability-id> --format json
```

The receiving worker verifies:

- packet digest;
- current head;
- mission and scope;
- read/write sets;
- leases;
- acceptance tests;
- pending effects;
- authority ceiling;
- provider-neutral resume data.

The sender retains responsibility until the handoff is acknowledged or the claim is explicitly released.

## Ambiguous external effect

Never retry from a timeout alone.

```text
rs inspect effect <operation-id>
rs reconcile <operation-id>
```

Possible outcomes:

- `ACCEPTED`: observed postconditions satisfy intent;
- `REJECTED`: provider or observation establishes non-completion;
- `PARTIAL`: some postconditions hold and a residual remains;
- `AMBIGUOUS`: evidence cannot decide; retry is blocked unless the provider contract proves it safe.

## Repeated failure

When the same failure signature recurs with unchanged material inputs:

```text
rs learn --from <failure-receipts>
rs distinguish <blocked-obligation>
```

The next equivalent retry is prohibited until a new distinction, implementation change, scope change, or invalidator exists.

## Completion

A packet closes only after:

1. acceptance tests produce receipts;
2. outputs are admitted at the appropriate boundary;
3. external effects are reconciled;
4. leases are released;
5. `AccretionDelta` is emitted;
6. a final checkpoint or handoff capsule exists;
7. the operating envelope is refreshed at the new head.
