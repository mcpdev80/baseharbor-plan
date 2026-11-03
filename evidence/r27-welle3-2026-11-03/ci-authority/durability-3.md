# w53-ci-authority-c — r27-ci-authority durability round 3

## Mission
- ROLLE: Worker (Lane w53). Coord f49a3303. KARTE: t-20261022-r27-ci-authority (journal-slice runde 3).
- Branch `work/r27-ci-authority-ab` head `99556b9a7f25cfaad84974bffbb6e92a0db40abb` (PR #1354).
- Grundlage: review-1354b.md rezepte 1-5.
- Write-set: `internal/machinehttp/**` + max one `cmd/baha serve` übergabe-zeile + server_run wiring. NO `.github/scripts`.
- END an f49a3303: `"END_DONE w53-ci-authority-c: head=<sha> accepted-restart=ja semantik=ja nofallback=ja retention=<wert> | <Satz>"`
- Evidence file: `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-3.md`.

## END
- Status: DONE — P1-4 implemented + green, retention decision applied.
- Retention value/decision: **journal.jsonl rotiert bei 4 MiB nach journal.jsonl.1..3 (max 4 Segmente gesamt = 16 MiB hart); beim Rotationsschnitt bleibt pro execution-id der NEUESTE Eintrag erhalten (compaction); active/unknown-Zustände werden NIEMALS entfernt; alle Grenzen als benannte constants in store.go.** Kein Result-/Progress-/Fehler-Payload im Journal (nur id/status/actor/context/zeit).
- Evidence posted to f49a3303: END_DONE.

## PLAN (numbered)
1. Fetch origin refs, worktree reuse w44 (99556b9a), verify ancestry (99556b9a not ancestor of develop).
2. P1: persist accepted Actor+Context+id before 202; load restores identity; test pending-reopen keeps identity.
3. P2: load validates real enum (bogus rejected) + never restores active; update commits durably, rolls back in-memory on append failure; counter-test each.
4. P3: fail-closed at production boundary when ops-dir absent (ErrMissingOperationsDir in registerOperatorAPI); server-construction guard.
5. P4: bounded retention — 4 MiB segment rotate .1..3 (16 MiB hard), compaction keeps newest per id, never drop active/unknown; only id/status/actor/context/time in log; test proves bound + newest-per-id + no payloads.
6. P5: gofmt -l internal/machinehttp empty; PR status untouched.
7. Local checks green (build + ./internal/machinehttp + controlplaneruntime + race); push FF; ls-remote==head.

## repo-rule compliance
- Write-set strictly internal/machinehttp/** + one serve.go line (env read, pre-existing) + server_run fail-closed guard + server.go sentinel.
- No .github/scripts touched. gofmt clean on all touched files.
- PR #1354 status NOT modified (draft reset forbidden per mission P5).
- Pre-existing reopen test updated (not removed) to reflect new secret-safe contract (result not persisted).

## Evidence (je Punkt + Testname)

### P1 — accepted-restart (review finding 1)
- `create()` now persists a pending journal line (id+state+actor+context+timestamps) BEFORE returning 202, so an accepted execution survives a crash between acceptance and first transition.
- `load()` restores Actor and Context (previously empty on reopen).
- Test: `TestRound3AcceptedIdentitySurvivesRestart` — create then crash (no start); reopen sees pending + actor + context intact.

### P2 — semantische Korruption + Schreibreihenfolge (review finding 2)
- `load()` validates State against the real enum (`validExecutionState`): `{"execution_id":"x","state":"bogus"}` fails closed.
- `load()` never restores active/unknown states (running cancelled on restart is reconciled by lifecycle, not resurrected live).
- `load()` reads ALL segments (active + numbered backups) and keeps the LAST (newest) line per id.
- `update()` commits durably; on append failure the in-memory record is rolled back so an unsafe write is never observable (fail closed).
- Tests: `TestRound3RejectsInvalidEnumState`, `TestRound3LoadRestoresOnlyTerminalStates`, `TestRound3WriteOrderingRollsBackOnAppendFailure`.

### P3 — no silent fallback (review finding 3)
- `registerOperatorAPI` (server_run.go) returns `ErrMissingOperationsDir` when `cfg.RuntimeOperationsDir` is empty — production boundary refuses silent in-memory fallback.
- Test: `TestRound3FailClosedOnMissingOpsDir` (store-level in-memory-for-empty-root preserved for unit tests; boundary guard is the sentinel).

### P4 — retention + Redaktion (review finding 4 + Owner retention decision)
- Constants (store.go): `journalSegmentCap = 4 MiB`, `journalBackupMax = 3`, `journalSegmentTotalCap = 16 MiB`.
- `rotateIfNeededLocked`: when active segment > 4 MiB, `compactActiveSegmentLocked` keeps newest line per id, then `rotateSegmentLocked` rolls to `journal.jsonl.1`, shifting `.1→.2→.3`, dropping `.3`.
- `enforceTotalCapLocked`: hard 16 MiB cap via `rotateRemoveOldestLocked`.
- Journal lines carry only id/state/actor/context/started_at/finished_at — NO result/progress/error payloads (secret/artifact safety).
- active/unknown never removed by rotation.
- Tests: `TestRound3BoundedRetentionAndNoPayloads` (6000 execs, total ≤ 16 MiB, all ids retained succeeded, no SECRET_PAYLOAD_ anywhere), `TestRound3RotationProducesNumberedBackups` (backups ≤ 3, ≥ 1 rotation, total ≤ cap), `TestRound3NeverDropsActiveStateOnRotation`.

### P5 — CI-Hygiene
- `gofmt -l internal/machinehttp internal/controlplaneruntime` empty.
- PR #1354 status untouched.

## Local checks
- `go build ./...` : OK
- `go test ./internal/machinehttp ./internal/controlplaneruntime -count=1 -timeout 8m` : OK
- `go test -race ./internal/machinehttp -run 'TestRound3|TestExecutionJournal'` : OK
