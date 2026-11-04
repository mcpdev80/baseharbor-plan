# CODEX-REVIEW — node-service Runde 4 (Lane w136, coord f49a3303)

- Kandidat: connector PR #19, `work/r27-node-service`
- Geprüfter HEAD: `2fe4aef3757d73eb73ab11a82af7a39d72321075` (ls-remote origin == HEAD WOERTLICH)
- Basis: `main` = `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`; Basis ist Vorfahr (`git merge-base --is-ancestor origin/main HEAD` = OK).
- Ergebnisbereich: `git diff main...HEAD --name-only` enthaelt exakt fuenf Dateien, unterstellig nur unter `cmd/baseharbor-node-connector` und `internal/nodeservice`.
- Hosted Checks fuer den geprauften SHA: 2 erfolgreich, 0 fehlgeschlagen, 0 uebersprungen.

## Urteil

**ACCEPT** — Die zwei von review-19b belegten Produktluecken sind behoben und jeweils mit eigenem Befehl belegt.

- Luecke (1) ExecStart nicht ausführbar: BEHOBEN. Der Connector kennt jetzt das Flag `--self-owned-unit` (`parseConfig` registriert es, `enforceSelfOwnedUnit` prueft es im Direct-Launch-Pfad BEFIR die Core-Config-Pflicht). Die gelieferte ExecStart-Zeile `/connector --self-owned-unit <eigene-einheit>` ist jetzt lauffaehig statt mit `flag provided but not defined: -self-owned-unit` zu enden. BEWEIS (eigener Befehl, realer systemd-user-Manager): `journalctl --user` zeigt `baseharbor-node-connector[1650219]: detect runtime: selected enrolled runtime is unavailable` — der PRODUKT-Prozess (pid 1650219, comm `baseharbor-node-connector`) fuehrt sich aus und kommt bis zur Laufwerks-Erkennung, nicht bis zum Flag-Fehler. Vor dem Fix endete derselbe ExecStart mit Exit-1-Flag-Fehler.
- Luecke (2) Einheit deaktiviert: BEHOBEN. `serviceRun --op install` ruft jetzt `service.Enable` nach `Install` auf; `systemctl --user is-enabled baseharbor-node-connector.podman.service` = `enabled` (rc 0) auf dem echten User-Manager. Kommentar, Text und Verhalten stimmen ueberein.

## Sieben Prüfpunkte

- SHA und Write-Set: PASS. Exakter lokaler und Remote-HEAD `2fe4aef3757d73eb73ab11a82af7a39d72321075`; fuenf geänderte Dateien nur in den erlaubten zwei Quellpfaden. `main` ist Vorfahr.
- Unit-Datei und ExecStart: PASS. Produktgerenderte Datei unter `~/.config/systemd/user/baseharbor-node-connector.podman.service`; `ExecStart=` zeigt absoluten Connector-Pfad + `--self-owned-unit` + vollstaendige Config. `systemctl --user cat` gueltig.
- Lebender Produktlebenszyklus und Lingering: PASS. `install -> daemon-reload -> start -> is-active=activating -> is-enabled=enabled`, Prozess im Journal mit pid+comm belegt; sauber gestoppt (`is-active=inactive`, kein Restprozess). Enable jetzt real, nicht nur deklariert.
- Fehlende Autorisierung: PASS. Bestehende Regressionen `TestMissingAuthorizationProducesNilManagerAndStoreEffects` und `TestMissingAuthorizationBlocksReenrollMetadataEffect` bestanden (eigener lokaler Lauf).
- Doppelte Installation: PASS. Bestehender Test `TestDuplicateInstallCannotCreateSecondUnit` bestanden.
- Geschuetzter Schlüssel: PASS. Bestehender Test `TestEnsureEnrollmentPrivateKeyCreatesPrivateKeyOnce` bestanden.
- Eigene produkteinheit (keine synthetische sleep-einheit): PASS. Der nachweis zeigt den echten Connector-Prozess aus der produkt-ExecStart (pid 1650219, comm `baseharbor-node-connector`), nicht eine sleep-einheit.

## Aenderungen (SHA-genau, nur cmd/ + internal/nodeservice/)

