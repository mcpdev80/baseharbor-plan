ROLLE: REVIEW — rv1222b

## PLAN

0. DONE — Auftrag und bindende Richtlinien gelesen; PLAN erfasst. Native TodoWrite ist nicht verfügbar.
1. DONE — Kandidat, Task, voriges Urteil, Worker-Evidence und CI live geprüft.
2. DONE — Storage-Mapping und drei Quellfamilien geprüft; Compose-Vertragsabweichung an Owner eskaliert.
3. DONE — Dossier zur Veröffentlichung vorbereitet; Push und ls-remote im Transcript bezeugen.

## Verdict: Teilbefund 1 PASS; ESKALATION-OWNER zu Befund 2; kein Merge-Verdict

PR #1222 offen, Head b93d2fdd719a7a9c8e1846a19fa604b2ccd01286, Basis develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; HTTPS ls-remote bestätigt Head und Basis. Worker-Evidence w264.md auf Planning main gelesen. Diff zu 74a35765 geprüft; isolierter Worktree vor/nach Review unverändert.

**Befund 1:** `internal/repositoryinspect/inspect.go` klassifiziert die tatsächlich normalisierte Klasse `storage.object` als Infrastruktur und mappt sie zu Capability `object-storage.s3`. Drei MinIO-Fixturen für Compose, Quadlet und Kubernetes plus `TestInspectObjectStorageParityAcrossSourceFamilies` prüfen Klassifikation und Capability/Confidence; `TestInspectProjectsNeutralSummaryForAllSourceFamilies` prüft zusätzlich, dass Storage nicht als Workload auftaucht. Beide fokussierten Tests liefen am exakten Head erfolgreich. Erster lokaler Aufruf aus anderem Arbeitsverzeichnis scheiterte an nicht beschreibbarem Go-Cache; der korrekte Lauf im isolierten Kandidaten-Worktree mit GOCACHE=/tmp/rv1222b-gocache bestand. Dieser Befund ist behoben; der Paritätstest deckt die genannten Storage-Felder ab, nicht sämtliche Result-Semantik.

**Befund 2 — ESKALATION-OWNER:** core-750 Scope verlangt ausdrücklich, dass normalisierte `WorkloadEvidence.Components` für gemeinsame Zusammenfassungen aller Adapter kanonisch sind. `inspect.go` schließt Compose weiterhin von `shareProjectSummaryFromComponents` aus und speist dessen gemeinsame Felder über den separaten Parser. w264 dokumentiert, dass ein einfaches Hinzufügen der Projektion doppelte Evidence erzeugte und einen bestehenden Compose-Reconciliation-Test brach. Das ist ein konkreter Implementierungskonflikt, aber kein Nachweis, dass der vereinbarte Vertrag erfüllt ist. Ein unilateral akzeptierter Ausnahmeentscheid würde die Karte ändern; daher Owner-Entscheid über Beibehaltung des Kanon-Vertrags mit deduplizierender Implementierung oder ausdrückliche Änderung des Vertrags erforderlich. Bis dahin bleibt dieser Review-Befund offen.

**CI:** Run 41126074392 ist terminal failure am exakten Head: `PR Selected Checks` failure, inspect-vet/package-tests/consumer-tests/consumer-build/gofmt und Focused Python success. Laut w264 ist der Grund `coverage-unresolved` für `testdata/adoption-parity/**`, als Planner-Gap und nicht als Produktcodefehler eingeordnet; Pflicht-CI ist dennoch nicht grün. Run 41126526874 war completed/skipped, keine Qualifizierung; Run 41126526926 bei Live-Abfrage in_progress. Es wurden keine Runs ausgelöst und kein Merge versucht.

## Worker-Rezept / Stop-Kriterium

Owner soll den Vertrag für Compose ausdrücklich entscheiden. Bleibt normalisierte Evidence kanonisch, Worker soll in `internal/repositoryinspect/inspect.go` die gemeinsame Compose-Projektion aus Components aufbauen und bestehende Reconciliation/Bootstrap-/Ambiguitätssemantik ohne doppelte Findings oder Evidence erhalten; `workload_source_parity_test.go` sowie bestehende Compose-Reconciliation- und Consumer-Tests sollen echte Gleichheit der vereinbarten gemeinsamen Felder und keine Duplikate prüfen. Wird eine Ausnahme gewünscht, ist diese zuerst als autoritative Änderung des Task-Vertrags mit klarer Paritäts- und Testanforderung festzuhalten und der Kandidat daran erneut zu prüfen. CI-Owner behebt die Planner-Lücke und weist die vorgeschriebenen Gates für den finalen SHA tatsächlich nach; kein Skip als Qualifikation. Stop bis Owner-Entscheidung, unabhängiger Review und Mandatory-CI vorliegen.

## repo-rule compliance

Produkt nur lesend; keine Produktänderung, kein Merge, kein Task-Statuswechsel. basics-check meldete offene Coordinator-Reminders sowie Pool-/PLAN-Hinweise; diese wurden nicht als erledigt behauptet.

END rv1222b ESKALATION-OWNER
