# OrCa deployment script builder

This compatibility reference is kept for older prompts.

For new local deployment work, use `../audithub-orca-local-deployment-builder/SKILL.md` and `local-deployment.md`.

## Current guidance

- Support Foundry and Hardhat local deployments.
- Reuse existing deployment scripts or test fixtures when realistic.
- Deploy campaign targets and required dependencies once.
- Add mocks only for missing external dependencies.
- Initialize contracts, roles, balances, approvals, oracle values, liquidity, collateral, debt, and shares as needed for ordinary flows.
- Record the deployment script path and setup assumptions in `orca_config/campaign.json`.

Relevant OrCa docs live under `../../veridise-docs/orca/`, especially:

- `../../veridise-docs/orca/user_guide/orca_configuration/`
- `../../veridise-docs/orca/user_guide/advanced_usage/`
