# CODEX-REVIEW 0427-118 maintenance client — PR #1428

## PLAN

1. Read the r5 mission and create the visible numbered plan — done.
2. Read round-5 evidence from planning origin/main and inspect the named candidate test functions and oracle lines at exact SHA — done.
3. Decide whether the reported mutants establish the disputed behaviors; record only the remaining review findings and corrected recipe — done.
4. Verify candidate head before and after, publish the updated verdict in this authorized act on planning origin/main, then post END — in progress.

## Review identity

- Lane: `0427-maintenance-client-review`.
- Role: CODEX-REVIEW only. No merge, candidate mutation, local test run, or CI rerun.
- Repository: `mcpdev80/baseharbor`, PR #1428, task `t-20261018-r27-maintenance-client`.
- Candidate head: `d4d0f77c0cf0db675b603daaf22ea859fac4290a`.
- Live base `develop`: `812c99c8873df400348fbc8cc9be5e650b8966c4`.
- Planning root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; remote `origin` is `https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.

## Verdict: REQUEST-CHANGES

The candidate is ancestry-clean, its nine-file write-set is scoped, and the exact-head hosted unit job passes. The production route preserves installation ownership and delegates mutations to existing lifecycle owners. Two durable-state defects remain: local destroy deletes the deployment state before the client tries to commit its maintenance window, while remote destroy returns without committing a window; and the current window file is replaced before history append succeeds, so an append failure can leave current state advanced while historical replay data is missing. These violate the required maintenance window/history behavior.

### Live refs and provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head` returned:

  ```text
  812c99c8873df400348fbc8cc9be5e650b8966c4 refs/heads/develop
  d4d0f77c0cf0db675b603daaf22ea859fac4290a refs/pull/1428/head
  ```

- Fetched those refs into `/tmp/opencode/0427-maintenance-client-review-wt`. `git merge-base --is-ancestor refs/remotes/origin/develop refs/remotes/origin/pr/1428` returned `0`.
- `git log --format='%H %an %s' develop..head` lists only three maintenance-card commits: `5e81b89b18d5f557518eff1bef06e38d1364e8df` (implementation), `8bb22dc956b62d41c34fbb764dbeca7dde064d87` (mutation proof documentation), and `d4d0f77c0cf0db675b603daaf22ea859fac4290a` (mutant seam test). No foreign candidate commit is present.
- PR API: OPEN, base `develop` at `812c99c8873df400348fbc8cc9be5e650b8966c4`, head `d4d0f77c0cf0db675b603daaf22ea859fac4290a`, mergeable `true`, merge state `clean`.

### Review findings

1. **Production routing and fail-closed behavior: PASS, with destroy persistence defects below.** `cmd/baha/app_maintenance_client.go:128-163` resolves the selected application and checks the installation authority before opening local inputs or invoking a lifecycle owner. Remote backup, restore, and update return `ErrorCapabilityMissing` before transport at lines 205-228; remote destroy requires `--yes` and routes through the existing destroy owner. `cmd/baha/app_maintenance_lifecycle_owner.go:21-33` delegates to the existing backup, restore, update, and destroy lifecycle functions; this client does not implement a second maintenance engine.

2. **Causal mutants: PASS based on candidate tests and published run record.** `cmd/baha/app_maintenance_mutant_test.go:23-194` exercises authority-before-owner, safe-path, remote-capability, input-before-authority, lifecycle-owner, failed-operation, cancellation, and replay guards. The published `evidence/r27-welle5-folge-2026-11-07/maintenance-client/round-1.md` records red outcomes after mutation of the production cancellation, path, authority, capability, digest replay, and history-append guards. This review did not rerun those checks.

3. **Blocking destroy/window defect.** The local destroy branch at `cmd/baha/app_maintenance_client.go:302-317` calls the existing lifecycle owner and then `commitApplicationMaintenanceWindow`. The existing owner deletes the deployment record at `cmd/baha/app_destroy_lifecycle.go:597-599`; `deployment.DeleteDeploymentRecord` removes the whole deployment root at `internal/deployment/deployment_store.go:602-607`. The subsequent window commit reloads that now-absent deployment via `applicationMaintenanceAuthority` (`app_maintenance_client.go:378-380`) and returns an error after destruction already succeeded. The remote destroy branch at `app_maintenance_client.go:209-228` returns from the destroy owner directly and never commits the maintenance window at all. Existing client tests replace `maintenanceLifecycleOwner` with test callbacks, so they do not cover this actual deletion behavior.

