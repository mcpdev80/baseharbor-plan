ROLLE: REVIEW — rv1230b

## PLAN

0. DONE — Auftrag und bindende Richtlinien gelesen; PLAN erfasst. Native TodoWrite ist nicht verfügbar.
1. DONE — Head, Basen, Karte, vorheriges Urteil und erreichbare CI-Evidence verifiziert.
2. DONE — Beauftragten historischen SHA und beide Diffs geprüft; aktuellen Head nicht als denselben Kandidaten ausgegeben.
3. DONE — Dossier zur Veröffentlichung vorbereitet; Push und ls-remote im Transcript bezeugen.

## Verdict: REQUEST_CHANGES für historischen SHA; aktueller Kandidat nicht abgenommen

Der Auftrag nennt 7d63e0c6b6fe947b6acb7367dc4b71cd9d937503. Der Live-PR #1230 ist offen gegen develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376 und steht inzwischen auf b4a55e1868047305e58d03b135474d8035513a61, Branch work/postrun-nonpr-skip; HTTPS ls-remote bezeugt PR-Branch, develop und main e92e20588c5737f566e29d47bbd08a9bcaed19d3. 7d63e0c6 ist ein verifizierter Vorfahr, kein aktueller Head. Run 41123188375 antwortet 404; die Commit-Check-API für 7d63e0c6 lieferte keine Check-Runs. Die behaupteten tatsächlich gelaufenen PR-Jobs sind für diesen SHA nicht bestätigt. q265.md ist auf dem abgefragten Planning-main und im Workspace nicht auffindbar.

**rv1230-Befunde bestehen auf 7d63e0c6:** Gegen main zeigt der Workflow-Diff weiterhin nur den Download-Guard, keinen Guard für `Decode pr-plan and extract candidate_sha`; dieser Schritt versucht nach übersprungenem Download `plan.zip` zu öffnen. Die zwei neuen Tests in `F1NegativeNonPRSkip` sind weiterhin nur YAML-String-Assertions, kein ausgeführter Fake-Producer-Skip. `gh api ... || echo ""` behandelt weiterhin fehlgeschlagene Event-Abfrage als erfolgreichen Non-PR-Skip. Der Auftrag bezeichnet rv1230 als BLOCKED; das veröffentlichte rv1230-Dossier lautete tatsächlich REQUEST_CHANGES mit diesen drei Befunden.

**Basen:** Gegen main beträgt der Merge-Base-Diff zwei Dateien, 81 additions/1 deletion, einschließlich eines CI-Trigger-Kommentars. Gegen develop umfasst der Merge-Base-Diff 2453 Dateien, 331343 additions/21727 deletions: der Kandidat ist auf der main-Historie aufgebaut und trägt eine umfassende fremde Änderungskette in den develop-PR. Das ist kein fokussierter Receipt-Diff; keine Freigabe für einen solchen Diff.

## Worker-Rezept und Stop-Kriterium

Auf aktueller develop-Basis einen isolierten fokussierten Kandidaten erstellen bzw. durch den zuständigen Owner integrieren, ohne fremde Änderungen zu überschreiben. In `.github/workflows/receipt-post-run.yml` Decode und alle Plan-abhängigen Steps bei echtem non-PR-Event überspringen; fehlgeschlagenen, leeren oder ungültigen Event-Lookup fail-closed behandeln. In `scripts/test_receipt_postrun.py` eine ausführbare Fake-Push-Regression ergänzen, die erfolgreichen Skip ohne Download/Decode/Receipt nachweist, sowie PR-Positivfall und API-Fehler testen. Einen echten PR-Run für exakt den endgültigen Head und seine tatsächlich ausgeführten Pflichtchecks sowie veröffentlichte Evidence belegen; neuen SHA und Diff erneut unabhängig prüfen lassen. Stop bei riesigem fremdem Diff, abweichendem Head, fehlender Evidence oder nicht grünem Pflichtgate.

