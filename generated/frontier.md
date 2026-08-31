# Current Frontier

> GENERATED from `work/items.jsonl` by `tools/build_frontier.py`. Do not edit by hand.

## Highest-value ready item

**RS-W001B — Make registered Rising Sea corpus retrieval-complete**

Ensure every source needed for canonical-spec compilation is either vendored byte-for-byte in the repository or points to a stable independently retrievable external object with an anchored digest.

Acceptance:

- No source needed by RS-W002 remains REGISTERED_ONLY
- Every VENDORED source rehashes to the registry SHA-256
- Every EXTERNAL source has a stable independently retrievable URI and anchored digest
- Large bundle sources may be represented by retrieval-complete constituent artifacts rather than duplicated archives when the mapping is explicit
- A fresh GitHub-only agent can obtain every source required to compile current specs

Strongest falsifier: A source required by RS-W002 can only be recovered from prior chat context or an unavailable transient artifact URI.

Next action: `Vendor the current v2 semantic source set first, update source availability and repo_path, then mechanically identify any historical sources still required by RS-W002.`

## Blocked

- `RS-W002` — Compile imported corpus into canonical current specs — blocked by: RS-W001B
- `RS-W003` — Compile dependency-aware implementation work graph — blocked by: RS-W002
- `RS-W004` — Run matched cold-agent flywheel navigation benchmark — blocked by: RS-W003
