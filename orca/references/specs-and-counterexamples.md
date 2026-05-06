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