## repo-rule compliance

Nur lesende Produktprüfung, keine Produktänderung, kein Merge, keine Claim-/Statusänderung. Die frühere rv1230-Evidence bleibt erhalten. Coordinator-Reminders und Pool-/PLAN-Flags sind offen und wurden nicht als erledigt behauptet.

END rv1230b REQUEST_CHANGES

## PLAN — korrigierter Head b4a55e18

0. DONE — Owner-Korrektur, Dispatch und Richtlinien gelesen; native TodoWrite ist nicht verfügbar.
1. DONE — Head, Basen, Evidence und Runs live abgeglichen.
2. DONE — Beide Diffs und rv1230-Befunde SHA-genau geprüft; Urteil und Rezept ergänzt.
3. DONE — Evidence für Planning-Publikation vorbereitet; Push und ls-remote im Transcript.

## Korrigiertes Urteil: REQUEST_CHANGES für b4a55e18

Die Owner-Korrektur ersetzt den im Dispatch genannten Kandidaten. PR #1230 ist live offen gegen develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; exakter Head b4a55e1868047305e58d03b135474d8035513a61, Branch work/postrun-nonpr-skip. HTTPS ls-remote bezeugt Head sowie main e92e20588c5737f566e29d47bbd08a9bcaed19d3 und develop. `git diff --name-status 7d63e0c6 b4a55e18` ist leer: der Dateibaum ist unverändert, obwohl der Commit ein anderer ist. Damit sind die zuvor dokumentierten drei rv1230-Befunde am korrigierten SHA erneut bestätigt:

- Workflow `.github/workflows/receipt-post-run.yml:153` führt den Decode-Schritt ohne Skip-Bedingung nach übersprungenem Download weiter aus; `plan.zip` fehlt.
- `scripts/test_receipt_postrun.py:772-823` prüft YAML-Zeichenfolgen, führt keinen Fake-Producer-Skip aus und erkennt den fehlenden Decode-Guard nicht.
- Event-API-Fehler wird in `.github/workflows/receipt-post-run.yml:94-97` als leerer Event und erfolgreicher Skip behandelt.

Diff gegen main: 2 Dateien, +81/-1. Merge-Base-Diff gegen develop: 2453 Dateien, +331343/-21727; `gh pr view` meldet mergeStateStatus DIRTY. Der PR ist daher auch integrationsseitig kein fokussierter, konfliktfreier develop-Kandidat. Die GitHub-Check-Runs-Abfrage für b4a55e18 und `statusCheckRollup` sind leer; `gh run list --commit` ergab keine Runs. Die behaupteten real gelaufenen PR-Jobs auf diesem Head sind nicht nachgewiesen. q265.md fehlt auf dem abgefragten Planning-main. Keine neuen Tests oder Hosted-Runs ausgelöst; vorhandene Git- und API-Zeugen verwendet.

## Rezept für den korrigierten Kandidaten

Der zuständige Worker soll die drei konkreten rv1230-Befunde wie im obigen Rezept beheben und den Receipt-Fix auf der aktuellen develop-Basis konfliktfrei und ohne die fremde Änderungskette bereitstellen. Ein ausführbarer Fake-Push-Test muss erfolgreichen Skip ohne Download, Decode und Receipt belegen; PR-Positivpfad und fehlgeschlagene Event-Abfrage ebenfalls prüfen. Danach den finalen Head, den fokussierten Diff und tatsächlich ausgeführte Pflichtchecks SHA-genau veröffentlichen und unabhängig erneut reviewen. Stop bei unverändertem Decode-Pfad, fehlender Testausführung, Konflikten, fehlender Evidence oder nicht grünem Pflichtgate. Kein Merge.

Planning- und Event-Hinweise: Event-Queue gelesen und ack aufgerufen; übrige Reminders/Pool/PLAN-Flags bleiben offen. Produkt ausschließlich lesend geprüft.

END rv1230b b4a55e18 REQUEST_CHANGES