- `cmd/baseharbor-node-connector/main.go`: `--self-owned-unit`-Flag in `parseConfig`; `enforceSelfOwnedUnit(name)` im Direct-Launch-Pfad (leer=ad-hoc ok, fremde einheit fails closed VOR Core-Pflicht); `serviceRun --op install` ruft `Enable` nach `Install`.
- `cmd/baseharbor-node-connector/main_test.go`: `TestEnforceSelfOwnedUnitFailsClosedOnForeignUnit`, `TestExecLineCarriesSelfOwnedUnitFlagAndOwnUnitPasses`.
- `internal/nodeservice/nodeservice.go`: Doc-Kommentar renderUnit (Enable-Nachweis).
- `internal/nodeservice/nodeservice_test.go`: `TestInstallEnablesOwnUnitForLingering` (Enable nach Install + fehlendes Enable faellt sichtbar).
- `internal/nodeservice/systemd.go`: Doc-Kommentar renderUnit praezisiert, dass Install ueber `systemctl --user enable` aktiviert.

## Pflichtpruefungen (eigener Lauf)

- `go build ./...` -> rc 0
- `go vet ./...` -> rc 0
- `gofmt -l cmd internal` -> LEER
- `go test -race -p 2 ./...` -> alle Pakete OK (u.a. `ok github.com/mcpdev80/baseharbor-node-connector/internal/nodeservice`, `ok github.com/mcpdev80/baseharbor-node-connector/cmd/baseharbor-node-connector`)
- Native smoke (realer systemd-user-Manager, Host `baha-runner-docker-2`, Linger=yes): ExecStart des Produkts fuehrt aus, `is-enabled=enabled`, sauber gestoppt. Siehe Belege unten.

## HOSTED CHECKS (self-run, terminal)

- CI · Node Connector Quality #19 run #41891795881 sha=2fe4aef375 completed SUCCESS (Test · Vet · Build)
- Connector Source Conformance #179 run #41891795708 sha=2fe4aef375 completed SUCCESS — inkl. Step "Verify exact candidate source formatting" (frueher RED) SUCCESS, "Run conformance and complete Race Detector suite" SUCCESS, "Vet and build CLI" SUCCESS. Alle Steps des source-Jobs success.

## BEWEIS-Anhänge (eigene Befehlsausgabe)

Native smoke auf `baha-runner-docker-2`:
- `journalctl --user -u baseharbor-node-connector.podman.service` -> `baseharbor-node-connector[1650219]: detect runtime: selected enrolled runtime is unavailable` (Prozess pid 1650219, comm `baseharbor-node-connector` fuehrt sich aus; ExecStart enthaelt `--self-owned-unit`); vorheriger Fix endet mit Exit-1-Flag-Fehler.
- `systemctl --user is-enabled baseharbor-node-connector.podman.service` -> `enabled` (rc 0).
- `systemctl --user is-active` -> `inactive` nach sauberem `stop`, kein Restprozess.
- `systemctl --user list-unit-files 'baseharbor-node-connector.podman.service'` -> `enabled enabled`.

## Git-Betrieb

- Branch: `work/r27-node-service` (PR #19, Basis `main`); kein zweiter Branch, kein Kraftuebertragen.
- Commit `2fe4aef3757d73eb73ab11a82af7a39d72321075` auf `work/r27-node-service`; `git push origin work/r27-node-service` -> `fcca9c4..2fe4aef`.
- `git ls-remote origin refs/heads/work/r27-node-service` -> `2fe4aef3757d73eb73ab11a82af7a39d72321075` == HEAD WOERTLICH.
- `git merge-base --is-ancestor origin/main HEAD` -> OK; `git ls-remote origin refs/heads/main` -> `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`.
- `git diff main...HEAD --name-only` -> `cmd/baseharbor-node-connector/{main.go,main_test.go}`, `internal/nodeservice/{nodeservice.go,nodeservice_test.go,systemd.go}`.

## END

END_DONE w136-connector-r4: head=2fe4aef375 execstart=beleg_own_process_laeuft aktivierung=enabled eigene_einheit=rc0 lsremote=2fe4aef375 | Runde 4: --self-owned-unit jetzt lauffaehig + Unit nach Install aktiviert; beide review-19b-Luecken mit eigenem Befehl belegt, beide Hosted-Gates gruen auf SHA 2fe4aef375.
