# OrCa [V] spec writer

This compatibility reference is kept for older prompts.

For new [V] work, use `../audithub-orca-v-spec-writer/SKILL.md` and `specs-and-counterexamples.md`.

## Current guidance

- Start from English properties in `orca_config/specs/properties.md`.
- Translate each property into one or more [V] specs.
- Prefer external API observations over implementation mirrors.
- Avoid lossy storage variables when a stable observable exists.
- For live-state campaigns, replace source-level struct fields with numeric field indexes, enum variants with numeric variant indexes, and interface names in `vars` with known deployed contract names. Do not apply those replacements solely for local-deployment campaigns.
- Record whether each [V] spec is exact, weaker, stronger, or related.
- Run a short validation task and repair invalid specs using spec-related `call_metrics.json` information.

[V] docs and examples live at:

- `../../veridise-docs/orca/user_guide/v/`
- `../../vspec-library/library/`
