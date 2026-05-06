# OrCa skill pack

## Purpose

Composable skills for planning, setting up, tuning, running, and analyzing OrCa fuzzing campaigns.

The pack keeps `orca/SKILL.md` as a backward-compatible campaign orchestrator and adds independently triggerable subskills for campaign stages:

- `audithub-orca-campaign-orchestrator`
- `audithub-orca-target-selector`
- `audithub-orca-live-state-setup`
- `audithub-orca-local-deployment-builder`
- `audithub-orca-smoke-run-debugger`
- `audithub-orca-call-metrics-analyzer`
- `audithub-orca-setup-tuner`
- `audithub-orca-property-discoverer`
- `audithub-orca-v-spec-writer`
- `audithub-orca-hint-writer`
- `audithub-orca-counterexample-analyzer`
- `audithub-orca-final-reporter`

The OrCa skills are designed to be used with sub-agents for large-source, large-log, large-metrics, or parallel setup work. The shared handoff and delegation guidance lives in `references/campaign-state-and-autonomy.md`.

## Authors

- Kostas Ferles