4. **Blocking history consistency defect.** `internal/application/maintenance_authority.go:291-315` writes and renames the latest `maintenance-authority.json` before calling `appendMaintenanceHistory`. `internal/application/maintenance_history.go:87-107` can then fail, including when the history exceeds its 4 MiB limit or when a write/chmod/rename fails. The call returns an error even though the latest window has advanced. A retry at that revision resolves the current window as already recorded (`loadMaintenanceRevision` prefers the current record) and does not repair the missing history entry; a later commit can supersede it, leaving the older revision unanswerable. The existing tests cover successful history replay and revision limits, but not failure between the two file commits.

5. **Public-surface registration: documented non-blocking for this bounded client card, not feature completion.** The constructor `applicationMaintenanceCommand` has no production call site in `cmd/baha/commands.go`; repository search finds the command/executor only in its defining file and tests. The separate `t-20261018-r27-public-surfaces` card explicitly owns `commands.go`, machine contracts, and shared registrations, and it depends on this maintenance-client card. Keep registration out of this write-set and record it as a required follow-up; do not describe the user-facing maintenance command as shipped until that integration lands. This split is consistent with the assigned file ownership, while the maintenance client still must provide a callable implementation rather than an empty adapter.

6. **Write-set and lifecycle collision: PASS.** `git diff --name-status develop...head` contains exactly these nine new files: `cmd/baha/app_maintenance_client.go`, `cmd/baha/app_maintenance_client_test.go`, `cmd/baha/app_maintenance_lifecycle_owner.go`, `cmd/baha/app_maintenance_mutant_test.go`, `cmd/baha/maintenance_remote_safety.go`, `cmd/baha/maintenance_test_seam_test.go`, `internal/application/maintenance_authority.go`, `internal/application/maintenance_authority_test.go`, and `internal/application/maintenance_history.go`. No `.github/**`, scripts, #110/#1383 lifecycle files, or fixture files are changed.

### Hosted CI

- Run `42386457934` completed successfully on the exact candidate SHA `d4d0f77c0cf0db675b603daaf22ea859fac4290a`.
- `PR · Validation · go-unit-tests` passed (7m52s); go-build, go-vet, cli-gofmt, source format, focused Python, trusted plan, workflow policy, and `PR Selected Checks` also passed.
- The current base workflow runs `go test ./cmd/baha` (line 122) and its unit job runs `go test ./...` (line 340); selected `go-unit-tests` is routed through `scripts/pr-unit-database.sh` (line 799). The job did not skip, so the new `cmd/baha` and `internal/application` tests are captured by hosted unit CI.
- `Targeted HA · docker` and `Targeted HA · podman` were skipped. These are not required to prove the fixture-based unit regressions in this card, and no native runtime success is claimed by this review. No CI rerun or workflow dispatch was started.

## Actionable recipe

- **Files and changes:** In `cmd/baha/app_maintenance_client.go`, make successful local and remote destroy preserve a durable result without trying to reload state after the destroy owner removes it. Use a retained tombstone or another existing-owner-controlled record location, and keep explicit approval and lifecycle consent unchanged. In `internal/application/maintenance_authority.go` and `internal/application/maintenance_history.go`, make latest-window and history updates recoverable as one transaction; a history append failure must not leave an advanced current record with a missing historical revision. Preflight bounded-history capacity before an irreversible operation where possible.
- **Test requirement:** Add a lifecycle test using the real destroy owner (or a faithful owner that deletes the deployment root) and assert successful destroy does not return a post-destroy persistence error and its durable outcome remains queryable. Add remote-destroy coverage for the same durable outcome. Add injected history-write/rename/size-limit failure coverage: retry the same revision, commit a later revision, then prove the earlier revision is still answerable and no partial state is reported as success. Keep all new tests in `go-unit-tests` (`go test ./cmd/baha` and `go test ./...`) on the exact candidate SHA. The public-surface registration remains with `t-20261018-r27-public-surfaces`.
- **Stop criterion:** Keep this candidate at request-changes until destroy success and replay remain consistent for both local and remote routes, and every history-write failure leaves recoverable, gap-free durable state. Stop if a proposed fix requires command/schema registration or `.github/**` changes outside the assigned owner; report that exact boundary instead of editing it.

## Repository-rule compliance

- Read-only review of the product repository and candidate. No product file was modified, no local tests were run, no CI was rerun, and no merge was attempted.
- No `.github/**` change or workflow action was performed; no runner or VM infrastructure was touched.
- Evidence is in the verified `baseharbor-plan` repository only. This file contains no Markdown checkbox lines.
- Existing unrelated untracked planning evidence was left untouched.

