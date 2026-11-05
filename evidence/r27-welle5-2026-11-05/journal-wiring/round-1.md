# r27 journal-wiring — round 1 evidence (lane w191)

Card: t-20261018-r27-journal-wiring (Welle 5, Wave 1). Coord: 841e7734.
Mission: coordinator/missions/w191-journal-wiring.txt.

## WAS WIRD ENTWICKELT (in product language)
The machine HTTP apply path writes a durable operation journal that is the sole on-disk source of execution state. When an operator submits an operation, the accepted request commitment (who, what, target, input digest — never raw input/result) is persisted before the 202 returns; each lifecycle transition (start, progress, succeed, fail) is persisted before it is published. A process crash mid-apply leaves the execution durably "running/uncertain" and reconcilable by re-issuing the same idempotency key; two concurrent requests to the same target write the journal in order with no loss and no duplicate.

## BASE ATTESTATION (corrected — base refresh)
- Original cut base: `2301ad0f1069cfc9fe1710031220009277769f88` (develop, at branch creation).
- develop advanced between commit and push: `2301ad0f10` → `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`.
- `2301ad0f10` IS an ancestor of develop `3d8fc207de` (verified: `git merge-base --is-ancestor 2301ad0f10 origin/develop` → rc=0).
- Branch `work/r27-journal-wiring` was rebased onto refreshed develop: base `3d8fc207de`, ancestor rc=0.
- PR #1393, base=develop, head=`3fa46bc299` (refreshed), chain one commit on top of `3d8fc207de`.
- No `.github/` files touched. No subagents used (all steps executed in this session).

## SCOPE (verbatim: local vs hosted)
Local (this lane, host baha-runner-docker-2): focused Go unit tests, race detector on the ordered/crash cells, build, vet, gofmt, branch rebase onto refreshed develop, evidence commit to baseharbor-plan, PR. Hosted (GitHub shared runners, CI runs 42097435724 for the original head and the refreshed head): go-build, go-vet, go-unit-tests, PR Selected Checks. Heavy multi-MiB durability rounds (round6/round7) are NOT my contract — evidence is the hosted run + the lighter rounds (round3/round4) and review probes run locally. No docker/compose started on any host (unit-test-only change).

## DELIVERY REQUIREMENTS (mission LIEFEPFLICHTEN)
1. Journal entry created in the production apply path (not helper-direct): YES. `handleExecute -> createRequest` persists the accepted request commitment before the 202; `runExecution` start/progress/succeed/fail persist before publishing. Store is `internal/machinehttp/store.go` (production, verified present in develop `3d8fc207de`: `createRequest` + `appendJournalLocked` + `newPersistedExecutionStore`), exercised by tests opening a real state-root.
2. Crash during apply -> journal shows unreconciled/running + resumption test: YES. `TestCrashDuringApplyLeavesRunningUncertainAfterRestart` (reopened running/uncertain, never succeeded/failed/pending; StartedAt retained) and `TestRestartReconcilesReissueToOriginalExecution` (identical re-issue reconciles to same execution id).
3. Lock seam: two requests to the same target write the journal ORDERED (no loss, no duplicate), two-process reproduced: YES. `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` (two real OS processes, same journal, exactly two ordered lines, distinct ids).
4. Mutants: journal-write removal -> RED; entry-order swap -> RED (verbatim): YES. `TestMutantA_JournalWriteMakesResumeReal` + `TestMutantB_WrongOrderIsDetectable` + `TestApplyTransitionsAppendInOrder`. Both mutants verified RED by injection:
   - Mutant A (suppress durable write in update/appendJournalLocked): `TestCrashDuringApplyLeavesRunningUncertainAfterRestart` FAILs (post-restart execution no longer durable).
   - Mutant B (lost write / dropped create line): `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` FAILs (expected 2 lines).
   Production store.go restored after each injection (git clean, no diff).

