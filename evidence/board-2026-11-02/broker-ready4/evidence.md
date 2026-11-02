# broker-ready4 — Evidence (PR B: bind runtimebroker/* to lifecycle gates)

Mission `coordinator/missions/broker-ready4.txt` scoped two small PRs:
- PR A `fix(runtime-broker): widen readiness grace` → `compose_render.go`
- PR B `ci(gate-map): bind runtimebroker paths to lifecycle gates` → `pr-gate-plan.py`

**Scope evolution:** PR #1265 (branch `work/s3-manifest`, head `27e4c23f`) already
contained both content changes AND only extended the go-test command in
`pr-gate-plan.py` — NO `internal/runtimebroker/*` file-path binding. PR #1265
stayed **fail-closed** at the gate for exactly this missing binding
(RunID 125059625061, coverage-unresolved on
`internal/runtimebroker/compose_render.go` + `broker_test.go` + `application/*`).

My task now (Coord re-scope): **PR B only** — add the missing
`internal/runtimebroker/*` file binding to `atomic/docker/lifecycle` +
`atomic/podman/lifecycle` (pattern #1262), no healthcheck part, no workflows,
then watch PRSC terminal.

## PLAN
- Inspect #1262 pattern via `gh api pulls/1262/files` (pr-gate-plan.py +23, test +59/-1).
- Confirm clean worktree at origin/develop 6624ad62, branch work/broker-ready4.
- Add `elif path.startswith('internal/runtimebroker/') and path.endswith('.go')`
  branch in `plan()` (before cmd/baha cli-unresolved catch-all), binding both
  existing atomic lifecycle gates. require(CODE_CHECKS)+require(CLI_CHECKS).
- Add planner test asserting resolved + gates=[atomic/docker/lifecycle,
  atomic/podman/lifecycle] + broad_required False.
- Run full python suite (184 passed) + local planner check.
- Commit 3ab9f01b, push (force-with-lease onto work/broker-ready4), head to PR #1264.
- Watch PRSC #1264 to terminal SUCCESS.

## PR B diff (commit 3ab9f01b)
```diff
 # scripts/pr-gate-plan.py
+        elif path.startswith('internal/runtimebroker/') and path.endswith('.go'):
+            # runtime-broker container realization + its tests (compose_render.go
+            # readiness grace, broker/retirement lifecycle). The broker renders
+            # and drives the runtime on BOTH runners (Docker/Compose and rootless
+            # Podman/Quadlet), so it must exercise the real atomic lifecycle gates
+            # on both.  Bind the whole package to those EXISTING gates only — no
+            # new release gate, no widening.  Without this branch the files fell to
+            # the generic internal/runtime/ catch-all and left PR Selected Checks
+            # fail-closed with 'unknown impact for internal/runtimebroker/…'
+            # (#1265).  Any other internal/runtimebroker/*.go that does not match an
+            # explicit reviewed-source clause below stays unresolved.
+            area = 'runtimebroker-lifecycle'
+            require(CODE_CHECKS)
+            require(CLI_CHECKS)
+            selected.add('atomic/docker/lifecycle')
+            selected.add('atomic/podman/lifecycle')
```
- `scripts/test_pr_gate_plan.py`: added
  `test_runtimebroker_package_binds_existing_lifecycle_gates_resolved`
  (5 subtests: broker.go, compose_render.go, retirement.go, broker_test.go,
  retirement_test.go → resolved, both lifecycle gates, broad_required False).
- Scope verified: `git diff --name-only` = scripts/pr-gate-plan.py,
  scripts/test_pr_gate_plan.py. NO healthcheck values, NO .github/workflows/*.

## Local verification
- `python -m pytest scripts/test_pr_gate_plan.py` → **184 passed, 531 subtests**.
- Isolated planner check of PR #1265's previously-failing paths:
  - `internal/runtimebroker/compose_render.go` → coverage_status=**resolved**,
    selected_gates=['atomic/docker/lifecycle','atomic/podman/lifecycle'],
    unresolved=[].
  - `internal/runtimebroker/broker_test.go` → same resolved + both gates.

## PRSC watch (Eigenes-Run-Pflicht) — TERMINAL SUCCESS
- PR #1264 (work/broker-ready4 → develop), head `3ab9f01b13b008627c50c74eda4db50687259802`.
- `PR Selected Checks`: **success** — terminal. Run-ID `125061665105`
  (job 125061665105, run 41377561980, run log: `PR Selected Checks: PASS`).
- Validation gates all SUCCESS: `source-contracts`, `pr-planner-tests`,
  `receipt-execution-tests`, `ci-policy`, `ci-executor-verifier-tests`,
  `Focused Python`, `Trusted Plan`, `Workflow policy`.
- The fail-closed from #1265's RunID 125059625061 is now resolved: the
  runtimebroker file binding supplies the existing atomic lifecycle gates, so
  the package is covered on BOTH runners. Not a flake.

## END
END_DONE broker-ready4: PR B = commit 3ab9f01b (scripts/pr-gate-plan.py runtimebroker/* → atomic/docker/lifecycle + atomic/podman/lifecycle; planner test), pushed to PR #1264 (head 3ab9f01b). PRSC #1264 TERMINAL SUCCESS RunID 125061665105 (PR Selected Checks: PASS). REST from earlier #1265 (application/* file binding still missing) now OUT of scope for this lane — only runtimebroker binding delivered; if #1265 is re-run the application/* surfaces may still need their own binding. No merge, no receipts, per STOP.
