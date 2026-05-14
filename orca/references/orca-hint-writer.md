# OrCa hint writer

This compatibility reference is kept for older prompts.

For new hint work, use `../audithub-orca-hint-writer/SKILL.md` and `call-metrics-and-tuning.md`.

## Current guidance

- Start from a target function, revert blocker, or `call_metrics.json` finding.
- Inspect modifiers, dependencies, required prior state, balances, approvals, and roles.
- Decide whether the blocker belongs in a hint, deployment setup, added user, helper, or blacklist.
- Keep hints broad enough to preserve fuzzing value.
- Review hint usage and failures in the next `call_metrics.json`.

Hint docs and examples live at:

- `../../veridise-docs/orca/user_guide/hints/`
- `../../orca-hints-library/library/`
