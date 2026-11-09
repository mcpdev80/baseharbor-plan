# CODEX-REVIEW 0427-159 r9 — PR #1499

ROLLE: REVIEW

URTEIL: KORREKTUR

## Kandidat und Nachweise

- PR #1499, Branch `0427-159-damagedstate`, exakter Head `3a14ce168b8129bde750369ca241c1ece4a195ee`, offen, Base `develop`.
- `origin/develop` ist `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` und Vorfahr des Kandidaten; `develop...head` = `0 9`. Kein Base-Drift.
- Lauf 42611864130: `completed/success` auf exakt `3a14ce168b8129bde750369ca241c1ece4a195ee`.
- Rohbelege am Aktenende.

## Prüfung gegen act-1499-review-r7

Der r7-Hauptmangel ist behoben: `internal/deployment/deployment_store.go`, `SaveDeploymentRecord`, schreibt `.owner` im Produktionspfad; `cmd/baha/app_lifecycle_damaged_state_test.go`, `TestRetainedOwnershipBandIsWrittenAndSurvivesDamagedState`, ruft den echten Writer auf, entfernt danach den maßgeblichen Record und prüft den erhaltenen Band sowie die Wiederherstellung. Der Test enthält auch ungebundene und fremde Band-Fälle. Die drei Namespace-Regressionsfälle sind erhalten; der damaged-before-budget-Pfad bleibt vor der generischen Repository-Inspektionsgrenze.

Es bleiben zwei Trust-Placement-Lücken:

1. **Band-Schreibfehler werden als Erfolg behandelt.** `SaveDeploymentRecord` ignoriert den Fehler von `writeRetainedOwnerBand` und gibt `nil` zurück, obwohl der Record erfolgreich gespeichert wurde. Damit kann ein erfolgreicher Produktionslauf die vom Resolver benötigte dauerhafte Identitätsquelle auslassen. Das widerspricht dem fail-closed-Schreibkriterium des r7-Rezepts.
2. **Der Band bindet nicht die vollständige Anwendungsidentität.** Er speichert nur Name und Environment; der Leser vergleicht nur diese beiden Felder und versieht danach den Fund mit der `ApplicationID` des aktuellen Aufrufers. Zwei unterschiedliche ApplicationIDs mit gleichem Namen und Environment sind damit nicht unterscheidbar. Der Resolver kann fremden beschädigten Zustand dem anfragenden ApplicationID zuordnen.

## Korrekturrezept und Stop-Kriterium

- `internal/deployment/deployment_store.go`: Band-Schreibfehler aus `SaveDeploymentRecord` propagieren; Record und Vertrauensmarker dürfen keinen erfolgreichen Save melden, wenn der Marker fehlt. Fehlerfall gezielt injizierbar testen und sicherstellen, dass Wiederholung/Recovery keinen widersprüchlichen Zustand als Erfolg behandelt.
- `internal/deployment/damaged_state.go` und `cmd/baha/app_context.go`: Band um die kanonische `ApplicationID` erweitern und beim Lesen gegen ID, Name und Environment prüfen. Fehlender, beschädigter oder fremder Marker muss unknown-owner bleiben und darf kein angefragtes Netzwerk erhalten.
- `cmd/baha/app_lifecycle_damaged_state_test.go`: Produktionspfad-Test ergänzen, in dem zwei Identitäten denselben Namen und dieselbe Umgebung, aber verschiedene ApplicationIDs haben; beim Aufruf der zweiten Identität darf der beschädigte erste Deployment-Band keine Attribution erhalten. Bestehenden Record-Verlust-Test und die drei Namespace-Tests erhalten.
- Stop review tot exact-head CI die Schreibfehler fail-closed-Regression und gleiche-Name/fremde-ID-Regression ausführt und besteht.

## Repo-Regelkonformität

Nur lesendes Produktreview. Keine Produktdateien, Läufe, PR-Status oder Branches verändert; keine Tests ausgeführt, keine Freigabe oder Merge.

## SOP-Rohbelege

```text
$ git ls-remote origin refs/pull/1499/head refs/heads/0427-159-damagedstate refs/heads/develop
3a14ce168b8129bde750369ca241c1ece4a195ee	refs/heads/0427-159-damagedstate
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
3a14ce168b8129bde750369ca241c1ece4a195ee	refs/pull/1499/head

$ gh pr view 1499 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-159-damagedstate","headRefOid":"3a14ce168b8129bde750369ca241c1ece4a195ee","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1499"}

$ gh run view 42611864130 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"3a14ce168b8129bde750369ca241c1ece4a195ee","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42611864130"}
```

END_DONE 0427-159-r9-review: KORREKTUR PR #1499 3a14ce168; production band and record-loss regression exist, but marker write errors are swallowed and the marker omits ApplicationID, leaving identity attribution ambiguous.
