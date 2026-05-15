# DeFi Vanguard skills

## Purpose

Composable skills for preparing DeFi Vanguard scans, analyzing results, and building custom detectors.

The pack keeps `defi-vanguard/SKILL.md` as the root entrypoint/router and provides role-specific guidance for the main DeFi Vanguard workflows:

- `Scan Planner`: Proposes project directories to scan and detectors to enable for a DeFi Vanguard run.
- `Result Analyzer`: Validates and triages DeFi Vanguard findings for Solidity projects.
- `Custom Detector Builder`: Writes PAQL-based custom detectors from user requirements and invariants.

The DeFi Vanguard skills are designed for repository inspection and result triage workflows. The detailed role guidance lives in `references/`.

## Example Prompts

Use these as prompt starters when you want Codex to invoke a specific DeFi Vanguard role.

- `Scan Planner`
  - "Inspect this Solidity repository and tell me which directories we should scan with DeFi Vanguard and which ones should be excluded as noise."
  - "Propose a DeFi Vanguard scan plan for this protocol and recommend whether we should enable all detectors or focus on a narrower detector set."
- `Result Analyzer`
  - "Review this DeFi Vanguard output and tell me which findings look like real vulnerabilities versus spurious warnings."
  - "Analyze these DeFi Vanguard results for access-control issues and summarize the valid findings in severity order."
- `Custom Detector Builder`
  - "Write a PAQL detector for this invariant: only the protocol admin should be able to change fee configuration."
  - "Help me build a custom DeFi Vanguard detector that flags public functions capable of moving funds without access control."

## Authors

- Kostas Ferles
- Ajinkya Rajput
