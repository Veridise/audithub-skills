# Target selection

Use this guide when selecting OrCa fuzzing targets or deciding between live-state and local deployment.

## Selection workflow

1. Honor explicit user or client target lists first.
2. If targets are open-ended, inspect contracts, tests, deployment scripts, docs, and protocol architecture.
3. Prioritize contracts where funds directly enter, exit, move, settle, liquidate, swap, borrow, lend, stake, unstake, bridge, mint, burn, or redeem.
4. Include contracts users interact with directly and contracts required to make those interactions meaningful.
5. Add administrative contracts only when they affect normal user flows, protocol accounting, upgrade safety, permissions, or pricing.
6. Exclude interfaces, abstract contracts, pure libraries, test-only mocks, and dead deployments unless they are required by wrappers or helpers.

## Common high-value targets

- Vaults, pools, markets, routers, gateways, staking contracts, escrow contracts, bridges, settlement contracts, auction/liquidation contracts, strategy contracts, and managers that hold or transfer funds.
- Token contracts when they are custom, rebasing, fee-on-transfer, pausable, upgradeable, permit-enabled, or tightly coupled to accounting.
- Oracles and price adapters when user actions depend on price, collateralization, or exchange rates.
- Access-control and registry contracts when they gate critical flows or route to live implementations.

## Mode decision

Prefer live-state fuzzing when:

- the relevant contracts are deployed and up to date on mainnet or a testnet;
- verified addresses, implementation ABIs, and a suitable chain/block are available;
- realistic state is hard to reproduce locally.

Prefer local deployment when:

- live deployments are stale, unavailable, private, or on unsupported networks;
- the campaign needs custom mocks, roles, balances, approvals, or oracle states;
- tests/deploy scripts reveal a reliable local initialization path.

Default to the latest block for live-state fuzzing unless the user wants historical benchmarking or a specific incident state.

## Output

Return or update a target set with:

- contract name and source path
- reason for inclusion or exclusion
- user-facing functions worth fuzzing
- dependencies needed for realistic execution
- recommended mode and any unresolved setup requirements
