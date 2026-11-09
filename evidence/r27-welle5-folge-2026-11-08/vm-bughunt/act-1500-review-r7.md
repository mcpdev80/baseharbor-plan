git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1500/head => fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop; 2370ad2984d8cc86e9a235db71952b0b429fa0a2 refs/pull/1500/head
gh pr view 1500 --repo mcpdev80/baseharbor --json state,mergeCommit => {"mergeCommit":null,"state":"OPEN"}

# CODEX-REVIEW 0427-165 r7 — PR #1500

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify live PR/develop refs, PR state, ancestry, and exact-head CI.
2. Check the target-wide lock path and orphan guard against #1507 and the r6 verdict.
3. Verify whether the new regression executes the actual target-definition detach while a local app lock is held.
4. Publish the review result to canonical baseharbor-plan main.

## Exact candidate and CI

- Live develop: `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`; live PR #1500 head: `2370ad2984d8cc86e9a235db71952b0b429fa0a2`.
- PR state is OPEN with `mergeCommit: null`. The PR reports `MERGEABLE/CLEAN`.
- `git merge-base --is-ancestor origin/develop origin/pr1500-r7` succeeds; the merge base is `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` and divergence is `0 1`. The candidate is one commit on the current develop tip.
- Run `42605735063` is terminal `completed/success` on the exact head: [run](https://github.com/mcpdev80/baseharbor/actions/runs/42605735063). `PR Selected Checks`, source format, go-unit-tests, deployment-package-tests, build, vet, gofmt, and both native destroy-retry jobs passed. Native Keycloak/Core and unrelated impact groups were skipped; skips are not treated as passes.

## Review against r6

1. **Current base and target-wide lock: passed.** `cmd/baha/target_definition_change.go:64-69` calls `lockExistingTargetDefinitionLifecycle` and rechecks the plan under the acquired lock before mutation. Its implementation at `:161-180` acquires `coreinstallation.AcquireTargetWideLifecycleLock(root)`, matching #1507. The orphan guard remains before the inventory/detach plan proceeds in `cmd/baha/target_definition_change_plan.go:132-170`; the refusal path does not prune records or detach the Target. `CollectableOrphans` identity checks and the previously approved refusal/test content are retained.
2. **#174 owner classification: passed.** Current `internal/deployment/deployment_list.go:73-85` retains `classifyOwnerWarning(err)` and the typed warning, rather than collapsing every owner failure into `missing`.
3. **Target-detach lock regression: not proven at the production mutation path.** `TestTargetDefinitionDetachHoldsSharedTargetWideLock` at `cmd/baha/target_definition_orphan_refusal_test.go:469-506` acquires a local per-app lifecycle lock, but then calls `lockExistingTargetDefinitionLifecycle` directly. It does not invoke `changeTargetDefinition` or the CLI detach handler, and it does not assert that the Target config and orphan records remain unchanged after a refused detach. Thus it proves the lock helper conflicts with the held app lock, but it would still pass if the production detach stopped calling that helper. The test comment describes stronger production-path coverage than the test performs.

## Correction and stop criterion

Extend the regression to invoke the real target-definition detach path while a local app lifecycle lock is held. Assert that the detach waits or fails closed because of the shared lock, and verify the Target definition and attached orphan record remain unchanged. The test must fail if the production detach path no longer routes through `lockExistingTargetDefinitionLifecycle` / `AcquireTargetWideLifecycleLock`. Keep the current exact develop ancestry, orphan guard, and #174 classification. Stop until this production-path regression is CI-covered and a terminal run on the resulting exact head passes `PR Selected Checks` and the relevant validation gates.

## Repo-rule compliance

- Product source and GitHub were read-only; no tests, reruns, approvals, or merges were performed.
- No `.github/**` files were changed. Merge decision remains with the owner.
- Evidence is in canonical baseharbor-plan, whose `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE 0427-165-r7-review: KORREKTUR for PR #1500 head 2370ad2984d8cc86e9a235db71952b0b429fa0a2; current develop and #174 semantics are present, but the lock regression tests only the helper, not the actual Target detach mutation.
