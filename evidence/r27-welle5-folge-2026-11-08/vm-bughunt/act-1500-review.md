# CODEX-REVIEW 0427-165 — PR #1500

ROLLE: REVIEW  
URTEIL: KORREKTUR  
Reviewed candidate: `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5`  
Base: `develop` at `20902f0a6ab016fd8fe6a501751e1becc5f334dd`  
PR: `https://github.com/mcpdev80/baseharbor/pull/1500`  
Hosted PR run: `42519204316` (terminal failure, associated with the exact candidate)

## PLAN

1. Freeze the current PR head and base, and inspect the exact candidate diff.
2. Trace the refusal, collection guidance, stable deployment UUID handling, and no-write behavior.
3. Verify regression coverage in hosted CI and inspect every failed native job and skipped check.
4. Publish this review in the Planning repository and verify both remote heads remain unchanged.

## Findings

### Blocking: the refusal recommends two paths that do not collect these records

`cmd/baha/target_definition_change_plan.go:155-166` names every returned record and refuses with `target_definition_collectable_orphans`. The guard executes before `ListDeployments`; for the ownerless orphan case it therefore improves the diagnostic and keeps the detach from reaching the write path.

The remediation is internally contradictory and not executable as written:

- `baha destroy --all` enters `destroyInstallation` (`cmd/baha/runtime_destroy_all.go:93-115`). That path discovers entries through `ListAllDeploymentsForDisplay`; ownerless records fail the installation-owner check and become `SKIPPED` warnings (`runtime_destroy_all.go:388-417`). The candidate's own `deployment_store.go:33-44` also says this destroy path lists them as `SKIPPED`. It does not collect them.
- `baha app destroy --uuid <id> --full-reset --yes` is not an available route from the `app destroy` command. Although `--uuid` support was added by `d8849198265f13d34e1ece95d6982ce6b613d2aa` in the common resolver, `newApplicationDestroyExecution` (`cmd/baha/app_destroy_lifecycle.go:51-65`) calls `extractApplicationEnvironment`, then `parseDestroyArgs`, and passes only the optional positional NAME to `resolveApplicationEnvironment`. The UUID is consumed and removed by `extractApplicationEnvironment` (`cmd/baha/app_context.go:549-563`) and is never forwarded from this destroy path. `parseDestroyArgs` accepts only `--yes`, `--full-reset`, and one NAME (`cmd/baha/app_lifecycle.go:327-346`). Thus the specifically recommended UUID selector cannot select a record here.
- Even if the selector were threaded through, the ownerless record cannot currently pass the fail-closed owner seam until its authoritative installation owner is restored. The remediation must not imply that a target-definition recovery file alone restores that owner.

The refusal text says to “collect” with `destroy --all` while parenthetically saying those records are `SKIPPED`; `Next` repeats the same false instruction. This is a blocking usability and acceptance defect: operators are directed to commands that preserve the orphan, not collect it.

### Blocking: the UUID regression fixture violates the storage identity contract

The candidate correctly stores the `DeploymentID` from the decoded record in the displayed IDs (`target_definition_change_plan.go:145-159`), but `CollectableOrphans` reads ownerless JSON directly and appends it without validating its identity against the storage path (`internal/deployment/deployment_list.go:134-151`). The normal loader explicitly rejects a record whose target or deployment UUID does not match its path (`internal/deployment/deployment_store.go:585-587`).

The command test's fixture is mismatched: it writes the record under `deployments/orphan1` (`target_definition_orphan_refusal_test.go:25`) while embedding the UUID `11111111-1111-4111-8111-111111111111` (`:32-38`), then asserts that embedded value is printed. It therefore does not prove the stable path UUID contract established by #1475 / `d88491982`; it demonstrates that the new helper trusts an inconsistent JSON identity. The deployment-package test uses a matching directory and UUID, but does not exercise the command refusal or mismatch case.

### No silent prune or destroy: verified

The candidate adds a read-only orphan inventory and returns a typed refusal before `ListDeployments` or any target-definition persistence. `TestTargetDeleteRefusesWhileCollectableOrphansAttached` verifies the target configuration remains and that no recovery file is written (`cmd/baha/target_definition_orphan_refusal_test.go:66-105`). The clean-target regression verifies that the guard is clear when no orphan exists (`:107-127`). No new destroy, prune, record-delete, or runtime-cleanup call is introduced in the candidate diff.

## CI and hosted state

