---
name: audithub-orca-target-selector
description: Select OrCa fuzzing targets and choose live-state vs local-deployment mode for Solidity protocols. Use when a user provides no explicit target list, asks which contracts to fuzz, wants critical contract selection for a bug bounty or open-ended review, or needs dependencies and mode recommendations for an OrCa campaign.
---

# OrCa target selector

## Overview

Identify the contracts that matter most for fuzzing and the dependencies needed to exercise them realistically.

## Required reference

Read `../references/target-selection.md`.

## Sub-agent use

Use a sub-agent when target selection requires broad source, test, deployment, or documentation review. For large repositories, split by package or subsystem and merge the returned target tables. Each sub-agent should classify candidates as primary target, supporting target, setup-only dependency, or excluded, and include enough rationale to prevent later stages from re-reading irrelevant code.

## Workflow

1. Inspect contracts, tests, docs, deployment scripts, and existing addresses.
2. If the user supplied targets, preserve them and identify dependencies needed for interaction.
3. If targets are open-ended, prioritize user-facing and fund-flow contracts.
4. Classify each candidate as primary target, supporting target, setup-only dependency, or excluded.
5. Recommend live-state when deployments are current and usable; otherwise recommend local deployment.
6. Update or return `orca_config/campaign.json` target and mode fields when asked to write artifacts.

## Output

Return a compact target table with contract name, path/address if known, classification, reason, key functions, required dependencies, recommended mode, and unresolved setup needs.

When excluding a tempting target, state why. This prevents later agents from re-adding irrelevant admin, interface, or setup-only contracts without new evidence.
