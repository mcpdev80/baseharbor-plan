# CODEX-REVIEW — journal wiring, PR #1393, Runde 2

- Datum: 2026-11-05
- Verdict: **REJECT** — die geforderten Konkurrenz- und Mutationstests sind weiterhin nicht diskriminierend nachgewiesen.
- Kandidat: `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170`
- Basis: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- PR: [#1393](https://github.com/mcpdev80/baseharbor/pull/1393), offen; `work/r27-journal-wiring` zeigt exakt auf den Kandidaten.
- Hosted CI: [Run 42116653735](https://github.com/mcpdev80/baseharbor/actions/runs/42116653735) ist `completed / success` am exakten Kandidaten-SHA.
- Scope: `git diff --name-only origin/develop...HEAD` enthält ausschließlich `execution_crash_resume_test.go`, `execution_mutants_test.go` und `execution_ordered_journal_test.go` unter `internal/machinehttp/`. `handler.go` ist auf Kandidat und develop Blob `060397d92ca550b7a7c323416a2828c1b6c85a2b`; `store.go` ist auf beiden Blob `b87cca57c180b4ef79c5ee0db544ae02410872eb`. Damit bleiben die produktiven Journal-Blobs aus #1373 unverändert.

## Kriterien und Befunde

1. **Produktionsnaht und echter Crash:** erfüllt. `handleExecute` ruft `createRequest` auf und läuft synchron in `runExecution`. Die Crash-Tests verwenden den echten HTTP-Endpunkt in einem Kindprozess, töten ihn nach dem dauerhaften `running`-Eintrag und prüfen denselben Root nach Neustart. Der identische Reissue-Pfad ist ebenfalls abgedeckt.
2. **Zwei konkurrierende Prozesse:** nicht erfüllt. `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` startet Prozess 1, wartet auf dessen vollständiges Ende (`p1.Wait()`), und startet erst danach Prozess 2. Das ist eine serielle Folge realer Prozesse, keine gleichzeitige Konkurrenz und kein prozessübergreifender Lock-/Append-Wettlauf. Der Barriere-Text im Test ändert diese Reihenfolge nicht.
3. **Mutant A — unterdrückter Start-Write:** nur teilweise erfüllt. Read-only-Chmod lässt `start` tatsächlich fehlschlagen und der Test zeigt einen grünen Ausgangszustand. Danach läuft aber nicht die Crash-/Resume-Zelle unter Mutation; `resumeCellWouldFail` implementiert eine eigene, verkürzte Auswertung über den Journalinhalt. Der verlangte rote Lauf der eigentlichen Zelle ist damit nicht belegt.
4. **Mutant B — verlorener Write:** nicht erfüllt. Die Testfunktion entfernt Writer Bs Zeile aus einer In-Memory-Slice. `orderedCellWouldFail` prüft dann nur `len(lines) != 2`; weder wird ein Write im Journalpfad mutiert/verloren noch die echte Ordnungszelle auf den mutierten Journalzustand angewendet. Das ist ein tautologischer Hilfscheck, kein Mutationstest. Eine unmutierte Gegenprobe der echten Zelle plus beide echten roten Einzelmutanten fehlt.
5. **Hosted / Remote / Scope:** erfüllt. `git ls-remote origin refs/heads/work/r27-journal-wiring` ergab `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170`. Es gibt keine Produktänderungen im PR-Diff; keine PR-Aktion ausgeführt.

## Eigene Läufe

Fokussiert ausgeführt (ohne `TestApplyTransitionsAppendInOrder`):

`go test ./internal/machinehttp -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable)$' -count=1 -v`

Ergebnis: alle fünf Tests PASS; die beiden Mutant-Tests loggen ihre jeweiligen synthetischen RED-Zeugen. Das bestätigt die Crash-Zellen, nicht aber die oben fehlende Diskriminierung.

`go test -race -count=20 ./internal/machinehttp -run '^TestTwoProcessesWriteJournalOrderedInProvenanceOrder$'`

Ergebnis: `ok ... 43.872s`. Der wiederholte Lauf kann die fehlende Parallelität des Testaufbaus nicht kompensieren.

## Lösungsrezept / erneute Prüfung

1. Ordnungszelle so umbauen, dass beide Kindprozesse vor Freigabe gleichzeitig laufen und denselben persistenten Journalpfad beschreiben. Prozess 2 muss nach dem gemeinsamen Barrier-Start geschrieben haben, bevor beide Kinder beendet werden; dann genau-einmal, vollständige Records und die vertraglich definierte Reihenfolge prüfen. `-race -count=20` auf diesem tatsächlich parallelen Aufbau erneut ausführen.
2. Mutation A als isolierten Einzelmutationslauf ausführen: den echten dauerhaften Start-Write unterdrücken und dieselbe Crash-/Restart-Zelle laufen lassen; deren konkrete erwartete Assertion muss rot sein. Unmutierter Kontrolllauf derselben Zelle muss grün sein.
3. Mutation B als separaten Einzelmutationslauf in der Append-/Persistenznaht ausführen: genau einen echten Journal-Write verlieren und die echte Zweiprozess-Ordnungszelle auf demselben Journal laufen lassen; deren Record-/Order-Assertion muss rot sein. Unmutierter Kontrolllauf muss grün sein. Mutationen nach jedem Lauf vollständig verwerfen.
4. Ergebnisse und exakte Testausgaben für beide Kontrollen und beide Mutanten sichern; bei geändertem Kandidaten die geforderten lokalen und Hosted-Checks am finalen SHA belegen und neue SHA-genaue Abnahme anfordern.

Keine Produktdatei geändert, kein PR-Review-/Merge-Klick und keine sonstige PR-Aktion ausgeführt.

## origin/main witness

- `git ls-tree origin/main evidence/r27-welle5-2026-11-05/journal-wiring/review-1393a.md` (after first publication): `100644 blob 5fb75674dbff0eb6489b75d4b46f01d458d819d8 evidence/r27-welle5-2026-11-05/journal-wiring/review-1393a.md`.
