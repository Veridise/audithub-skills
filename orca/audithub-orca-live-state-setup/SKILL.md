---
name: audithub-orca-live-state-setup
description: Prepare live-state OrCa campaign inputs for deployed Solidity contracts. Use when a campaign will fuzz on-chain state, needs chain/block/address/name/ABI data, needs Etherscan or explorer ABI handling, needs proxy implementation ABI resolution, or needs on-chain deployment JSON validation.
---

# OrCa live-state setup

## Overview

Build a proxy-aware live-state deployment configuration that OrCa can fuzz from a selected chain and block.

## Required reference

Read `../references/live-state-setup.md`. Skip `../references/campaign-state-and-autonomy.md` if already loaded by the campaign orchestrator; read it only when running this skill standalone.

For the concrete OrCa configuration and on-chain deployment JSON formatting rules, also read the OrCa documentation under `../../veridise-docs/orca/user_guide/orca_configuration/`, especially `common_settings.md` for fork network/block fields, `advanced_settings.md` for fuzzing targets, and `build_system_and_deployment/debug.md` for deployment/proxy caveats. Use `../references/live-state-setup.md#on-chain-deployment-json-checks` as the skill-pack validation checklist after applying those docs.

## Sub-agent use

Use a sub-agent for proxy/ABI/address discovery or explorer-derived source review when it would add large external or source context. Return chain, block, target names, proxy-to-implementation mappings, ABI/source paths, unresolved inputs, and live-state [V] compatibility notes. Keep current block selection and network freshness explicit with concrete block numbers and dates when applicable.

When delegating, instruct the sub-agent to use explorer JSON API endpoints rather than opening HTML pages — see `../references/live-state-setup.md#explorer-api-patterns`. Each HTML page visit adds thousands of tokens to context; a targeted API call adds tens of tokens.

## ABI and proxy resolution

Use explorer JSON API endpoints, not HTML page navigation. See `../references/live-state-setup.md#explorer-api-patterns` for Etherscan-specific patterns.

When writing or validating on-chain deployment JSON, always include the full ABI for each contract being fuzzed. Do not trim the ABI down to only the functions that seem relevant, even if a smaller ABI would be sufficient for the immediate setup task.

For proxy implementation at a **historical block**: query `getLogs` for `Upgraded(address)` events (topic0 `0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b`) from block 0 to the target block (`toBlock=<fork_block>`) and take the last result. This is a single API call; do not open multiple Etherscan HTML pages to reconstruct proxy history.

## Workflow

1. Confirm target chain and block. Use the latest block by default only when current chain data has been fetched or supplied.
2. Gather addresses, display names, and source/ABI data for every target.
3. Detect proxies and resolve implementation ABIs while keeping the proxy address as the fuzzed address.
4. Format and validate the on-chain deployment JSON against the OrCa documentation listed above before any smoke run.
5. Record source paths for targets when available, because live-state [V] specs may need Solidity source to map struct fields and enum variants to numeric indexes.
6. Record live-state details in `orca_config/campaign.json` when writing artifacts.
7. Leave special fuzz users empty unless balances, roles, or approvals justify adding them.

## [V] spec compatibility

Live-state OrCa does not have source-level type information from on-chain data. When handing off to `audithub-orca-v-spec-writer`, include enough source context to replace struct field names with numeric field indexes, enum variant names with numeric variant indexes, and interface-typed `vars` entries with the known deployed contract names. These replacements are specific to live-state campaigns and are not required merely because a local deployment campaign exists.

## Output

Return or write:

- chain and fork block
- target address/name/ABI entries
- proxy and implementation address mapping
- ABI source notes
- validation issues and fixes

If live data must be fetched and network access is unavailable, stop with a precise list of missing chain/block/address/ABI inputs.
