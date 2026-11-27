# PR #1881 / 0428-310 — R6 exact-head content verdict

ROLE=REVIEW
Reviewer: w267-0428-284-pridentity
Decision: PASS against the dispute correction recipe at final head `1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5`.

## PLAN

1. Refresh PR head, develop, commit parents, exact delta, and the supplied run IDs.
2. Verify the injected sync fault now follows the `syncDir` error contract and the test comment/assertion agree.
3. Recheck retry/recovery and retained exact marker-content validation.
4. Record the transport incident separately from candidate content; stage this read-only verdict.

## Exact candidate and ancestry

PR #1881 is OPEN on branch `lane-0428-310-migration-marker`, base `develop`, final head `1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5`.

The final commit is a merge commit with parents `772ebc3999971d4d8479e3dda5a40299230f415f5` and `6944e8761af6f07b801f55e39bb9a5409226c10b`. The first parent is the sync-fault correction; the second is the exact current develop head. Remote compare confirms develop is an ancestor (merge base `6944e8761af6f07b801f55e39bb9a5409226c10b`, ahead 6 / behind 0). Compared with the R4 head `d7d1ea2db70ab1243835ba500b261183724a63ad`, the candidate delta is limited to `internal/orgconfig/migration.go` and `internal/orgconfig/migration_marker_test.go`; the develop merge contributes its already-integrated docs/catalog files, not an unrelated candidate payload.

The owner-reported, self-corrected force-with-lease intermediate is recorded as a transport/process defect. The final parent chain and remote tree comparison show no surviving content consequence from it; it is not a finding against this candidate's product content.

## Dispute-recipe review

- Injected error contract: PASS. `migration.go:59-65` adds `orgconfigSyncDirFault` inside the real `syncDir` path. `syncDir` wraps a returned fault as `*syncDurabilityError` at `migration.go:242-249`, so `errors.As` observes the same type as for production open/Sync/Close failures. The fault helper now injects through that hook at `migration_marker_test.go:439-449` instead of replacing `orgconfigSyncDir` with an unwrapped plain error.
- Assertion and comment: PASS. `migration_marker_test.go:451-459` now accurately states that the fault flows through `syncDir` and is wrapped; the assertion at `:480-482` requires `errors.As(migrateErr, &syncErr)` for `*syncDurabilityError`, matching the path above.
- Retry/recovery: PASS. `migration_marker_test.go:494-558` injects the first sync failure, checks no completion marker and retained canonical data, then retries with the fault removed and checks the canonical marker content after success.
- Marker-content checks retained: PASS. The R6 delta does not touch marker creation/verification or `store.go`; the exact canonical-content check (`verifyFrozenMarkerContent` / `frozenMarkerComplete`) and loader completion predicate remain unchanged from the reviewed candidate.

## Hosted evidence

Runs `46057404217` and `46058741643` are distinct terminal `pull_request` runs on exact head `1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5` and branch `lane-0428-310-migration-marker`.

Both are FAILURE at the aggregate level. Workflow policy, source format, native gate plan, and two onboarding native checks succeeded. Trusted Plan failed on the class-A uncatalogued-source rows for `internal/orgconfig/migration.go`, `migration_marker_test.go`, and `store.go`; `PR Selected Checks` then failed because `UNIT_SCOPE` was empty and the unit result was skipped. Other downstream jobs were skipped, not green evidence. The pair is exact-head evidence but not a passing CI qualification; the class-A freeze remains the gate blocker.

## Final disposition

Content verdict PASS at `1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5`. Mark content lift-ready for the owner's Freeze #136 decision. CI qualification remains pending: after the class-A lift, required tests must execute on the exact head and the terminal `PR Selected Checks` aggregate must succeed before merge. No tests were run locally; no PR mutation or merge was performed.

END_DONE w267-0428-284-pridentity: #1881 content PASS at 1cd5029f7149f3bc72bfce7f7ff28e662f6bddf5; transport incident had no content consequence; Trusted Plan and Selected Checks remain failed under class-A freeze.
