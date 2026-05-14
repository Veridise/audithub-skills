---
name: audithub-orca-call-metrics-analyzer
description: Analyze OrCa call_metrics.json outputs for fuzzing efficiency and blockers. Use when a user provides call_metrics.json, asks why functions revert or have low successful-call percentages, wants hint usage analysis, needs per-function metrics triage, or wants tuning hypotheses for an OrCa campaign.
---

# OrCa call metrics analyzer

## Overview

Turn OrCa metrics into a prioritized explanation of what the fuzzer can and cannot currently exercise.

## Required reference

Read `../references/call-metrics-and-tuning.md`.

## Sub-agent use

This skill is a strong default candidate for sub-agent execution because `call_metrics.json` can be large. When used as a sub-agent, return normalized analysis instead of raw metrics:

- top blockers and strategic functions
- dominant revert reasons/selectors and suspected source checks
- hint usage or hint failure issues
- functions that look healthy enough to leave alone
- concrete tuning hypotheses with expected validation metrics

For later campaign stages, save the full raw metrics to `orca_config/analysis/call_metrics_<run>.json` or another local artifact, then pass only this summary back to the orchestrator. If comparing runs, read both metrics files locally and return a compact diff of changed success rates, new blockers, resolved blockers, and hint effectiveness.

## Workflow

1. Parse `call_metrics.json`; do not rely on visual inspection when structured parsing is available.
2. Rank functions by low success rate, high revert volume, and strategic importance.
3. Review dominant revert messages/selectors and map them to source checks.
4. Identify likely blockers: arguments, access, balances, approvals, state ordering, or bad setup.
5. Review hint usage and hint failures when hints exist.
6. Store normalized analysis in `orca_config/analysis/call_metrics_<run>.json` when writing artifacts.

## Output

Report:

- top poorly performing functions and success rates
- dominant revert reasons and suspected source checks
- functions that are acceptable as-is and why
- hint usage issues
- concrete tuning hypotheses for `audithub-orca-setup-tuner`

Treat low success as a signal for investigation, not an automatic defect. Preserve fuzzing breadth in recommendations.
