---
name: audithub-orca-setup-tuner
description: Tune OrCa campaign setup after metrics analysis. Use when an OrCa run has poorly performing functions, access-control/balance/approval/state blockers, failing hints, missing target contracts, or when the campaign needs users, hints, helper contracts, deployment-state changes, fuzz targets, or blacklists while preserving fuzzing breadth.
---

# OrCa setup tuner

## Overview

Convert metrics and hypotheses into concrete campaign changes without overfitting the fuzzer into a scripted happy path.

## Required reference

Read `../references/call-metrics-and-tuning.md` and `../references/campaign-state-and-autonomy.md`.

## Sub-agent use

Use sub-agents to explore or implement independent tuning paths in parallel. Give each sub-agent a compact metrics summary, the relevant source paths/functions, and clear write ownership. Good splits:

- hint writer owns `orca_config/hints/`
- deployment builder owns the local deployment script and setup assumptions
- user/role/balance seeding returns campaign user and setup-state patch proposals
- helper-contract worker owns helper contracts or helper functions
- target/blacklist reviewer returns target addition and blacklist patch proposals

Require each sub-agent to report blocker, action, breadth risk, changed files or patch proposals, and validation metric. Integrate their outputs before the next run and avoid conflicting edits to the same campaign fields.

## Workflow

1. Start from the latest `call_metrics.json` analysis and campaign state.
2. For each blocker, choose the least narrowing useful action.
3. Prefer deployment/user/setup fixes for missing state, hints for argument constraints, helper functions for complex interfaces, and blacklists for harmful admin or state-poisoning functions.
4. Document the breadth risk of every change.
5. Update campaign files or return exact edits when asked.
6. Recommend the next short run timeout, usually 60-600 seconds, and enforce gates before running.
7. Treat `fuzz_targets` as contract-level selection only; if you need to remove noisy or harmful calls inside a contract, use `fuzzing_blacklist` instead of narrowing the target to a selector-like shape.

## Task patience

When a run is submitted from this stage, remember that OrCa execution can continue for at least the configured timeout and then spend additional minutes on setup phases such as source fetching, deployment, or ABI extraction. Avoid treating the task as abandoned too early, and prefer infrequent, backoff-based status checks instead of repeated polling.

## Decision rules

- Add contracts when current targets require another contract for meaningful state changes.
- Add users when real protocol roles, balances, or approvals are blocking execution.
- Add hints when random arguments rarely satisfy meaningful preconditions.
- Add helpers when the real interface requires complex setup values or multi-step wrappers.
- Update deployment when local state is unrealistic.
- Blacklist functions whose successful execution mostly destroys useful fuzzing state or only tests already-understood access control.
- If a campaign was accidentally narrowed too far, restore breadth first and then blacklist only the harmful functions that are clearly unnecessary for the property.

## Output

For each proposed or implemented change, include blocker, action, expected effect, breadth risk, artifact path, and validation run recommendation.

Do not optimize for high success percentages by forcing a single fixed argument set unless the user explicitly wants a benchmark or reproduction.
