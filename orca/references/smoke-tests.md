# Prompt-level smoke tests

Use these prompts to forward-test the skill pack. They are smoke tests for behavior, not executable unit tests.

## Campaign orchestrator

Prompt: "Use `audithub-orca-campaign-orchestrator` to run an autonomous OrCa campaign for this Foundry lending protocol."

Acceptance: creates/updates campaign state, delegates source-heavy/metrics/log/setup stages with compact handoffs, starts only allowed short runs, and asks before any run over 10 minutes or run 11.

## Target selector

Prompt: "Use `audithub-orca-target-selector` to choose fuzz targets in this Solidity repo. No contract list is provided."

Acceptance: prioritizes fund-flow and user-facing contracts, includes required dependencies, excludes interfaces/libraries, and recommends live-state or local mode.

## Live-state setup

Prompt: "Use `audithub-orca-live-state-setup` for these deployed proxy contracts on Ethereum."

Acceptance: records chain/block/addresses, resolves implementation ABIs for proxy targets, and validates on-chain JSON shape.

## Local deployment builder

Prompt: "Use `audithub-orca-local-deployment-builder` to create a local deployment for this protocol. It needs mocks, token minting, roles, and approvals."

Acceptance: reuses project deployment patterns, deploys dependencies once, seeds realistic state, and avoids granting broad fuzz-user privileges without reason.

## Smoke run debugger

Prompt: "Use `audithub-orca-smoke-run-debugger` to diagnose this failed first OrCa run."

Acceptance: confirms dummy spec/setup, inspects logs, separates deployment/config errors from fuzzing issues, and updates the ledger.

## Call metrics analyzer

Prompt: "Use `audithub-orca-call-metrics-analyzer` on this `call_metrics.json`; many functions have under 1% success and two hints are failing."

Acceptance: analyzes large metrics through a compact summary, ranks low-performing functions, ties revert reasons to blockers, reviews hint usage, and emits tuning hypotheses.

## Setup tuner

Prompt: "Use `audithub-orca-setup-tuner` to improve this campaign based on the latest metrics."

Acceptance: recommends or parallelizes users/hints/helpers/deployment changes/blacklists with breadth-risk notes, disjoint ownership or patch proposals, and concrete next-run parameters.

## Property discoverer

Prompt: "Use `audithub-orca-property-discoverer` to draft English OrCa properties for this lending protocol."

Acceptance: reads code/tests/docs, writes observable English properties, groups them by protocol concern, and records likely [V] feasibility.

## V spec writer

Prompt: "Use `audithub-orca-v-spec-writer` to translate these English properties into valid [V] specs."

Acceptance: maps each English property to one or more [V] specs, notes weakened/strengthened variants, writes spec paths, and plans short validation.

## Hint writer

Prompt: "Use `audithub-orca-hint-writer` to write hints for these low-success functions from the latest metrics analysis."

Acceptance: ties each hint to a concrete blocker, avoids over-narrowing inputs, writes hint paths, and names post-run metrics to check.

## Counterexample analyzer

Prompt: "Use `audithub-orca-counterexample-analyzer` to analyze these OrCa counterexamples."

Acceptance: reconstructs sequences, classifies bug vs spec issue, drafts PoC guidance, and treats uncertainty conservatively.

## Final reporter

Prompt: "Use `audithub-orca-final-reporter` to summarize this long OrCa run."

Acceptance: reports confirmed findings, no-counterexample evidence, interesting metrics, coverage gaps, and residual risk.
