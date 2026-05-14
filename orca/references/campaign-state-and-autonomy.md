# Campaign state and autonomy

Use these files as durable handoffs between OrCa skills. Create them in the target project, not in this skill repository.

## Campaign file

`orca_config/campaign.json` records the current campaign definition.

Required top-level fields:

```json
{
  "campaign_name": "short-human-name",
  "mode": "live-state | local-deployment",
  "targets": [],
  "deployment": {},
  "specs": [],
  "hints": [],
  "users": [],
  "fuzzing_blacklist": [],
  "fuzz_targets": [],
  "orca_parameters": {
    "timeout": 60,
    "reentrancy_checking": false,
    "fuzz_pure": false
  },
  "tuning_notes": []
}
```

Target entries should include contract name, source path when known, address for live-state targets, ABI path or source, and why the target matters. Deployment entries should distinguish live-state chain/block/address inputs from local deployment script inputs.

## Run ledger

`orca_config/run_ledger.json` records every OrCa run attempt, including failed setup runs.

```json
{
  "run_count": 0,
  "autonomous_campaign_requested": false,
  "permission_checkpoints": [],
  "runs": []
}
```

Each `runs[]` entry should include run number, timeout seconds, mode, task ID or local command if available, status, start/end timestamps when known, important artifact paths, fetched log references for failed AuditHub tasks, and a short outcome summary.

## Version management

AuditHub campaigns are version-gated. Any change to a project file—deployment script, embedded [V] specification or hint, on-chain deployment JSON, or any other input file—requires creating a **new project version** before those changes can take effect in an OrCa task.

- Create a new version after every edit to project files, before starting or restarting a run.
- Before submitting a task, confirm that the version being targeted reflects the current intended changes. Running against an older version due to a missed version bump is a common mistake.

## Permission gates

Before starting any OrCa run:

- Ask the user for permission if `timeout > 600`.
- Ask the user for permission if `run_count >= 10`.
- If neither gate applies, short runs may proceed autonomously only when the user has explicitly requested an autonomous campaign or explicitly requested the run.
- Record the permission decision in `permission_checkpoints` before running.

If a user grants a long run or post-run-10 permission, treat that approval as applying only to the specific next run unless they explicitly authorize a bounded batch.

## Analysis artifacts

After a task completes, fetch the task's `call_metrics.json` from the task artifacts and save it locally.

If an AuditHub OrCa task fails, fetch the logs for that particular task ID before debugging or retrying. Use the logs to classify the failure, and record the relevant diagnosis or log reference in `orca_config/run_ledger.json`.

Normalize analysis into `orca_config/analysis/call_metrics_<run>.json` when practical. Include:

- per-function success/revert rates
- dominant revert reasons
- suspected blockers
- hint usage and hint failures
- recommended tuning actions
- actions intentionally skipped to preserve fuzzing breadth

Use `orca_config/specs/properties.md` to map English properties to generated [V] files, intentionally weakened/strengthened variants, validation results, and known spec limitations.

## Sub-agent delegation

Use sub-agents aggressively when a stage would otherwise pull large source trees, task logs, traces, or metrics files into the campaign orchestrator context. The orchestrator should keep the campaign state, permission gates, next-run decisions, and final integration locally; delegate bounded analysis or implementation tasks that can return compact handoffs.

Good delegation targets:

- source discovery for targets, protocol properties, deployment requirements, hints, helper contracts, and [V] binding details
- large `call_metrics.json` analysis, including diffing metrics between runs
- failed task log analysis and failure classification
- independent setup fixes after metrics analysis, such as hint writing, deployment-script updates, user/role seeding, helper additions, target changes, or blacklist proposals
- counterexample trace reading and PoC planning
- final report evidence gathering from ledgers, metrics, and issue artifacts

Do not ask a sub-agent to start OrCa runs unless it has the current `run_ledger.json`, the permission gates above, the target AuditHub version, and a clear instruction to record the attempted run. Prefer to keep run submission and ledger ownership in the orchestrator.

When delegating, give only the necessary inputs:

- the relevant subskill name and reference file(s)
- exact artifact paths, task IDs, source paths, or contract/function names
- the current campaign decision that should be treated as fixed
- the expected output schema or artifact path

Require compact returns:

- decisions and rationale, not raw logs or full metrics
- source references and line numbers for claims
- concrete edits or artifact paths when files were changed
- unresolved blockers and the minimum extra context needed
- next validation metric or run recommendation

For parallel work, split by write ownership. For example, one sub-agent may own `orca_config/hints/`, another a deployment script, and another a users/roles proposal. If multiple agents need to affect `orca_config/campaign.json`, have them return mergeable patch proposals for the orchestrator to apply instead of editing the file concurrently. Tell agents that other agents may be editing nearby campaign files and that they must not revert unrelated changes.
