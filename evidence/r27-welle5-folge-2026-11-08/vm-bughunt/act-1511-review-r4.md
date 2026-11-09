git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1511/head => fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop; 066436e2f9d1fd2743a2d50604d05b360e5944c3 refs/pull/1511/head
gh pr view 1511 --repo mcpdev80/baseharbor --json state,mergeCommit => {"mergeCommit":null,"state":"OPEN"}

# CODEX-REVIEW 0427-178 r4 — PR #1511

ROLLE: REVIEW

URTEIL: APPROVE, r4 delta only. This is not merge authorization.

## PLAN

1. Verify the live PR head, PR state, develop head, and terminal exact-head run.
2. Inspect only the r4 delta from `97c0f1ed95698524ffe2a0f8edca89efc4b90711`.
3. Trace owner-load classification, best-effort and strict-list behavior, regression coverage, and CI routing.
4. Publish the review verdict and remote evidence in this planning file.

## Remote candidate and checks

- `git ls-remote` reports live develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` and PR #1511 head `066436e2f9d1fd2743a2d50604d05b360e5944c3`.
- `gh pr view 1511 --json state,mergeCommit` reports `OPEN` and `mergeCommit: null`. GitHub reports the PR base as `develop`, head `066436e2f9d1fd2743a2d50604d05b360e5944c3`, mergeable `MERGEABLE`, merge state `CLEAN`.
- Exact delta `97c0f1ed9..066436e2f` touches only `internal/deployment/deployment_list_owner_batch.go` and `internal/deployment/deployment_list_owner_scale_test.go` (18 insertions in production; 98 test insertions). No other file changed in this delta.
- Run `42599582591` is terminal `completed/success` on exact head `066436e2f9d1fd2743a2d50604d05b360e5944c3`: [run](https://github.com/mcpdev80/baseharbor/actions/runs/42599582591). `PR · Validation · deployment-package-tests` job `129100511036` passed; `PR Selected Checks` job `129101034461` passed. Source format, cli-guided-tests, source-contracts, build and vet also passed. Native Keycloak/Core and other unrelated runtime groups were skipped; no skipped result is counted as a pass.
- The PR base/merge base is `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`, while live develop is `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`. This verdict accepts only the r4 code delta; it does not claim that the old-base candidate is ready to land on today's develop.

## Review of the r4 delta

`ownerBatch.loadOwner` now distinguishes the authoritative owner-load errors instead of treating every non-`os.ErrNotExist` error as foreign. At `internal/deployment/deployment_list_owner_batch.go:102-123`, missing remains `ErrDeploymentOwnerMissing`; `isAccessDeniedLoadError` wraps `ErrDeploymentOwnerAccessDenied` while preserving the filesystem cause; `isMalformedInstallationLoadError` returns the separate malformed-state sentinel; only the residual load error remains foreign. The code reuses the same access/malformed predicates used by the #174 single-record path. Successful owner loads still call `verifyDeploymentOwnerAgainstInstallation` per deployment (`:128-132`), so the batch caches the Target owner state rather than a per-record authorization verdict.

The new `TestBatchedListClassifiesAccessDeniedFileError` at `internal/deployment/deployment_list_owner_scale_test.go:385-470` injects a deterministic permission-denied result at the owner installation-load seam. For best-effort listing it asserts no record is returned, a warning is emitted with the access classification, the warning unwraps to both `ErrDeploymentOwnerAccessDenied` and the underlying permission error, and it is not foreign. For strict listing it asserts zero records, the access-denied sentinel, and neither foreign nor missing classification. Both modes assert exactly one owner-load attempt. This closes the precise r2 gap: the test exercises an owner-file load failure, rather than only a tenant resolver denial.

The test is durable CI evidence: `scripts/pr-incremental-reuse.py:31` maps `deployment-package-tests` to `./internal/deployment/...`; the PR workflow selects that validation group for deployment-package changes, and the exact-head job `129100511036` passed. `PR Selected Checks` also passed on the same run.

## Verdict and stop conditions

The r4 delta resolves the blocking r2 finding. I approve this delta on exact head `066436e2f9d1fd2743a2d50604d05b360e5944c3`. No code correction is required for this delta.

Before landing, the owner should refresh/revalidate against the live develop head and require terminal checks for that resulting exact candidate. Current develop advanced beyond the PR base. Merge authority is expressly outside this review; no approval action or merge was performed.

## Repo-rule compliance

- Product repository was read-only. No tests, reruns, workflow dispatches, approvals, or merges were performed.
- No `.github/**` files were changed.
- Evidence is in the canonical planning repository with origin `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE 0427-178-r4-review: APPROVE r4 delta only on PR #1511 head 066436e2f9d1fd2743a2d50604d05b360e5944c3; exact run 42599582591 succeeded including deployment-package-tests and PR Selected Checks. PR remains OPEN; merge authority belongs to the owner.