## END

END_BLOCKED 0427-maintenance-client-review: REQUEST-CHANGES; candidate d4d0f77c0cf0db675b603daaf22ea859fac4290a is ancestry-clean with hosted unit CI green, but destroy removes state before local window persistence and remote destroy omits the window; history write failure can leave a superseded operation unanswerable.

## Planning origin witness

Output of `git -C baseharbor-plan ls-tree -r origin/main --name-only | rg '^evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review\.md$'` before this publication update:

```text
evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review.md
```

## REREVIEW RESULT — PR #1428

### Review identity and exact provenance

- Role: CODEX-REVIEW rereview only. Candidate was not modified; no local tests, CI rerun, merge, VM, or workflow action was performed.
- Candidate head: `a3416743b179f3b678f5bcd028eeb2121f638c30`.
- Exact fetched `develop`: `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head` returned:

  ```text
  06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 refs/heads/develop
  a3416743b179f3b678f5bcd028eeb2121f638c30 refs/pull/1428/head
  ```

- `git merge-base --is-ancestor refs/remotes/origin/develop refs/remotes/origin/pr/1428` returned `0`.
- `git log --format='%H %an %s' develop..head` lists only four task commits: `d4dd5137687d42ebe549215c85efa2c03903d489`, `a7704406366a6f655e824450e4f5a731e93e9d15`, `f3e047e1febc7205c62f8ec7347cb5be14df3913`, and candidate `a3416743b179f3b678f5bcd028eeb2121f638c30`.
- Against current `develop`, the full write-set is ten files, all `cmd/baha/*maintenance*` or `internal/application/maintenance_*`; no `.github/**`, scripts, #110 lifecycle/fixture, or unrelated paths are changed. Direct tree comparison of previous reviewed head `d4d0f77c0cf0db675b603daaf22ea859fac4290a` to the new head shows the round-two delta in four maintenance files: `cmd/baha/app_maintenance_client.go`, `cmd/baha/app_maintenance_round2_test.go`, `internal/application/maintenance_authority.go`, and `internal/application/maintenance_history.go`. The previous candidate was based on `812c99c8873df400348fbc8cc9be5e650b8966c4`; the new candidate is rebased on `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- GitHub reports the PR OPEN, exact head above, base `develop`, mergeable, merge state `CLEAN`.

### Verdict: REQUEST-CHANGES

1. **Local destroy window retention: NOT FIXED.** `cmd/baha/app_maintenance_client.go:325-348` commits the window before invoking the destroy owner, but the owner ultimately calls `deployment.DeleteDeploymentRecord`, which removes the complete deployment root (`internal/deployment/deployment_store.go:602-607`). The window and history are stored under `resolved.stateRoot()`, so the successful teardown deletes the just-committed window. `TestApplicationMaintenanceDestroyCommitsWindowFromRetainedAuthority` (`cmd/baha/app_maintenance_round2_test.go:55-91`) deliberately removes that same root at lines 77-79 but asserts only that the command returned nil; it never proves a durable window remains queryable.
2. **Remote destroy window retention: NOT FIXED.** The remote path now also commits via the retained authority before teardown (`app_maintenance_client.go:242-265`), so it includes a commit attempt, but the same state-root deletion loses that record. `TestApplicationMaintenanceRemoteDestroyCommitsWindow` (`app_maintenance_round2_test.go:99-137`) likewise removes the root and checks only for nil, without asserting retained history after teardown. Both tests would also pass if a no-op owner returned nil without committing the maintenance window, so they are not causal evidence for the required durable outcome.
3. **History append failure and capacity preflight: PARTIAL / NOT FIXED.** `internal/application/maintenance_authority.go:350-359` now rolls the current window back after append failure, and the append-failure regression exercises that lower-level rollback. However, the preflight at line 343 calls `maintenanceHistoryHasCapacity(stateRoot, current)` with the previous window record instead of `submitted`; the helper appends its argument when calculating size (`maintenance_authority.go:367-378`). An oversized submitted history record therefore is not preflighted before the current window rename. `TestMaintenanceHistoryCapacityPreflightFailsBeforeCommit` (`cmd/baha/app_maintenance_round2_test.go:207-243`) wraps/replaces `application.CommitMaintenanceAuthority` and calls the helper itself with the correct `submitted` record at lines 215-222, so it tests the wrapper's preflight rather than proving the production commit uses the submitted record. Also, destroy's outer rollback (`app_maintenance_client.go:345-347`) restores/removes only the current window through `RollbackMaintenanceAuthorityWindow`; it does not remove the already-appended failed destroy entry from history. A retry after a failed destroy can then reuse the missing current revision and be refused as a duplicate history revision.
4. **Causal mutants: INSUFFICIENT.** `TestMaintenanceHistoryAppendRollbackIsLoadbearing` exercises a history append rollback mutant, but neither successful destroy test asserts window/history durability or demonstrates red/green when the pre-teardown commit is removed. The capacity test's test-side wrapper makes the intended production preflight non-loadbearing. Hosted green status cannot establish these absent assertions.
5. **Write-set and hosted test capture: PASS.** Current diff is confined to maintenance-prefixed files. Run `42395015763` is terminal success on the exact head: nine checks passed, including `PR · Validation · go-unit-tests`, go-build, go-vet, cli-gofmt, source format, trusted plan, workflow policy, focused Python, and `PR Selected Checks`. The new round-two Go tests are in `cmd/baha` / `internal/application` and are captured by the non-skipped hosted `go-unit-tests` job. Targeted Docker and Podman jobs are skipped; this rereview does not claim native runtime evidence and did not rerun CI.

