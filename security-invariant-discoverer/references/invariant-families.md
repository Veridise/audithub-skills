# Attack-Relevant Invariant Families

Use this as a checklist, not a substitute for reading the code. Add only invariants with plausible security harm if violated.

## Value Conservation and Solvency

- Contract-held assets, reserves, collateral, escrow, or vault assets must not decrease except through authorized withdrawals, redemptions, liquidations, fees, claims, or governance actions.
- Total liabilities must not exceed assets under the protocol’s solvency model.
- User withdrawals/redemptions must be proportional to ownership and must not let early users drain assets owed to later users.
- Fees, yield, rewards, subsidies, bad debt, and insurance funds must be accounted separately from user principal when the protocol relies on that separation.
- Donations or direct token transfers must not manipulate exchange rates, reserves, collateral ratios, debt shares, or claimable amounts unless explicitly intended.

## Mint/Burn/Transfer Accounting

- Every mint, burn, and transfer must change all accounting representations by the same amount: balances, total supply, shares, debt, indexes, snapshots, voting weight, events, and allowances where applicable.
- No path may mint claimable value without equivalent payment, collateral, debt, burned shares, or authorized reward emission.
- No path may burn or transfer less than the amount charged, requested, emitted, or used for allowance checks.
- Supply caps, per-account caps, position limits, and storage-width limits must apply to every mint or balance-increasing path.
- Casts between integer widths must either be proven safe or guarded. A larger external amount must never be truncated into a smaller internal amount.

## Rounding, Precision, and Exchange Rates

- Rounding direction must favor protocol solvency and prevent free value across deposit/withdraw, mint/redeem, borrow/repay, stake/unstake, and swap paths.
- Repeated small operations must not accumulate value extraction beyond intended tolerance.
- Exchange rates, indexes, accumulators, and share prices must not be manipulable by direct transfers, empty-market first deposits, flash-loan balances, stale cached values, or temporary reserve changes.
- Zero-supply, zero-liquidity, zero-debt, and dust states must reset or initialize safely.
- Decimal normalization between tokens, price feeds, and accounting units must be consistent and bounded.

## Access Control and Privilege Boundaries

- Admin-only, owner-only, role-gated, keeper-only, claimer-only, bridge-only, oracle-only, hook-only, or pair-only functions must be unreachable by ordinary callers.
- Privileged configuration changes must not bypass caps, solvency, timelocks, initialization rules, role separation, or pending/accepted ownership flows.
- Revoking or changing privileged addresses must revoke stale approvals and stale authority where the old address could still act.
- Emergency or pause controls must block the intended risky actions without freezing required exits unless that is explicitly part of the design.
- Initialization must happen exactly once, with nonzero and mutually consistent critical addresses.

## User Isolation and Authorization

- One user’s operation must not change another user’s balance, debt, collateral, rewards, claim state, delegate state, allowances, nonce, or position except through authorized transfer/liquidation/socialized-loss rules.
- `transferFrom`, delegated withdrawal, permit, operator approval, claim-on-behalf, and callback-mediated actions must spend the correct allowance/authorization and only for the authorized amount.
- Replays across chains, domains, nonces, deadlines, token ids, permit types, or signature schemes must be impossible.
- Arrays and batch inputs must be length-consistent, duplicate-safe where needed, and atomic on malformed input.

## External Calls, Hooks, and Reentrancy

- State must be safe before and after external calls to tokens, vaults, routers, hooks, receivers, or arbitrary callbacks.
- Reentrancy must not bypass limits, double-claim rewards, double-withdraw assets, observe inconsistent accounting, or reorder accounting updates for profit.
- Hook return values must be validated before they redirect value, change recipients, or influence accounting.
- Callback failures must not leave partial state unless the design explicitly supports partial success safely.
- External call targets must be authenticated when the protocol assumes a specific counterparty.

## Oracle, Pricing, and Time

- Oracle prices must be fresh, positive, correctly scaled, and from the intended base/quote orientation before being used for collateral, liquidation, swaps, mints, or fees.
- Stale, paused, sequencer-down, incomplete-round, or out-of-bounds oracle data must not authorize value-moving actions.
- Time-dependent windows, draw periods, epochs, vesting, cooldowns, deadlines, and rate limits must be monotonic and cannot be skipped or replayed.
- Cached rates and snapshots must be updated before use when stale state changes user value.

## Liquidation, Auctions, and AMMs

- Liquidations must only occur for eligible unsafe positions and must not seize more collateral or repay less debt than allowed.
- Liquidation discounts, penalties, close factors, and bad-debt handling must preserve solvency and user priority rules.
- AMM reserves, pool balances, and invariant calculations must match actual token balances or explicitly account for deltas.
- Swaps, auctions, and liquidations must enforce token identity, slippage, recipient, deadline, and amount bounds.
- Fee-on-transfer, rebasing, or nonstandard tokens must be rejected or explicitly accounted for.

## Rewards, Claims, and Distribution

- Rewards/prizes/airdrops/fees must not be claimable more than once for the same entitlement.
- Claimable amounts must correspond to eligible balances, time weights, snapshots, proofs, or contribution records.
- Updating reward indexes or distribution state must not steal accrued rewards from users who have not interacted.
- Fee recipients and reward recipients must not receive more than the configured share.
- Changing reward parameters must not retroactively corrupt already accrued entitlements unless explicitly governed.

## Lifecycle, Upgrade, and Registry Integrity

- Deployment/factory registries must reflect only successfully deployed/initialized instances.
- Upgrades must preserve storage layout, roles, assets, accounting units, and initialization status.
- Registries, factories, module lists, markets, vaults, routes, and adapters must not accept duplicate, incompatible, or malicious entries when later logic assumes uniqueness or compatibility.
- Closed, migrated, deprecated, paused, or settled states must prevent new unsafe actions while preserving intended exits and claims.

## Cross-Chain and Bridging

- Messages must be authenticated by the expected bridge, chain/domain, sender, nonce, and replay-protection mechanism.
- Minted wrapped assets or credited balances must correspond to locked/burned assets on the source side under the bridge’s trust model.
- Failed, retried, or out-of-order messages must not double-credit, double-release, or permanently lock funds.

## Standards and Token Compatibility

- ERC20/ERC721/ERC1155/ERC4626/ERC2612 behavior must match the standard where integrators rely on it.
- Events must match actual state transitions when off-chain systems, indexers, or claim logic rely on them.
- Return values and safe-transfer semantics must be handled for missing-return, false-return, reverting, fee-on-transfer, rebasing, blocklisted, pausable, hook-enabled, and high-decimal tokens.
- Zero-address, self-transfer, self-approval, dust, max-uint, and boundary-value behavior must be safe.

## Output Discipline

For each candidate invariant, keep it only if a violation can produce at least one of:

- loss or theft of funds;
- free mint, underburn, underpayment, or over-redemption;
- insolvency, bad debt, or collateral shortfall;
- unauthorized privilege, claim, upgrade, or configuration;
- locked funds or denial of required exits;
- unfair liquidation, auction, swap, or reward distribution;
- accounting corruption across balances, supply, allowances, events, snapshots, or indexes;
- replay, double claim, duplicated credit, or stale-state extraction;
- griefing that imposes material cost or blocks protocol/user operation.
