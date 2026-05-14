---
name: audithub-orca-hint-writer
description: Write OrCa hints from function execution preconditions and metrics blockers. Use when functions have low success due to complex argument values, required state, balances, approvals, access control, or helper-derived values, or when call_metrics.json hint usage shows invalid or failing hints.
---

# OrCa hint writer

## Overview

Turn hard-to-satisfy execution preconditions into OrCa hints without over-constraining the campaign.

## Required references

Read `../references/call-metrics-and-tuning.md`. For hint language details, read the needed files under `../../veridise-docs/orca/user_guide/hints/`. For examples, use `../../orca-hints-library/library/`.

## Sub-agent use

Use a sub-agent when hint writing requires reading substantial source code or dependency logic for a narrow set of functions. Pass the metrics blocker summary, target function names, relevant source paths, and campaign mode. The sub-agent should return only hint files/snippets, the source checks they address, breadth risk, and the next metrics to inspect.

Hint writing can run in parallel with deployment, user, helper, or blacklist work as long as this agent owns only hint artifacts.

## Workflow

1. Start from a target function, a revert blocker, or metrics analysis.
2. Inspect the function, modifiers, dependencies, and required previous calls.
3. Identify preconditions involving arguments, balances, allowances, roles, ownership, existing state, oracle values, or helper-derived values.
4. Decide whether the precondition belongs in a hint, deployment setup, added user, helper, or blacklist.
5. Write concise hints and place them under `orca_config/hints/` when storing artifacts.
6. After the next run, review hint usage and failures from `call_metrics.json`.

## Guardrails

- Do not force one exact argument tuple unless this is a reproduction or benchmark.
- Do not use hints to bypass the protocol path that should be tested.
- Prefer setup changes for missing balances/approvals/roles that should exist broadly.
- Prefer helpers when a value is naturally computed by protocol logic or a complex interface.

## Output

Return hint files plus a short note for each hint: blocker addressed, expected effect, breadth risk, and validation metric to check after the next run.
