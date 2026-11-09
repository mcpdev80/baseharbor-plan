# CODEX-REVIEW 0427-165 r3 — PR #1500

ROLLE: REVIEW  
URTEIL: KORREKTUR

Reviewed PR head: `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe`  
Base `develop`: `20902f0a6ab016fd8fe6a501751e1becc5f334dd`  
Task: `t-20261108-bughunt-target-delete-orphan-records`  
Hosted run: [42539114216](https://github.com/mcpdev80/baseharbor/actions/runs/42539114216)

## PLAN

1. Confirm live PR/base SHA and inspect the r2-to-r3 and exact-head changes.
2. Check whether each recovery instruction can resolve the named ownerless record.
3. Verify the missing, whitespace, mismatch, and valid identity cases and their hosted CI selection.
4. Compare native failures with the parent run, classify their cause, and publish the verdict.

## Findings

### 1. Canonical identity comparison still normalizes malformed values

In `internal/deployment/deployment_list.go:171,174`, the new conditions reject empty values and compare `strings.TrimSpace(value)` with the directory/Target name. This still admits a noncanonical value with surrounding whitespace: for example, an embedded DeploymentID of `" <folder-uuid> "` passes after trimming. The code comment and r3 report promise exact canonical equality, but the implementation only compares normalized values.

The regression suite covers whitespace-only DeploymentID and Target (`TestCollectableOrphansRejectsBlankDeploymentID`, `TestCollectableOrphansRejectsBlankTarget`), a mismatched UUID, and a matching UUID. It does not test a missing JSON field separately from whitespace, nor a value padded with whitespace. The command-level blank fixture sets both fields to whitespace together, so it does not prove each malformed field independently through the refusal path.

Malformed records are excluded from `CollectableOrphans`; the subsequent `ListDeployments` fails at the owner check. The blank and mismatch command regressions assert only that some error occurs. They do not assert the record's directory identity is reported, although the card requires a refusal that names existing records.

### 2. The refusal's Next command is not a healing step in this state

The revised message correctly retracts `baha destroy --all` as a per-record collector. The source path `cmd/baha/runtime_destroy_all.go:388-417` handles installation-wide inventory and marks unregistered state skipped; it does not collect valid ownerless records.

However, `target_definition_change_plan.go:166` tells the operator to restore the Target using `baha target create <name> --from-recovery <recovery-file>`. This refusal happens before detachment and leaves the Target configuration present. The command is therefore not the next step for this refusal. The regression `TestTargetDeleteRefusesWhileCollectableOrphansAttached` also asserts that refusal did not create a recovery file.

The trailing suggestion to run `baha app destroy` is not demonstrated as healing for the reported state. The deployment owner contract says state is unreadable without its authoritative Core owner (`internal/deployment/deployment_store.go:20-25`); the destroy lifecycle resolves the application manifest and checks the selected Core target before cleanup (`cmd/baha/app_destroy_lifecycle.go:87-105,105-126`). The actionable recovery would need to say that the Target must remain attached and that both the authoritative Core installation owner and the original source repository/manifest must be restored before running `baha app destroy`. If those prerequisites cannot be restored, the message must say there is no supported recovery command and keep the record attached for operator recovery. Do not label that preservation as a completed healing path.

The package comment for `ErrTargetDetachedWithOrphans` in `internal/deployment/deployment_store.go:32-43` also remains stale: it still describes a “collect path” and says the destroy contract lists the records with a collect reason, which conflicts with the new message.

I attempted to independently build the develop CLI for the command check. The build could not complete in this review sandbox because it returned `disk quota exceeded`; I did not run a local destroy command. The round-3 dossier records a develop-binary `destroy --help` check, and the source confirms the non-collector behavior above. No destructive runtime action was attempted.

### 3. CI selection is real, but the missing-field case is not yet a regression

Run 42539114216 is terminal **failure** on the exact PR head. The selected package jobs relevant to this change did execute and pass:

- `PR · Validation · go-unit-tests`, job 128909945168: success. Its log runs `scripts/pr-unit-database.sh` and records the `cmd/baha` package passing.
- `PR · Validation · deployment-package-tests`, job 128909945317: success. Its log reports `matched_tests: ["./internal/deployment"]`.

Thus the current CLI and deployment-package regressions are picked up by hosted CI. Before acceptance, add explicit absent-field and padded-value regressions, including refusal-path assertions that preserve the Target and identify the on-disk record. Keep them in these CI-selected packages.

### 4. Native failures are external STATE, but the required aggregate is red

On the exact head, `PR · Native Keycloak/Core · docker` (job 128909945122) and `… · podman` (job 128909945199) both fail in `TestControlPlaneSingleDefaultNativeRuntimeInCI`. Their log line is `control_plane_single_native_ci_test.go:38`: Core startup reports that Core is already running for the shared `w169-ci-bootstrap-…` target and refuses the second same-engine Target. Parent run 42532556867 on the previous PR head `a14cf361d0d6bacfe2a4ab1a963d1a39e676583a` fails the same test in both engines with the same existing-Core conflict. That supports classifying these as the recurring 0427-172 STATE, not an r3 regression. They remain red, not green.

The current `PR Selected Checks` job 128912557301 is also terminal failure (its “Require normal selected job results” step fails). This blocks acceptance under the current gate state; the review does not waive or rerun it.

## Actionable correction recipe

1. In `internal/deployment/deployment_list.go:171-175`, require raw decoded DeploymentID and Target to equal the canonical directory UUID and Target exactly; do not trim before equality.
2. In `internal/deployment/collectable_orphans_test.go`, add fixtures for each absent JSON field and for whitespace-padded values, while retaining the whitespace-only, mismatch, valid, and owned cases. In `cmd/baha/target_definition_orphan_refusal_test.go`, assert each malformed-record refusal preserves the Target and names the on-disk deployment directory/record.
3. In `cmd/baha/target_definition_change_plan.go:160-166`, make the Next step executable for a refusal that leaves the Target attached. State the authoritative Core-owner and source-repository prerequisites for `app destroy`, or state that no supported cleanup exists and require operator recovery. Remove the `target create --from-recovery` direction when this refusal has produced no recovery file. Update the stale `ErrTargetDetachedWithOrphans` comment in `internal/deployment/deployment_store.go:32-43`.
4. Add a reproducible regression or command-level proof that the documented recovery prerequisites actually allow `baha app destroy` to remove the record; keep source/Core fixtures isolated. Require the exact-head `go-unit-tests` and `deployment-package-tests` results after correction.
5. Keep the native Keycloak/Core failures recorded as 0427-172 STATE. Stop before acceptance while `PR Selected Checks` is red; accept only after that required result is terminal success or an explicit owner-authorized resolution and a fresh exact-head check.

## Evidence and scope

The live PR metadata confirms base `develop@20902f0a6ab016fd8fe6a501751e1becc5f334dd` and head `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe`. The r2-to-r3 product delta is limited to the recovery text, identity filtering, and two regression-test files. No product files were changed by this review, no workflow was rerun or dispatched, and no local containers were started.

END_DONE 0427-165-review-r3: KORREKTUR — identity matching still accepts whitespace-padded values, malformed records are not proven named, the refusal Next step is not executable as written, and required hosted aggregate is red; native 172 failures are external STATE. Candidate `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe`.
