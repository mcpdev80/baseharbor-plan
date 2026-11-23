# #1614 terminal hop — receipt chain

**Card:** 0428-062 (lane `lane-0428-062-cli2-app-status`)
**Date:** 2026-11-23
**Author:** Worker (this lane)

## Situation: concurrent hop by another lane

At session start, PR #1614 head had moved from my hop `61063fc7f` to the remote
backing branch head `3b40c05d`. Another lane had already performed the develop
hop on this backing branch:

- `3b40c05d` parents = `61063fc7f` + `ddddbed16` (additive `--no-ff` merge).
- `ddddbed16` = develop tip = `b41103867` + #1723 (`fix(0428-199): respect
  --workload-port on local apply/up path`, files `app_apply.go`,
  `app_workload_ports.go`, `runtime.go`, `workload_port_local_regression_test.go`).
- `ddddbed16` is the **current** `refs/heads/develop` head at the time of the run.

My local merge `227fc132c` (`61063fc7f` + exact `b41103867`) is a **content
subset** of the remote `3b40c05d`:

- My `#1614` product files (`cmd/baha/app_observe.go`, `app_status_result.go`,
  `app_status_versions_test.go`, `app_tls.go`, `app_versions_*`,
  `app_workspace_source_model.go`, `machine_coverage.go`,
  `management_core_git_candidate_test.go`, `contracts/machine/v1/read-models.schema.json`,
  `internal/machinereadmodels/release.go`, `docs/**`) are **byte-identical** in
  `3b40c05d` (`git diff 61063fc7f..3b40c05d` on these paths = empty).
- The additional remote content (`app_apply.go`, `app_edit.go`,
  `app_edit_apply_test.go`, `app_wizard_controller.go`, `app_workload_ports.go`,
  `runtime.go`, `workload_port_local_regression_test.go`) is #1801/#1723, not
  my write-set.

**Decision:** I did **not** push `227fc132c` (would race the remote backing
branch whose head already carries my content + the develop hop). The remote PR
head `3b40c05d` is the terminal candidate. I verified its run instead.

## Delta-check (confidence, no conflict protocol needed)

- `b41103867` (#1801) files `app_edit.go`, `app_edit_apply_test.go`,
  `app_wizard_controller.go` are **not** in my `#1614` write-set → no overlap.
- `ddddbed16` (#1723) files `app_apply.go`, `app_workload_ports.go`,
  `runtime.go`, `workload_port_local_regression_test.go` are **not** in my
  `#1614` write-set → no overlap.
- `#1614` NET diff vs develop = exactly my 23 product paths. Catalog
  `scripts/pr-gate-coverage.json` byte-equal with develop (0 changed lines).
  `.github/**` untouched (not in NET diff).

## Terminal CI run — witnesses

| Item | Witness |
| --- | --- |
| Run ID | `45168506606` |
| Head SHA | `3b40c05dad5f292af2d669bb95d94c0e3ed581b3` |
| Run status | `completed` / `conclusion: success` |
| No failures | only skipped cells (not selected for this NET diff); zero `failure`/`failure` check-runs |

### BASE_SHA (trusted-plan)

- Job `PR · Trusted Plan` → `conclusion: success` (job id `137671609238`).
- Job log: `BASE_SHA: ddddbed16e34638f35968e2dc99921f970ba3720` — the current
  develop tip at trigger time.
- `ref: ddddbed16e34638f35968e2dc99921f970ba3720` checked out in the job.

### Receipt chain (1656-kette)

| Receipt | Witness |
| --- | --- |
| docker coreless-lifecycle foundation job | `completed / success` (job id `137671780791`) |
| `TestCorelessFreshWorkloadRuntimeLifecycle` | `--- PASS: ... (68.82s)` in job log |
| `TestCorelessLocalProdRuntimeLifecycle` | `--- PASS: ... (74.58s)` in job log |
| lifecycle-family membership | run selected for `integration/docker/coreless-lifecycle` (NET diff maps through `machine_coverage.go`) |

## Conclusion

The terminal required CI run for `#1614`'s content reached a **SUCCESS** terminal
state with BASE_SHA == the current develop tip (`ddddbed16`) and the full
receipt chain (trusted-plan success + docker coreless-lifecycle foundation PASS
with both lifecycle tests passing). The develop hop was already performed by a
concurrent lane on the shared backing branch; my `#1614` product content is
byte-identical there. No push was made by this lane (race-avoidance). The
candidate at `3b40c05d` is ready for review → merge by a separate lane.
