# CODEX-REVIEW — PR #1390

## Candidate and scope

- PR: [#1390](https://github.com/mcpdev80/baseharbor/pull/1390)
- Reviewed head: `c8c8810f01706c1af7f00631f77b77821c4b140c`
- Current PR base from GitHub: `77511c8a6672f34faf0d5ac543ba126485f05c41` (`develop`).
- PR state at review: open; head was unchanged and matched the mission.
- `git diff --name-only <base>...<head>`: `cmd/baha/application_lifecycle_lock_test.go`, `internal/stableid/two_process_lock_test.go`.
- Task: `t-20261018-r27-mutation-lock`, status `review`; `plan.py show` reported all three dependencies accepted.

## Required checks and observed evidence

- Hosted run [42055095457](https://github.com/mcpdev80/baseharbor/actions/runs/42055095457) completed successfully at the reviewed SHA. `PR Selected Checks` and `PR · Validation · authority-package-tests` are `SUCCESS`; the required CLI and source validation jobs are also successful. Other unrelated runtime/release jobs were skipped by the workflow policy.
- Independent remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1390/head` returned `c8c8810f01706c1af7f00631f77b77821c4b140c`, equal to the reviewed head.
- Real separate-process filesystem seam, run locally at the candidate: `go test ./internal/stableid -run '^TestLifecycleLockExcludesTwoSeparateProcesses$' -count=1` — `ok github.com/mcpdev80/baseharbor/internal/stableid 0.006s`. The test re-executes the binary as separate processes, observes exclusion while the parent holds the flock, then verifies a child can acquire after release.
- Production-path cells, run locally at the candidate: `go test ./cmd/baha -run '^(TestStaleDestructionConsentRequiresRepreview|TestSharedBackendReconcileRejectsSecondProcess|TestTargetSelectionMutationRejectsSecondProcess|TestSharedConsumersSerializeOnTargetOwner|TestTargetLifecycleLockRejectsSecondProcess)$' -count=1` — `ok github.com/mcpdev80/baseharbor/cmd/baha 1.792s`. These exercise the destruction authorization, shared reconcile, target selection mutation, shared Target consumers, and Target lifecycle lock entry points. The concurrency cases use separate re-exec processes where indicated by the test bodies.
- Lock-disabled mutant in a separate scratch worktree: omitted `flock` from the existing lock implementation; `TestTargetLifecycleLockRejectsSecondProcess` failed because the child entered the Target owner while the parent held it.
- Revision/consent-binding-disabled mutant in a separate scratch worktree: disabled the `consent.PlanID == planID` equality in the shared consent validator; `TestStaleDestructionConsentRequiresRepreview` failed at line 100 because the request was refused for `impact-confirmation-required`, not the required `stale-impact-consent`. This demonstrates the regression cell is sensitive to removal of the binding. An initial scratch mutation at the later re-plan comparison did not reach this guard and remained green; I moved the mutation to the effective shared consent check, where the cell failed as required.

## Lock-client inventory

I enumerated production Go call sites from both the current PR base and candidate head, excluding tests, definitions, and forwarding wrappers. Both sides contain the same 21 clients; there is no uncovered client:

1. `cmd/baha/app_apply.go:98`
2. `cmd/baha/app_lifecycle.go:249`
3. `cmd/baha/app_lifecycle.go:291`
4. `cmd/baha/app_new_wizard.go:183`
5. `cmd/baha/app_remote_lifecycle.go:84`
6. `cmd/baha/app_up_lifecycle.go:42`
7. `cmd/baha/application_restore_authorization.go:26`
8. `cmd/baha/application_stop_impact.go:122`
9. `cmd/baha/control_plane_destroy.go:101`
10. `cmd/baha/control_plane_stop.go:45`
11. `cmd/baha/core_installation.go:69`
12. `cmd/baha/target_definition_change.go:165`
13. `cmd/baha/target_selection_mutation.go:50`
14. `cmd/baha/update_core_native.go:430`
15. `cmd/baha/update_ha_recovery_command.go:21`
16. `internal/application/shared_backends.go:170`
17. `internal/application/shared_backends_resources_runtime.go:418`
18. `internal/coreinstallation/installation.go:158`
19. `internal/deployment/config_mutation.go:77`
20. `internal/serviceaccess/local_issuer.go:75`
21. `internal/serviceaccess/local_issuer.go:277`

The exact enumerated inventory at base `77511c8…` and head `c8c8810…` compared identical. `target_selection_mutation.go:50` and `deployment/config_mutation.go:77` use the existing state-file lock variant; the other sites use the lifecycle lock or its existing owner wrapper.

## Verdict and action recipe

**ACCEPT** for the test-only candidate at `c8c8810f01706c1af7f00631f77b77821c4b140c`. The two-process filesystem test is genuine, the production cells traverse the relevant lock and consent paths, both requested mutants are detected, and the 21-client inventory remains complete. No correction is required for this candidate; preserve these cells and their skip-free `TestMain` helper dispatch in any subsequent revision. A changed head requires the candidate tests and hosted checks to be revalidated.

## Repo-rule compliance

Read-only, SHA-exact review. No product files, branch, PR, card, or task note were changed. This requested evidence file is the only write. No PR action was taken.
