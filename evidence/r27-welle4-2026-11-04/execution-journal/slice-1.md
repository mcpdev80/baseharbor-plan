# Execution-journal slice-1 — r27 execution journal (lane w112)

- Task: t-20261018-r27-execution-journal · lane w112 · Coordinator f49a3303
- Repo: baseharbor (core) · branch work/r27-execution-journal (from develop) · commit 0ce814d0
- PR: https://github.com/mcpdev80/baseharbor/pull/1373 (DRAFT, base develop)
- Remote develop at push: 2a43984a34d59c35cc4f23986d550a8b7cd319ee
- Date: 2026-11-04

## Scope (per Owner-coordinator ablehnung 2026-11-04)

- Criteria (1)(4)(5) already covered by the merged journal state at bb9bc0ef (unchanged here).
- This slice closes criteria (2) and (3), which were OPEN:
  - (2) duplicate request with changed content must be rejected (typed error, no effect).
  - (3) reconnect must retrieve the same operation (same execution id, not a second execution).
- Write-set: internal/machinehttp only (store.go + tests). No cmd/baha, no .github.

## Root cause found

- executionStore.create() indexed only by a fresh ExecutionID; it never compared operationID, so a repeat of the same operation id (reconnect with identical content, or a duplicate with changed content) minted a second execution with no comparison.
- git grep -i reconnect on develop matched only docs/, confirming there is no reconnect path.

## Fix

- Added operationsIndex (operationID -> executionID) to executionStore, kept in memory alongside records; the journal stays append-only per line.
- create() resolve logic: a byte-identical repeat (same operation id + actor + context) returns the existing execution so the operation replays once; a repeat with changed actor/context fails closed with a typed ErrorValidationFailed and indexes no second execution.
- sameOperationContext() compares actor + context via reflect.DeepEqual.

## Witnesses (test evidence)

- Red-first: TestReconnectReturnsSameOperationProvesRed and TestCreateDuplicateSameOperationDifferentContentRejectsRed both FAILED against the pre-fix develop baseline, then PASSED after the fix (order preserved).
- TestDuplicateAfterStartStillRejects: duplicate still rejected after the first execution moved to running, original stays running, no second execution indexed.
- TestCreateReconnectIdenticalReturnsSameOperation: identical reconnect returns the original execution id.

## Local checks run against 0ce814d0

- go build ./... : OK
- go vet ./internal/machinehttp/ : OK
- gofmt -l internal/machinehttp/store.go internal/machinehttp/execution_duplicate_reject_test.go internal/machinehttp/execution_reconnect_test.go : empty (clean)
- go test ./internal/machine/... ./internal/machinehttp/... -count=1 :
  - ok github.com/mcpdev80/baseharbor/internal/machine 0.003s
  - ok github.com/mcpdev80/baseharbor/internal/machinehttp 24.xxxxxs
- PR #1373 draft CI (terminal): Workflow policy = SUCCESS, PR · Source format = SUCCESS, all other gates SKIPPED (draft scope, no product gates on a draft).

## Files changed

- internal/machinehttp/store.go (operationsIndex + resolve logic + sameOperationContext helper)
- internal/machinehttp/execution_duplicate_reject_test.go (new: criteria 2 + after-start guard)
- internal/machinehttp/execution_reconnect_test.go (new: criteria 3)

## END LINE

- END_DONE w112-execution-journal: head=0ce814d0 pr=1373 (draft) faelle=2,3 closed; 1,4,5 covered by bb9bc0ef lsremote=2a43984a | rejected duplicate + reconnect-same-operation added to store.create; build/vet/gofmt + go test ./internal/machinehttp green; PR1373 draft CI terminal green.
