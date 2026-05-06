# Call metrics and tuning

Use this guide when analyzing `call_metrics.json` and tuning an OrCa campaign.

## Function metrics

Focus first on per-function successful-call percentage. Random fuzzing is expected to revert often, but very low success rates deserve investigation.

Rough interpretation:

- 10% or higher can be acceptable for argument-sensitive functions.
- 1-10% often needs review of revert reasons and execution depth.
- Below 1% usually indicates a blocker unless the function is intentionally hard to call.
- 0% should be explained, blacklisted, or fixed through setup/hints/users/helpers.

Do not optimize success rate alone. The goal is broad, surprising protocol exercise, not perfectly scripted happy paths.

## Common blockers

- argument constraints are too complex for random generation;
- access control prevents ordinary fuzz users;
- sender lacks token/native balance;
- sender lacks token allowance;
- required state transition has not happened yet;
- oracle, registry, or external dependency is unset or unrealistic;
- prior successful calls corrupt state into an uninteresting dead zone;
- a function is administrative and not useful for normal protocol exploration.

## Revert analysis

For each low-performing function:

- rank revert messages/selectors by frequency;
- map each revert to source checks and modifiers;
- estimate how deep OrCa reaches before reverting;
- distinguish intended preconditions from setup mistakes;
- decide whether the function should be improved, blacklisted, or left as-is.

## Hint metrics

When hints are added, review hint usage in the next `call_metrics.json`.

Investigate:

- hints never selected or never valid;
- hint calls that fail frequently;
- runtime failures inside hint expressions or helper calls;
- hints that over-constrain inputs to one narrow value family.

## Tuning actions

Possible actions:

- add target contracts needed for meaningful state transitions;
- add fuzz users with relevant balances, roles, or approvals;
- add hints for hard argument constraints;
- add helper contracts/functions for complex interfaces or reusable values;
- update local deployment or auxiliary live-state setup for balances, approvals, roles, oracle values, or liquidity;
- add blacklists for functions that are reachable but harm useful exploration.

Use blacklists carefully. Good candidates are functions whose only relevant property is access control or whose successful random execution poisons the protocol state, such as setting an oracle address to an arbitrary non-oracle.

## Breadth guardrails

Flag a tuning action as too narrow when it:

- restricts a function to one hard-coded argument tuple;
- grants broad admin power to ordinary fuzz users without a specific reason;
- bypasses the protocol path that should be tested;
- makes every call follow the same scripted sequence;
- hides an important precondition instead of exercising it.
