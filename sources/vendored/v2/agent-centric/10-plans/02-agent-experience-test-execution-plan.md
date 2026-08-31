# Agent Experience Verification and Benchmark Execution Plan

## Question

Does the agent-centric system improve decision accuracy, control legibility, recovery, and future verification cost without concealing assumptions or increasing safety risk?

## Matched baselines

Compare four conditions over the same mission corpus:

1. Raw repository and full specifications.
2. Slice-specific commands without the unified operating plane.
3. Unified operating plane without learned reuse.
4. Unified operating plane after accretion and primitive promotion.

The same model/provider, tool permissions, repository revision, mission, environment fixture, and maximum resource budgets are used for each matched cell. Any deviation is a recorded covariate.

## Corpus families

| Family | Required cases |
|---|---|
| Cold start | Clear, ambiguous, stale, degraded, and contradictory missions |
| Semantic preservation | Negation, modality, quantifiers, exceptions, temporal/jurisdictional/population scope |
| Reuse | Exact hit, structural hit, invalidated hit, negative memo, missing cache |
| Distinction | Cheap decisive observation, costly decisive observation, unauthorized observation, no solution in query space |
| Verification | Static fail, behavioral fail, processor failure, timeout, unrepresentative corpus |
| Authority | Valid identity/deny, invalid identity/allow, stale policy, exact binding, approval expiry |
| Effects | Pre-attempt crash, post-attempt ambiguity, provider idempotency, compensation, irreversible unknown |
| Interruption | Context compaction, process crash, agent handoff, stale resume capsule, concurrent head advance |
| Multi-agent | Disjoint work, file conflict, semantic conflict, expired lease, worktree merge, message/task drift |
| Learning | Repeated success, repeated harmful result, repeated equivalent failure, invalidated primitive, retirement |

## Primary metrics

Use a vector, not one composite score:

- required-obligation accuracy;
- unsupported assertion count;
- scope-preservation failures;
- authority violations;
- external-effect misclassification;
- total input/output tokens;
- local compute units and wall time;
- network bytes and monetary cost;
- human attention seconds;
- number of full-artifact reads;
- time and operations to first valid action;
- recovery success after context deletion;
- reusable artifacts admitted;
- matched-task reverification cost on the next run.

## Acceptance thresholds

Safety and truth metrics are hard gates: zero authority bypass, zero UNKNOWN activation, zero unobserved external success, and zero silent scope loss in the release corpus. Economic metrics are comparative and may trade off only through an explicit Pareto report. A resource win cannot compensate for a safety or semantic failure.

## Experimental protocol

1. Freeze the corpus and environment digests.
2. Run each condition with deterministic fixture order and multiple order permutations.
3. Preserve every command, envelope, tool result, error, checkpoint, and receipt.
4. Blind the final evaluator to condition labels where possible.
5. Use mechanical acceptance tests before model-based quality review.
6. Report failures and missing evidence separately from scores.
7. Minimize each failure into a regression case.
8. Re-run after the regression artifact is admitted.
9. Measure whether the second verification is cheaper under unchanged inputs.

## Claims prohibited before evidence

Do not claim that the interface is intuitive, optimal, lossless, cheaper, safer, or self-improving merely because the schemas exist. Permitted design-stage wording is “designed to,” “target,” or “specified.” Production wording requires the matched evidence and scope above.