### Actionable recipe

- **Files and changes:** In `cmd/baha/app_maintenance_client.go` and the existing deployment lifecycle owner, retain the maintenance window/history in durable storage that survives `DeleteDeploymentRecord` for both local and remote destroy. Make failed destroy rollback remove both the current-window update and its history append so the same operation can be retried. In `internal/application/maintenance_authority.go:343`, preflight the submitted record, not the previous current record; keep the append transaction fail-closed.
- **Tests:** Update `cmd/baha/app_maintenance_round2_test.go` so faithful local and remote destroy owners delete the deployment root, then assert the exact committed window and history remain loadable after success. Add failure-and-retry coverage proving a rejected destroy leaves neither a phantom history revision nor a stuck duplicate on retry. Make the capacity test call the production commit path directly with an oversized submitted record and assert the production append hook was never invoked and the previous current state remains unchanged. Retain and extend the history append failure/rollback mutant so disabling each production guard makes its own regression fail. These tests are executed by hosted `PR · Validation · go-unit-tests` on pull-request changes; no `.github/**` change is requested.
- **Stop criterion:** Keep this candidate at request-changes until both destroy paths preserve queryable durable windows after actual root teardown, failed destroys can be retried without history divergence, and production capacity preflight and each required mutant are demonstrated by load-bearing tests on a green exact-head hosted run.

## REREVIEW END

END_BLOCKED 0427-maintenance-client-rereview: REQUEST-CHANGES; candidate a3416743b179f3b678f5bcd028eeb2121f638c30 is ancestry-clean with hosted CI green, but teardown deletes the precommitted window, failed destroy can leave history residue, and capacity preflight checks the old record rather than the submission.

Planning-root re-verification before this rereview evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned exactly `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `remote -v` showed origin fetch/push at `https://github.com/mcpdev80/baseharbor-plan.git`; live origin/main before this evidence commit was `cfc432bf98080c9bec3ebe9640a401e833bf4258`.


Remote publication witness from `git ls-tree -r origin/main --name-only | rg '^evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review\.md$'`:

```text
evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review.md
```

Final unchanged-candidate witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head`:

```text
06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 refs/heads/develop
a3416743b179f3b678f5bcd028eeb2121f638c30 refs/pull/1428/head
```

Final remote-tree witness from `git -C /tmp/opencode/0427-maintenance-client-rereview-plan-wt ls-tree -r origin/main --name-only | rg '^evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review\\.md$'`:

```text
evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review.md
```


## R5 contradiction recheck — PR #1428 head 396529860e1f349576190f435cb06e2b7b496866

### Verdict: REQUEST-CHANGES; the r5 evidence does not fully close both review findings

Exact candidate witnesses before this recheck: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head` returned `8a3f58da905fad52327d33466fde1d9568092519 refs/heads/develop` and `396529860e1f349576190f435cb06e2b7b496866 refs/pull/1428/head`. The develop SHA is an ancestor of this candidate (`git merge-base --is-ancestor` exit 0). The candidate was inspected detached and was not modified. Round-5 evidence was read from planning `origin/main` at `796b93653d0aa961d3127a4f6b729d1a0046c05f`; its tree entry was `100644 blob 756d453f40c1675f46f024f92a4d432dbf2b0fc5 evidence/r27-welle5-folge-2026-11-07/maintenance-client/round-5.md`.

