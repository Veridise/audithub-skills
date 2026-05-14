# Local deployment setup

Use this guide to build realistic local OrCa deployments.

## Deployment workflow

1. Detect Foundry or Hardhat conventions from project files and existing scripts.
2. Reuse existing deployment or fixture logic when it is current and realistic.
3. Inspect constructors, initializers, roles, registries, tokens, oracles, and protocol dependencies.
4. Deploy only concrete contracts needed for the campaign targets and their required dependencies.
5. Initialize contracts with realistic values, not minimal placeholders that break ordinary flows.
6. Add mocks for external tokens, feeds, routers, bridges, keepers, or off-chain systems only when no real local dependency exists.
7. Seed useful state: roles, balances, approvals, prices, liquidity, collateral, debt, shares, and protocol configuration.

## User setup

Prefer a small set of default users with distinct roles:

- ordinary user with relevant token balances and approvals
- second ordinary user for cross-user accounting
- privileged deployer/admin only when needed for setup, not ordinary fuzzing
- keeper/liquidator/strategist role only when those flows are central

Grant roles intentionally and document why each fuzz user exists.

## OrCa-friendly deployment properties

The deployment script should:

- be deterministic under a local Anvil-style chain;
- avoid wall-clock, network, or secret dependencies;
- expose deployed addresses in the format expected by OrCa;
- avoid duplicate deployments of the same dependency;
- keep mocks simple but behaviorally plausible;
- include setup calls needed for ordinary protocol interaction.

## Debugging local setup failures

If an OrCa smoke run fails before fuzzing:

- for failed AuditHub tasks, fetch the task logs for that specific task before diagnosing the setup issue;
- run or inspect the deployment script locally;
- compare deployment ordering with constructor/initializer dependencies;
- check missing roles, invalid oracle values, unsupported cheatcodes, bad artifact paths, and mock behavior;
- inspect logs before changing fuzzing parameters.
