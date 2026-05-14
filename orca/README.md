# OrCa skill pack

## Purpose

Composable skills for planning, setting up, tuning, running, and analyzing OrCa fuzzing campaigns.

The pack keeps `orca/SKILL.md` as a backward-compatible campaign orchestrator and adds independently triggerable subskills for campaign stages:

- `audithub-orca-campaign-orchestrator`: Coordinates full or multi-stage OrCa fuzzing campaigns from setup through final reporting.
- `audithub-orca-target-selector`: Selects OrCa fuzzing targets and recommends live-state or local-deployment mode.
- `audithub-orca-live-state-setup`: Prepares live-state campaign inputs for deployed Solidity contracts.
- `audithub-orca-local-deployment-builder`: Builds or updates realistic local deployment scripts for OrCa fuzzing.
- `audithub-orca-smoke-run-debugger`: Creates dummy specs, inspects smoke runs, and debugs early setup failures.
- `audithub-orca-call-metrics-analyzer`: Analyzes `call_metrics.json` for efficiency, blockers, and tuning hypotheses.
- `audithub-orca-setup-tuner`: Tunes campaign setup after metrics analysis to reduce blockers while preserving breadth.
- `audithub-orca-property-discoverer`: Discovers English-language protocol properties for OrCa fuzzing.
- `audithub-orca-v-spec-writer`: Translates English protocol properties into OrCa `[V]` specifications.
- `audithub-orca-hint-writer`: Writes OrCa hints from execution preconditions and metrics blockers.
- `audithub-orca-counterexample-analyzer`: Analyzes counterexamples and classifies real bugs versus specification issues.
- `audithub-orca-final-reporter`: Summarizes final OrCa campaign results, findings, and follow-up risks.

The OrCa skills are designed to be used with sub-agents for large-source, large-log, large-metrics, or parallel setup work. The shared handoff and delegation guidance lives in `references/campaign-state-and-autonomy.md`.

## Example Prompts

Use these as prompt starters when you want Codex to invoke a specific OrCa skill.

- `audithub-orca-live-state-setup`
  - "Help me prepare a live-state OrCa setup for this deployed protocol. I have the chain, fork block, and proxy addresses, but I need help resolving the implementation ABI and validating the on-chain deployment JSON."
  - "Build a live-state campaign input for these contracts and tell me what source, ABI, and proxy mapping details are still missing."
- `audithub-orca-local-deployment-builder`
  - "Inspect this Foundry project and draft an OrCa local deployment script that seeds the minimum realistic state for fuzzing."
  - "Update the deployment setup so the fuzz users have the right balances, approvals, and roles without over-granting admin access."
- `audithub-orca-call-metrics-analyzer`
  - "Analyze this `call_metrics.json` and tell me which functions are most blocked, why they revert, and what tuning hypotheses we should try next."
  - "Compare these two `call_metrics.json` files and summarize the success-rate changes, new blockers, and hint effectiveness."
- `audithub-orca-v-spec-writer`
  - "Turn these English protocol properties into OrCa `[V]` specs and note which ones are exact versus weaker or related."
  - "Repair these invalid `[V]` specs using the latest `call_metrics.json` errors and explain the semantic gap, if any."
- `audithub-orca-hint-writer`
  - "Write OrCa hints for the functions that are failing because of approvals, balances, or required prior state."
  - "Review these metrics blockers and suggest hints that improve execution without over-constraining the campaign."
- `audithub-orca-counterexample-analyzer`
  - "Analyze this OrCa counterexample and tell me whether it looks like a real bug, a specification issue, or intended behavior."
  - "Given this violated `[V]` spec and trace, classify the result and sketch a Foundry reproduction plan if it looks exploitable."

## Authors

- Kostas Ferles
- Benjamin Mariano
