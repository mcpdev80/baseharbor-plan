# PR #1882 / card 0428-315 — exact-head content review

ROLE=REVIEW
Reviewer lane: `w267-0428-284-pridentity`
Task owner from current Plan main: `w400-0428-315-timeoutsfix`.
Plan main reviewed: `2f40ca1630f5919ec7c129a038ff6e2185130966`.
Task: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/tasks/t-20261125-hunt42-timeout-constant-matrix.md
Evidence on Plan main: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/evidence/2026-11-27/0428-315/akte.md
Evidence blob: `2925b6c0e91fda7b74f35cdfedc4e6c8ae46d81d`.

## Exact candidate and diff

Repo `mcpdev80/baseharbor`, PR #1882, branch `lane-0428-315-timeouts`, exact head `d51763d0dcb881e49279cd270c3265c00282b5b5`, current `develop` `6944e8761af6f07b801f55e39bb9a5409226c10b`. PR state OPEN. Current develop is an ancestor of the candidate.

The exact diff contains eight paths: `cmd/baha/app_observe.go`, `internal/application/timeouts.go`, `internal/application/timeouts_test.go`, `internal/metrics/perses_contract_test.go`, `internal/metrics/perses_tempo_datasource.go`, `internal/objectstorage/seaweedfs.go`, `internal/objectstorage/runtime_resources_test.go`, and `scripts/pr-gate-coverage.json`; diff stat 201 insertions, 16 deletions. `git diff --check` is clean. The matrix preserves the existing 120s/40s/30s/15s/10s CLI values, uses the 10s shared group for Tempo, and preserves separate 90s readiness and 3s existing-provider probe budgets.

## Review verdict: CHANGES

Finding — Tempo's matrix alias is mutable although the card calls for a constant matrix and the change is described as behavior-neutral. `internal/metrics/perses_tempo_datasource.go:64-71` declares `var tempoTraceQueryTimeout = application.FastServiceTimeout`. This permits package code to mutate the timeout at runtime and removes the compile-time invariant that the old `const` provided; it also makes the new `TestTempoTraceQueryTimeoutReadsFastServiceMatrix` a point-in-time value assertion rather than a guarantee that the alias cannot drift.

Correction recipe: retain the shared matrix source with `const tempoTraceQueryTimeout = application.FastServiceTimeout`. Keep the existing value test and add a compile-time constant use (or another static assertion) so the alias cannot become mutable in a later change. No value tuning is requested.

## Required checks and current state

The task requires package/test inventory, test-to-gate selection proof, and actual exact-SHA execution. The akte names `TestStatusTimeoutMatrixValues`, `TestStatusTimeoutMatrixDistinctGroups`, `TestManagementServicesShareManagementGroup`, `TestSharedMatrixIsTheSingleSource`, `TestTempoTraceQueryTimeoutReadsFastServiceMatrix`, and `TestSharedProviderReconcileReadsOverallMatrixAndBudgetsDistinct`. It records format/vet/build prechecks and the package-shard route, but no passing exact-head test run.

Current exact-head pull_request runs are `46037189378` and `46037549519`; both are terminal FAILURE on `d51763d0dcb881e49279cd270c3265c00282b5b5`, with Trusted Plan failure and downstream `PR Selected Checks` failure because the trusted base catalog does not contain the two added source rows. The card identifies this as the owner-scope class-A catalog blocker. Run `46046111688` is not an #1882 pendant: its head is #1884's `4e499b3cf67ad86cb022640589dba05bfa26922d` and its branch is `lane-0428-292-consent-ux`. It does not qualify as #1882 evidence.

No local tests were run. No PR mutation or merge was performed; Freeze #136 remains active.

END_DONE w267-0428-284-pridentity: #1882 content review completed as CHANGES at d51763d0dcb881e49279cd270c3265c00282b5b5; no merge.
