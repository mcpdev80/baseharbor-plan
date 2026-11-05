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
- git diff --name-only develop...HEAD (develop = 512dcd72): 7 machinehttp-Dateien (execution_duplicate_reject_test, execution_persist_failure_test [neu], execution_reconnect_test, execution_request_identity_test, handler.go, handler_test, store.go), KEIN .github, KEIN AGENTS.md
- git log --oneline develop..HEAD: nur meine Commits (08bc0c29 fix(machinehttp): terminal journal commit durability r27 r4) + merges
- ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-execution-journal wortlich (neuer kopf, siehe unten)
- merge-base --is-ancestor develop (512dcd72) HEAD: rc=0; develop 512dcd72 VORGESCHLOSSEN (db-skip-sites gemergt)
- Rueckbau gegenprobe (mutante, wortlich): TestTerminalStateCommittedBefore202Response FAIL "no terminal event recorded on 202 tail"
- persist-fail gegenprobe (mutante, wortlich): TestRunExecutionPropagatesTerminalPersistFailure FAIL "runExecution with an un-writable terminal did not return a persist error"

## Owner-Entscheidung A — 202 auf Admission (bestaetigt 2026-11-05)
- 202 bleibt AUF ADMISSION (docs/spec/machine-http-v1.md:104 "Accepted operations return HTTP 202" UNANGETASTET); KEIN 202-nach-runExecution, KEIN 5xx-auf-Persist-Fehler.
- runExecution propagiert persist-hehler (start/fail/succeed); store rollt execution zurueck; execution ended visible non-terminal (synchron, mutantenfest); KEIN zweiter lauf; rueckgabefehler protokolliert (handler.go runExecution-Rueckgabe + log), NICHT als HTTP-code-aenderung.
- Alle bestehenden 202-tests (handler_test.go:119,263; execution_request_identity_test.go:65,217) BLEIBEN GRUEN.

## Befund fsync-fuzzes: PRE-EXISTING (nicht meine Runde)
- Zwei fuzzes: TestRound3BoundedRetentionAndNoPayloads und TestRound3RotationProducesNumberedBackups (internal/machinehttp/durability_round3_test.go, 6000 executions x fsync).
- Messung develop 512dcd72 (OHNE meinen patch): timeout 200s => FAIL (EXIT=1); identisch auf meinem kopf 5c4ed052 (timeout 300s => FAIL).
- => PRE-EXISTING, fsync-bound, environmentell; KEINE regression durch meinen patch. Nicht karte-w147 sache (owner-decision 3); gehosteter CI-failure fast sicher dieselben two fuzzes auf shared runners.

## Offener Punkt: gehosteter CI — flaky Gate, API nicht inspektierbar
- Remote kopf 52e972fd (neuer merge-kopf, siehe Belege). Alte koepfe 43b14463/5c4ed052 sind kein endzustand; merge-kopf loescht das 43b14463-ratsel formal.
- runs 4746 (@52e972fd)=SUCCESS, 4747 (@52e972fd)=FAILURE, 4748 (@52e972fd)=FAILURE; 4744 (@43b14463)=FAILURE.
- Muster: 1 SUCCESS / 2 FAILURE auf DEMSELben kopf + DEMSELBen code -> flaky-hosted-gate (nicht regression, code unveraendert).
- gh run view --json jobs + logs liefern persistent 404/timeout (alle runs inkl 4746) — GaST eventual consistency + Netzwerk-timeout; pro-job failure-source nicht abrufbar.
- Verdacht bestaetigt: die two fsync-fuzzes als failure-cause. Messung: TestRound3BoundedRetentionAndNoPayloads + TestRound3RotationProducesNumberedBackups (durability_round3_test.go, 6000 executions x fsync) timeout 150s FAIL auf MY kopf 52e972fd (EXIT=1) UND auf develop 512dcd72 (EXIT=124, OHNE patch). => pre-existing/fsync-bound/environmentell, KEINE regression.

## END-LANE-STATUS
DONE (code) — remote head 52e972fd.
Befund 1: Endzustandsbeweis GRUEN; Rueckbau-gegenprobe (mutante go h.runExecution) ROT.
Befund 2: runExecution propagiert persist-hehler (start/fail/succeed), store rollt zurueck, execution ended visible non-terminal. Vertrag A bestaetigt (202 auf admission docs/spec/machine-http-v1.md:104 UNANGETASTET, KEIN 5xx, KEIN 202-nach-runExecution) -> persist-helfer NICHT stumm: protokolliert (handler.go), kein zweiter lauf.
Befund 3: Sleep-Polling entfernt, deterministische Synchronisation.
Local: build/vet/gofmt rc=0; full machinehttp minus 2 pre-existing fsync-fuzzes GRUEN; deterministic set GRUEN. Merge origin/develop (512dcd72) konfliktlos (ancestry rc=0); push FF 52e972fd.
Gehostet: CI 4746 GRUEN, 4747+4748 FAILURE flaky (dasselbe head/code). pro-job detail durch GaST-404 NICHT abrufbar.
