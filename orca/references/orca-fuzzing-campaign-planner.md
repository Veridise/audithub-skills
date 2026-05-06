# OrCa fuzzing campaign planner

This compatibility reference is kept for older prompts that route through the original `audithub-orca` skill.

For new full-campaign work, use `../audithub-orca-campaign-orchestrator/SKILL.md`.

## Current routing

- Target selection and mode choice: `../audithub-orca-target-selector/SKILL.md`
- Live-state setup: `../audithub-orca-live-state-setup/SKILL.md`
- Local deployment setup: `../audithub-orca-local-deployment-builder/SKILL.md`
- Smoke runs and setup debugging: `../audithub-orca-smoke-run-debugger/SKILL.md`
- Metrics analysis and tuning: `../audithub-orca-call-metrics-analyzer/SKILL.md` and `../audithub-orca-setup-tuner/SKILL.md`
- Property discovery and [V] specs: `../audithub-orca-property-discoverer/SKILL.md` and `../audithub-orca-v-spec-writer/SKILL.md`
- Counterexamples and final reporting: `../audithub-orca-counterexample-analyzer/SKILL.md` and `../audithub-orca-final-reporter/SKILL.md`

## Public handoff files

Use `campaign-state-and-autonomy.md` for the required handoff files and permission gates:

- `orca_config/campaign.json`
- `orca_config/run_ledger.json`
- `orca_config/analysis/call_metrics_<run>.json`
- `orca_config/specs/properties.md`

Any OrCa run must enforce the autonomy rules in `campaign-state-and-autonomy.md`.
