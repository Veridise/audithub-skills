---
name: security-invariant-discoverer
description: Discover security-relevant invariants for smart-contract protocols. Use when the agent is asked to read Solidity, EVM, DeFi, token, vault, bridge, governance, staking, liquidation, oracle, or protocol code and produce a complete list of invariants whose violation is a viable attack surface causing loss, theft, denial of service, privilege escalation, accounting corruption, unfair value extraction, or harm to users/protocols. Also use when asked to improve, audit, or generalize invariant lists for fuzzing, formal verification, specs, or security review without writing exploits.
---

# Security Invariant Discoverer

## Goal

Produce an English-language list of attack-relevant invariants. Include only invariants whose violation can plausibly harm users or the protocol. Do not write exploit code or proof-of-concept transactions unless the user separately asks.

## Required Reference

Read `references/invariant-families.md` before drafting the invariant list.

## Workflow

1. Inspect first-party contracts before dependencies. Identify assets, accounting units, actors, trusted roles, external integrations, lifecycle states, and value flows.
2. Read tests, docs, interfaces, deployment scripts, comments, and known issue notes when available. Treat tests as evidence of intended behavior, not as a complete spec.
3. Enumerate every externally reachable path that can move value, mint/burn/transfer accounting units, change configuration, update oracle/state, execute callbacks/hooks, or cross a trust boundary.
4. For every path, ask: “If this rule is false, who can profit, who loses funds/rights, what can be frozen, or what accounting becomes corrupted?”
5. Use the required reference as a checklist. Add project-specific invariants beyond the checklist when code suggests them.
6. Prefer observable properties over implementation mirrors: balances, total supply, reserves, debt, collateral, ownership, allowances, roles, emitted state changes, oracle values, liquidation results, claim state, and external token balances.
7. Separate assumptions about trusted dependencies from invariants enforced by this protocol.
8. Do not stop at generic solvency/access-control invariants. Look for width casts, rounding asymmetry, stale caches, partial-state updates, callbacks, malformed arrays, unchecked return values, external accounting drift, and nonstandard token behavior.

## Output Format

Group invariants by security theme. For each invariant include:

- **Invariant:** concise statement of what must always hold or what a successful action must preserve.
- **Attack surface if violated:** concrete harm class, such as fund loss, free mint, underburn, locked funds, unfair liquidation, unauthorized claim, griefing, or accounting corruption.
- **Relevant code:** contracts/functions or modules involved.
- **Observables:** values or effects that demonstrate the invariant.
- **Notes:** assumptions, rounding tolerance, helper/ghost-state needs, or cases where a stronger/weaker formal spec may be required.

End with a short **Highest-Risk Invariants** section listing the invariants most likely to expose real bugs in this codebase.

## Quality Bar

- Include action-specific invariants, not only steady-state invariants.
- Include negative invariants: actions that must revert, must be impossible, or must not partially succeed.
- Include cross-function invariants: one path must not violate assumptions made by another path.
- Include per-actor isolation: one user’s operation must not steal from, dilute, freeze, or misattribute another user’s position.
- Include representation invariants: internal units, external token balances, events, allowances, snapshots, and indexes must agree.
- Exclude purely cosmetic, gas-only, or style properties unless they create a security impact.
