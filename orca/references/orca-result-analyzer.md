# OrCa result analyzer

This compatibility reference is kept for older prompts.

For new result work, route by artifact:

- `call_metrics.json`: `../audithub-orca-call-metrics-analyzer/SKILL.md`
- Setup tuning from metrics: `../audithub-orca-setup-tuner/SKILL.md`
- Counterexamples: `../audithub-orca-counterexample-analyzer/SKILL.md`
- Final campaign summary: `../audithub-orca-final-reporter/SKILL.md`

## Current guidance

Analyze OrCa results in layers:

1. Confirm whether the run reached fuzzing or failed during setup/configuration.
   For failed AuditHub OrCa tasks, fetch the task logs for that specific task before debugging the issue.
2. Use per-function metrics to identify poorly performing functions and blockers.
3. Review hint usage when hints exist.
4. For counterexamples, map the sequence to code and the intended English property before deciding whether it is a real bug or a bad spec.
5. For final reporting, summarize confirmed findings, interesting metrics, coverage gaps, and residual risk.

Relevant shared references:

- `call-metrics-and-tuning.md`
- `specs-and-counterexamples.md`
- `campaign-state-and-autonomy.md`
