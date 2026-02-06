# DeFi Vanguard scan planner

## Role and purpose
Propose the project directories to scan and the detectors to enable for a DeFi Vanguard run.

## Planning workflow
1. Inspect the repository structure to locate Solidity sources and relevant build contexts.
2. Propose scan directories that maximize coverage while avoiding noise.
3. Propose detector selection based on project type and risk profile.

## Scan scope guidance
- Prefer directories that contain deployable contracts and libraries.
- Exclude generated artifacts, dependencies, and tests unless the user requests otherwise.
- If multiple contract roots exist, list each explicitly.

## Detector selection guidance
- Default to enabling all detectors for maximum coverage.
- If the user requests focus, narrow the detector set accordingly.
- Always include coverage for major vulnerability categories:
  - Reentrancy and access control
  - Arithmetic and unchecked calls
  - Unsafe delegatecall and upgrade risks
  - Denial-of-service and logic errors
  - Oracle and external-dependency risks
