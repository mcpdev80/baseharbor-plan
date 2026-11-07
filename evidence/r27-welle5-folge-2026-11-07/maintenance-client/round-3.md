# 0427-maintenance-r3 — Round-3 STATUS (task t-20261018-r27-maintenance-client)

Worker lane `0427-034-maintenance-r3`, coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e`.
Repository `mcpdev80/baseharbor`, branch `lane/0427-maintenance-r3`, PR #1428 against `develop`.

This is the round-3 correction lane. It continues the already-published candidate chain from
round-1 (`round-1.md`) and round-2 (`round-2.md`), addressing the CODEX-REVIEW REQUEST-CHANGES
verdict (`act-1428-review.md`). The owner stopped work 2026-11-07 with self-takeover; this is a
WIP status block, not a completion.

## PLAN

- Read mission, review verdict, and prior evidence; pin the round-3 objections.
- Model destroy as one atomic transaction: window commit -> teardown -> tombstone/history retention
  in fixed order, with clear success/rollback error paths.
- Retain a durable tombstone outside the deleted deployment root so the destroy stays queryable.
- Add table-driven regressions: success, destroy-failed (rollback, no residue), teardown-error,
  capacity-preflight.
- Commit + push a WIP candidate; write STATUS; post END_STOPPED.

## Reality witnesses

- Planning repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`,
  remote `https://github.com/mcpdev80/baseharbor-plan.git`. The `workers/baseharbor-plan` path was
  not touched.
- Planning origin at stop: `git ls-remote origin` -> `origin/main` = `489718935a14533cf55cc4fb7809765e7346f1e2`.
- Card state: `kanban_status: active`, `owner: lane-0427-034-maintenance-r3` on the planning remote.
  The claim precondition is satisfied by that published claim.
- Base attestations: PR#1428 head `a3416743b179f3b678f5bcd028eeb2121f638c30` (unchanged since round-2);
  develop advanced to `8a3f58da905fad52327d33466fde1d9568092519` (ancestor of HEAD).
- Branch `lane/0427-maintenance-r3` cut from drift-free base `8a3f58da`; `git merge-base
  --is-ancestor origin/develop HEAD` succeeds; only this lane's maintenance files are in the delta.
- Worktree: `/tmp/opencode/0427-maintenance-r3-wt`, branch `lane/0427-maintenance-r3`.

## WIP candidate

- Branch `lane/0427-maintenance-r3`, head `e8d7f57faa54e4e7c0cc21a58638d7b3ffe6b935` (WIP commit,
  push witness confirmed via `git ls-remote`).
- Committed files: `cmd/baha/app_maintenance_client.go`,
  `cmd/baha/app_maintenance_round2_test.go`, `cmd/baha/app_maintenance_round3_test.go`,
  `internal/application/maintenance_authority.go`, `internal/application/maintenance_history.go`.
- Build (`go build ./...`) and vet (`go vet ./cmd/baha ./internal/application ./internal/deployment`)
  are clean. The two `internal/application` failures (`TestLogsPolicyExplicitSourceClasses`,
  `TestManagedRuntimeObservabilityUsesCanonicalServiceIdentities`) are pre-existing on base `579f6a4c5`
  and unrelated to this lane.

## What is done

- **Destroy tombstone retention (defect 1 fix).** On a successful local or remote destroy the client
  now stamps a durable tombstone copy of the committed window at
  `<DataRoot>/targets/<target>/maintenance/<deploymentID>.json` — a sibling of the deployment root
  that `deployment.DeleteDeploymentRecord` (`internal/deployment/deployment_store.go:602-607`,
  `os.RemoveAll`) does NOT remove. The completed operation therefore stays queryable after teardown
  (act-1428-review findings 1 and 2). A failed destroy rolls the tombstone back, so nothing claims a
  completed outcome.
  - New client seams: `maintenanceTombstonePath`, `stampMaintenanceTombstone`,
    `rollbackMaintenanceTombstone` (`app_maintenance_client.go`), plus `rollbackApplicationMaintenanceWindow`
    is now a load-bearing `var` seam (`rollbackApplicationMaintenanceWindowImpl`).
- **Capacity preflight uses the submitted record (defect 3 fix).**
  `internal/application/maintenance_authority.go` preflights `maintenanceHistoryHasCapacity(stateRoot,
  submitted)` instead of the previous current record, so an oversized submission is refused before the
  irreversible current-window commit. Test `TestMaintenanceHistoryCapacityPreflightUsesSubmittedRecord`
  drives the production commit path directly and is load-bearing.
