# PR #1285 — Codex Review Runde 2

ROLLE: REVIEW
Urteil: REJECT
Reviewer: OpenAI Codex, unabhängige Session; Session-ID und genaue Modellkennung nicht verfügbar, kein Horde-Task zugewiesen.
Kandidat: b8666695a80f4b81d165915da4eb966e5550347c; develop: 9a93865a935624045e96a503da0a3a1c2f7d1559. Vor und nach Review via ls-remote bestätigt. Vollständigen PR-Diff und rcptverfix/evidence.md geprüft.

## Blockierende Befunde und Worker-Rezept

1. `scripts/receipt_verifier.py:511-515` behandelt jede conclusion außer None/success als ausgeführten Fehler. GitHub liefert aber `skipped` für regulär nicht ausgewählte Jobs: diese werden damit blockiert, entgegen dem Vertrag und genau dem Ziel des Fixes. Der positive Test `test_not_required_skipped_is_accepted` prüft nur den früheren No-op-Rücksprung und erreicht diese Schleife nicht. Worker: skipped explizit zulassen, tatsächlich ausgeführte negative terminale Zustände blockieren; einen realistischen aufgelösten Pilotplan mit optional skipped und denselben Plan mit optional failure testen. No-op-Verhalten separat nach Vertrag prüfen.
2. Zeilen 474-475 interpolieren `str(check_id)`, obwohl `required_validation_checks` aus Objekten wie `{'id': 'source-contracts', 'owner': ..., 'command': ...}` besteht (Planner-Zeile 59 ff. und 1865); der maßgebliche `pr-authenticated-results.py` extrahiert `c['id']`. Der Code sucht somit nach einem Jobnamen mit Python-Dict statt `PR · Validation · source-contracts` und blockiert echte Plans. Die neuen Tests verwenden unrealistische Zahlen `[7]`. Worker: Schema validieren, ID aus jedem Objekt extrahieren und mit echtem Planobjekt sowohl erfolgreichen als auch fehlenden/fehlgeschlagenen Job testen.
3. Die beiden behaupteten Reihenfolgetests für Duplikate fügen beide einen erfolgreichen Shadow per `extra_jobs` an; weder werden Reihenfolge noch ein fehlgeschlagener ursprünglicher Job variiert. Die Zählprüfung selbst blockiert Duplikate, aber die verlangte Regression beider Reihenfolgen fehlt. Worker: success/failure-Paare explizit in beiden Reihenfolgen liefern und Ambiguität nachweisen.
4. Promotable gemäß RUNBOOK.md:166 ist in der vorgelegten Evidence nicht nachgewiesen. Worker/Coordinator: aktuellen main/develop/Integration-Kandidaten nach dem dort beschriebenen Verfahren belegen, bevor eine Merge-Entscheidung fällt.

## Weitere Kriterien

Exakte native Prefixe und Consumer-/Demo-Dependency-Zweige sind vorhanden. Der PR ist aktuell CLEAN/MERGEABLE; keine Review-Threads. Run 41452440424: PR Selected Checks SUCCESS, Job 125302012137, App 15368, auf dem geprüften Head; Focused Python, receipt-execution-tests, pr-planner-tests und weitere ausgewählte Validierungen SUCCESS. Grüne Tests widerlegen die oben belegten realen Schema- und Skipped-Fehler nicht. Die Worker-Evidence enthält veraltete Angaben zur vorherigen Revision neben der Korrekturrunde. Kein Merge durchgeführt.
