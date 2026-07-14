---
name: audithub-orca-token-holder-finder
description: Fetch the top holder wallet for one or more ERC-20 contracts via the Covalent (GoldRush) `token_holders_v2` endpoint so live-state OrCa campaigns can seed real token holders into the `users` field of `config.json`. Use when a campaign needs realistic balances or approvals and the candidate user addresses are ERC-20 holders.
---

# OrCa token holder finder

## Overview

Resolve a top holder wallet address for each input contract address by querying the Covalent `token_holders_v2` endpoint at a fixed historical block. Non-ERC-20 inputs (and any other contract Covalent does not have token holder data for) surface as `null` in the result map. This skill is a thin Covalent wrapper; it does not read source, ABIs, or run any OrCa command.

## Inputs

Pass exactly three things:

- `chain` — Covalent chain slug as a string (not a numeric chain id). Common values:

  | OrCa `fork_network` | Covalent `chain`        |
  | ------------------- | ----------------------- |
  | `mainnet`           | `eth-mainnet`           |
  | `testnet`           | `eth-sepolia`           |
  | `bsc-mainnet`       | `bsc-mainnet`           |
  | `bsc-testnet`       | `bsc-testnet`           |
  | `base-mainnet`      | `base-mainnet`          |
  | `base-testnet`      | `base-sepolia`          |
  | `arbitrum-mainnet`  | `arbitrum-mainnet`      |
  | `arbitrum-testnet`  | `arbitrum-sepolia`      |

  If the campaign uses a fork network that is not in this table, derive the slug from Covalent's documented chain list before calling and record the mapping in the caller's notes.

- `block_height` — integer block to query holders at. Use **`fork_block - 1`** from the project seed so the holder snapshot is strictly before the fuzz starts. Do not pass the fork block itself or "latest"; Covalent's snapshot at the fork block can be off-by-one with the forked state OrCa sees.

- `contracts` — list of contract addresses (0x-prefixed, casing preserved).

Do not pass source, ABIs, RPC URLs, fuzz config, or anything else.

## Output

A JSON map from input contract address to either:

- `{ "top_holder": "<wallet address>", "balance": "<decimal string as returned by Covalent>" }` — the wallet with the largest balance at `block_height`, or
- `null` — Covalent returned no holders (typical for non-ERC-20 contracts) or every retry failed.

Ensure that the wallet addresses are checksum addresses before returning them.

Keys must match the input casing. Every input address must appear as a key.

## API call

For each input address, issue exactly:

```text
GET https://api.covalenthq.com/v1/<chain>/tokens/<address>/token_holders_v2/
    ?block-height=<block_height>
    &key=<GOLDRUSH_API_KEY>
```

- Read `GOLDRUSH_API_KEY` from environment. If not set, source `~/Projects/Veridise/mcp-servers/src/ah/.env` once before the first call.
- Covalent may return more items than needed — that is fine, the top holder is always `data.items[0]`.
- One HTTP request per address. Sleep between requests only when the previous call rate-limited.

## Response handling

The Covalent response is shaped:

```json
{ "data": { "items": [...], "pagination": {...}, ... },
  "error": false, "error_message": null, "error_code": null }
```

Decode each response and branch on:

- `error == false` and `data.items` is a non-empty list: set `top_holder = data.items[0].address` and `balance = data.items[0].balance`. The first item is the largest holder at `block_height` because Covalent sorts the response by balance descending.

- `error == false` and `data.items` is an empty list: record `null` for that address. This is the canonical "not an ERC-20" / "no holders at this block" response. Do not retry.

- `error == true` and the response indicates rate limiting or a transient backend issue (HTTP 429, HTTP 5xx, `error_code` in `{ 429, 500, 502, 503, 504 }`, or `error_message` containing "rate limit", "throttle", "timeout", or "temporarily unavailable"): wait ~2 seconds and retry. Use exponential backoff up to 4 attempts, then record `null` for that address and continue with the next one.

- `error == true` for any other reason (HTTP 4xx other than 429, `error_code` 401/403, malformed address, unknown chain, etc.): stop and report the failure to the caller. These indicate a misconfigured input (wrong `chain`, missing key, invalid block) and should not be silently turned into `null`, because they would otherwise hide a setup bug from the caller.

Treat the rate-limit / transient-error branch as the only retryable case. Do not pattern-match further into `error_message`.

## Sub-agent use

Invoke this skill from a sub-agent so the main agent's context is not polluted with raw API response bodies. The sub-agent should receive only `chain`, `block_height`, and the address list, and should return only the result map plus a one-line note per address whose retries were exhausted. Do not return raw Covalent JSON to the caller.

## Consuming the result

The caller patches `config.json` so each non-`null` `top_holder` becomes a key in the `users` map with the all-zero private key:

```json
"users": {
    "<top_holder_address>": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
```

The all-zero private key is the convention used by other live-state benchmarks (see `audithub-orca-live-state-setup`) to mark an address that OrCa should impersonate via the forked state rather than actually sign for.


## Output checks

Before handing back to the caller, verify:

- every input address appears as a key in the output map;
- each non-`null` value has both `top_holder` and `balance` populated;
- `top_holder` values are 0x-prefixed 20-byte hex addresses;
- `balance` values are decimal strings, not numbers (Covalent returns very large integers as JSON strings);
- raw API JSON is not included in the returned payload.
