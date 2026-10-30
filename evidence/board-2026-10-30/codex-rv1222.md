ROLLE: REVIEW — rv1222

## PLAN

0. DONE — Dispatch und bindende Richtlinien gelesen; PLAN hier erfasst. Native TodoWrite ist in dieser Sitzung nicht verfügbar.
1. BLOCKED — Vertrag und Remote geprüft; beauftragter Kandidat und Evidence nicht auffindbar.
2. BLOCKED — Acceptance-Prüfung und inhaltliches Urteil benötigen den tatsächlich beauftragten Kandidaten.
3. DONE — Blocker-Evidence zur Veröffentlichung vorbereitet; Push und ls-remote sind im ausführenden Transcript nachzuweisen.

## Verdict: BLOCKED — kein Acceptance- oder Merge-Verdict

Der Auftrag bezeichnet PR #1222, Head 2f98804d und Runs 41120374094/41120389942. Die authentifizierte Live-API meldet #1222 offen bei Head 74a357654c174e0818e5323ed71cab4c694157b2 und Basis 72ba7a99ff7dcd4b04ee3cf16516991ef567d376. HTTPS ls-remote bestätigt für die angegebene Branch und develop genau diese SHAs. API commits/2f98804d antwortet 422 (kein Commit), beide Run-APIs antworten 404. Auch der Fetch des PR-Refs liefert 74a35765, nicht 2f98804d. Die genannte Planning-Evidence q263.md ist lokal nicht vorhanden; Dateisuche fand lediglich den q263-Dispatch. Die gemeldeten erfolgreichen Runs können daher nicht verifiziert werden.

core-750 verlangt unter anderem Quellfamilien-Parität, normalisierte Ports und Health, Workload-/Infrastructure-Klassen, source-neutrale Capability-Findings, source-neutralen Log-Vorschlag, gleiche Result-Semantik für Human/JSON/MCP, keine Mutation und bestehendes Compose-Verhalten. Die vorhandene rv1224-Evidence beurteilt den anderen Head 74a35765; sie belegt keine Abnahme von 2f98804d. Die aktuelle Task-Abfrage zeigt zwei nicht akzeptierte Abhängigkeiten. Ein inhaltliches Urteil über den beauftragten Kandidaten wäre ohne überprüfbaren Diff und Run-Zeugen spekulativ.

## Lösungsrezept und Stop-Kriterium

Der zuständige Owner/Worker soll den tatsächlich veröffentlichten Repository-, PR- und vollständigen Head-SHA sowie die zugehörigen zugänglichen PR-/Qualify-Run-IDs und q263-Evidence bereitstellen oder den Dispatch auf den verifizierten Live-Stand korrigieren. Danach SHA-genauen Diff und jeden Acceptance-Punkt einschließlich capability mapping und rv1224-Bemerkungen unabhängig prüfen, zugehörige geforderte Go-Tests/vet und CI nachweisen. Stop bei fehlendem SHA, fehlender Evidence, offenem Pflichtbefund oder nicht erfülltem Gate. Keine Produktänderung oder Merge durch diese Review-Lane.

## repo-rule compliance

Nur Remote-Lesezugriffe und Planning-Evidence; kein Produkt-Push, Merge, Review-Freigabe oder Änderung fremder Claims. basics-check meldete offene Coordinator-Reminders, Pool- und PLAN-Flags; unbekannte Lanes bleiben unberührt. Die Evidence ist kein Ersatz für die fehlende Kandidatenprüfung.

END rv1222 BLOCKED

## PLAN — korrigierte Mission rv1222

0. DONE — Korrigierten Dispatch und Richtlinien gelesen; native TodoWrite ist nicht verfügbar.
1. DONE — Head, Basis, Task-Vertrag, frühere Evidence und CI live abgeglichen.
2. DONE — Acceptance und Capability-Mapping anhand des Kandidaten geprüft; Urteil und Rezept erfasst.
3. DONE — Evidence zur Veröffentlichung vorbereitet; Push und ls-remote im Transcript.