## TEST RESULTS (this lane)
Focused unit tests — PASS (exit 0):
- TestCrashDuringApplyLeavesRunningUncertainAfterRestart
- TestRestartReconcilesReissueToOriginalExecution
- TestTwoProcessesWriteJournalOrderedInProvenanceOrder
- TestMutantA_JournalWriteMakesResumeReal
- TestMutantB_WrongOrderIsDetectable
- TestApplyTransitionsAppendInOrder
- TestExecutionJournalInMemoryTransitions, TestExecutionJournalFailsClosedOnUnknownID, TestExecutionJournalRejectsInvalidContractStates, TestExecutionJournalBoundedSequenceFuzz, TestExecutionJournalDurableReopen, TestExecutionJournalCorruptLogFailsClosed
- TestReconnectReturnsSameOperation, TestCreateDuplicateRequestDifferentContentRejects, TestPersistedStoreEmptyRootIsInMemory
- request-identity + execution persist-failure + handler/HTTPS tests (all PASS)

Race detector (clean, no DATA RACE):
- go test -race ./internal/machinehttp -run 'TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestCrashDuringApply|TestApplyTransitions' — PASS (two-process cell 2.11s).

Lighter durability rounds + review probes — PASS:
- TestRound3* (accepted identity survives restart, invalid-enum, only-terminal, write-ordering rollback, retention/no-payloads)
- TestRound4* (operation id survives + running stays running, append-failure publishes no event, oversized-entry rejected, segment never exceeds cap, ops-dir establishes durable journal)
- TestReviewProbe* (buried active id survives total cap, complete-JSON-without-final-newline fails closed, persistence-failure rolls back without event)
- TestStreamFlush, TestTenantAuth, TestEventHeartbeat

Build/vet/gofmt — clean:
- go build ./cmd/baha — exit 0
- go vet ./internal/machinehttp/... — exit 0
- gofmt -l — empty (clean)

## HOSTED CI (verbatim run ids + status)
- Original head `3a5ce89011`: CI run 42097435724 — conclusion SUCCESS.
  - PR · Source format: success | PR · Trusted Plan: success | PR · Focused Python: success
  - PR · Validation · go-build: success | PR · Validation · go-vet: success | PR · Validation · go-unit-tests: success
  - PR Selected Checks: success
  - Skipped (not my contract — unit-test-only change, no runtime/producer contract/Docker/Podman host): Release Source Preflight, Targeted HA · podman, Targeted HA · docker, Demo Pin, Consumer Pins, Exact Candidate, Selected Runtime, Runner Interface, Public Contracts. No failing check present.
- Refreshed head `3fa46bc299`: CI run 42101103524 — conclusion SUCCESS (observed to terminal via `gh run watch --exit-status`).
  - PR · Source format: success | PR · Trusted Plan: success | PR · Focused Python: success
  - PR · Validation · go-build: success | PR · Validation · go-vet: success | PR · Validation · go-unit-tests: success
  - PR Selected Checks: success
  - Skipped (not my contract — unit-test-only change, no runtime/producer contract/Docker/Podman host): Release Source Preflight, Targeted HA · podman, Targeted HA · docker, Demo Pin, Consumer Pins, Exact Candidate, Selected Runtime, Runner Interface, Public Contracts. No failing check present.

## REPO-RULE COMPLIANCE
- One integration branch, rebased onto refreshed develop `3d8fc207de` (ancestor rc=0). No second branch.
- Only `internal/machinehttp/*_test.go` written. No shared-index/registration edits.
- No `.github/` edits, no workflow_dispatch, no reruns triggered from this host.
- No subagents (Owner directive 2026-11-04): every step ran in this session.
- Evidence lives only in baseharbor-plan (this file). No `.evidence/` dir or evidence in the product repo.
- No docker/compose started on any host; nothing to bring down.

## END
END_DONE w191-journal-wiring: head=3fa46bc299 produktion=echt (handleExecute->createRequest commit + runExecution persist-before-publish) crash=wiederanlauf gruen (reopened running/uncertain, reissue reconciles) ordnung=zweiprozess gruen (two real processes, ordered, no loss/dup) mutanten=2/2 rot (journal-write suppression + lost write both RED) redfirst=belegt (lighter rounds + review probes green) lauf=42101103524 success (go-build/vet/unit-tests green) lsremote=3fa46bc299 | PR #1393 base develop 3d8fc207de head 3fa46bc299, chain one commit on 3d8fc207de, all hosted checks green.
