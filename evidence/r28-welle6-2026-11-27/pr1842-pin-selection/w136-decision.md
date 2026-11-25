# Independent Codex decision — make #1842 pin validation explicit

- PR #1842: https://github.com/mcpdev80/baseharbor/pull/1842
- Exact reviewed head: `8b172f7c5312267cfa79417f620613410468a2e2`
- Base: `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`
- Lane/commit author: `w177-0428-284-demo-pin-1812` (matches)
- Run `45611830424`: top-level SUCCESS; `PR Selected Checks` from integration 15368 SUCCESS; no `PR · Demo Pin` or named Demo-source-pin validator executed. Native gates skipped. This proves the ordinary PR selection check, not pin validation.
- Current three-file diff includes the one-line pin plus `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_coverage.py` selection changes.

## Verdict: choose the existing dispatch-era validation contract (no CI YAML change)

**Terminology:** “existing Hosted pre-release validation dispatch” means the `Release · Pre-Release Validation` `workflow_dispatch` entry in `.github/workflows/pre-release.yml`, invoked with explicit `ref=<PR head>` and `demo_ref=<pin>` inputs (Leg-B precedent style, e.g. run 45570395768). `.github/workflows/pre-release-runtime-suite.yml` is `workflow_call`-only and is not directly dispatched.

For a data-only pin PR, `ci.yml:1080` only runs `PR · Demo Pin` if runtime, integration, or public-contract selection is true. The pin-only candidate sets none, so this job cannot fire through the current predicate. The final `PR Selected Checks` can succeed while that job is skipped; do not treat its success or the local red-first tests as pin-validation evidence.

The proposed planner-only change also does not qualify itself on this PR: `ci.yml:865-869` loads `pr-gate-plan.py` and `pr-check-runner.py` from the trusted base/controller, not from the candidate head. Moreover, the trusted `scripts/pr-check-runner.py:383-393` still validates the literal `docs/releases/v0.4.27.demo-ref`, not v0.4.28. A current-head test showing that the candidate planner selects `demo-source-pin-validation` therefore does not prove that the hosted PR run executes a v0.4.28 pin check.

The minimum purpose-bound accepted path is an explicit hosted `Release · Pre-Release Validation` dispatch using the existing, trusted source-binding and runtime workflow. Its contract is inspectable:

- `.github/workflows/pre-release.yml:175-194` reads `docs/releases/${tag}.demo-ref`, validates a full SHA, and rejects an explicit `demo_ref` that differs from the file.
- `pre-release.yml:2150-2179` exposes `workflow_dispatch` inputs `tag`, `ref`, `demo_ref`, and `only_gates`.
- `pre-release.yml:721-758` passes the resolved `demo_ref` into selected Docker and Podman runtime suites.
- `.github/workflows/pre-release-runtime-suite.yml:6` distinguishes `Executed` from `Reused`; lines 204-216 fetch and check out the exact supplied Demo SHA. Reuse is not execution proof for this disposition.

## Fix-forward recipe for w177

1. Keep #1842 limited to the intended data row: revert the candidate-only `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_coverage.py` additions. Do not edit `.github/**`. Preserve `%an == w177-0428-284-demo-pin-1812`, current develop ancestry, and the one-line pin `docs/releases/v0.4.28.demo-ref` = `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`.
2. On the resulting exact data-only head, require ready PR CI terminal success, including `PR Selected Checks` from integration 15368. This is the normal source/plan check, not the pin-runtime witness.
3. Dispatch `Release · Pre-Release Validation` with `ref=<new exact PR head>`, `tag=v0.4.28`, `demo_ref=1a3c055cc0eef3f961722f12d843e33f6c1ca43e`, and `only_gates=atomic/docker/guided,atomic/docker/lifecycle,atomic/podman/guided,atomic/podman/lifecycle`.
4. Require top-level terminal SUCCESS; verify the source binding names the exact Core head and Demo SHA; require all four gate jobs to say `Executed` and finish SUCCESS. Any reused-only or skipped gate is nonqualifying. If develop advances, hop/requalify against the new tip before dispatch.

This is pin-specific qualification only. It does not replace the later #1812 full runtime-gate sequence. Run `45570395768` is not an execution precedent: its API job list shows its HA/integration gate matrices skipped. No workflow or product auth/consent change is authorized or needed for this path. No implementation or merge is performed by this reviewer.
