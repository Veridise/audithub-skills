---
name: audithub-orca-campaign-orchestrator
description: Coordinate full or multi-stage AuditHub OrCa fuzzing campaigns for Solidity projects. Use when a user asks to run an autonomous OrCa campaign, plan and execute setup/tuning/spec/long-run loops, resume an OrCa campaign, or coordinate target selection, deployment setup, smoke runs, call_metrics.json analysis, tuning, [V] specs, counterexample triage, and final reporting.
---

# OrCa campaign orchestrator

## Overview

Coordinate an OrCa fuzzing campaign end to end while keeping each stage composable. Load only the subskill and reference needed for the current stage.

## Required reference

Read `../references/campaign-state-and-autonomy.md` before starting or resuming a campaign. Enforce its permission gates before every OrCa run.

## Sub-agent strategy

Use sub-agents to keep the orchestrator context small and to parallelize independent campaign work. The orchestrator owns campaign state, permission gates, run submission decisions, version checks, and final integration. Delegate bounded tasks that require large source/log/metrics/traces context, then integrate only their compact handoffs into `orca_config/campaign.json`, `orca_config/run_ledger.json`, and `orca_config/analysis/`.

Prefer sub-agents for:

- source-heavy target, property, deployment, hint, helper, and [V] binding discovery
- **ABI and proxy resolution for live-state campaigns** — web and API lookups add large amounts of context; delegate this to a sub-agent that returns only the resolved addresses, ABI paths, and proxy mapping
- `call_metrics.json` analysis, including run-to-run metric diffs
- failed AuditHub task log analysis and failure classification
- independent setup fixes after metrics analysis: hints, deployment scripts, users/roles/balances, helper contracts, target additions, and blacklist proposals
- counterexample trace triage and PoC planning
- final report evidence gathering

When multiple setup fixes are independent, run them in parallel with disjoint write ownership. For example: one agent owns `orca_config/hints/`, one owns the deployment script, and one proposes campaign users/roles or blacklist edits. If several agents need `orca_config/campaign.json`, collect patch proposals and merge them in the orchestrator. Pass each agent only the latest analysis summary, relevant source paths, and the artifact it owns.

## Workflow

1. Establish campaign state.
   - Inspect the Solidity repo, existing OrCa files, deployment scripts, docs, tests, and any `orca_config/` files.
   - Create or update `orca_config/campaign.json` and `orca_config/run_ledger.json`.
   - If the user requested autonomy, set `autonomous_campaign_requested` in the ledger.

2. Select targets and mode.
   - Use `audithub-orca-target-selector` when targets or mode are not explicit.
   - Use `audithub-orca-live-state-setup` for live-state campaigns.
   - Use `audithub-orca-local-deployment-builder` for local deployment campaigns.
   - Delegate source-heavy target/mode discovery when the repository is large; require a compact target table and unresolved setup needs.

3. Bootstrap the campaign.
   - Use `audithub-orca-smoke-run-debugger` to add the dummy spec when no real spec exists.
   - Start with short defaults, usually 60-120 seconds, and no advanced blacklists or fuzz targets unless already justified.

4. Iterate setup quality.
   - After each run, fetch `call_metrics.json` from the task artifacts, then use `audithub-orca-call-metrics-analyzer`.
   - If an AuditHub OrCa task fails, fetch that task's logs before diagnosing the failure or changing campaign inputs.
   - Use `audithub-orca-setup-tuner` for users, hints, helpers, deployment state, target additions, or blacklists.
   - Delegate large metrics and log analysis. Feed the setup tuner only normalized blockers, dominant reverts, and suggested validation metrics.
   - If metrics suggest several independent fixes, run separate sub-agents in parallel with disjoint ownership for hints, deployment changes, users/roles, helpers, target set, or blacklist candidates.
   - Repeat short runs until setup is reasonably efficient; use up to 10 minutes without asking only when the autonomy gates allow it.

5. Add real specifications.
   - Use `audithub-orca-property-discoverer` to write English properties.
   - Use `audithub-orca-v-spec-writer` to generate [V] specs and record mapping notes.
   - Delegate property discovery by subsystem or target group when source review is large.
   - Delegate [V] translation from the English properties plus the minimum source context needed for binding; do not pass the full reasoning history that produced the English property unless it affects exactness.
   - For live-state campaigns, ensure the [V] handoff records source-derived struct field indexes, enum variant indexes, and deployed contract names used in place of interfaces. Do not require those replacements for local-deployment campaigns.
   - Run short validation and repair invalid specs using spec metrics from `call_metrics.json`.

6. Preserve full ABI data in deployment JSON.
   - For every contract being fuzzed, keep the full ABI in the on-chain deployment JSON.
   - Do not “optimize” the JSON by removing functions that appear irrelevant, because later setup, proxy resolution, smoke debugging, and specification work may still need the complete interface.

7. Run and report.
   - Ask before any run over 600 seconds.
   - Ask before run 11 or later.
   - Use `audithub-orca-counterexample-analyzer` for any violations, and carry each violation forward into the final report with an explicit classification.
   - Use `audithub-orca-final-reporter` for the final summary.

## Task patience

OrCa task execution often takes longer than the configured fuzzing timeout alone. A submitted task may still be busy for at least that many seconds, and setup phases such as source fetching, deployment, and ABI extraction can add several more minutes. Do not mark a task as stalled or abandon it early solely because it has not completed yet. When checking status, prefer infrequent, backoff-based polling over repeated rapid checks.

## OrCa run policy

Before invoking AuditHub, local OrCa, or any command that starts a fuzzing run, read the ledger and apply:

- If `timeout > 600`, ask the user first.
- If `run_count >= 10`, ask the user first.
- If the user has not requested autonomous execution, ask before every run unless the current user request explicitly asks for that run.
- Record every attempted run in the ledger, including setup failures.
- For any failed AuditHub OrCa task, fetch the task logs for that specific task ID and record the relevant log-derived diagnosis in the ledger before retrying.
- After any edit to a deployment script, [V] spec, hint, on-chain deployment JSON, or other project file, a new version must be created before running. Confirm the task targets the intended version before submitting.

## Output

Keep user-facing updates concise: current stage, next run timeout, blockers, and what changed in campaign state. Do not paste large metrics files; summarize and store normalized analysis in `orca_config/analysis/`.