GitHub reports run `42519204316` for the exact PR head as terminal `failure`; `gh pr checks` also reports `PR Selected Checks: fail`. The relevant test routing did run on the pull-request trigger:

- `TestTargetDeleteRefusesWhileCollectableOrphansAttached`, `TestTargetDeleteProceedsWithoutOrphans`, and the command-side UUID assertion are included in `go-unit-tests`; its log reports `ok github.com/mcpdev80/baseharbor/cmd/baha` and `ok github.com/mcpdev80/baseharbor/internal/deployment`.
- The deployment regressions are also selected by `deployment-package-tests`; its log reports `matched_tests: ["./internal/deployment"]` and the job passed.
- These are package-wide executed suites, not skipped jobs. The hosted run did not print individual test names because the commands are non-verbose.

Failed gates and classification:

- `PR · Native destroy retry · docker` (job `128848810725`) failed `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`. Hosted log line: `installation_destroy_native_test.go:229: freshly acknowledged installation retry failed full destroy did not complete; 3 cleanup result(s) require attention and BaseHarbor state was preserved`. The candidate refusal is structurally unreachable from this test: `CollectableOrphans` is called only from `buildTargetDefinitionChangePlan` and target-definition mutation; destroy uses `discoverFullDestroyDeployments` / `ListAllDeploymentsForDisplay` (round-2 call-graph evidence). Round-2 also records the same failure on a clean develop checkout. I classify this as a non-causal CI STATE for this candidate, not as a source regression. It remains an actual failed job and is not green.
- `PR · Native Keycloak/Core · docker` (job `128848829737`) and `… · podman` (job `128848829759`) failed `TestControlPlaneSingleDefaultNativeRuntimeInCI`; the log says a Core was already running on the same engine for another Target. Per the requested 0427-172 park, these are recorded as STATE, not counted as pass.
- The aggregate `PR Selected Checks` is red. Conditional checks shown as `skipping` are not passes and are not used as evidence.

## Actionable correction recipe

- In `cmd/baha/target_definition_change_plan.go:160,166`, remove the claim that `baha destroy --all` collects these records. Do not recommend `app destroy --uuid` until the UUID is actually threaded through `newApplicationDestroyExecution` and proven to work with the restored owner. Keep the detach fail-closed and state the real supported recovery prerequisite; if no safe supported cleanup path exists for ownerless records, say so plainly and retain the target for operator recovery rather than suggesting a nonexistent collection operation.
- In `internal/deployment/deployment_list.go:134-151`, validate decoded ownerless records against their canonical deployment-directory UUID and target before returning them. Preserve fail-closed behavior for malformed or mismatched identities; never print an embedded UUID that disagrees with the storage key.
- In `cmd/baha/target_definition_orphan_refusal_test.go:19-50`, seed the record in a directory named by the same UUID. Add a mismatch regression proving the refusal does not claim the embedded foreign UUID and leaves the target and recovery state unchanged. Add a command-path regression for whichever recovery instruction remains in the message; it must prove the selected record is actually resolved, not merely that the error contains a command string. Keep the existing collectable-present and clean-target cases.
- Stop criterion: on the revised exact head, all three identity/refusal cases pass in `go-unit-tests` and `deployment-package-tests`; every advertised recovery command is accepted by the production dispatcher and reaches the intended record; no orphan is silently pruned or destroyed; the hosted destroy-retry failure is resolved or explicitly accepted by the CI owner, and `PR Selected Checks` is terminal success. The 0427-172 parked failures must remain explicitly identified as STATE and never be described as green.

## Provenance and publication

Planning repository verification before the evidence commit:

```text
/tmp/opencode/0427-165-review-wt
https://github.com/mcpdev80/baseharbor-plan.git
53dec171c2fbe873ac82089c07cbe54d7debb9c4	refs/heads/main
```

Product remote witness before review publication:

```text
20902f0a6ab016fd8fe6a501751e1becc5f334dd	refs/heads/develop
cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5	refs/pull/1500/head
```

Exact diff base is merge-base `128e6f50b538cb6ba2925432740aa37014fcc09a`; the PR diff contains six files: `.gitignore`, `cmd/baha/target_definition_change_plan.go`, `cmd/baha/target_definition_orphan_refusal_test.go`, `internal/deployment/collectable_orphans_test.go`, `internal/deployment/deployment_list.go`, and `internal/deployment/deployment_store.go`. No `.github/**` path is changed.

END_DONE 0427-165-review: KORREKTUR — false collection guidance and unchecked UUID/path identity block acceptance; candidate `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5`.
