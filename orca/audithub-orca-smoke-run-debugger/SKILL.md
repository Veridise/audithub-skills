---
name: audithub-orca-smoke-run-debugger
description: Create dummy OrCa specs, perform or inspect short initial OrCa smoke runs, and debug setup failures. Use when a campaign needs the universal dummy spec, a first 1-2 minute run, diagnosis of failed local deployment scripts, diagnosis of malformed on-chain deployment JSON, or run-ledger updates for early OrCa attempts.
---

# OrCa smoke run debugger

## Overview

Get the first OrCa task to run successfully before spending effort on tuning or real specs.

## Required references

Read `../references/campaign-state-and-autonomy.md` and the dummy spec section of `../references/specs-and-counterexamples.md`.

## Sub-agent use

Use a sub-agent for long task logs, verbose local deployment output, or source-heavy setup failure diagnosis. The sub-agent should classify the failure, cite the key log lines or source references, and return the smallest viable fix or next diagnostic step. Keep run submission, permission checks, AuditHub version selection, and ledger updates in the main orchestrator unless explicitly delegated with the current ledger and gates.

## Workflow

1. Ensure a placeholder spec exists when no real [V] specs exist:

```text
vars: uint a
spec: []!finished(*, False)
```

2. Use default OrCa parameters for the first task; set timeout to 60-120 seconds unless the user specified otherwise.
3. Before running, enforce the autonomy gates from `run_ledger.json`.
4. If an AuditHub OrCa task fails, fetch the task logs for that specific task before changing campaign parameters.
5. If a local run fails, inspect local logs before changing campaign parameters.
6. For local deployment failures, reproduce or inspect deployment under a local Anvil-style chain when practical.
7. For live-state failures, validate chain, block, address, proxy ABI, and on-chain deployment JSON formatting.
8. If the on-chain deployment JSON has a trimmed ABI, restore the full ABI for each fuzzed contract before retrying; never keep only the functions that seem immediately relevant.
9. Record the run attempt and log-derived diagnosis in `orca_config/run_ledger.json`.
10. Before the first run, sanity-check campaign shape: `fuzz_targets` must list contract names, not function selectors, and function-level narrowing belongs in `fuzzing_blacklist`.

## Task patience

The first OrCa task is often slow to finish. Treat it as potentially running for at least the configured timeout, plus extra minutes for task setup work such as source fetching, deployment, and ABI extraction. Do not declare it failed or stop checking too early just because the status has not changed yet. Use spaced-out status checks rather than frequent polling unless logs or task status clearly indicate failure.

## Failure classification

- `deployment`: constructor, initializer, mock, role, balance, approval, artifact, or local-chain issue.
- `onchain_config`: malformed JSON, wrong ABI, wrong chain/block, bad proxy handling, missing address.
- `orca_config`: invalid paths, missing spec, unsupported parameter, bad target name, or an empty transaction set caused by incorrect target/filter shape.
- `environment`: credentials, RPC, AuditHub task setup, dependency installation, or command availability.
- `fuzzing`: OrCa started and fuzzed but hit runtime behavior that should be analyzed through call metrics.

Do not proceed into tuning until at least one OrCa task reaches the fuzzing stage successfully.
