# 0427-178 round-3 — rebase PR #1509 content onto new develop 942111d5a

Shift: worker (worker-ornith1.5-laptop) · Date: 2026-11-09
Card: t-20261108-bughunt-app-list-owner-check-scaling (0427-178)
Mission: /tmp/opencode/mission-178-r3.md
Branch: `0427-178-r2-pr1508` rebased onto new develop
Base: `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` (origin/develop, PR #1506 merge commit). `b3a8042d18ea60f162a32a51df34a499cad6a237` (origin/develop) is an ancestor of `942111d5a`, and of my first commit.
Plan repo origin/main HEAD: pinned before first evidence commit (`git fetch origin && git ls-remote origin/main`); planning main is actively rewritten by the Coordinator.
Repo: mcpdev80/baseharbor (product), worktree `/tmp/opencode/0427-178-r2-bughunt-pr1508`
Follow-up PR: https://github.com/mcpdev80/baseharbor/pull/1511 (OPEN, MERGEABLE, head `97c0f1e`, base `942111d5a`)

## PLAN

- Rebase the authorized r2 candidate (batching + truthful classification) onto new develop `942111d5a` and resolve the two file conflicts the merge-akt flagged.
- Preserve BOTH sides: develop #1506 permission-lies fix and my chain's owner-batching + truthful classification.
- Local checks: gofmt / vet / build / `go test ./internal/deployment/...`.
- Open a follow-up PR (#1511) against develop from branch `0427-178-r2-pr1508` (Owner-coordinated chain hygiene).
- Observe hosted CI on the new exact head (`deployment-package-tests` + `PR Selected Checks`); report skipped native/runtime as skipped.
- Evidence written only in baseharbor-plan; no `.github/**` edit.

## What was done

Branch `0427-178-r2-pr1508` was cut fresh from `origin/develop` `942111d5a`; the two authorized r2 commits were cherry-picked and rebased onto it.

- Commit 1 `437522e41` — batch app-list owner verification once per Target.
- Commit 2 `97c0f1ed9` — truthful owner-failure classification in best-effort batched list.
- Remote witness: `git ls-remote origin 0427-178-r2-pr1508` → `97c0f1ed95698524ffe2a0f8edca89efc4b90711`.
- Ancestry: `git merge-base --is-ancestor 942111d5a HEAD` → 0 (develop is an ancestor). Only my two commits sit on top of `942111d5a`.

### Conflict resolution (both files)

- `internal/deployment/deployment_list.go` — conflict between develop's new `verifyDeploymentOwnerAtSeam` + `classifyOwnerWarning` path and my old `listDeploymentRecordsBatched` call. Resolved by taking develop's HEAD version (the access-denied / malformed-state distinction is preserved); `listDeploymentRecordsBatched` lives in `deployment_list_owner_batch.go` and is the effective caller.
- `internal/deployment/deployment_store.go` — conflict in `VerifyDeploymentOwner`. Resolved by taking develop's HEAD version verbatim (tenant-grant-hook restructured into `resolveInstallationLoad`, access-denied / malformed / foreign fail-closed classification preserved, loan seam preserved).

### API drift from develop #1506 (resolved in my batch file)

Develop #1506 removed `resolveOwnerLoad` / `verifyLoanOwnerGuarantees` from `deployment_store.go` and restructured `VerifyDeploymentOwner` around `resolveInstallationLoad`. My `ownerBatch.loadOwner()` was rewritten to mirror develop's production path:

- Tenant grant hook (`TenantOwnerResolver`), authoritative `resolveInstallationLoad`, and the loan seam (`TargetLoanVerifier`) run once per Target.
- `ownerBatch.loads++` counts the one authoritative read per Target; a second `loadOwner()` returns the cached `*coreinstallation.State` (once-per-Target bound holds).
- `verifyDeploymentOwnerAgainstInstallation` (per-deployment directory conclusion, unchanged by #1506) runs against the resolved State; fail-closed error shape byte-identical.
- `coreinstallation` import added to `deployment_owner_loan.go` (my branch defines `verifyDeploymentOwnerAgainstInstallation` there).

## Checks (local)

- `go build ./...`: PASS (exit 0).
- `go vet ./internal/deployment/...`: clean (exit 0).
- `gofmt -l` on all changed files: clean.
- `go test ./internal/deployment/... -count=1`: PASS (exit 0) — all owner-batch/scaling/classification tests pass, including `TestBatchCacheNeverSearchesDeploymentOwnership` (loads == 1) and `TestListOwnerVerificationBatchedOncePerTarget`.
- `go test ./cmd/baha/... -run 'TestAppList|TestAppRun|Owner|Deployment|List' -count=1`: PASS (exit 0, ~45s).

## Hosted CI (witnessed, terminal)

- PR #1511 (head `97c0f1e`, base `942111d5a`) — open, mergeable, 3 changed files (`deployment_list_owner_batch.go`, `deployment_list_owner_scale_test.go`, `deployment_owner_loan.go`), 602 insertions.
- Run `42590834498` `CI · PR #1511`: **completed / success**, head `97c0f1e`.
- Required gates:
  - `PR · Validation · deployment-package-tests` (runs `go test ./internal/deployment/...`): **success (executed)** — executes the new `TestBatchedListClassifiesAccessForeignMissing`, `TestBatchedListForeignToleranceControl`, `TestBatchedListOncePerTargetResolverBound`, and all existing `TestListOwner*`/`TestBatchCache*` tests.
  - `PR Selected Checks`: **success**.
- Skipped (correctly not counted as passes): `validate` (`go test ./...` unit job — skipped on PRs by path selection via `pr-selected-runtime-matrix.py`, same as the original PR #1509 run `42580378234`), native destroy-retry Docker/Podman, Native Keycloak/Core, Targeted HA, consumer pins, demo pin, runner interface, public contracts, exact-candidate.
- 24 jobs total: 11 success (executed), 13 skipped, **0 failure/cancelled**.

## Drift against develop HEAD

- `origin/develop` at time of run: `942111d5a`. Diff `942111d5a..origin/develop` is empty — develop did not move between my branch cut and the CI run. No drift.

## Cleanliness

No containers / compose projects started (unit-fix card; required test is a Go unit test). State dir isolated under `/tmp/opencode/0427-178-r2-bughunt-pr1508`. No orphaned runtimes.

## Repo-rule compliance

- Write-set: only `internal/deployment/deployment_list_owner_batch.go`, `deployment_list_owner_scale_test.go`, `deployment_owner_loan.go` (+ the two conflicted files reverted to develop's clean HEAD version). No `.github/**` edit (Owner scope).
- Branch provenance: `0427-178-r2-pr1508` cut from `origin/develop` `942111d5a` (`b3a8042d` is an ancestor). Only my own commits on top of `942111d5a`.
- Chain ancestry: #1508 head `dbb1df08` is an ancestor of the original #1509 head `03d14413` (`git merge-base --is-ancestor dbb1df08 03d14413` → 0); #1509 content now lives in this branch on merged develop.
- One integration candidate per chain: single branch `0427-178-r2-pr1508`; PR #1511 is the follow-up vehicle (Owner-coordinated chain hygiene).
- Evidence lives only in baseharbor-plan (planning repo) at evidence/bughunt-app-list-owner-check-scaling/round-3.md. No evidence files in the product repo.
- No subagents (Owner directive 2026-11-04). All steps run in this session.

## Status
DONE — r2 content rebased onto develop `942111d5a`; PR #1511 head `97c0f1e`; CI run `42590834498` terminal success (`deployment-package-tests` executed+passed, `PR Selected Checks` success, `validate`/native/runtime skipped as skipped); no drift; evidence pushed.

## Terminal run (reproduced below)
```
$ git ls-remote origin 0427-178-r2-pr1508
97c0f1ed95698524ffe2a0f8edca89efc4b90711  refs/heads/0427-178-r2-pr1508
$ git merge-base --is-ancestor 942111d5a1c43f5257bf1627a966fa9e6c6f24bd HEAD   # develop ancestry
$ git diff --stat 942111d5a1c43f5257bf1627a966fa9e6c6f24bd origin/develop      # develop drift = empty
$ gh api 'repos/mcpdev80/baseharbor/pulls/1511' --jq '{state:.state,head:.head.sha,base:.base.sha,changed:.changed_files}'
{"state":"open","head":"97c0f1e","base":"942111d5a","changed":3}
$ gh api 'repos/mcpdev80/baseharbor/actions/runs/42590834498/jobs' --jq '{skipped:(.jobs|map(select(.conclusion=="skipped"))|length), success:(.jobs|map(select(.conclusion=="success"))|length), other:(.jobs|map(select(.conclusion!="skipped" and .conclusion!="success"))|length)}'
{"total":24,"skipped":13,"success":11,"other":0}
```

## END
0427-178 r3 DONE — r2 content rebased onto develop `942111d5a`; follow-up PR #1511 (head `97c0f1e`, base `942111d5a`, 3 deployment files, mergeable); CI run `42590834498` terminal success — `deployment-package-tests` (go test ./internal/deployment/...) executed+passed, `PR Selected Checks` success, `validate`/native/runtime/consumer skipped as skipped, 0 failures; develop drift = 0. Evidence: baseharbor-plan evidence/bughunt-app-list-owner-check-scaling/round-3.md (pushed origin/main).