## Korrigiertes Urteil: REQUEST_CHANGES

Die frühere BLOCKED-Mission bezog sich auf einen falschen Head und ist storniert. Aktuelle Prüfung: PR #1222 offen bei 74a357654c174e0818e5323ed71cab4c694157b2 gegen develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; beide per HTTPS ls-remote bezeugt. Run 41059938103 completed/success; PR Selected Checks success von Actions App 15368 und inspect-package-tests, inspect-vet, inspect-consumer-tests und build success. Reuse der vorhandenen exact-head Evidence, kein erneuter gehosteter Lauf. Full Go test laut rv1224-Evidence timeout; vollständiges Go vet nicht nachgewiesen. Die Task-Abfrage zeigt zwei nicht akzeptierte Abhängigkeiten. Kein Merge.

**Befund, nach rv1224 neu festgestellt:** `internal/repositoryinspect/workload_source.go:644-656` normalisiert MinIO/SeaweedFS als `storage.object`; `workload_source_compose_quadlet.go:42-43` verwendet denselben Klassennamen. Quadlet und Kubernetes verwenden den gemeinsamen Classifier. Die neue Projektion in `inspect.go:471-490` und das Mapping `inspect.go:508-520` erkennen dagegen `object-storage.s3` als *Klasse*, nicht `storage.object`. Ein non-Compose Objekt-Storage-Component mit Image wird daher als Workload statt Infrastruktur klassifiziert und sein normalisierter Infrastrukturtyp erzeugt kein `object-storage.s3`-Finding. Das verletzt Source-neutral Classification und Capability-Findings. Die Paritätsfixtur prüft nur SQL und Cache und deckt Objekt-Storage nicht ab. Die frühere rv1224-ACCEPT-Aussage deckt diesen Unterschied nicht ab und ist insoweit nicht übernehmbar.

Weiterer Vertragsabgleich: `inspect.go:215-217` schließt Compose ausdrücklich von der Projektion aus `WorkloadEvidence.Components` aus; gemeinsame Compose-Ports, Health und Klassifikation stammen weiterhin aus dem separaten Parser (`:162-187`). Das widerspricht dem ausdrücklichen core-750 Scope, der normalisierte Components für gemeinsame Zusammenfassungen aller Adapter als kanonische Quelle verlangt. Der Test prüft primär Anwesenheit statt Gleichheit vollständiger Semantik und belegt diese Vertragsanforderung nicht. Das zuvor gemeldete Evidence-Kind für den Logs-Vorschlag ist hingegen im Code korrigiert.

## Worker-Rezept

In `internal/repositoryinspect/inspect.go` den tatsächlich vom Normalizer ausgegebenen Typ `storage.object` auf Infrastruktur und Capability `object-storage.s3` abbilden. Gemeinsame Ports, Health und Workload-/Infrastruktur-Projektion für Compose, Quadlet und Kubernetes aus den normalisierten Components speisen; Compose-spezifische Bootstrap-/Ambiguitätsdetails erhalten und doppelte Ergebnisse vermeiden. In `workload_source_parity_test.go` echte gleichwertige MinIO- oder SeaweedFS-Fixturen aller drei Familien und Vergleiche von Klasse, Capability und vollständiger gemeinsamer Semantik ergänzen; bestehende Compose- und Consumer-Tests mit fokussierten Tests ausführen. Für den endgültigen SHA die auf der Karte geforderten full Go tests/vet und Mandatory-CI mit tatsächlichen Ergebnissen nachweisen; bei abweichendem Mapping, Paritätsfehlern, fehlenden Pflichtchecks oder offenen Abhängigkeiten stoppen und erneut unabhängig prüfen lassen.

## repo-rule compliance — korrigierte Mission

Lesender Review; keine Produktänderung, kein Task-Statuswechsel, keine Freigabe oder Merge. Planning check: 0 Fehler, 14 bestehende Warnungen. Coordinator-Reminders und Pool-Hinweise bleiben offen.

END rv1222 REQUEST_CHANGES
