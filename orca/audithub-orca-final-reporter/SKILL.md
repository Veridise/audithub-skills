---
name: audithub-orca-final-reporter
description: Summarize final OrCa campaign results for Solidity protocols. Use after long OrCa runs or campaign completion to report confirmed findings, counterexample status, interesting call_metrics.json metrics, fuzzing efficiency, coverage gaps, residual risks, and recommended follow-up.
---

# OrCa final reporter

## Overview

Produce the closing campaign summary: what was fuzzed, how well it ran, what was found, and what remains uncertain.

## References

Use `../references/call-metrics-and-tuning.md`, `../references/specs-and-counterexamples.md`, and campaign state from `../references/campaign-state-and-autonomy.md`.

## Sub-agent use

Use sub-agents for evidence gathering when the campaign has many runs, large metrics files, or multiple counterexample analyses. Delegate bounded summaries such as metrics progression, spec validation status, tuning history, or counterexample classification rollups. The final reporter should integrate those compact summaries into one evidence-based report without importing every raw artifact into context.

## Workflow

1. Read campaign targets, mode, deployment setup, specs, hints, run ledger, final `call_metrics.json`, and counterexample analyses.
2. Summarize run duration, run count, timeout progression, target contracts, specs, hints, users, and major tuning changes.
3. If counterexamples exist, summarize their classifications and link to PoC/write-up status.
4. Report every violation that was found, even if it is ultimately classified as intended behavior, a false positive, a bad spec, or an inconclusive signal.
5. Explain each violation in context so the reader can distinguish real bugs from intended behavior, incomplete specifications, or other non-bug outcomes.
6. If no counterexamples exist, summarize evidence of useful fuzzing: successful calls, important functions exercised, hint effectiveness, and residual gaps.
7. Identify inefficiencies found only in long runs and recommend whether to reopen tuning.
8. Include residual risk and limitations without overstating assurance.

## Output

Return a concise report with:

- campaign scope and setup
- run summary
- findings and counterexample status
- interesting metrics
- coverage gaps and residual risk
- follow-up recommendations

Keep the report evidence-based. Do not claim absence of bugs; say no counterexamples were found for the checked specs under the campaign setup and run duration. When violations exist, include them all and clearly label whether each one looks like a real bug, intended behavior, a spec issue, or an inconclusive signal.
