# CODEX-REVIEW 0427-162 — PR #1510

ROLLE: REVIEW
URTEIL: KORREKTUR

## PLAN

1. Kandidaten-SHA, Basis, Vorgänger und Hosted-Checks sha-genau verifizieren.
2. Den Recovery-Text mit dem tatsächlichen `baha up`-Routing und den Produktionsregressionen abgleichen.
3. Prüfen, ob die #172-Änderung Teil dieses PR-Deltas oder geerbter develop-Drift ist.
4. Urteil und konkretes Korrekturrezept in Planning-Evidence veröffentlichen.

## Geprüfter Stand

- Repository: `mcpdev80/baseharbor`
- PR: #1510, base `develop` = `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`
- Kandidat: `bc1a721e8e46ca82f81e978fc7c186bb135bf67a`
- `git ls-remote` bezeugte `develop` bei `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` und `refs/pull/1510/head` bei `bc1a721e8e46ca82f81e978fc7c186bb135bf67a`.
- `git merge-base --is-ancestor origin/develop origin/pr1510` exit 0. #1489 ist geschlossen ohne Merge; sein früherer Kandidat `03fa07f823899ebc7bef1be1103489187fd5b6e1` ist in der Nachfolgerkette abgelöst.
- Der PR-Diff gegen develop umfasst ausschließlich `cmd/baha/onboarding.go`, `cmd/baha/use_target.go` und `cmd/baha/use_target_connection_test.go`.
- Das Recovery-Wording und die zwei neuen Verbindungsregressionen sind gegenüber dem früheren #1489-Stand `03fa07f8` byte-identisch. Der #172-Marker/TestMain-Heilungsstand ist bereits Bestandteil von develop `942111d5`; diese Dateien sind nicht Teil des #1510-Deltas.

## Hosted-Checks

Run `42583974762` ist `completed/success` auf exakt `bc1a721e8e46ca82f81e978fc7c186bb135bf67a`. `PR Selected Checks` (GitHub Actions job `129053385200`), `go-unit-tests`, build, vet und gofmt bestanden. Native Keycloak/Core Docker und Podman sowie destroy-retry Docker und Podman wurden ausgeführt und bestanden. Die übrigen ausgewiesenen Checks blieben `skipped`; sie werden nicht als grün gewertet.

## Befund

Die neue Regression belegt den Verbindungs- und Fail-closed-Pfad: ein verifiziertes Core ohne lokales base-CA-Issuer-Verzeichnis kann über `VerifyCoreConnection` ausgewählt werden; ein fehlendes Core wird weiter abgewiesen. Der Test liegt in `cmd/baha/use_target_connection_test.go` und wird von `go-unit-tests` erfasst.

Der Recovery-Hinweis verspricht jedoch an drei Stellen, dass gewöhnliches `baha up` das Management-Core dieses Targets einrichtet oder repariert: `cmd/baha/use_target.go:91,98,118,129` und `cmd/baha/onboarding.go:201`. Das ist vom Arbeitsverzeichnis abhängig. `cmd/baha/commands.go:76-80` dokumentiert `baha up` als App-Konvergenz innerhalb eines Application-Repositorys; es installiert dort ausdrücklich kein Management-Core. `cmd/baha/runtime_repository_up.go:14-17,35-46` bestätigt, dass dieser Pfad ohne `--control-plane-only` in die Application-Lifecycle-Verarbeitung geht. Das echte Core-Setup wird durch `baha up --control-plane-only` ausgewählt. Daher kann der aktuelle Rat im üblichen Application-Repository den beschriebenen Recovery-Zweck verfehlen, obwohl der Befehl `baha up` existiert und außerhalb eines Application-Repositorys Core-Setup auslösen kann.

## Korrekturrezept

- Dateien: `cmd/baha/use_target.go` und `cmd/baha/onboarding.go`.
- Änderung: Core-Recovery-Hinweise müssen den eindeutigen Core-Befehl nennen, etwa `baha up --control-plane-only`; falls die Kurzform `baha up` erhalten bleibt, muss sie ausdrücklich auf Aufruf außerhalb eines Application-Repositorys beschränkt werden. `baha use` beziehungsweise onboarding danach erneut ausführen lassen.
- Testanforderung: ergänze eine CLI-/Produktionspfad-Regression, die für die fehlende und nicht erreichbare Core-Verbindung den ausgegebenen Repair-Hinweis prüft und sicherstellt, dass er den tatsächlichen Core-Setup-Pfad nennt. Behalte die bestehende positive Keycloak-gebundene Auswahl und die fehlendes-Core-Fail-closed-Gegenprobe. Die Tests müssen im bestehenden `go-unit-tests`-Job laufen.
- Stop-Kriterium: Korrektur ist erst abnahmefähig, wenn der konkrete Rat im Application-Repository tatsächlich `--control-plane-only` verwendet oder die Arbeitsverzeichnis-Bedingung klar benennt, die Regression im gehosteten `go-unit-tests`-Job läuft und ein terminaler Lauf auf dem korrigierten exakten PR-Head vorliegt. Kein Skipped-Check zählt als bestanden.

Der #172-Heilungsbeleg ist hier kein zusätzlicher Blocker: er ist geerbte develop-Basis und unverändert gegenüber dem reviewed Inhaltsdelta. Der Blocker ist die irreführende, nicht arbeitsverzeichnis-feste Recovery-Anweisung.

END 0427-162 REVIEW: KORREKTUR — PR #1510 `bc1a721e8e46ca82f81e978fc7c186bb135bf67a`; Evidence wird in Planning origin/main veröffentlicht.
