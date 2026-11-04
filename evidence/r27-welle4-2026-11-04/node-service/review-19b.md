# CODEX-REVIEW — node-service Runde 3

- Kandidat: baseharbor-node-connector PR #19, `work/r27-node-service`
- Geprüfter HEAD: `fcca9c4a295625062827343263de5b2ddaff4d62`
- Basis: `main` = `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`; Basis ist Vorfahr.
- Ergebnisbereich: `git diff main...HEAD --name-only` enthält genau sechs Dateien, ausschließlich unter `cmd/baseharbor-node-connector` und `internal/nodeservice`.
- Hosted Checks für den geprüften SHA: 2 erfolgreich, 0 fehlgeschlagen, 2 übersprungen. Quality run `41882233802` und Source-Conformance run `41882233837` erfolgreich; die beiden nativen/verschlüsselten Integrationsjobs sind **skipped**, nicht bestanden.
- Arbeitsbaum des Produkt-Repositories blieb unverändert. Review-Modell/Kanal laut Missionszuweisung: GPT-6 Luna.

## Urteil

**REJECT** — Die vorhandene echte User-Manager-Probe belegt Dateiablage, Laden, Starten, Neustarten und Entfernen einer synthetischen `ExecStart=/bin/sleep 3600`-Unit. Sie belegt nicht, dass die vom Produkt erzeugte Kommandozeile den Connector ausführt. `execLineFor` erzeugt `<absoluter-pfad> --self-owned-unit <unit>`, aber weder `run` noch `parseConfig` kennen dieses Flag. Der direkte Aufruf des Kandidaten mit genau diesem Argument endet mit `flag provided but not defined: -self-owned-unit` (Exit 1). Zusätzlich bleibt die installierte Unit deaktiviert: auf dem echten User-Manager ergab `systemctl --user is-enabled <review-unit>` `disabled` / Exit 1, obwohl Kommentar und `WantedBy=default.target` Lingering-Autostart behaupten. Diese zwei Produktlücken verhindern die Abnahme.

## Sieben Prüfpunkte

| # | Prüfung | Ergebnis und Beleg |
|---|---|---|
| 1 | SHA und Write-Set | **PASS.** Exakter lokaler und Remote-Branch-HEAD `fcca9c4a295625062827343263de5b2ddaff4d62`; sechs geänderte Dateien nur in den erlaubten zwei Quellpfaden. PR #19 war OPEN, READY, MERGEABLE/CLEAN gegen `main`. |
| 2 | Unit-Datei und ExecStart | **FAIL.** Die echte, vom Produkt gerenderte Datei lag unter `/home/marcel/.config/systemd/user/baseharbor-node-connector.codex-r19b-review.service`, Mode `0600`; `systemctl --user cat` zeigte `[Unit]`, `[Service]`, absolute `ExecStart=... --self-owned-unit ...` und `[Install]`. Die Manager-Syntax/Dateiablage ist gültig. Der Befehl selbst ist ungültig: `main.go:130-135` hängt `--self-owned-unit` an; `main.go:138-150, 216-250` dispatcht nur das `service`-Subkommando und registriert das Flag nicht. Gegenprobe `go run ./cmd/baseharbor-node-connector --self-owned-unit codex-review.service` -> Exit 1, `flag provided but not defined: -self-owned-unit`. |
| 3 | Lebender Produktlebenszyklus und Lingering | **FAIL.** Echter Connector-Service-Probe-Manager: Install/daemon-reload/start/is-active/restart/stop/uninstall jeweils RC 0; `MainPID` wechselte von `824327` auf `824958`; nach Uninstall Unit-Datei entfernt und Unit inaktiv. Das war jedoch ein Reviewer-Test mit synthetischem `/bin/sleep`, kein laufender Connector: Die produktive ExecStart-Gegenprobe oben scheitert vor dem Dienststart. `is-enabled` vor Uninstall war `disabled` (Exit 1). `systemd.go:148-149` verspricht Autostart; `nodeservice.go:313-326` besitzt Enable, aber `nodeservice.go:252-270`/`systemd.go:114-141` rufen es bei Install nicht auf. Test `nodeservice_test.go:435-488` prüft nur, dass `ExecStart=` im File steht; danach wird ein externer `systemctl restart` ausgeführt, kein `is-enabled`/Enable-Nachweis. |
| 4 | Fehlende Autorisierung: Null-Effekt | **PASS.** Bestehende gezielte Regressionen `TestMissingAuthorizationProducesNilManagerAndStoreEffects` und `TestMissingAuthorizationBlocksReenrollMetadataEffect` bestanden; Authorization wird vor Manager-/Store-Wirkung geprüft. |
| 5 | Doppelte Installation: keine zweite Unit | **PASS.** Auf dem echten Manager zwei Installationen desselben selbstverwalteten Unit-Namens ergaben genau ein Unit-Artefakt und genau eine geladene passende Unit (`artifact_count=1 loaded_unit_count=1`). |
| 6 | Geschützter Schlüssel bei fehlerhafter Wiederholung | **PASS.** Bestehende Regression `TestEnsureEnrollmentPrivateKeyCreatesPrivateKeyOnce` bestanden; gezielter Lauf der drei angeforderten Auth-/Duplikat-/Schlüsseltests war erfolgreich. |
| 7 | Neutraler Gegenbeweis zur früheren Host-Ausrede | **PASS.** Auf `baha-runner-docker-2`, mit derselben konfigurierten SSH- und `systemctl --user`-Befehlskette, lud eine von Hand geschriebene Unit am echten XDG-Pfad: daemon-reload RC 0, start RC 0, `is-active=active` RC 0, restart RC 0 mit neuer MainPID (`746484` → `746513`), stop RC 0, danach Prozess weg und Probe-Unit entfernt. `Linger=yes`. Damit war die frühere Behauptung eines ungeeigneten User-Managers auf diesem Host falsch. |

