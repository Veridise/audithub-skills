# Live-state setup

Use this guide to prepare OrCa live-state campaign inputs.

## Required inputs

Collect:

- chain/network identifier
- fork block number
- target contract addresses
- target display names
- ABIs for callable contracts
- implementation addresses and implementation ABIs for proxy targets
- optional users only when the campaign has a concrete reason to include them

Default to the most recent safe block unless the user requested a historical block. If current chain data is needed, fetch it from a reliable explorer or RPC source and cite the source in the campaign notes.

## Proxy handling

For each address, check whether it is a proxy before saving the ABI:

- EIP-1967 transparent/UUPS proxy implementation slot
- beacon proxy beacon and implementation
- minimal proxy clone target
- explorer "read as proxy" metadata
- project deployment manifests

Use the proxy address as the live target address, but use the implementation ABI for callable functions. Record both proxy and implementation addresses in `orca_config/campaign.json`.

## On-chain deployment JSON checks

Before a smoke run, verify:

- every target address is checksummed and on the selected chain;
- every ABI is an array or valid artifact containing an ABI array;
- proxy targets use implementation ABI, not proxy admin ABI;
- names are unique and match the campaign target names;
- fork block is an integer and not in the future;
- no required dependency address is missing;
- optional users are valid addresses and not privileged unless intentionally selected.

## Initial user policy

Start without special fuzz users unless the target relies on known balances, roles, or approvals. Add users later when metrics show access control, balance, or approval bottlenecks.

## Explorer API patterns

**Always prefer JSON API endpoints over opening HTML explorer pages.** Each HTML page visit adds thousands of tokens to context; a targeted API call adds tens of tokens. For Etherscan-compatible explorers, use the v2 API:

```text
https://api.etherscan.io/v2/api?chainid=<ID>&module=<module>&action=<action>&...&apikey=<key>
```

Common chain IDs: `1` (Ethereum mainnet), `8453` (Base), `42161` (Arbitrum One), `10` (Optimism), `137` (Polygon).

**ABI for a non-proxy contract:**

```text
module=contract&action=getabi&address=<addr>
```

Returns a JSON string of the ABI array.

**Source code and proxy detection:**

```text
module=contract&action=getsourcecode&address=<addr>
```

Returns metadata including `Implementation` (non-empty when Etherscan detects a proxy). Use this as the first proxy check before any slot-level inspection.

**Proxy implementation at a historical block** (single call — do not open multiple HTML pages):

```text
module=logs&action=getLogs&fromBlock=0&toBlock=<fork_block>&address=<proxy_addr>
  &topic0=0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b
  &page=1&offset=1000
```

The topic is `Upgraded(address)`. Take the last entry's `data` or `topics[1]` field (address-padded to 32 bytes) as the implementation address at that block. If the result is empty, no upgrade event existed before the fork block; the original constructor implementation applies.

**Contract creation info** (find deployer and tx hash):

```text
module=contract&action=getcontractcreation&contractaddresses=<addr>
```

If an API key is not available, note the missing key and stop rather than falling back to HTML page visits.
