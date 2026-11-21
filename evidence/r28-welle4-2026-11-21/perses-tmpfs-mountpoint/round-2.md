# 0428-177 / PR #1724 — exact-head closeout

- Exact PR head: `2b44beb372d77a684d9838355dc62fd97edd886f`.
- Exact hosted run: [44888485898](https://github.com/mcpdev80/baseharbor/actions/runs/44888485898), conclusion SUCCESS.
- Test: `internal/application.TestPersesRuntimeSmokeDockerIsolated`.
- Test registration/mapping: `scripts/pr-gate-coverage.json`, gate `native/docker/perses-runtime-smoke`; selection proof is enforced by `scripts/test_ci_check_routes.py` and `scripts/test_pr_gate_coverage.py`.
- Mapped CI gate: `PR · Native · native/docker/perses-runtime-smoke`, job `136798927544`, SUCCESS on Docker. `PR Selected Checks`, job `136801240628`, SUCCESS.
- The same exact run also passed Workflow policy, Trusted Plan, source format, all four CLI shards, packages, owner, build, vet, focused Python, and the selected Docker observability runtime gate. Other unselected gates were skipped by the trusted plan.
- PR #1724 merged normally (no bypass) at `2026-11-21T09:23:52Z`; merge commit `f7c4bfa22589c7be3e605ceff769ada5fec4100f`.
- Result: the Docker Perses runtime smoke now executes with the hosted-runner mount configuration and all selected required checks are green. The stacked datasource PR #1684 can now be retargeted/revalidated on `develop`.
