# w58-ci-authority-d — r27-ci-authority durability round 4

## Mission
- ROLLE: Worker (Lane w58). Coord f49a3303. KARTE: t-20261022-r27-ci-authority (journal runde 4).
- Branch `work/r27-ci-authority-ab` head `4f09aac6` (PR #1354, DRAFT lassen — coord schaltet vor review um).
- Grundlage: review-1354c.md rezepte 1-5.
- Write-set: card line — quote in §Write-set below. `internal/**` regeltauglich, `cmd/baha/**` nur kartlich gedeckt.
- Evidence file: `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-4.md`.
- END an f49a3303: `"END_DONE w58-ci-authority-d: head=<sha> opid-restart=ja append-vor-event=ja limit=hart roottest=echt scope=zitiert | <Satz>"`
- STOP: punkt 3 erfordert entry-groessen-policy die der karte widerspricht => END_BLOCKED mit kartenzeile.

## END
- Status: BLOCKED (awaiting Owner scope call on P1) — implementation done for P1-P4, one existing round-3 test conflicts with mission P1's "running stays running". QUESTION line posted to f49a3303 (176 pending).

## Pending scope decision (posted QUESTION, awaiting Owner)
- Mission P1 mandates `running` be restored on reopen (Gegentest: create->start(running)->reload == running).
- I implemented it (operation_id in journal line + load; load restores last-state-per-id incl. running; fixed latent segment-order bug so newest active segment wins on reopen).
- Conflict: `TestRound3LoadRestoresOnlyTerminalStates` asserts a standalone `running` journal line must NOT be restored — the OLD design the review flagged as finding 1.
- Awaiting Owner: (A) flip the assertion to the new contract, or (B) restore running only from active segment (not rotated backups).

## PLAN (numbered)
1. Fetch origin refs (`work/r27-ci-authority-ab` + `develop`), ancestry rc=0 WÖRLICH, worktree add `/tmp/opencode/w58-ci-authority-d-wt` on `work/r27-ci-authority-ab`, verify head/PR status.
2. P1 OPERATIONID + RESTART-KORRELATION: every journal entry carries `operation_id`; reload restores LAST state per execution, `running` stays `running` (no pending-downgrade); Gegentest: create->start(running)->reload-> state==running + operationid set.
3. P2 APPEND VOR EVENT: reorder update() so `appendJournalLocked` runs BEFORE `fn(record)`/emit; append-error => no event on subscriber channels, no record-mutation; test: dir at journal path forces error, subscriber received==0.
4. P3 HARTES SEGMENT-LIMIT: 4 MiB enforced at write; oversized entry rotates BEFORE append (never 5 MiB in 4 MiB seg); single >limit entry => reject with err documented; 5 MiB actor => assert file <= 4 MiB literally; active ids preserved.
5. P4 ROOT-SCHUTZ-TEST ECHT: real test where the guard lives for ErrMissingOperationsRoot-like behavior on empty dir + active operator-API; do NOT repeat claimed controlplaneruntime test, write it real.
6. P5 SCOPE-BEREINIGUNG: pull back `cmd/baha/machine_http_executor_validation_test.go` unless card-allowed, quote card write-set line in evidence; document controlplaneruntime as allowed if in scope.
7. RULES: no existing test func deleted (`^-func Test` empty WÖRLICH); gofmt+vet empty; `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go build ./...` + `go test ./internal/machinehttp -count=1 -timeout 8m` green; merge develop at drift rc=0; push FF; ls-remote==head; PR-STATUS untouched.
8. Evidence written + END posted to f49a3303.

## Write-set (card line + scope)
- Card write-set line to quote (verify in card / plan.py): __TO-CITE__
- `internal/**` allowed by card (verify write-set line). `cmd/baha/**` only if card-allowed.

## repo-rule compliance
- No existing test function deleted (verified `^-func Test` empty).
- gofmt -l clean on all touched files; go vet clean.
- PR #1354 status NOT modified (draft left as-is; coord switches before review).

## Evidence (je Punkt + Testname + Zeugnis)

### P1 — operation_id + restart correlation (review finding 1)
- __TODO: bullets + test names + witnesses__

### P2 — append-before-event ordering (review finding 2)
- __TODO: bullets + test names + witnesses__

### P3 — hard segment limit (review finding 3)
- __TODO: bullets + test names + witnesses__

### P4 — real root-guard test (review finding 4)
- __TODO: bullets + test names + witnesses__

### P5 — scope cleanup (review finding 5 + card write-set)
- __TODO: bullets + card quote + witnesses__

## Local checks
- go build ./... : __TODO__
- go test ./internal/machinehttp -count=1 -timeout 8m : __TODO__
- gofmt -l / go vet : __TODO__
- push FF, ls-remote == head : __TODO__
