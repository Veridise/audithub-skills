---
name: audithub-orca-local-deployment-builder
description: Build or update realistic local deployment scripts for OrCa fuzzing campaigns. Use when live-state fuzzing is unavailable or unsuitable, when a Foundry or Hardhat protocol needs an OrCa deployment script, or when setup needs mocks, initialized contracts, roles, balances, approvals, liquidity, oracle values, or default fuzz users.
---

# OrCa local deployment builder

## Overview

Create local deployments that let OrCa exercise realistic protocol behavior instead of failing on missing initialization or unrealistic external dependencies.

## Required reference

Read `../references/local-deployment.md` and `../references/campaign-state-and-autonomy.md`.

## Sub-agent use

Use a sub-agent when deployment setup requires reading many fixtures, tests, constructors, mocks, or external dependency flows. As a delegated task, return the deployment order, required mocks, seeded state, users, changed files, unresolved risks, and validation command/run recommendation. This work can run in parallel with hint writing, property discovery, or target review if it owns only deployment artifacts and setup notes.

## Workflow

1. Detect whether the project is Foundry or Hardhat. If neither is present, explain the blocker.
2. Inspect existing deployment scripts, fixtures, tests, constructor arguments, initializers, roles, tokens, oracle dependencies, and registries.
3. Build one deployment path that deploys the campaign targets and required dependencies once.
4. Add mocks only for missing external systems and keep them behaviorally plausible.
5. Seed users, balances, approvals, roles, oracle values, liquidity, collateral, debt, shares, and other state needed for ordinary flows.
6. Record the deployment script path, deployed target names, users, and setup assumptions in `orca_config/campaign.json` when writing artifacts.

## Output

If asked to write files, place the script in the framework-appropriate script/deploy area and keep OrCa campaign metadata under `orca_config/`. If returning only a design, include the exact deployment order, mocks, users, seeded state, and unresolved risks.

Do not deploy abstract contracts or interfaces. Do not grant ordinary fuzz users broad admin access unless that is the behavior being tested and the campaign notes explain why.
