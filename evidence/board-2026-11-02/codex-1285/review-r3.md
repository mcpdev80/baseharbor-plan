# PR #1285 — Codex Review Runde 3

ROLLE: REVIEW
Urteil: REJECT (Merge-Vorbedingung nicht nachgewiesen)
Reviewer: OpenAI Codex, unabhängige Session; Session-ID und genaue Modellkennung nicht verfügbar; kein Horde-Task zugewiesen.
Kandidat 20bef715e0180eddd71e2172c3bfb021ae76109f; develop 9a93865a935624045e96a503da0a3a1c2f7d1559; main e92e20588c5737f566e29d47bbd08a9bcaed19d3. `git ls-remote` vor und nach Prüfung kontrolliert.

## Kandidat

- Vollständiger PR-Diff gelesen: receipt_verifier.py und drei Testdateien. Optional skipped wird im erreichten Pilotpfad zugelassen, failure/timed_out/action_required blockieren; identische Plan-Fixture mit skipped/failure testet beide Fälle.
- required_validation_checks liest validierte Objekt-IDs; neue Fixtures enthalten id/owner/command. Native Prefixe und Consumer-/Demo-Dependencies vorhanden.
- Genau ein Job je erforderlichem Namen; Regressionen enthalten Erfolg/Fehler in beiden Reihenfolgen. Fixture enthält darüber hinaus bereits einen dritten gleichnamigen Job; sie testet Ambiguität, aber nicht isoliert ein Paar.
- CLEAN/MERGEABLE, keine Review-Threads; Actions Run 41456543735: PR Selected Checks SUCCESS auf dem SHA (Job 125316163625, App 15368), Focused Python, Planner und Receipt-Validierung SUCCESS.

## Promotable: nicht nachgewiesen

Selbst berechnet im isolierten `/tmp/codex1285-r3-sim.git` nach Abruf der drei exakten Remote-Refs: `git merge-tree --write-tree e92e20588c5737f566e29d47bbd08a9bcaed19d3 20bef715e0180eddd71e2172c3bfb021ae76109f` endet mit Status 1 und zahlreichen echten Konflikten, u. a. `.github/workflows/receipt-post-run.yml`, `scripts/receipt_verifier.py`, `scripts/pr-gate-plan.py`, go.mod und CHANGELOG.md. Der ausgegebene Tree `37bc83316d5f3733631afab1348aa823ea76278b` enthält Konfliktmarkierungen und ist kein verifizierter Union-Tree. Deshalb wurden die verlangten S/M2-Commits und die Aussage „keine Defense-Minus-Zeilen“ nicht vorgetäuscht: ohne konfliktfrei aufgelösten, nach inhaltlichen Kriterien geprüften Union-Tree ist der Nachweis nicht erbracht. Der direkte Konflikt ist kein Beweis, dass die ausdrücklich erlaubte S/M2-Simulation unmöglich wäre.

Rezept: Worker/Coordinator erstellt einen prüfbaren Union-Tree für diese exakten main-/develop-/Kandidaten-SHAs, löst Konflikte unter Erhaltung der main-Defense und der Kandidatenänderung inhaltlich auf, dokumentiert die Defense-Prüfung und berechnet damit S und M2 gemäß RUNBOOK.md:166 einschließlich merge-tree und diff main..M2. Danach aktuelle Remote-SHAs und die Pflichtchecks erneut prüfen. Keine Produktänderung in dieser Review-Session und kein Merge ohne diese Vorbedingung.