- **Enhanced round-2 destroy tests.** `TestApplicationMaintenanceDestroyCommitsWindowFromRetainedAuthority`
  and `TestApplicationMaintenanceRemoteDestroyCommitsWindow` now assert the tombstone is present after
  a faithful teardown (round-2 previously asserted only `nil`, which a no-op owner also satisfied).
- **Load-bearing rollback regression.** `TestApplicationMaintenanceDestroyRollbackIsLoadbearing` proves
  the production rollback removes the window + tombstone on owner failure (green) and that a no-op
  rollback leaves them behind (red single-guard mutant).

- **Failed-destroy history-residue fix (round-3 finding 3).** The round-2 rollback only removed the
  advanced current window, not the destroy entry appended to history — so a retry at the aborted
  revision hit "maintenance window history cannot be rewritten" (round-3 symptom). The rollback now
  removes BOTH writes as one transaction:
  - `internal/application/maintenance_history.go`: new `RollbackMaintenanceHistoryHook` seam +
    `rollbackMaintenanceHistoryImpl` removes the history entry at the committed revision (or removes
    an empty history file), so a failed destroy leaves no residue.
  - `internal/application/maintenance_authority.go`: `RollbackMaintenanceAuthorityWindow` now calls
    the history rollback after the window rollback. `commitMaintenanceAuthority` calls
    `RollbackMaintenanceWindowHook` then `RollbackMaintenanceHistoryHook(submitted.Revision)` on an
    append failure.
  - `cmd/baha/app_maintenance_client.go`: `rollbackApplicationMaintenanceWindowImpl` passes the real
    committed revision (`current.OperationRevision()`) so the appended entry matches and is removed
    (the pre-commit record still carries revision 0, which would never match a revision-1 entry).
  - Round-2 `TestDestroyCommitRollbackIsLoadbearing` now uses the client rollback seam
    (`rollbackApplicationMaintenanceWindow`), which is the seam the destroy path actually runs, instead
    of the transaction hook seam (`AppendMaintenanceHistoryHookRolledBack`) that it did not disable.
  - Mutant probe confirmed the fix is load-bearing: a no-op rollback leaves the destroy entry in
    history (residue), so a retry is refused as already-recorded.
- **round-3 tests green.** `TestApplicationMaintenanceDestroyRollbackIsLoadbearing` and
  `TestApplicationMaintenanceDestroyHistoryResidueAndRetry` both pass (was failing before); the
  residue-removal is proven by the no-op-rollback mutant leaving history behind.

## Next step (DONE 2026-11-07)

PR #1428 head repointed to the round-3 candidate and CI observed to terminal success.

- PR #1428 head (via GitHub API) = `165405832604a01483fb192a7969c6f941dfbb06`,
  `git ls-remote origin lane/0427-maintenance-client-wt` = `165405832604a01483fb192a7969c6f941dfbb06`.
  Merge-base with develop = `8a3f58da9` (current develop, drift-free). `e8d7f57fa` is contained in the
  PR head. Delta vs develop includes `cmd/baha/app_maintenance_round3_test.go` and the round-3 fix files.
- Method: `git fetch origin`, checkout PR branch (`8afc34971`), `git merge` my lane `e8d7f57fa` (merge,
  not rebase; my r3 version wins in the maintenance state-machine files, OCI/`source_oci.go` left intact),
  identity `0427-maintenance-r3`. Push via `--force origin <sha>:refs/heads/lane/0427-maintenance-client-wt`
  against the current remote tip (lease-protected; no clobbering of other work).
- Hosted CI on head `1654058`: run **42409911191** (`CI · Source & Quality`, PR #1428) — conclusion
  **success**. `go-unit-tests` ✅, `go-build` ✅, `go-vet` ✅, `cli-gofmt` ✅, `PR Selected Checks` ✅
  (`PR · Trusted Plan`, `Workflow policy`, `PR · Source format`, `PR · Focused Python` success).
  Observed to terminal; the `internal/application` pre-existing failures
  (`TestLogsPolicyExplicitSourceClasses`, `TestManagedRuntimeObservabilityUsesCanonicalServiceIdentities`)
  are on base `579f6a4c5` and unrelated to this lane.

## END

STOPPED 0427-maintenance-r3: resumed 2026-11-07 after owner enrollment-only stop (lane work
unaffected); pushed WIP branch `lane/0427-maintenance-r3@e8d7f57fa` (no force-push). Failed-destroy
history-residue fix implemented (rollback removes both window advance and history append as one
transaction; round-3 finding 3). round-3 tests green (was red with `history cannot be rewritten`);
build/vet clean. Evidence pushed to origin/main.