Weitere lokale Checks auf exakt diesem Kandidaten: `go test ./internal/nodeservice ./internal/targetaccess -count=1`, `go vet ./...`, `go build -buildvcs=false ./...` und `gofmt -l cmd internal` (leer) erfolgreich. Der lokale native Systemd-Test wird in dieser VM wegen fehlendem User-Bus übersprungen; die oben genannten Remote-Proben sind separat gemessen und nicht als dieser Testlauf ausgegeben.

## REZEPT (Pflicht bei REJECT)

- **Dateien:** `cmd/baseharbor-node-connector/main.go`, `internal/nodeservice/nodeservice.go`, `internal/nodeservice/systemd.go`, plus gezielte Tests in `cmd/baseharbor-node-connector/main_test.go` und `internal/nodeservice/nodeservice_test.go`.
- **Änderung:** Die gerenderte ExecStart muss in einen tatsächlich unterstützten Connector-Laufmodus mit allen nötigen Konfigurationswerten führen; kein nicht registriertes `--self-owned-unit` ausgeben. Install muss die eigene Unit entsprechend dem dokumentierten Vertrag aktivieren (Enable und Deaktivierung beim Entfernen); alternativ muss der Task-Vertrag ausdrücklich geändert und die gegenteilige Lingering-Aussage aus Code/Tests/Doku entfernt werden. Die Identitätsbindung und Authentisierung vor allen Nebenwirkungen beibehalten.
- **Testanforderung:** Auf einem echten User-Manager genau die produktiv gerenderte ExecStart ausführen und Exit/Prozess nachweisen; `install -> daemon-reload -> start -> is-active -> restart` mit neuer MainPID `-> stop -> uninstall`, jede Stufe RC 0 und danach Unit-Datei/Prozess entfernt. Aktivierungsstatus beziehungsweise dokumentierte Vertragsgrenze messen. Zusätzlich fehlende Autorisierung mit null Manager-/Store-Effekten, doppelte Installation mit genau einem Artefakt sowie Schlüssel-Erhalt bei fehlerhafter Wiederholung prüfen. Für den korrigierten SHA Required Checks terminal beobachten; skips separat ausweisen.
- **Stop-Kriterium:** REJECT beibehalten, solange produktive ExecStart mit unbekanntem Argument endet, Aktivierung trotz behauptetem Lingering deaktiviert bleibt, irgendeine Lifecycle-Stufe fehlschlägt, eine zweite Unit/Restprozess entsteht oder unauthentisierte Wirkung beobachtet wird.

## END

END_DONE codex-r19b: verdict=REJECT open=produktive ExecStart ist nicht ausführbar; Lingering-Aktivierung fehlt | Die echte User-Manager-Probe widerlegt den früheren Host-Blocker, während die synthetische Sleep-Unit die beiden Produktfehler nicht abdeckt.
