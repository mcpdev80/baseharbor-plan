# CODEX-REVIEW 0427-165 r8 — PR #1500

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify live PR head, branch, current base ancestry, and the terminal hosted run on the exact candidate.
2. Compare the r8 delta with the r7 correction recipe and inspect the shared target-wide lock path.
3. Recheck the fail-closed orphan identity checks and whether the new regression proves a lock-held target-wide mutation.
4. Record the exact-head verdict, correction recipe, and raw remote witnesses.

## Exact remote state and CI

Raw witnesses:

```text
$ git ls-remote origin refs/pull/1500/head
77064cfab2c1920f9dbc41fe9056037e9ebb5bfa	refs/pull/1500/head

$ gh pr view 1500 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url
{"baseRefName":"develop","headRefName":"0427-165-target-delete-orphanrec","headRefOid":"77064cfab2c1920f9dbc41fe9056037e9ebb5bfa","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1500"}
```

- PR #1500 is open on branch `0427-165-target-delete-orphanrec`; live head is `77064cfab2c1920f9dbc41fe9056037e9ebb5bfa`.
- Current `develop` `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor of the candidate. The candidate is the r7 parent plus the r8 regression change.
- Run `42609509644` is terminal `completed/success` on exact head `77064cfab2c1920f9dbc41fe9056037e9ebb5bfa`: https://github.com/mcpdev80/baseharbor/actions/runs/42609509644. `PR Selected Checks`, `go-unit-tests`, `deployment-package-tests`, build, vet, gofmt, and native destroy-retry Docker/Podman succeeded. Targeted HA and several unrelated impact cells were skipped; skips are not passes.
- The named `165-akte-round-8.md` was not present in the available Planning checkout/workspace search. This verdict is based on the r7 review recipe, the r7 evidence, and the exact current PR candidate.

## Review against r7 correction recipe

1. **Production Target-definition path and #1507 shared lock: retained in the current base.** The PR's r8 delta changes only `cmd/baha/target_definition_orphan_refusal_test.go`. The production `lockExistingTargetDefinitionLifecycle` still calls `coreinstallation.AcquireTargetWideLifecycleLock(root)` (`cmd/baha/target_definition_change.go:161-180`), and `changeTargetDefinition` acquires it before re-reading the plan and mutating the configuration (`:64-82`). No target-definition production code was altered by r8.

2. **Fail-closed identity checks: pass.** `deployment.CollectableOrphans` requires the decoded deployment UUID to equal the directory name and the decoded Target to equal the requested Target exactly, without trimming (`internal/deployment/deployment_list.go:112-127, 173-191`). Mismatched, blank, missing, and whitespace-padded identities are excluded. The owner-missing guard still refuses detach when an ownerless deployment directory exists. Unit and target-delete regressions cover mismatched UUID, blank/missing fields, padded values, and canonical matching records.

3. **Lock-held target-wide mutation regression: not proven.** `TestTargetDefinitionDetachHoldsSharedTargetWideLock` now calls production `deleteTarget` while holding a local per-app lock and checks that Target configuration and the orphan file remain unchanged (`cmd/baha/target_definition_orphan_refusal_test.go:468-550`). But it first removes the Core runtime owner and seeds a genuine collectable orphan (`:491-507`). `buildTargetDefinitionChangePlan` returns the orphan refusal before `changeTargetDefinition` reaches `lockExistingTargetDefinitionLifecycle` (`cmd/baha/target_definition_change_plan.go:132-169`, then `cmd/baha/target_definition_change.go:64-70`). The test explicitly accepts `target_definition_collectable_orphans` as a valid outcome (`target_definition_orphan_refusal_test.go:535-539`). Thus it passes without acquiring or contending on `AcquireTargetWideLifecycleLock`; the intended lock-held mutation behavior is untested.

## Correction recipe and stop criteria

- Keep the current production target-definition route through `AcquireTargetWideLifecycleLock` and preserve the exact raw identity checks.
- Split the regression conditions so the lock assertion cannot be satisfied by the orphan guard. For the lock case, seed a valid Target state with no collectable orphans, hold the local per-app lifecycle lock, and invoke the production detach path. Assert a specific lock-contention refusal (or bounded wait followed by refusal), prove the Target definition and relevant target-wide state remain unchanged, and ensure `target_definition_collectable_orphans` is not accepted in that case.
- Retain a separate production-path orphan refusal test for the ownerless record case. The lock regression must fail if the production detach stops acquiring `AcquireTargetWideLifecycleLock`.
- Stop review until the lock-specific regression is added and CI-covered, then confirm terminal required checks on the resulting exact HEAD. No merge or approval was performed.

## Repo-rule compliance

- Product source and GitHub were read-only; no tests, reruns, workflow dispatches, approvals, or merges were performed.
- The product checkout had unrelated untracked `cmd/baha/app_prune.go` and `cmd/baha/app_prune_test.go`; they were left untouched. The PR was inspected using a separate fetched review ref without checkout.
- No `.github/**` changes were made by the reviewed r8 delta.

END_DONE 0427-165-r8-review: KORREKTUR PR #1500 head 77064cfab2c1920f9dbc41fe9056037e9ebb5bfa; exact-head run 42609509644 succeeded and fail-closed identity checks remain correct, but the new regression can pass at the orphan guard before exercising the shared target-wide lock.
