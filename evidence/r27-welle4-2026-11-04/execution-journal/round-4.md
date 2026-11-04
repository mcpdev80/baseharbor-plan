# Evidence: w147-journal-r4 — r27 execution-journal RUNDE 4

## Lane / Mission
- Lane: w147-journal-r4, Coord f49a3303, KARTE t-20261018-r27-execution-journal (RUNDE 4)
- REPO baseharbor, ZWEIG work/r27-execution-journal, PR #1373, head 0d89a13e63a (PR-Basis 1 commit behind live develop)
- Worktree: /tmp/opencode/w147-journal-r4-wt (@ 0d89a13e63a61fe027e458b36fbda255d37f53dc)
- Review-Verdict gelesen: baseharbor-plan/evidence/r27-welle4-2026-11-04/execution-journal/review-1373c.md (REJECT)
- 3 Pflichten: (1) ruckbau-fester Endzustandsbeweis, (2) Persistenzfehler beim terminalen Ubergang durchreichen, (3) kein Sleep-Polling in neuen Tests

## PLAN-Checkliste
- Mission + review-1373c vollstaendig gelesen VOR dem Coding
- worktree angelegt, provenance verifiziert (base 2ea2c6f1 = merge-base rc=0; PR 1 commit behind develop)
- write-set: git diff --name-only origin/develop...HEAD = genau 6 machinehttp-Dateien, KEIN .github, KEIN AGENTS.md
- commit-log origin/develop..HEAD: nur eigene Commits
- remote ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-execution-journal == 0d89a13e63a (wortlich)
- Baseline: race count=20 fokussiert GRUEN; build/vet/gofmt GRUEN; volles Paket nur Retention-Fuzz auf fsync (pre-existing, clean-identisch)
- Befund 1 + 3 implementiert + rueckbau-gegenprobe (mutante rot)
- Befund 2: Vertrag offen (Antwortcode bei terminal-fehler) -> OWNER-QUESTION, KEINE Self-Decision im Code
- Fachfrage an Owner gepostet; auf Antwort gewartet

## Befund 1 — Endzustandsbeweis (befund 1)
- Handler handler.go:211 ruft runExecution SYNC auf; runExecution ruft start/succeed/fail SYNC, Store update() rollt bei Persistenzfehler zurueck (store.go:303-317, appendJournalLineLocked write->sync->close). Sync = Endzustand RUECKKEHR des handlers.
- Neue Tests in execution_request_identity_test.go: nach ServeHTTP-Rueckkehr wird SOFORT (kein Pollen) gelesen (a) terminaler Execution-Zustand im Store, (b) terminale Journal-Zeile lesbar.
- Rueckbau-GEGENPROBE wegwerf-Kopie: handler.go:211 -> `go h.runExecution(...)` => NEUER TEST MUSS ROT. Krankes Commit = mutante Kopie, rote Ausgabe wortlich in Evidence (§5.6).

## Befund 2 — Persistenzfehler durchreichen (befund 2)
- handler.go:214-232 runExecution verwirft Fehler von start/progress/fail/succeed (`_ =`). Terminaler Ubergang fail/succeed darf nicht still erfolgreich sein.
- Store already fails closed: succeed/fail auf Schreibfehler => update rollt zurueck => Error. Nur runExecution schluckt ihn. Fix: runExecution gibt terminalen Fehler an handleExecute propagieren (synchron, kein Fire-and-forget).
- VERTRAGS-OFFENHEIT: Mission sagt STOP + MELDEN wenn Vertrag Antwortcode bei terminal-fehler nach 202-Codierung offen laesst. handleExecute hat die 202 bereits codiert (handler.go:201-202). Vertrag/Store-Vertrag laisse Antwortcode offen. -> OWNER-QUESTION statt Self-Decision im Code.

## Befund 3 — Sleep-Polling entfernen (befund 3)
- execution_request_identity_test.go:67,101,111 enthalten time.Sleep in Poll-Schleifen. Ersetzen durch deterministische Synchronisation (Channel/WaitForCondition mit Timeout als Fehler). Timeout im Fehlerfall erlaubt.

## Belege
- git diff --name-only origin/develop...HEAD: 7 machinehttp-Dateien (execution_duplicate_reject_test, execution_persist_failure_test [neu], execution_reconnect_test, execution_request_identity_test, handler.go, handler_test, store.go), KEIN .github, KEIN AGENTS.md
- git log --oneline origin/develop..HEAD: nur meine Commits (08bc0c29 fix(machinehttp): terminal journal commit durability r27 r4) + merge 43b14463
- ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-execution-journal == 43b14463c498d73cd98c577844ee32612bba526e (wortlich, echte adresse)
- merge-base --is-ancestor origin/develop HEAD: rc=0 (develop ea3fb38e => merge 43b14463; PR-Basis 2ea2c6f1 = merge-base)
- Rueckbau gegenprobe (mutante, wortlich): TestTerminalStateCommittedBefore202Response FAIL "no terminal event recorded on 202 tail"
- persist-fail gegenprobe (mutante, wortlich): TestRunExecutionPropagatesTerminalPersistFailure FAIL "runExecution with an un-writable terminal did not return a persist error"
- Gehosteter CI run 41927801032 @ 43b14463c TERMINAL success: go-unit-tests + go-build + go-vet + PR · Source format success

## END-LANE-STATUS
DONE — remote head 43b14463c498d73cd98c577844ee32612bba526e.
Befund 1: Endzustandsbeweis GRUEN, Rueckbau-gegenprobe (mutante go h.runExecution) ROT belegt.
Befund 2: runExecution propagiert persist-hehler, persist-fail-test GRUEN, gegenprobe (mutante swallowing) ROT belegt. Vertrag offen (handler.go:202 202 codiert VOR handler.go:211, store.go update rollt zurueck) -> QUESTION an Owner fuer Antwortcode bei terminal-fehler, fail-closed implementiert.
Befund 3: Sleep-Polling entfernt, deterministische Synchronisation.
Merge origin/develop konfliktlos; push FF; CI 41927801032 terminal-gruen.
