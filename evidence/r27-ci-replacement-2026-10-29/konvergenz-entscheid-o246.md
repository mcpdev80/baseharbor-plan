# Konvergenz-Entscheidung PR #1213 (rv1213 j) — Coordinator-Eskalation nach §1/§3.6
## Beweislage
- 5 Reviews auf demselben Trio A/B/C (rv1213f..j), Kandidaten F->G->H->I/J/J2/K2 mit je echten Behauptungen (Callgraph-Konsolidierung JETZT echt: ein Publisher, Matrix 10/10, ReceiptError/Push-Restoration in K2 sichtbar in diff).
- Codex bleibt im Rahmen: kein 'ESKALATION OWNER'-Label, Verdict REQUEST_CHANGES mit denselben drei Punkten, file:line-Angaben wandern bei jedem Kandidaten mit (zuletzt tasklink.py:955-967, :969-997, :996-1015).
- Kosten: ~12 Worker-Runden / 10 Codex-Reviews; jede Runde liefert objektiv neue Teilbehebungen, aber die Latte liegt auf 'injizierte Fehler in JEDEM Stage durch echten Verifier + bare remote, inklusive Blob-Rekonstruktion im Snapshot-Restore'.
## Optionen
1. **Accept-with-notes** (Empfehlung des Coordinators, wenn du das Risiko trägst): A/B/C sind funktional in den K2-Commits adressiert; Restbefunde sind Tiefe der BEWEISFÜHRUNG (Injektions-Tests), nicht fehlendes Verhalten. Merge + nachgelagerte Task-Karte 'publication failure-injection tests' für die fehlenden Injektionstests.
2. **Eine letzte Runde L mit Test-Erst-Mission**: exakte Injektions-Matrix (fetch-fail, stale, unpushed-retry, push-fail, commit-fail, readback-mismatch, blob-restore) als 7 failing Tests zuerst, dann Code. Hohe Kosten-Erwartung, Konvergenz ungewiss.
3. **Reviewer-Wechsel**:独立 Codex-Session mit den rv1213f..j-Dossiers als Entscheidungsgrund 'ACCEPT oder final', ohne neue Kriterien.
4. **Owner-Entscheid anders**: du zitierst Vertragsstelle, die du anders gewichtest.
## Stand der Kette
Ruleset-Paket liegt fertig (nur 25223521 empfohlen), #1207-Kettenzyklus + Retained-Negative + Ready-Sperre alle NACH diesem Entscheid.
