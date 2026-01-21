---
name: audithub-orca
description: Use for AuditHub OrCa agent workflows such as planning fuzzing campaigns, writing [V] specifications, authoring OrCa hints, generating deployment scripts, and triaging user-provided OrCa results for Solidity projects. Trigger when a user asks for OrCa campaign preparation, OrCa specs/hints, deployment scripts, or OrCa result analysis.
---

# OrCa skill overview

Use OrCa to plan fuzzing campaigns for Solidity projects and to produce OrCa artifacts (hints, [V] specs, deployment scripts) plus results triage. Follow the role-specific guidance below and refer to the OrCa documentation in `references/` (hint language, [V] language, deployment tips, and general OrCa usage).

## Roles and routing

- Fuzzing campaign planner: Build a fuzzing campaign definition and return it in the required format.
  - See `references/orca-fuzzing-campaign-planner.md`.
- V Spec Writer: Convert properties into [V] specs.
  - See `references/orca-v-spec-writer.md` and OrCa [V] language docs in `references/`.
- Hint Writer: Convert conditions into OrCa hints.
  - See `references/orca-hint-writer.md` and OrCa hint language docs in `references/`.
- Deployment Script Builder: Create Foundry or Hardhat deployment scripts for OrCa campaigns.
  - See `references/orca-deployment-script-builder.md` and OrCa deployment docs in `references/`.
- Result Analyzer: Triage OrCa outputs into a structured JSON report.
  - See `references/orca-result-analyzer.md`.

## Fuzzing campaign elements

A fuzzing campaign consists of these elements:

- Specifications: A list of [V] spec files that define the properties to fuzz.
- Hints: A list of OrCa hint files that guide fuzzing inputs and sequences.
- Deployment script: A path to a deployment script that sets up the target contracts for fuzzing.
- OrCa parameters: Parameters that control the fuzzing run, including:
  - `timeout`: Seconds to run the campaign.
  - `reentrancy_checking`: Set true only to detect reentrancy exploits.
  - `fuzz_pure`: Set true only to fuzz pure/view functions.
  - `fuzz_targets`: Contract names to focus fuzzing on (optional).
  - `fuzzing_blacklist`: Functions to exclude from fuzzing (optional).
  - `fork_network`: Fork network identifier (set only if provided by user).
  - `fork_block_number`: Fork block number (set only if provided by user).

## General expectations

- Use available repository inspection tools to understand contracts, dependencies, and call flows.
- Keep outputs strict to the specified format for each role.
- Prefer concrete, code-grounded findings over speculation.

## References
Make sure to always inspect all files under `references/orca-docs/user_guide/advanced_usage/`.
