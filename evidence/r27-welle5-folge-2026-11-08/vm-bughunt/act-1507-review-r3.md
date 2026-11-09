# CODEX-REVIEW 0427-176 r3 — PR #1507

## PLAN

1. Verify the current PR head, current develop head, merge base, exact hosted run, and candidate diff from live remotes.
2. Review target-wide lock acquisition, dotfile scan, fail-closed scan errors, and the lock hold through production mutations.
3. Verify both production-path regression directions and CI selection of the tests.
4. Record the exact review verdict and, if approved, perform the authorized standard merge with fresh remote witnesses.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`; PR #1507; task 0427-176.
- The originally named head `8dc5a91932df17879b602937ccf5877403a4b4b6` was superseded. Live `gh run list --repo mcpdev80/baseharbor --branch 0427-176-lockfairness` returned current run `42598253700` on head `bf7e7d3ecf8160ce4077c41bbc8768b5549d4066`, terminal `completed/success`; direct `gh api repos/mcpdev80/baseharbor/actions/runs/42598253700` returned the same `id`, `head_sha`, status, conclusion, and URL.
- The user-supplied run id `42597866777` was not found by GitHub. The actual exact-head run for the earlier `8dc5a919...` head was `42596428831` and completed successfully. The current candidate was independently rechecked on its own newer head as required.
- Immediately before merge, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1507/head refs/heads/develop` returned `bf7e7d3ecf8160ce4077c41bbc8768b5549d4066 refs/pull/1507/head` and `fe16127ac19526e7ed287fd8d4d3428fa2a4f174 refs/heads/develop`.
- GitHub PR API reported base `develop` at `fe16127ac19526e7ed287fd8d4d3428fa2a4f174`, head `bf7e7d3ecf8160ce4077c41bbc8768b5549d4066`, `mergeable=true`, and `mergeable_state=clean`. The fetched merge base is exactly `fe16127ac19526e7ed287fd8d4d3428fa2a4f174`; current develop is an ancestor of the candidate with no develop drift.
- The four commits in the candidate range are the 0427-176 lifecycle-lock changes. The current develop-based diff has 19 files, 835 additions and 53 deletions; the previously seen `internal/deployment` expansion is not in this current PR diff. No `.github/**` files are changed.

## Review against r2 findings

### Target-wide lock and fail-closed scan

- `internal/coreinstallation/lifecycle_lock.go:44-53` exports `AcquireTargetWideLifecycleLock` as a production wrapper around the stableid implementation.
- `internal/stableid/lock.go:111-135` acquires the shared `.installation.lock` before creating the per-app dotfile and releases the shared lock only after dotfile acquisition. This makes app-dotfile creation mutually exclusive with the target-wide scan critical section.
- `internal/stableid/lock.go:157-178` treats a missing deployments directory as empty but returns every other `ReadDir` error. `internal/stableid/lock.go:200-227` holds `.installation.lock` while scanning and returns an error on either an active app dotfile or scan failure; it never treats a read failure as an empty scan.
- `cmd/baha/application_lifecycle_lock.go:75-87` routes target-wide operations through this exported acquire path. Whole-target stop/destroy, Core installation, and target-definition change retain the returned lock until their operation finishes (`cmd/baha/control_plane_stop.go:45-50`, `cmd/baha/control_plane_destroy.go:101-106`, `cmd/baha/core_installation.go:69-73`, and `cmd/baha/target_definition_change.go:176-180`).

### Both regression directions

- `TestProductionTargetWideMutationCannotOverlapLocalAppLifecycle` at `cmd/baha/application_lifecycle_lock_test.go:252-292` acquires the local app through the production helper and attempts a target-wide operation through the same production seam; the target-wide operation must fail while the app dotfile is held.
- `TestProductionAppCannotBeginDuringTargetWideScan` at `cmd/baha/application_lifecycle_lock_test.go:294-331` holds the exported production target-wide lock+scan, verifies `AcquireAppLifecycleLock` cannot create the app dotfile while that scan is held, then verifies acquisition succeeds after release.
- `TestProductionTargetWideScanFailsClosedOnScanError` at `cmd/baha/application_lifecycle_lock_test.go:333-359` checks the exported scan path rejects an unreadable deployments namespace. It is skipped only when running as root because root bypasses the permission fixture.
- The production concurrency regression in `cmd/baha` and the lock primitive tests in `internal/stableid` are included in the hosted `PR · Validation · go-unit-tests` job. The exact run log shows this check executes `bash scripts/pr-unit-database.sh`, which runs `go test ./... -count=1`; trigger is the PR validation workflow. The same run passed this job, and Docker/Podman native destroy-retry jobs passed.

## Verdict

ROLLE: REVIEW
URTEIL: APPROVE

The current develop-based candidate closes the r2 production-scan gap, uses one shared critical section for app-dotfile creation and whole-target scanning, rejects scan errors, retains the lock through target-wide production mutations, and tests both directions. The exact current head has a terminal successful hosted run, including `go-unit-tests`, Docker and Podman native destroy-retry, and `PR Selected Checks`. Conditional native Keycloak/Core, selected-runtime, and release/source-pin jobs are reported as skipped, not passed.

## Merge record

ROLLE: MERGE

- Merge command and method: standard merge, without force or protection bypass.
- The PR head and develop witnesses above were fetched immediately before merge; terminal exact-head run: `42598253700`, URL https://github.com/mcpdev80/baseharbor/actions/runs/42598253700.
- Command: `gh pr merge 1507 --repo mcpdev80/baseharbor --merge`.
- GitHub API confirms PR #1507 merged at `2026-11-09T10:19:48Z`, merge commit `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`.
- Post-merge remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1507/head` returned `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop` and `bf7e7d3ecf8160ce4077c41bbc8768b5549d4066 refs/pull/1507/head`.

## repo-rule compliance

- Product files and workflow files were read-only during review; no checks were rerun.
- Evidence repository origin: `https://github.com/mcpdev80/baseharbor-plan.git`.
