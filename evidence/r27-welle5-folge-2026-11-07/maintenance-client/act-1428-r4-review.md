# CODEX-REVIEW 0427-maintenance-r4-review — PR #1428

## PLAN

1. Read the r4 mission and record its numbered plan — done.
2. Read task contract; fetch exact PR/base refs; inspect only the two prior findings plus write-set, gates, and test CI selection — pending.
3. Record SHA-specific verdict and actionable recipe in canonical planning evidence — pending.
4. Publish evidence to origin/main, verify remote witnesses and unchanged candidate, then post END — pending.

## Candidate and hosted evidence

- Planning repository root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (exact `git rev-parse --show-toplevel` output); origin fetch/push URL: `https://github.com/mcpdev80/baseharbor-plan.git`.
- PR #1428 is OPEN, base `develop`, head `396529860e1f349576190f435cb06e2b7b496866`; live `git ls-remote` returned develop `8a3f58da905fad52327d33466fde1d9568092519` and PR head `396529860e1f349576190f435cb06e2b7b496866`.
- `git merge-base --is-ancestor 8a3f58da905fad52327d33466fde1d9568092519 396529860e1f349576190f435cb06e2b7b496866` exited 0. PR state is CLEAN and MERGEABLE.
- The 12-file delta is confined to maintenance implementation/tests in `cmd/baha/*` and `internal/application/*`; no `.github/**` or unrelated lifecycle/fixture/OCI files changed. No gate weakening appears in the delta.
- Hosted run `42416537555` is terminal success on exact head `396529860e1f349576190f435cb06e2b7b496866`. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `PR · Focused Python`, `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, and `PR Selected Checks` passed. Runtime-targeted Docker/Podman jobs were skipped. Existing `.github/workflows/ci.yml:340` runs `go test ./...`; the test package is covered by the passing hosted Go unit job. No workflow was changed, and no rerun or local test was performed.
- Candidate worktree was detached at the exact PR head and remained unchanged during review.

## Review of prior findings

1. **Stale destroy tombstone: corrected.** Both local (`cmd/baha/app_maintenance_client.go:352-363`) and remote (`:260-267`) destroy paths now use the `MaintenanceAuthorityRecord` returned from `commitApplicationMaintenanceWindowAuthority`, rather than the pre-commit authority. The new `assertCommittedDestroyTombstone` at `cmd/baha/app_maintenance_round4_test.go:227-245` verifies operation `destroy`, revision 1, and contract version after both successful routes. This resolves the prior stale-record defect for those tested fresh-window cases.

2. **All-exit matrix and last-bearing assertions: incomplete.** The table does cover local/remote success, owner failure, and history-append failure (`cmd/baha/app_maintenance_round4_test.go:50-99`). Success cases check tombstone contents; failure cases check absence of current window/tombstone. However, the `replay` field is declared at `:31-33` but is never set or read, and the table has no replay case. Production code writes/rolls back tombstones but has no tombstone reader; the only production tombstone references are stamp and rollback (`app_maintenance_client.go:267,273,363,369,517,551`). `applicationMaintenanceAuthority` still requires `deployment.LoadDeploymentRecord` (`:381-414`), so after successful teardown a replay cannot consult the retained tombstone. The mission’s replay-consistency criterion is therefore not demonstrated or implemented by the retained record.

   The history-residue rows are not load-bearing for residue. The injected `AppendMaintenanceHistoryHook` at `:129-135` returns an error before appending anything, so there is no residue for `RollbackMaintenanceHistoryHook` to remove. The `local-history-failure` and `local-history-failure-residue` rows at `:65-78` use the same setup. The retry assertions at `:204-222` also fail on `cerr == nil` (the successful retry result) and execute the same call twice; the failure hook remains installed, so those assertions only pass because retry continues to fail. They neither demonstrate clean retry nor detect a no-op history rollback mutant.

   Remediation: in `cmd/baha/app_maintenance_client.go`, add a tombstone lookup/replay path before rejecting a destroyed deployment for missing authority, and return the same already-recorded destroy outcome without rerunning lifecycle work for both local and remote selection. In `cmd/baha/app_maintenance_round4_test.go`, add local and remote replay rows that first destroy, then resubmit/resolve the same operation from the tombstone and assert no second owner call and the same durable result. For history residue, make the test seam perform the real history append and then return the injected error, disable only `RollbackMaintenanceHistoryHook` in the mutant case, restore the hook before retry, assert the retry succeeds, and assert the retained history contains exactly the expected revisions. Remove the duplicate retry block. Stop criterion: replay returns the recorded destroy result without invoking an owner; all local/remote success and failure cases have explicit durable-state assertions; the appended-then-error mutant goes red when history rollback is disabled and the repaired retry succeeds under the normal hook.

## Verdict

REQUEST-CHANGES for PR #1428 at `396529860e1f349576190f435cb06e2b7b496866`. The tombstone now contains the committed destroy record, but the required replay path is absent, and the history-residue/retry rows do not test residue or a successful retry. Keep the hosted CI evidence as-is; after correction, the existing `go-unit-tests` and `PR Selected Checks` must pass on the new exact head. No local tests or CI reruns were triggered during this review.

END BLOCKED 0427-maintenance-r4-review: request-changes; candidate `396529860e1f349576190f435cb06e2b7b496866`.
