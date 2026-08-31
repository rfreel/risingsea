# Rising Sea — Current System Specification

Status: `TARGET`

## Objective

Minimize expected future inference cost while constraining unsafe false activation, activation from UNKNOWN, stale activation, and authority bypass to zero within the declared operating model.

## Synthetic system

Rising Sea is a model-based epistemic control system with a learning compiler.

```text
canonical history
    ↓
semantic state
    ↓
proof state
    ↓
decision frontier
    ↓
work graph
    ↓
action model
    ↓
execution state
    ↓
procedural substrate
    ↓
agent operating plane
```

Upper layers are projections of lower layers. They do not acquire independent authority.

## Core semantic operators

### RESIDUALIZE

Given a finite obligation set, partition it into:

- mechanically entailed;
- mechanically contradicted;
- unresolved.

Only unresolved obligations may reach generative inference.

### DISTINGUISH

Find the cheapest authorized observation that separates remaining applicability outcomes. If none is available, retain an explicit indistinguishability witness and `UNKNOWN`.

### RECONCILE

Compare intended external effect with independently observed external state and return `ACCEPTED`, `REJECTED`, `PARTIAL`, or `UNKNOWN`.

## Flywheel

```text
SOURCE CORPUS
    ↓ compile
CURRENT SPEC
    ↓ decompose
WORK PACKETS
    ↓ select
ONE READY ITEM
    ↓ execute
WITNESS
    ↓ adjudicate
RECEIPT
    ↓ compile learning
TEST / RULE / NEGATIVE MEMO / WORKFLOW / PRIMITIVE
    ↓
CHEAPER NEXT LOOP
```

## Canonical object classes

- `SourceArtifact`: imported evidence or planning material.
- `Spec`: current normative planning contract.
- `WorkPacket`: self-contained executable planning unit.
- `Receipt`: immutable evidence about an attempted work packet.
- `MemoryItem`: reusable procedural rule, anti-pattern, or negative memo derived from evidence.
- `GeneratedProjection`: rebuildable triage/index/frontier view.

## WorkPacket minimum contract

Every packet must contain:

- stable `id`;
- `title`;
- `status`;
- objective;
- dependencies;
- referenced specs;
- required inputs;
- expected outputs;
- acceptance criteria;
- strongest falsifier;
- authority ceiling;
- expected accretion;
- exact next command or action when executable.

A worker should not need to reread the original planning corpus to execute a packet.

## Completion contract

A work packet closes only when:

```text
work performed
+ acceptance witness
+ verification receipt
+ status transition
+ accretion delta or explicit no_accretion_reason
```

## Learning contract

Repeated observations may compile into deterministic substrate only through evidence-bearing promotion.

Examples:

- repeated bug → regression test or static rule;
- repeated review finding → deterministic gate;
- repeated refutation → negative memo;
- repeated successful procedure → workflow candidate;
- repeated harmful procedure → anti-pattern or deny rule.

Prose learning alone does not close a recurring failure mode.

## Current implementation boundary

This repository currently establishes the planning flywheel and its machine-readable control surfaces. It does not yet establish a production Rising Sea runtime.
