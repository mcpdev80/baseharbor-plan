# CODEX-REVIEW — journal wiring, PR #1393

- Datum: 2026-11-05
- Verdict: **REJECT** (Abnahme nicht belegt; gezielte Korrektur und erneute SHA-genaue Prüfung erforderlich)
- Kandidat: `3fa46bc299b0e372d59b214ec8708b918e46c37d`
- Basis: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- PR: [#1393](https://github.com/mcpdev80/baseharbor/pull/1393), offen; der Remote-Zweig `work/r27-journal-wiring` zeigt exakt auf den Kandidaten. PR #1392 ist geschlossen und zeigt auf den früheren Kopf `3a5ce890118741d91d65b57aca89bf897a18af26`.
- Hosted CI: [Run 42101103524](https://github.com/mcpdev80/baseharbor/actions/runs/42101103524) ist `completed / success` und hat exakt den Kandidaten-SHA.
- Scope: `git diff --name-only origin/develop...HEAD` enthält ausschließlich die drei neuen Dateien `internal/machinehttp/execution_crash_resume_test.go`, `internal/machinehttp/execution_mutants_test.go` und `internal/machinehttp/execution_ordered_journal_test.go` (490 additions, keine Löschungen). Die Produktionsverdrahtung liegt bereits in der Basis. `handleExecute` ruft `h.executions.createRequest(...)` vor dem 202 auf und führt danach synchron `h.runExecution(...)` aus (außer bei gesetztem Test-Hook); `runExecution` persistiert start und terminalen Zustand. `store.go` hat auf Kandidat und develop denselben Blob `b87cca57c180b4ef79c5ee0db544ae02410872eb`; der PR verändert keine der von #1373 eingeführten Journal-Dateien.

## Kriterien und Befunde

1. **Produktionsnaht gelesen:** erfüllt als Quelllesung. `internal/machinehttp/handler.go:156` zeigt die echte Sequenz `createRequest` → Antwortcodierung → `runExecution`; die persistente Implementierung von `store.go` ist identisch zu develop. Die drei PR-Dateien ändern jedoch nur Tests.
2. **Crash-Wiederanlauf-Zelle:** nicht erfüllt. `TestCrashDuringApplyLeavesRunningUncertainAfterRestart` und `TestRestartReconcilesReissueToOriginalExecution` verwenden direkte Store-Aufrufe (`createRequest`, `start`) und setzen den alten Store im selben Testprozess auf `nil`. Es wird weder ein echter Prozess beendet/neugestartet noch die HTTP-Produktionsnaht ausgeführt. Die Assertions zu `running` und Reissue sind sinnvoll, beweisen aber den verlangten Crash-/Apply-Pfad nicht.
3. **Zweiprozess-Ordnung:** nur teilweise erfüllt. `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` startet echte Kindprozesse via `os/exec`, aber strikt seriell: Prozess 1 endet, dann startet Prozess 2. Damit werden weder konkurrierende Writer noch die behauptete prozessübergreifende Ordnung/Lock-Kollision nachgebaut. Die zwei Zeilen werden auf Anzahl, JSON-Gültigkeit und unterschiedliche IDs geprüft.
4. **Mutanten:** nicht erfüllt. `TestMutantA_JournalWriteMakesResumeReal` öffnet einen unabhängigen leeren Temp-Root; es unterdrückt keinen Write des Kandidaten und lässt keine Resume-Zelle unter Mutation rot laufen. `TestMutantB_WrongOrderIsDetectable` prüft eine tatsächliche Writer-Order, führt aber keine Ordnungs-Mutation aus und zeigt keinen roten Mutationstest. Auch `TestApplyTransitionsAppendInOrder` benutzt direkte Store-Helper-Aufrufe statt des geforderten Mutation-Laufs. Die geforderten zwei realen Einzelmutanten (Journal-Write unterdrückt; Write verloren) sind daher **0/2 nachgewiesen**.
5. **#1373-Blobs / Hosted / Remote:** `store.go`-Blob auf Kandidat und develop identisch; der PR-Diff enthält keine bestehenden Journal-/Blob-Dateien. `ls-remote origin refs/heads/work/r27-journal-wiring` ergab exakt `3fa46bc299b0e372d59b214ec8708b918e46c37d`; Hosted-Run 42101103524 ist terminal erfolgreich am selben SHA.

## Lokaler Lauf

Der geforderte fokussierte Lauf wurde mit
`go test ./internal/machinehttp -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable|TestApplyTransitionsAppendInOrder)$' -count=1 -v`
versucht. Zunächst konnte das konfigurierte GOCACHE nicht beschrieben werden (`read-only file system`). Mit `GOCACHE=/tmp/baseharbor-review1392a-gocache` endete der Build vor Testausführung wegen `disk quota exceeded`. Daher liegt kein eigener grüner/roter Testlauf vor; der Hosted-Run ersetzt die oben fehlenden diskriminierenden Prüfungen nicht.

## Lösungsrezept / Wiederaufnahme

1. Crash-Zelle durch die echte HTTP-`handleExecute`-Produktionsnaht führen, den laufenden Apply in einem Kindprozess tatsächlich abbrechen und nach Neustart mit demselben persistenten Root sowohl `running/uncertain` als auch identische Reissue-ID verifizieren.
2. Zwei Kindprozesse gleichzeitig (Barriere/Handshake) auf dieselbe persistente Journaldatei schreiben lassen; jede Operation muss genau einmal und vollständig erscheinen. Reihenfolge über einen vorab definierten Provenienz-/Sequenzvertrag prüfen, nicht durch bloß serielle Starts.
3. Zwei getrennte, kontrollierte Mutationseinzeläufe ausführen: (a) Journal-Write vor Apply unterdrücken, (b) einen Journal-Write verlieren/fehlschlagen lassen. Jeweils die zugehörige Produktionszelle ausführen und die konkrete erwartete Assertion als ROT erfassen; anschließend Mutationen verwerfen.
4. Auf dem finalen Kandidaten die fokussierten Zellen erfolgreich ausführen und einen Hosted-Lauf am finalen SHA belegen; danach neue SHA-genaue Abnahme.

Kein Produktcode geändert, keine PR-Aktion ausgeführt.
