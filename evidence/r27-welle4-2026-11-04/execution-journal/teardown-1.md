## w134 teardown-1: terminal journal write race fixed

ROLLE: Worker (Lane w134). Coord f49a3303. KARTE: t-20261018-r27-execution-journal. REPO: baseharbor. ZWEIG: work/r27-execution-journal (PR #1373).

### WAS WIRD ENTWICKELT (Produkt-/Funktions-Sprache)

Beim Maschinen-Ausfuehrungsprotokoll (execution journal) der machinehttp-API war die Zusage des akzeptierten Auftrags nicht lueckendig im Protokoll fixiert: Ein Hintergrund-Goroutine schrieb den finalen Endzustand (succeed/fail) in das Journal, NACHDEM die 202-Antwort bereits zurueckgegeben war. Zwischen 202-Antwort und Journal-Eintrag bestand ein Fenster, in dem der Prozess sterben konnte und die akzeptierte Ausfuehrung im Protokoll verloren gainge. Zudem rachte sich das asynchrone Schreiben bei Test-Teardown einen Datenwettlauf (TempDir-Cleanup: "directory not empty"). Der finale Protokoll-Eintrag ist jetzt SYNCHRON, bevor handleExecute zurueckgibt.

### PLAN-CHECKLISTE

- Fehler reproduziert (-race intermittierend rot: directory not empty).
- Schreiber lokalisiert (handler.go runExecution, goroutine hinter handleExecute).
- Fix: runExecution synchron in handleExecute erwartet, kein fire-and-forget.
- Nachweis: -count=10 gruen, -race gruen,全package -race gruen.
- Mutation belegt: fire-and-forget wieder => test wieder rot.
- CI gehostet beobachtet (run 41892296752) => Success, terminal.

### 1. FEHLERBILD (wortlich, vorher)

```
--- FAIL: TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest (0.00s)
    testing.go:1464: TempDir RemoveAll cleanup: unlinkat /tmp/TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest3634897540/001/journal: directory not empty
```

Zusaetzlich unter -race (race detector, original unveraendert):
```
--- FAIL: TestRequestIdentityIndexSurvivesJournalReopen (0.00s)
    execution_request_identity_test.go:80: changed-content reuse appended journal line: before=2 after=3
```

Wiederholbar mit:
```
go test ./internal/machinehttp -run 'TestRequestIdentity' -race -count=20
```
Intermittierend: ohne -race meist gruen, mit -race wiederholt rot (Wettlauf des Background-Schreibers).

### 2. SCHREIBER: DATEI:ZEILE

- Goroutine-Start: internal/machinehttp/handler.go:206 (ursprenglich)
  `go h.runExecution(context.WithoutCancel(ctx), ...)` — hinter handleExecute, fire-and-forget.
- Schreiben des finalen Endzustands: internal/machinehttp/handler.go:231
  `_ = h.executions.succeed(executionID, result)` (bzw. fail an handler.go:225).
- Journal-Append des Endzustands: internal/machinehttp/store.go appendJournalLocked -> appendJournalLineLocked (write->Sync->Close, synchron, aber im background-goroutine).
- Ursache: handleExecute startete runExecution als background-goroutine; der 202-Antwort folgte kein await. Der executorFunc der Test ist ein no-op, der schnell zurueckgibt, aber succeed() schreibt erst nach der executor-Rueckgabe ins Journal => der Test liest journalLineCount synchron, bevor der schreiben-de goroutine fertig ist; spaeter loescht t.TempDir() das journal-Verzeichnis, waehrend der schreiber noch eine zeile anhaengt => "directory not empty".

### 3. BEHEBUNG: SYNCHRONER ABSCHLUSS VOR handleExecute-Rueckgabe

- Neue synchrone stelle: internal/machinehttp/handler.go ~211
  `h.runExecution(context.WithoutCancel(ctx), ...)` — KEIN `go`-praefix mehr. handleExecute WAITET den terminalen Journal-Commit (succeed/fail), bevor die 202-Antwort zurueckgegeben wird.
- Event-Emission bleibt auf dem synchronen Commit-Pfad: emitLocked (store.go) mutiert record.events / nextSeq unter s.mu und DARF nicht aus einem background-goroutine laufen (Wettlauf um record.events). Ein asynchroner event-fan-out wurde implementiert und wieder zurueckgenommen, weil er einen data-race ausloeste; der commit-before-publish-Pfad bleibt damit fully synchronous.
- Kein sleep/keine poll-Schleife; Abschluss ist deterministisch (goroutine-Beendigung).
- Dokumentation (handler.go runExecution): Vertrag commit-before-publish (task t-20261018-r27-execution-journal, Outcome-zeile) benannt.

### 4. NACHWEIS (wortlich, nachher)

```
$ go test ./internal/machinehttp -run 'TestRequestIdentity' -count=10
ok  	github.com/mcpdev80/baseharbor/internal/machinehttp	0.062s

$ go test ./internal/machinehttp -run 'TestRequestIdentity' -race -count=10
ok  	github.com/mcpdev80/baseharbor/internal/machinehttp	1.060s

$ go test ./internal/machinehttp/ -race
ok  	github.com/mcpdev80/baseharbor/internal/machinehttp	320.750s
```
-v (Auszug, gruen):
```
=== RUN   TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest
--- PASS: TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest (0.00s)
=== RUN   TestRequestIdentityIndexSurvivesJournalReopen
--- PASS: TestRequestIdentityIndexSurvivesJournalReopen (0.00s)
```

### 5. MUTATIONSBELEG (synchrone stelle -> wieder goroutine => test rot)

Mutation zurueck zu `go h.runExecution(...)` (nur handler.go, committet zurueckgestellt):
```
$ go test ./internal/machinehttp -run 'TestRequestIdentity' -race -count=20
--- FAIL: TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest (0.00s)
    testing.go:1464: TempDir RemoveAll cleanup: unlinkat /tmp/.../journal: directory not empty
...
FAIL
```
Belegt: die synchrone await-stelle ist die ursache; ohne sie wiederholt sich der fehler. Fix wiederhergestellt (commit 0d89a13e).

### 6. GEHOSTETER LAUF (beobachtet, terminal)

- Run-ID: 41892296752 (ci.yml, pull_request, "CI · PR #1373 #4711", gestartet 2026-11-04 18:57 UTC).
- Status: Success (terminal). Total duration 8m 5s.
- PR · Validation · go-unit-tests: gruen (laeuft TestRequestIdentity... unter -race-artiger matrix). Keine rote zeile.
- Kein rerun getriggert; .github/** nicht angefasst (Owner-scope).

### 7. GRENZEN-EINHALTUNG

- KEIN second branch: weiter auf work/r27-execution-journal (canonical candidate). ls-remote witness section 8.
- KEIN force-push / kein rebase. merge-only; fix = commit 0d89a13e.
- KEIN .github/** / workflow-touch. name-only-diff section 8 listet nur internal/machinehttp/*.
- KEIN merge (PR #1373 bleibt offen; merge = Owner/Codex-Abschluss).
- KEIN subagent (executed fully in this session).
- scratch nie in oekosystem-wurzel.

### 8. BELEG (vor END)

- git ls-remote origin refs/heads/work/r27-execution-journal:
  0d89a13e63a61fe027e458b36fbda255d37f53dc
- local head: 0d89a13e63a61fe027e458b36fbda255d37f53dc (remote == local, wortlich).
- git merge-base --is-ancestor ecbb8854 HEAD -> rc=0 (ecbb8854, PR #1355, IS ancestor — single-candidate chain).
- git merge-base --is-ancestor origin/develop HEAD -> rc=0 (develop 2ea2c6f1 IS ancestor).
- git diff origin/develop...HEAD --name-only (wortlich, NUR dieses projekt):
  internal/machinehttp/execution_duplicate_reject_test.go
  internal/machinehttp/execution_reconnect_test.go
  internal/machinehttp/execution_request_identity_test.go
  internal/machinehttp/handler.go
  internal/machinehttp/handler_test.go
  internal/machinehttp/store.go
- mein fix (committet, unveraendert): NUR internal/machinehttp/handler.go, 6 insertions / 1 deletion (synchrone await-stelle). store.go-Aenderungen sind bestehende, committete r27-arbeit des zweigs (createRequest/requestIndex), NICHT mein teardown-fix.

### END

END_DONE w134-journal-base: head=0d89a13e basis=2ea2c6f1 ancestor=ecbb8854+develop yes ls-remote=0d89a13e gates=terminal CI Success (run 41892296752, go-unit-tests gruen) — teardown-race behoben: runExecution jetzt synchron vor 202-Antwort (handler.go, 6 Zeilen), Event-Emission bleibt sync-commit-pfad; -count=10 + -race gruen, Mutation belegt (goroutine => wieder rot), PR #1373 offen, KEIN .github-touch.
