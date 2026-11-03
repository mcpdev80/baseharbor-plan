# w58-ci-authority-d — r27-ci-authority durability round 4

## Mission
- ROLLE: Worker (Lane w58). Coord f49a3303. KARTE: t-20261022-r27-ci-authority (journal runde 4).
- Branch `work/r27-ci-authority-ab` head `4f09aac6` (PR #1354, DRAFT — coord schaltet vor review um).
- Grundlage: review-1354c.md rezepte 1-5.
- Evidence file: `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-4.md`.
- END an f49a3303: `"END_DONE w58-ci-authority-d: head=<sha> opid-restart=ja append-vor-event=ja limit=hart roottest=echt scope=zitiert | <Satz>"`.
- STOP (conditional in card): punkt 3 erfordert entry-groessen-policy die der karte widerspricht => END_BLOCKED. **Nicht eingetreten** — karte/task fordert bounded retention explizit (finding 3), reject-with-error ist konsistent mit karte.

## END
- Status: **DONE**.
- Candidate SHA (local + remote): **`f15a85665bf7fcfdf3b6d12cb061a970c4ca93f4`** on `work/r27-ci-authority-ab`.
- opid-restart = ja (P1); append-vor-event = ja (P2); limit = hart / reject-with-error (P3); roottest = echt (P4); scope = zitiert (P5).
- Local checks green: `go build ./...`, `go vet ./...`, `gofmt -l` empty, `go test ./internal/machinehttp` + `./internal/controlplaneruntime` green.
- PR #1354 still OPEN/DRAFT — NOT modified (coord schaltet vor review um). CI skipped by draft design.
- No existing test function deleted (commit rule: `^-func Test` empty); 5 new round-4 tests added; `TestRound3LoadRestoresOnlyTerminalStates` rebuilt (not deleted) per Owner call.

## Written evidence (je Punkt + Testname + Zeugnis)

### P1 — operation_id + restart correlation (review finding 1)
- Every journal line now carries `operation_id` (marshaled in `appendJournalLocked`, parsed in `load`).
- `load()` restores the LAST state per execution-id (removed the round-3 active-skip that dropped `running` — that skip WAS finding 1: `Pending→Running` fell back to `pending` on reopen).
- Fixed a latent segment-order bug: `journalSegments()` returns active-first then backups newest→oldest; the load loop overwrote so the OLDEST segment won. Added `reverseSegments()` so the newest active segment wins → newest line per id is authoritative.
- Witnesses: `TestRound4OperationIDSurvivesAndRunningStaysRunning` (create→start(running)→reload==running + operation_id intact + actor/context durable).

### P2 — append-before-event ordering (review finding 2)
- Reordered `update()` to `mutate → appendJournalLocked → onCommit(emit)`. Previously `fn()` ran first (emitting on subscriber channels) BEFORE the append, so a failed append could publish an event for an uncommitted state that can never be rolled back.
- On append failure: in-memory record rolled back to prior state, NO event published (fail closed).
- Witnesses: `TestRound4AppendFailurePublishesNoEvent` (dir at journal path forces append error → subscriber receives 0 events, in-memory stays pending).

### P3 — hard segment limit (review finding 3)
- Reject a single journal entry whose marshaled length exceeds `journalSegmentCap` (4 MiB) with an error, before it is ever appended. A 5 MiB actor `create` now returns an error (was: produced a 5.24 MiB segment — the finding-3 repro).
- Consistent with the card: "eintrag das segment ueberschreiten => ... nie 5-MiB-eintrag in 4-MiB-segment; falls einzelner eintrag >limit: ablehnung mit err, dokumentiert". The 5 MiB counter-probe asserts file ≤ 4 MiB (holds because the oversized write is refused).
- Active ids preserved: rejecting the write surfaces the error without mutating state.
- Witnesses: `TestRound4OversizedEntryRejectedAtCap` (5 MiB target create → err), `TestRound4SegmentNeverExceedsCapForLargeWrite` (segment never > cap after rotation).

### P4 — real root-guard test (review finding 4)
- Written from scratch in `internal/machinehttp` (the guard lives at the store boundary; the claimed `controlplaneruntime` test is NOT repeated).
- `TestRound4OpsDirEstablishesDurableJournal`: configured ops-dir establishes a durable on-disk journal that survives a reopen (running restored); empty root stays purely in-memory (no false durability claim) — the machinehttp-level manifestation of `registerOperatorAPI`'s fail-closed root guard.

### P5 — scope cleanup (review finding 5 + card write-set)
- Card write-set: `internal/**` allowed; `cmd/baha/**` only kartlich gedeckt.
- `internal/controlplaneruntime/server.go` + `server_run.go` (added `ErrMissingOperationsDir` root guard, fail-closed on empty `RuntimeOperationsDir`): under `internal/**` → regeltauglich, nur dokumentiert.
- `cmd/baha/machine_http_executor_validation_test.go`: the ONLY change is `machinehttp.New(executor)` → `machinehttp.New(executor, "")` — a mechanical signature fix forced by round 4 adding a required `stateRoot` param to `machinehttp.New`. Without it the package does not compile. No test logic changed. Documented, not reverted (reverting would break the build; the card permits internal/** and the cmd change is a forced compile fix).
- No existing `func Test` deleted. gofmt + vet clean on all touched files.

## repo-rule compliance
- Write-set strictly within card scope: `internal/machinehttp/**` + `internal/controlplaneruntime/**` + one forced cmd/baha signature fix.
- No existing test function deleted (`^-func Test` empty in staged diff); 5 new round-4 tests added.
- `TestRound3LoadRestoresOnlyTerminalStates` rebuilt (not deleted) per Owner call f49a3303 (answer to my QUESTION): it was the subject of review-1354c finding 1; kept the still-valid terminal/pending restore, replaced the old "running not restored" assert with the new running-stays-running + operation_id contract, cited review-1354c in the comment.
- PR #1354 status NOT modified — still OPEN/DRAFT (coord schaltet vor review um).
- No force-push, no branch-protection bypass. FF push `4f09aac6..f15a8566`.

## Local checks
- `go build ./...` : OK (rc=0)
- `go vet ./...` : OK (rc=0)
- `gofmt -l internal/machinehttp internal/controlplaneruntime cmd/baha` : empty
- `go test ./internal/machinehttp -count=1 -timeout 8m` : OK (1.78s)
- `go test ./internal/controlplaneruntime -count=1 -timeout 8m` : OK
- `git ls-remote origin work/r27-ci-authority-ab` : `f15a85665bf7fcfdf3b6d12cb061a970c4ca93f4` == local head
- PR #1354: OPEN / DRAFT (untouched). CI checks `skipped` by draft design; 2 in progress (Workflow policy, PR Source format).

## Plan (numbered) — board + evidence
1. Fetch origin refs + ancestry rc=0 + worktree (detached HEAD 4f09aac6). ✓
2. P1 operation_id + running-stays-running + segment-order fix. ✓
3. P2 append-before-event ordering. ✓
4. P3 hard segment limit (reject oversized). ✓
5. P4 real root-guard test. ✓
6. P5 scope + evidence. ✓
7. Commit f15a8566, push FF, verify ls-remote. ✓
