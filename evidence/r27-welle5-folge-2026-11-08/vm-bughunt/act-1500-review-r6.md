git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1500/head => fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop; f966505cda93aa35da60ad65afee5e885e4886c9 refs/pull/1500/head
gh pr view 1500 --repo mcpdev80/baseharbor --json state,mergeCommit => {"mergeCommit":null,"state":"OPEN"}

# CODEX-REVIEW 0427-165 r6 — PR #1500

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify the exact remote PR head, develop head, PR state, and hosted run.
2. Compare the r5 candidate with r6 and inspect the orphan-refusal delta plus its interaction with #174 and #1507.
3. Record a SHA-specific verdict and actionable correction recipe in this file.
4. Publish the review evidence to canonical baseharbor-plan main and verify the remote tree witness.

## Candidate and hosted evidence

- PR #1500 is OPEN at exact head `f966505cda93aa35da60ad65afee5e885e4886c9`; `mergeCommit` is null. The PR is reported mergeable/clean, but its checked-out candidate is not based on current develop.
- Live `develop` is `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`. The PR candidate's merge base is `e072e142ec9511f3cc86ffa67c7debd022d7760a`; `git merge-base --is-ancestor origin/develop origin/pr1500` exits 1, and the left/right divergence is `6 6`. The PR API's base SHA is `fe16127ac19526e7ed287fd8d4d3428fa2a4f174`, also behind live develop. The r6 run therefore does not include the later #1507 integration.
- Run `42598338207` is `completed/success` on exact head `f966505cda93aa35da60ad65afee5e885e4886c9` (`pull_request`): [run](https://github.com/mcpdev80/baseharbor/actions/runs/42598338207). `PR Selected Checks`, `PR · Source format`, `PR · Validation · go-unit-tests`, `deployment-package-tests`, `go-build`, `go-vet`, and `cli-gofmt` passed. Native destroy-retry Docker and Podman passed. Native Keycloak/Core Docker and Podman also executed and passed. The aggregate `validate` job and unrelated impact groups were skipped; they are not counted as passes. No failures or pending jobs were reported by this run.

## R6 delta and integration review

The r6 change moves `ErrTargetDetachedWithOrphans` and its comment out of `internal/deployment/deployment_store.go` into `internal/deployment/deployment_orphan_refusal.go`; the candidate's store file is 790 lines. This is a behavior-neutral extraction that addresses the source-readability limit. The orphan refusal, collectable-record identity checks, and their tests remain intact: `cmd/baha/target_definition_change_plan.go`, `cmd/baha/target_definition_orphan_refusal_test.go`, and `internal/deployment/collectable_orphans_test.go` are unchanged from the previously approved r5 head `64d621f40e85402b92805d64b65647ca8dc304f1`.

The #174 owner-state classification remains present in `internal/deployment/deployment_list.go`: the best-effort path calls `classifyOwnerWarning(err)` and records that kind instead of folding every owner error into `missing`. The new `CollectableOrphans` reader is present alongside that classification. This portion is compatible with the #174 access/malformed-state behavior.

The #1507 lifecycle-lock integration is not present in this PR head. In `cmd/baha/target_definition_change.go:161-176`, the candidate's `lockExistingTargetDefinitionLifecycle` returns `coreinstallation.AcquireLifecycleLock(root)`. Current develop's corresponding function at lines 161-180 uses `coreinstallation.AcquireTargetWideLifecycleLock(root)`, with comments stating that a target-definition mutation must coordinate with local app lifecycle locks and fail closed if one is running. Current develop gained this code in #1507, after the candidate's base `e072e142e`. Consequently, the exact-head run 42598338207 cannot prove the combined behavior against #1507, and its green results do not validate current develop integration.

## Actionable correction recipe

- Refresh PR #1500 onto the live develop head `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` and resolve the `target_definition_change.go` overlap by retaining #1507's `AcquireTargetWideLifecycleLock(root)` in `lockExistingTargetDefinitionLifecycle`. Do not restore the narrower `AcquireLifecycleLock` call.
- Preserve the #174 `classifyOwnerWarning` distinction and the orphan guard's fail-closed identity checks during the rebase. Keep the current behavior-only file extraction; do not weaken the readability audit.
- Add or retain a production-path regression that holds a local app lifecycle lock while attempting target-definition detach and proves the target-wide mutation waits or refuses without changing the Target config or orphan records. The regression must distinguish the shared target-wide lock from a per-operation lock and run in the hosted `go-unit-tests` group. The existing #1507 generic lock regression alone does not show that this Target command is wired through the shared lock after the rebase.
- Stop until the current develop head is an ancestor of the refreshed candidate and a terminal exact-head PR run passes `PR Selected Checks`, source format, unit and deployment-package tests, and the applicable native gates. Report any skipped job as skipped. Only then is a new merge review eligible.

## Repo-rule compliance

- Product repository was read-only; no tests, reruns, workflow dispatches, approvals, or merges were performed.
- No `.github/**` files were changed.
- Evidence destination is the canonical planning repository whose `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE 0427-165-review-r6: KORREKTUR for PR #1500 head f966505cda93aa35da60ad65afee5e885e4886c9; exact-head run 42598338207 succeeded, but current develop fea92f379 is not an ancestor and the candidate retains AcquireLifecycleLock instead of #1507's AcquireTargetWideLifecycleLock. No merge performed.
