# Specifications and counterexamples

Use this guide for English property discovery, [V] writing, [V] validation, and counterexample triage.

## Property discovery

Read protocol code, tests, docs, deployment scripts, and any known design notes. Look for properties involving:

- conservation of funds or shares;
- collateralization, solvency, and liquidation rules;
- exchange-rate and accounting monotonicity;
- access control and privilege boundaries;
- user isolation between balances, debts, positions, and allowances;
- oracle, registry, and upgrade assumptions;
- pause/emergency behavior;
- ERC standards and custom token behavior;
- fee, reward, and yield accounting.

Write English properties before [V]. Each property should say what should hold, when it should hold, and which observable protocol values demonstrate it.

## Common invariant families

Many real protocol bugs fall into a small number of recurring families. Consider whichever apply to the target contract, and add project-specific properties (oracle bounds, lifecycle/pause guards, monotonic accruals, user isolation, collateralization) on top when the code suggests them. Multiple specs from different families on the same campaign are usually better than one carefully crafted spec.

- **Fund / value conservation.** A contract holding tokens or ETH should not lose net value to ordinary callers. Useful for staking, vaults, AMMs, escrow, subsidies, treasuries, NFT auctions.
  - `vars: Token t, Custodian c`
  - `spec: []!finished(*, t.balanceOf(c) < old(t.balanceOf(c)))`
  - When a small loss is normal (DEX swap fees, withdrawal fees), use a slippage envelope: `K * new < (K - tolerance) * old`. When `old(...)` is unreliable on a live-state fork, pin the threshold to the on-chain balance at `fork_block` instead.

- **Loose access control.** Every owner-only, admin-only, or role-gated mutator. Default fuzz users are non-privileged, so a successful call from any of them is a counterexample. Add one spec per privileged function discoverable in the ABI.
  - `vars: Contract c`
  - `spec: []!finished(c.privilegedFn)`

- **AMM constant-product / reserves match balances.** Uniswap-V2-shaped pairs, custom AMMs, bonding curves.
  - `[]!finished(*, p.getReserves()[0] * p.getReserves()[1] < old(p.getReserves()[0] * p.getReserves()[1]))`
  - or `p.token0().balanceOf(address(p)) < p.getReserves()[0]` (and the analogue for token1).

- **ERC-20 transfer correctness.** When fee-on-transfer, rebasing, blacklist, or a custom `_transfer` is suspected.
  - `inv: to != sender ==> (t.balanceOf(sender) = old(t.balanceOf(sender)) - amt && t.balanceOf(to) = old(t.balanceOf(to)) + amt) over t.transfer(to, amt)`

- **ERC-721 transfer authorization.** `transferFrom(from, to, id)` requires owner, approved, operator, or self-call.
  - `[]!finished(t.transferFrom(from, to, id), from != t.ownerOf(id) || old(sender != t.getApproved(id) && !t.isApprovedForAll(from, sender) && from != sender))`

- **Pay-for-token / no-free-mint.** A buyer's token balance only grows if they actually paid.
  - `[]!finished(*, d.balanceOf(sender) > old(d.balanceOf(sender)) && balance(sender) - old(balance(sender)) < PRICE_WEI)`

These are starting points, not a checklist. Skip families that don't fit the protocol, and write properties that aren't on this list when the code motivates them.

## [V] translation

When translating English properties:

- read `../veridise-docs/orca/user_guide/v/` from the root OrCa skill directory, or `../../veridise-docs/orca/user_guide/v/` from subskill directories;
- prefer external API observations over mirroring internal implementation details;
- avoid relying on lossy storage variables when a more robust observable exists;
- for live-state campaigns, assume OrCa does not have source-level type information from on-chain data. Replace struct field names with numeric field indexes from the Solidity source, enum variant names with numeric variant indexes, and interface names in `vars` with the known deployed contract name;
- for local-deployment campaigns, do not make those live-state replacements unless validation shows they are needed;
- split one English property into multiple [V] specs when needed;
- record when the [V] spec is weaker, stronger, or only related to the English property.

Live-state mapping examples:

- if `foo` is the second field in `struct S`, write `s[1]` instead of `s.foo`;
- if `VARIANT1` is the second variant in `enum Enum`, write `1` instead of `Enum.VARIANT1`;
- if a deployed token target is named `MyToken`, write `MyToken t` in `vars` instead of `IERC20 t`.

Record the source path and mapping notes for every live-state struct field, enum variant, or interface replacement so later validation can audit the index choices.

Use examples from `../vspec-library/library/` from the root OrCa skill directory, or `../../vspec-library/library/` from subskill directories.

## Dummy spec

Use this dummy specification when OrCa requires a spec before real properties exist:

```text
vars: uint a
spec: []!finished(*, False)
```

## [V] validation

After adding specs, run a short OrCa task, usually about one minute. OrCa may not crash on invalid [V], so inspect spec-related metrics in `call_metrics.json`.

For invalid specs:

- use the reported error information;
- fix syntax, typing, binding, or unsupported expressions;
- rerun the short validation until every intended spec is valid;
- record validation status in `orca_config/specs/properties.md`.

## Counterexample triage

For each counterexample:

1. Reconstruct the sequence and map calls to source behavior.
2. Decide whether the sequence violates the intended English property or only exploits a bad [V] formulation.
3. If possible, produce a Foundry proof of concept or a precise test outline.
4. Check final state for exploitability: drained funds, unauthorized privileges, broken accounting, bad collateralization, stuck state, or unsafe external effects.
5. When uncertain, treat it as potentially real until disproven.

Write confirmed or plausible bugs with the violated property, violating sequence, consequences, and PoC evidence.