1. **Retry rollback implementation is present, but the claimed retry regression is not valid for owner-failure residue.** `rollbackApplicationMaintenanceWindowImpl` passes the committed revision to `application.RollbackMaintenanceAuthorityWindow` (`cmd/baha/app_maintenance_client.go:574-586`; `internal/application/maintenance_authority.go:455-460`), and that function removes the history entry. The separate `TestApplicationMaintenanceDestroyHistoryResidueAndRetry` verifies the inner history-append-failure transaction and then a successful retry (`cmd/baha/app_maintenance_round3_test.go:107-154`). However, the r5-cited matrix does not prove retry after a successful window commit followed by lifecycle-owner failure: its owner-failure rows do not set `retryableAfter` (`cmd/baha/app_maintenance_round4_test.go:59-90`). The only retry-enabled rows are history-append failures; the hook remains set to return the failure, and both retry checks at lines 204-220 fail if the retry returns nil. The duplicated assertions therefore expect retry failure, contrary to their comments. The round-5 mutation probe that replaces the outer rollback with a no-op fails earlier on current-window presence (`round-5.md`, Finding 1), so it does not demonstrate the specifically disputed history-residue/retry oracle. I withdraw the claim that source rollback is missing, but the promised owner-failure history/retry proof remains outstanding.

   Corrected recipe: in `cmd/baha/app_maintenance_round4_test.go`, make a `local-owner-failure` and a `remote-owner-failure` case assert the history contents and then retry the same committed revision after restoring the lifecycle owner; assert retry succeeds and exactly one durable entry remains. Add a targeted mutant that disables only the history-removal half of `RollbackMaintenanceAuthorityWindow` while retaining current-window rollback; the owner-failure regression must go red because the stale history revision rejects retry. Stop criterion: both local and remote owner-failure cases prove history is removed and the same revision is accepted on retry, and the isolated history-removal mutant makes those assertions fail.

2. **Tombstone persistence is proven; tombstone replay is not wired.** The local and remote destroy paths stamp a sibling tombstone before teardown (`cmd/baha/app_maintenance_client.go:256-275, 352-372`). The round-4 matrix uses a faithful owner that removes the deployment root (`cmd/baha/app_maintenance_round4_test.go:137-153`) and reads the tombstone file directly, checking operation and committed revision (`:184-200`). The r5 no-op stamp probe consequently proves the file is durable after teardown. But `loadMaintenanceRevision` reads only the current window and history beneath `stateRoot` (`internal/application/maintenance_history.go:197-219`); it has no tombstone fallback. Search of the candidate shows `maintenanceTombstonePath` is used by the writer and tests, with no production tombstone reader. Once `DeleteDeploymentRecord` removes the deployment root, the reported `loadMaintenanceRevision` replay cannot consume the sibling tombstone. Thus the evidence proves a retained JSON artifact, not a working replay path.

   Corrected recipe: in the production maintenance replay/authority lookup, add a tombstone read fallback keyed by target and deployment identity when the deployment root is absent; validate its contract version and revision and preserve fail-closed handling of malformed or mismatched tombstones. Extend `TestApplicationMaintenanceDestroyAllExitsMatrix` (or a focused production-path test) so both local and remote successful teardown invoke the actual replay lookup and receive the committed destroy revision. The no-op/missing-reader mutant must make that lookup fail. Stop criterion: after the faithful owner deletes the deployment root, the supported production lookup replays the exact committed destroy record from the sibling tombstone for both routes; direct `os.ReadFile` alone does not meet it.

- Existing hosted CI record in round-5 evidence: run `42416537555` on the exact candidate was terminal success; `PR · Validation · go-unit-tests` covered the Go changes. No CI was rerun and no local test or gate was run for this recheck.
- Write scope remained review-only. No product file or workflow was changed, and no release/tag action was taken.
- Planning root verification: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned exactly `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; origin fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git`.
- END BLOCKED 0427-maintenance-r5-recheck: REQUEST-CHANGES; candidate `396529860e1f349576190f435cb06e2b7b496866`; retry matrix has an inverted/duplicated oracle and tombstone persistence has no production replay reader.


## R5 publication witness

Pre-publication `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review.md` output:

```text
100644 blob 27fa71492f416b9b63a2307a30c65dc205e7b954	evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-review.md
```

Candidate `git ls-remote` immediately before publication still returned develop `8a3f58da905fad52327d33466fde1d9568092519` and PR #1428 head `396529860e1f349576190f435cb06e2b7b496866`.
