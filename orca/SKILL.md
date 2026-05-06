---
name: audithub-orca
description: Backward-compatible orchestrator for AuditHub OrCa fuzzing workflows. Use when a user asks for a full or multi-stage OrCa campaign, autonomous OrCa setup/run/tuning, target selection, live-state setup, local deployment setup, smoke-run debugging, call_metrics.json analysis, setup tuning, property discovery, [V] specs, hints, counterexample triage, or final OrCa reporting for Solidity projects.
---

# OrCa compatibility orchestrator

Use this root skill as a thin router for OrCa work. For focused requests, read only the matching subskill `SKILL.md` plus the shared references it names. For end-to-end requests, use `audithub-orca-campaign-orchestrator`.

OrCa tasks can be slow to settle. Treat a submitted task as potentially running for at least the configured timeout in seconds, plus extra minutes for setup stages such as source fetching, deployment, and ABI extraction. Do not give up early just because the task has not finished yet, and avoid frequent status polling; use a generous backoff unless the task has clearly failed.

## Routing

- Full or autonomous campaign: `audithub-orca-campaign-orchestrator/SKILL.md`.
- Select contracts or decide live-state vs local: `audithub-orca-target-selector/SKILL.md`.
- Prepare on-chain campaign inputs: `audithub-orca-live-state-setup/SKILL.md`.
- Build local Foundry/Hardhat deployment: `audithub-orca-local-deployment-builder/SKILL.md`.
- Create dummy spec, run short smoke task, or debug setup failures: `audithub-orca-smoke-run-debugger/SKILL.md`.
- Analyze `call_metrics.json`: `audithub-orca-call-metrics-analyzer/SKILL.md`.
- Improve setup using users, hints, helpers, deployment state, targets, or blacklists: `audithub-orca-setup-tuner/SKILL.md`.
- Discover English protocol properties: `audithub-orca-property-discoverer/SKILL.md`.
- Translate English properties to [V]: `audithub-orca-v-spec-writer/SKILL.md`.
- If a run fails on V syntax or target-shape mistakes, check the V spec writer or smoke-run debugger before tuning.
- Write OrCa hints: `audithub-orca-hint-writer/SKILL.md`.
- Triage counterexamples and PoC evidence: `audithub-orca-counterexample-analyzer/SKILL.md`.
- Summarize campaign results: `audithub-orca-final-reporter/SKILL.md`.

## Shared contract

Use the public handoff files described in `references/campaign-state-and-autonomy.md`:

- `orca_config/campaign.json`
- `orca_config/run_ledger.json`
- `orca_config/analysis/call_metrics_<run>.json`
- `orca_config/specs/properties.md`

Use the sub-agent delegation guidance in `references/campaign-state-and-autonomy.md` whenever source review, task logs, `call_metrics.json`, traces, or parallel setup changes would otherwise dominate the root context. Keep this root skill focused on routing, permission gates, campaign state, and compact handoffs.

Before starting any OrCa run, enforce these gates:

- Ask the user before any run with `timeout > 600` seconds.
- Ask the user before the 11th OrCa run or later in the same campaign.
- Short runs of 10 minutes or less may proceed autonomously only after the user has requested an autonomous campaign or explicitly requested that run.
- When an AuditHub OrCa task fails, fetch the logs for that specific task before debugging or retrying.

## Documentation paths

- OrCa docs: `../veridise-docs/orca/`
- [V] docs: `../veridise-docs/orca/user_guide/v/`
- Hint docs: `../veridise-docs/orca/user_guide/hints/`
- OrCa configuration docs: `../veridise-docs/orca/user_guide/orca_configuration/`
- Advanced triage docs: `../veridise-docs/orca/user_guide/advanced_usage/`
- [V] examples: `../vspec-library/library/`
- Hint examples: `../orca-hints-library/library/`
