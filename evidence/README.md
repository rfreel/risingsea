# Evidence

Evidence closes claims; prose does not.

## Receipt rule

Every completed work packet must have a receipt at:

```text
evidence/receipts/<work-id>.json
```

A receipt should bind:

- work packet ID;
- exact inputs or source refs;
- verification performed;
- observed outputs;
- claim status (`PASS | FAIL | UNKNOWN`);
- produced artifacts;
- accretion delta or `no_accretion_reason`;
- unresolved limitations.

A receipt proves only what its witness establishes. It does not imply promotion, authorization, external execution, or global validity unless those are separately evidenced.
