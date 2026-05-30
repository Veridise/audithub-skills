---
name: audithub-orca-v-spec-writer
description: Translate English protocol properties into OrCa [V] specifications and validation notes. Use when a user asks for [V] specs, wants properties.md converted into OrCa specs, needs invalid [V] specs repaired from call_metrics.json spec errors, or needs weakened/strengthened/related [V] variants documented.
---

# OrCa [V] spec writer

## Overview

Convert intended protocol properties into [V] specs while preserving the mapping back to the English property.

## Preflight Checks

Before handing off or running a new [V] spec, verify the following:

- Equality uses `=` in [V], not `==`.
- Use `nulladdr` for zero-address checks; `address(0)` is rejected by the parser.
- Avoid `bytes32(0)` literals; restructure the spec to compare without the explicit cast.
- Exactly one of `spec` or `inv` is present in each file.
- Any function-argument binding is intentional and not shadowing a free variable by accident.
- The spec has a short validation path planned before it is used in a broader campaign.
- Re-run all preflight checks on cached or inherited specs before submission; do not assume they still pass.

## Required references

Read `../references/specs-and-counterexamples.md`. For language details, read only the needed files under `../../veridise-docs/orca/user_guide/v/`. For examples, use `../../vspec-library/library/`.

## Sub-agent use

Use a sub-agent for [V] translation when the English properties are already established. Pass only the English property set, selected target/source paths, campaign mode, deployed contract names for live-state campaigns, and any known struct/enum/interface mapping requirements. The translation step should not need the full reasoning history behind property discovery unless that history changes exactness or intended semantics.

For large property sets, split translation by property group or target contract. Require each sub-agent to return [V] files or exact snippets plus a mapping table with exactness, dependencies, validation status, and limitations.

## Workflow

1. Start from English properties. If none exist, use `audithub-orca-property-discoverer` first.
2. Inspect source code only enough to bind functions, events, return values, observable state, and live-state type/index mappings when needed.
3. Write one or more [V] specs per property as needed.
4. Prefer external API observations over internal implementation mirrors.
5. Avoid lossy storage variables when a more stable observable can express the property.
6. For live-state campaigns, do not use source-level type names that OrCa will not know from on-chain data:
   - Replace struct field names with numeric field indexes from the Solidity definition. For example, if `foo` is the second field of `S`, write `s[1]` instead of `s.foo`.
   - Replace enum variant names with numeric variant indexes from the Solidity definition. For example, if `VARIANT1` is the second variant of `Enum`, write `1` instead of `Enum.VARIANT1`.
   - In `vars`, use the known deployed contract name instead of an interface name. For example, write `MyToken t`, not `IERC20 t`.
   - Record the source path and struct/enum/interface mapping notes next to the spec so reviewers can verify each replacement.
7. For local-deployment campaigns, source-level struct fields, enum variants, and interfaces may be used when supported by the local project artifacts; do not apply the live-state numeric replacements unless validation shows they are required.
8. Do not introduce a fresh free variable for every function argument by default. When a property can refer to an argument directly, bind it directly in the predicate or quantifier instead of creating a separate named variable. Only add a new free variable when it is required for clarity, reuse, or the [V] syntax makes the binding explicit and necessary. One of the few common cases where a free variable is warranted, aside from a contract variable, is when you need to connect the same value across two different [V] statements or otherwise share it across separate parts of the property. For example, to state that `closeAuction` can never succeed twice for the same auction ID, you may introduce a shared `id` in `vars` and compare both calls against that same `id` in the spec.
9. Record whether each [V] spec is exact, weaker, stronger, or related.
10. Place specs under `orca_config/v_specs/` when writing artifacts and update `orca_config/specs/properties.md`.
11. After a short validation run, use spec errors from `call_metrics.json` to repair invalid specs.
12. When writing repair notes, record exactness and any known semantic gap so the next run is not blocked by the same ambiguity.

## Output

Return or write [V] files plus a mapping table: English property, [V] file, exactness, dependencies, validation status, and known limitations.

Do not silently drop an English property because exact [V] encoding is hard. Write the closest useful check and record the gap.
