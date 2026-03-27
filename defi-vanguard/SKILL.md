---
name: audithub-vanguard
description: Use for AuditHub DeFi Vanguard workflows such as preparing static analysis runs, interpreting user-provided DeFi Vanguard results, and coordinating triage for Solidity projects. Trigger when a user asks for DeFi Vanguard analysis preparation, vulnerability triage based on DeFi Vanguard output, or static analysis findings.
---

# DeFi Vanguard skill overview

Use DeFi Vanguard to prepare static analysis scans for Solidity projects and to triage results. Follow the role-specific guidance below and refer to DeFi Vanguard detector documentation in `references/`. 

## Roles and routing

- Scan Planner: Propose directories to scan and detectors to use for DeFi Vanguard.
  - See `references/vanguard-scan-planner.md`.
- Result Analyzer: Triage DeFi Vanguard outputs into a structured JSON report.
  - See `references/vanguard-result-analyzer.md`.
- Custom Detector Builder: Build definitions of custom detectors. 
  - See `references/vanguard-custom-detector-builder.md`.
  - Focus on documenation in `references/defi-vanguard-docs/custom-detectors`

## General expectations

- Use available repository inspection tools to understand contracts and findings.
- Keep outputs strict to the specified format for each role.
- Prefer concrete, code-grounded findings over speculation.

## References

Make sure to leverage documentation files under `references/defi-vanguard-docs`