---
name: audithub-orca-counterexample-analyzer
description: Analyze OrCa counterexamples and classify real bugs versus specification issues. Use when OrCa reports violated [V] specs, a user provides counterexample sequences, traces, or failing artifacts, or when a campaign needs PoC guidance, Foundry reproduction planning, exploitability assessment, and write-up material.
---

# OrCa counterexample analyzer

## Overview

Determine whether an OrCa violation is a real protocol bug, a benign or intended outcome, a bad or incomplete spec, or an inconclusive signal that needs a PoC.

## Required reference

Read the counterexample triage section of `../references/specs-and-counterexamples.md`.

## Sub-agent use

Use a sub-agent for long counterexample traces, verbose logs, or PoC planning that requires substantial source/test reading. Return a compact sequence summary, classification, exploitability reasoning, source references, PoC status, and suggested spec fix or issue write-up material. Do not return full traces unless the user explicitly asks for them.

## Workflow

1. Ingest counterexample sequence, violated spec, run metadata, logs, and relevant code.
2. Map each call to contract functions, caller, arguments, state dependencies, and expected effects.
3. Compare the violated [V] spec with the original English property.
4. Inspect final state for exploitability or security impact.
5. Attempt to produce a Foundry PoC or precise reproduction plan when project tooling supports it.
6. Classify as `bug`, `spec_issue`, `benign_expected`, or `inconclusive`.
7. Draft a concise write-up for any `bug` or `inconclusive` high-impact case.

## Classification guidance

- AuditHub marks every spec violation as "critical" by default, but that label is only a signal that the checked specification was violated, not proof of a critical bug.
- Always analyze the actual sequence and the spec text before deciding whether the violation is a real bug, intended behavior, or a spec problem.
- Treat uncertainty as potentially real until code and state evidence rules it out.
- A trivial counterexample often means the [V] spec does not state the intended English property.
- Common benign cases include reward accrual, delayed withdrawals, admin-only flows, or other intended state-dependent behavior that can look like a violation if the spec is too broad.
- A sequence ending in drained funds, unauthorized privileges, broken accounting, bad collateralization, or stuck funds should be treated as a likely bug.
- For live-state fuzzing, consider that the protocol may already be in a bad state at the fork block.

## Output

Return classification, reasoning, sequence summary, impacted property, exploitability assessment, PoC status, and suggested spec fix or issue write-up next step. If the violation turns out to be intended behavior, a false positive, or a spec gap, say so explicitly instead of downplaying the finding.
