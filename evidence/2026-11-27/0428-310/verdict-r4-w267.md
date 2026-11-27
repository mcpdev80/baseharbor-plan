# PR #1881 / 0428-310 — R4 exact-head content verdict

ROLE=REVIEW
Reviewer: w267-0428-284-pridentity
Content decision: CHANGES. The production durability path follows the recipe, but the new injected-failure test has a statically provable error-type mismatch and will fail when executed.

## PLAN

1. Refresh PR head, develop, compare, and supplied run 46054369694.
2. Inspect error propagation, injected sync-failure behavior, recovery retry, and retained marker-content checks at the exact head.
3. Record the current CI outcome and whether this is a passing exact-head witness.
4. Stage a read-only verdict; no product changes, PR mutation, or merge.

## Exact refs

PR #1881 is OPEN on branch `lane-0428-310-migration-marker`, exact head `d7d1ea2db70ab1243835ba500b261183724a63ad`. Exact current develop is `6944e8761af6f07b801f55e39bb9a5409226c10b`. Compare reports four candidate commits and one develop-side commit not in the candidate (merge base `ea5218d72e263f21e79853b679af50074dab8c25`); this is a content-only review and the head must be brought current before merge qualification.

## Dispute-recipe review

- Directory-sync error propagation: PASS. `internal/orgconfig/migration.go:156-186` fsyncs the temp file, renames it, and returns `orgconfigSyncDir` errors. `migrateToCanonical` at `:122-147` exits on that error and does not write the completion marker. Its second directory sync also propagates errors. `syncDir` at `:235-249` returns wrapped errors from open, Sync, and Close instead of suppressing them.
- Injected failure regression: CHANGES. At `migration.go:65`, `errSyncDirFailure` is a plain `errors.New`. The test seam at `migration_marker_test.go:444-449` returns that error unchanged. `writeDurableCanonicalData` at `migration.go:186` passes the seam's error through, and `migrateToCanonical` returns it unchanged. But `migration_marker_test.go:480-482` requires `errors.As(migrateErr, &syncErr)` for `*syncDurabilityError`. No such wrapper is created on this injected path, so this assertion fails before the marker assertions run. The test's comment at `:457-459` also incorrectly says the injected error is a `syncDurabilityError`.
- Retry/recovery check: the retry sequence is present at `migration_marker_test.go:494-558`: it verifies canonical data survives the injected error, retries after restoring the seam, and checks the marker is complete with exact canonical content. It is a direct migration retry test, not a process-restart fixture. The preceding test-helper/type assertion defect must be fixed before this new suite can qualify.
- Marker-content checks retained: PASS. `migration.go:88-115` still requires readable exact canonical marker content; `store.go`'s completion predicate continues to use `frozenMarkerComplete`, rather than marker existence alone.

The production sync error wrapper's `unsupported` field/helper is not used to soften the result: every sync error still fails closed. No production code path here converts an unconfirmed data-directory sync into a completion marker.

Correction recipe: make the injected seam reflect the production error contract, for example return `&syncDurabilityError{err: errSyncDirFailure}` and assert `errors.Is(migrateErr, errSyncDirFailure)` plus `errors.As` to the wrapper; alternatively assert the injected sentinel directly and remove the false wrapper expectation/comment. Keep marker absence, retry, and exact-content checks intact.

## Hosted state

Run `46054369694` is a terminal `pull_request` FAILURE on this exact head and branch. `PR · Trusted Plan` failed with uncatalogued source rows for `internal/orgconfig/migration.go`, `migration_marker_test.go`, and `store.go`; `PR Selected Checks` also failed because `UNIT_SCOPE` is empty and the unit result is skipped. `Workflow policy`, `PR · Source format`, `PR · Native gate plan`, and two native jobs succeeded; other jobs were skipped. Therefore the report “only Trusted Plan red, rest green” is not literal: the aggregate is red, and skipped jobs are not green evidence. The supplied second exact-head close/reopen witness has not yet arrived in this review; no two-run passing qualification is claimed.

## Final disposition

Content verdict CHANGES for the injected-failure regression mismatch above. Do not mark #1881 lift-ready yet. The production propagation/order fix is present, but the regression is guaranteed to fail when the unit shard runs; the trusted catalog remains frozen/red, the exact-head aggregate failed, and the candidate is one develop-side commit behind. Correction is limited to the seam/test error contract. After correction and freeze/current-base integration, required exact-head checks must execute and pass before merge. No tests were run locally and no PR mutation or merge was performed.

END_DONE w267-0428-284-pridentity: #1881 CHANGES at d7d1ea2db70ab1243835ba500b261183724a63ad for injected-error type mismatch; Trusted Plan and Selected Checks failed.
