---
name: audithub-orca-property-discoverer
description: Discover English-language protocol properties for OrCa fuzzing. Use when a user wants real specifications after setup tuning, asks what invariants or temporal properties should hold, needs code/tests/docs reviewed for OrCa properties, or wants a properties.md handoff before [V] translation.
---

# OrCa property discoverer

## Overview

Draft code-grounded English properties before writing [V] specs.

## Required reference

Read `../references/specs-and-counterexamples.md`.

## Sub-agent use

Use sub-agents for source-heavy property discovery. Split by subsystem, target contract group, or property category when possible, and ask each agent to return only English properties, observables, rationale, source references, and [V] feasibility notes. The main campaign context does not need the full code-reading trail once the English properties and caveats are captured in `orca_config/specs/properties.md`.

## Workflow

1. Inspect target contracts, tests, docs, deployment scripts, and prior findings.
2. Identify protocol assets, accounting units, actors, trust boundaries, and lifecycle states.
3. Draft English properties that express intended behavior through observable API effects where possible.
4. Group properties by accounting, access control, solvency, standards compliance, oracle assumptions, lifecycle, and emergency behavior.
5. Mark properties that may need helper contracts, ghost variables, approximations, or weaker/stronger [V] variants.
6. Write or update `orca_config/specs/properties.md` when asked to store artifacts.

## Output

For each property include title, English statement, contracts/functions involved, observables, rationale, likely [V] feasibility, and caveats.

Do not mirror implementation internals as the property itself; use code review to infer intended behavior, then express the intended protocol rule.
