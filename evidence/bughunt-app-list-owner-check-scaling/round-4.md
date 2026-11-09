# 0427-178 round-4 — batched owner-load classifies access-denied like VerifyDeploymentOwner

Shift: worker (worker-ornith1.5-laptop) · Date: 2026-11-09
Card: t-20261108-bughunt-app-list-owner-check-scaling (0427-178)
Mission: /tmp/opencode/mission-178-r4.md
Branch: `0427-178-r2-pr1508` on PR #1511
Base: `97c0f1ed95698524ffe2a0f8edca89efc4b90711` (PR #1511 head, the approved r2 candidate). `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` (develop) is an ancestor of the branch head and of my fix commit.
Plan repo origin/main HEAD: pinned before first evidence commit (`git fetch origin && git ls-remote origin/main`); planning main is actively rewritten by the Coordinator.
Repo: mcpdev80/baseharbor (product), worktree `/tmp/opencode/0427-178-r4-wt`

## PLAN

- Round out PR #1511 (KORREKTUR block from act-1511-review.md): the batched owner-load (`ownerBatch.loadOwner`) folded EVERY load error except `os.ErrNotExist` into `ErrDeploymentOwnerForeign`, mis-classifying an unreadable Core installation as a foreign owner.
- Reuse the central owner-load classification (`deployment_owner_classification.go` / `VerifyDeploymentOwner`) in `loadOwner`: `os.ErrNotExist` stays Missing, a read failure is `ErrDeploymentOwnerAccessDenied`, a present-but-malformed installation is `ErrDeploymentOwnerMalformedState`, and only a positively-loaded identity whose Target diverges is foreign.
- Add a CI-covered regression that deterministically fails `resolveInstallationLoad` for the target-owner with `os.ErrPermission` and asserts correct classification in the batch-list path (best-effort and normal).
- Keep the delta minimal (only the two files); keep `TestBatchedListClassifiesAccessForeignMissing` unchanged and green.
- Hosted run terminal on the exact fixed head; skipped as skipped; ls-remote + cleanliness.

## Fix (content delta)

File: `internal/deployment/deployment_list_owner_batch.go`, `ownerBatch.loadOwner`.

- Before: the `else if err != nil` branch returned `ErrDeploymentOwnerMissing` only for `os.ErrNotExist`, and `ErrDeploymentOwnerForeign` for every other error — so a permission/open failure on `installation.json` became a foreign owner.
- After: the branch now reuses the central classification. `os.ErrNotExist` → `ErrDeploymentOwnerMissing`; `isAccessDeniedLoadError(err)` → `fmt.Errorf("%w: %w", ErrDeploymentOwnerAccessDenied, err)`; `isMalformedInstallationLoadError(err)` → `fmt.Errorf("%w: %w", ErrDeploymentOwnerMalformedState, err)`; otherwise `ErrDeploymentOwnerForeign`. Added the `fmt` import.
- This is byte-identical in classification to the single-record path (`VerifyDeploymentOwner`, `deployment_store.go`), restoring the card-174 declaration the rebase had lost from the batched path.

## Test (CI-covered regression)

New test `TestBatchedListClassifiesAccessDeniedFileError` in `internal/deployment/deployment_list_owner_scale_test.go`:

- Injects a deterministic `os.ErrPermission` at the authoritative installation-load seam via the package-internal `testLoadInstallationForOwner` seam (independent of root-dependent file permissions on CI runners).
- Runs for both `bestEffort=true` and `bestEffort=false`:
  - Best-effort: the per-record warning is Kind `"access"` with `errors.Is(ErrDeploymentOwnerAccessDenied)` and preserves the underlying permission error; zero records returned.
  - Normal: `batch.err` is set, zero records returned, fails with `ErrDeploymentOwnerAccessDenied` and is never `ErrDeploymentOwnerForeign` or `ErrDeploymentOwnerMissing`.
- The once-per-Target load bound (`batch.loads == 1`) is preserved.
- Existing `TestBatchedListClassifiesAccessForeignMissing` (resolver-injection case) left unchanged and green; the full deployment suite passes.
- Negative-verified: reverting `loadOwner` to the buggy fold-to-foreign makes the test fail on both subtests.

### CI coverage statement

- The new test lives in `internal/deployment/` and runs in the normal `go-unit-tests` job (`go test ./...`); it is also covered by the path-selected `PR · Validation · deployment-package-tests` job (`go test ./internal/deployment/...`).
- Job `PR · Validation · deployment-package-tests` for run `42599582591` on head `066436e`: executed, **success**. No `.github/**` edit was needed; the existing go-unit-tests / deployment-package-tests groups already cover `internal/deployment/`.
- Trigger: `pull_request` on PR #1511 (base develop), selected by the CI PR path matrix. No Owner-scope workflow edit required.

## Hosted CI (witnessed, terminal)

- PR #1511 head `066436e2f9d1fd2743a2d50604d05b360e5944c3` (branch `0427-178-r2-pr1508`), base develop `942111d5a`, open, mergeable.
- Run `42599582591` `CI · PR #1511`: **completed / success**, head `066436e`.
- Job summary: 11 success (executed), 13 skipped, **0 failing/cancelled**.
- Executed (not skipped): go-unit-tests (via PR Selected Checks + deployment-package-tests), cli-vet, cli-guided-tests, cli-build, source-format, source-contracts, trusted-plan, native impact-selection, focused-python.
- Skipped (correctly not counted): native docker/podman destroy-retry, native Keycloak/Core, Targeted HA docker/podman, consumer/demo pins, runner interface, selected runtime, exact-candidate, `validate`.
- My new test executed within deployment-package-tests (success).

## Drift against develop HEAD

- Branch base `97c0f1ed` (the approved r2 PR head). Only my single fix commit `066436e2f` sits on top (`git log --oneline 97c0f1ed..066436e2f`). `git merge-base --is-ancestor 942111d5a HEAD` -> 0. One integration candidate per chain: single branch `0427-178-r2-pr1508`.

## Cleanliness

No containers / compose projects started (pure Go unit-fix; required test is a Go unit test). State dir isolated under `/tmp/opencode/0427-178-r4-wt`. No baseharbor containers running (`docker ps` witness).

## Repo-rule compliance

- Write-set: only `internal/deployment/deployment_list_owner_batch.go` (fix) and `internal/deployment/deployment_list_owner_scale_test.go` (new test). No `.github/**` edit (Owner scope).
- Branch provenance: `0427-178-r2-pr1508` base `97c0f1ed` (approved r2 head); only my fix commit `066436e2f` on top. Remote witness: `git ls-remote origin 0427-178-r2-pr1508` == PR #1511 head == `066436e2f9d1fd2743a2d50604d05b360e5944c3`.
- One integration candidate per chain.
- Evidence lives only in baseharbor-plan (planning repo) at evidence/bughunt-app-list-owner-check-scaling/round-4.md. No evidence files in the product repo.
- No subagents (Owner directive 2026-11-04). All steps run in this session.

## Status
DONE — batched owner-load reuses the central #174 classification; new CI regression `TestBatchedListClassifiesAccessDeniedFileError` green and negative-verified; PR #1511 head `066436e`; hosted run `42599582591` terminal success (deployment-package-tests executed+passed, skipped as skipped, 0 failures). Evidence pushed.

## Terminal run (reproduced below)
```
$ git ls-remote origin 0427-178-r2-pr1508
066436e2f9d1fd2743a2d50604d05b360e5944c3  refs/heads/0427-178-r2-pr1508
$ git ls-remote origin refs/pull/1511/head
066436e2f9d1fd2743a2d50604d05b360e5944c3  refs/pull/1511/head
$ git merge-base --is-ancestor 97c0f1ed95698524ffe2a0f8edca89efc4b90711 066436e2f9d1fd2743a2d50604d05b360e5944c3
$ git log --oneline 97c0f1ed95698524ffe2a0f8edca89efc4b90711..066436e2f9d1fd2743a2d50604d05b360e5944c3
066436e2f fix(deployment): batched owner-load classifies access-denied like VerifyDeploymentOwner
$ gh api 'repos/mcpdev80/baseharbor/actions/runs/42599582591/jobs' --jq '{skipped:(.jobs|map(select(.conclusion=="skipped"))|length), success:(.jobs|map(select(.conclusion=="success"))|length), failing:(.jobs|map(select(.conclusion!="skipped" and .conclusion!="success"))|length)}'
{"failing":0,"skipped":13,"success":11,"total":24}
```

## END
0427-178 r4 DONE — PR #1511 head `066436e2f` (branch `0427-178-r2-pr1508`); batched owner-load reuses central #174 classification (Missing / AccessDenied / MalformedState / Foreign); new CI regression `TestBatchedListClassifiesAccessDeniedFileError` green (negative-verified); hosted run `42599582591` terminal success (deployment-package-tests executed+passed, 13 skipped as skipped, 0 failures). Evidence: baseharbor-plan evidence/bughunt-app-list-owner-check-scaling/round-4.md (pushed origin/main).
