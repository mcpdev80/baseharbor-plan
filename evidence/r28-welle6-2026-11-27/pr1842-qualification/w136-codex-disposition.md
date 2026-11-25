# Independent Codex disposition — PR #1842 (ready evidence reconciliation)

- PR: https://github.com/mcpdev80/baseharbor/pull/1842
- Exact reviewed head: `317d2f2593336a4e4dddfa7f4d304bc034ee5515`
- Base at run time: `a87da7d179e08d43e8987885c38ab459ff1d887d`
- Current develop after #1832 merge: `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`
- Owner lane and commit author: `w177-0428-284-demo-pin-1812` (exact match)
- Actual exact diff: one line in `docs/releases/v0.4.28.demo-ref`, `b41127723e523134a1c14ee3c36cf133237162ce` -> `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`. It is not a `scripts/release-requirements.json`-only diff.

## Verdict: B — ready checks required; their success does not validate this pin

Independent inspection of `.github/workflows/ci.yml` at base `a87da7d179e08d43e8987885c38ab459ff1d887d`:

- `ci.yml:1502`: `PR Selected Checks` runs only when `github.event.pull_request.draft == false`.
- `ci.yml:529`: `PR · Native` additionally requires the trusted native impact result `required == 'true'`.
- `ci.yml:556`: this is `set -euo pipefail`, not a draft condition. The selected native command is at `ci.yml:558`, under the job condition at line 529.
- `ci.yml:1080`: `PR · Demo Pin` also requires a non-draft PR, plus runtime, integration or public-contract selection.

After the PR was marked ready, run 45606949460 attempt 2 reached terminal SUCCESS and the current `PR Selected Checks` context passed. The native impact planner succeeded but selected no native gates; native jobs and `PR · Demo Pin` remained skipped. The exact diff planner selects broad Go unit/vet/build checks for this one-file documentation pin, but no pin-specific validation. This reconciles B: ready PR checks are mandatory and now green, but they do not supply pin-use evidence. No CI workflow edit is authorized.

The pinned Demo SHA exists, is the second parent of merged Demo develop `486c48be56f996fe976e0881a63e64bb7de92eb2`, and has the same tree as that merge. Run 45570395768 is not an executed-native witness: its job list shows the HA and integration matrices skipped.

## Acceptance remains withheld: concrete validation assignment for w177 via coordinator

After #1832 merged, current BaseHarbor develop is `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`, but #1842 still has base `a87da7d179e08d43e8987885c38ab459ff1d887d` and GitHub reports `mergeState=behind`. The old head/run cannot qualify a merge against the strict up-to-date check.

1. Hop the one-file pin candidate onto develop `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`, preserving author lane and exact one-file scope.
2. On the new exact head, finish ready PR CI with `PR Selected Checks` success from Actions integration 15368.
3. Dispatch `Release · Pre-Release Validation` with `ref=<new exact PR head>`, `tag=v0.4.28`, `demo_ref=1a3c055cc0eef3f961722f12d843e33f6c1ca43e`, `only_gates=atomic/docker/guided,atomic/docker/lifecycle,atomic/podman/guided,atomic/podman/lifecycle`.
4. Require top-level terminal success and per-gate EXECUTED proof using that exact head and explicit Demo SHA; reused/skipped is nonqualifying.

The workflow dispatch exposes `ref`, `demo_ref`, and `only_gates` at `.github/workflows/pre-release.yml:2152-2179`; the workflow verifies the explicit SHA equals the candidate pin at lines 175-194 and requires current develop ancestry at lines 153-158. No code or workflow file was edited by this reviewer.
