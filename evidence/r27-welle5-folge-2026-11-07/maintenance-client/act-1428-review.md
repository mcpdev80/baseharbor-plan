# CODEX-REVIEW 0427-118 maintenance client — PR #1428

## PLAN

1. Read mission, canonical task contract, relevant product rules, and evidence for the prior blockers/public-surfaces finding — DONE.
2. Fetch exact live `develop` and PR #1428 refs; verify ancestry and inspect all changed maintenance files, tests, and candidate-only commits — DONE.
3. Assess installation-authority routing, fail-closed behavior, causal mutants, maintenance window/history persistence, public-surfaces finding, and CI selection — DONE.
4. Record verdict and actionable recipe, validate and publish this evidence to `baseharbor-plan` origin/main, then post END — IN PROGRESS.

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
