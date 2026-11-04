# CODEX-REVIEW — Node Connector PR #19, Runde 4

- Kandidat: `mcpdev80/baseharbor-node-connector` PR #19, `work/r27-node-service`
- SHA-genau geprüft: `2fe4aef3757d73eb73ab11a82af7a39d72321075`
- Basis `main`: `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`; Basis ist Vorfahr. Remote `ls-remote` stimmt für beide SHA.
- PR: OPEN, READY (nicht Draft), MERGEABLE/CLEAN.
- Hosted checks, Run `41891795881`/`41891795708`: `Test · Vet · Build` SUCCESS, `source` SUCCESS; `Actual encrypted transport` und `Managed native enrollment` SKIPPED. Alle vier sind terminal, aber nur zwei erfolgreich.
- `git diff main...HEAD --name-only` enthält sechs Pfade, alle innerhalb `cmd/baseharbor-node-connector` bzw. `internal/nodeservice`. Die Lane-Evidence zählt fünf und lässt `internal/nodeservice/reenroll.go` aus; dieser Pfad liegt ebenfalls im erlaubten Write-Set.
- Produktcheckout blieb sauber. `gofmt -l cmd internal` war leer.

## Urteil

**REJECT.** Die 19b-Lücken sind teilweise geschlossen: die produktive Unit startet den Connector-Binary, der User-Manager markiert die Unit nach erfolgreichem Enable als aktiviert, eine doppelte Installation hinterlässt eine einzige Unit, und die Null-Effekt-/Schlüsselregressionen bestehen.

Zwei konkrete Gegenproben bleiben rot für die Abnahme. Erstens akzeptiert die neue Eigentumsprüfung einen fremden Namen, sobald dieser den Produktnamen als Teilzeichenfolge enthält. Zweitens gibt der Install-Befehl Erfolg zurück, wenn `systemctl --user enable` fehlschlägt. Dazu kommt: der behauptete Red-first-Test für Enable wird auf dem kranken Commit grün, weil er `Service.Enable()` direkt aufruft statt den geänderten CLI-Installpfad zu testen. Die beiden native Hosted Jobs sind übersprungen.

## Prüfpunkte

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | SHA, Basis, Write-Set | **PASS mit Evidenzabweichung.** Remote HEAD `2fe4aef3757d73eb73ab11a82af7a39d72321075`; `main` ist Vorfahr. Sechs geänderte Pfade, alle im erlaubten Command-/nodeservice-Scope. `round-4.md` nennt fünf Pfade, obwohl `reenroll.go` ebenfalls im Diff gegen `main` steht. |
| 2 | Eigentumsmerkmal und Zurückweisung fremder Werte | **FAIL.** `parseConfig` registriert `--self-owned-unit` und prüft es vor den übrigen Connector-Konfigurationsanforderungen (`main.go:282-293`). Die Prüfung selbst ist jedoch nur `strings.Contains(name, "baseharbor-node-connector")` (`main.go:155-161`; dieselbe Teilzeichenfolgenprüfung in `nodeservice.go:482-499`). Gegenprobe mit `foreign-baseharbor-node-connector.evil.container` endete mit `--core is required`, nicht mit dem Eigentumsfehler: der fremde/mismatched Wert wurde angenommen. `TestEnforceSelfOwnedUnitFailsClosedOnForeignUnit` deckt nur `foreign-core.service` ab und verfehlt den kollidierenden Marker-Fall. |
| 3 | Produktunit startet Anmelder, PID+comm | **PARTIAL.** Auf `baha-runner-docker-2` installierte ich mit dem Kandidaten eine einzigartige Unit. Die gerenderte ExecStart zeigte absoluten Binary-Pfad und `--self-owned-unit`. `MainPID=2066661`, `/proc/<pid>/comm=(baseharbor-no)`, `ActiveState=active`, `SubState=running` wurden während des Starts gemessen; Journald zeigte anschließend `--core is required` und Restart-Versuche, weil dieser isolierte User-Manager keine `BASEHARBOR_CONNECTOR_*`-Umgebung gesetzt hatte. Es war der echte Connector-Prozess, keine Sleep-Probe, aber kein stabiler Anmeldebetrieb. Die Unit wurde gestoppt und deinstalliert; kein Review-Unit-File blieb zurück. |
| 4 | Enable nach Install und Red-first | **FAIL.** Erfolgsfall auf echtem User-Manager: `service --op install` rc=0, `systemctl --user is-enabled`=`enabled` rc=0; `Linger=yes`. Eigene Fehler-Injektion: PATH-Wrapper ließ `systemctl --user enable` mit rc=42 fehlschlagen und leitete alle anderen Aufrufe an `/usr/bin/systemctl` weiter. Trotzdem gab `service --op install` rc=0 zurück; danach war die Unit `disabled`, `is-enabled` rc=1. Grund: `main.go:117` verwirft den Rückgabewert mit `_ = service.Enable(...)`. **Red-first neu nachgerechnet:** das neue `TestInstallEnablesOwnUnitForLingering`, in die exakte kranke Revision `fcca9c4a295625062827343263de5b2ddaff4d62` kopiert und dort ausgeführt, war PASS. Wörtlich: `=== RUN TestInstallEnablesOwnUnitForLingering`, `--- PASS: TestInstallEnablesOwnUnitForLingering`, `PASS`, `ok ... 0.004s`. Der Test ruft `svc.Enable` selbst auf und prüft nicht, dass `serviceRun install` Enable aufruft oder dessen Fehler meldet. Der Code-Diff `fcca9c4a...` → Kandidat enthält zwar echte Funktionsänderungen (Flag/Guard und Enable-Aufruf in `main.go`), aber dieser Enable-Test ist kein Red-first-Nachweis für die Änderung. |
| 5 | Fehlende Autorisierung, Null-Effekt | **PASS.** `TestMissingAuthorizationProducesNilManagerAndStoreEffects` und `TestMissingAuthorizationBlocksReenrollMetadataEffect` liefen erfolgreich; die Autorisierung stoppt die Manager-/Metadata-Wirkung vor Ausführung. |
| 6 | Doppelinstallation und geschützter Schlüssel | **PASS.** Live auf demselben User-Manager zweimal installiert: beide Installationen rc=0, genau eine passende Unit-Datei (`matching_unit_file_count=1`). `TestDuplicateInstallCannotCreateSecondUnit` und `TestEnsureEnrollmentPrivateKeyCreatesPrivateKeyOnce` liefen erfolgreich. |
| 7 | Gates terminal | **PASS-terminal, mit Skips ausgewiesen.** `Test · Vet · Build` und `source` sind terminal SUCCESS. `Actual encrypted transport` und `Managed native enrollment` sind terminal **skipped**, keine grünen Resultate. Mein gezielter lokaler Lauf der Eigentums-, Autorisierungs-, Duplikat-, Enable- und Schlüsseltests war erfolgreich (mit `-vet=off`); außerdem lief der unabhängige native User-Manager-Service-Test. Das ersetzt nicht die fehlende CLI-Fehlerregression. |

## REZEPT

- **Dateien:** `cmd/baseharbor-node-connector/main.go`, `cmd/baseharbor-node-connector/main_test.go`, `internal/nodeservice/nodeservice.go`, `internal/nodeservice/nodeservice_test.go`.
- **Änderung:** Bind den Self-Owned-Wert an den kanonischen Namensraum bzw. die erwartete Unit-Identität statt eine Teilzeichenfolge zu akzeptieren. Weist Fremdpräfixe, fremde Suffixe und widersprüchliche Werte fail-closed zurück. In `serviceRun install` muss ein Enable-Fehler als Install-Fehler zurückkommen; ein nicht aktivierter Zustand darf nicht als erfolgreiche Installation erscheinen.
- **Testanforderung:** Ergänze Ownership-Gegenproben mit `foreign-baseharbor-node-connector.evil.container` und ähnlichen Marker-Kollisionen. Teste den echten Install-Aufrufpfad: erfolgreicher Enable führt zu `is-enabled=enabled`; injizierter Enable-Fehler liefert nonzero und kann nicht als Erfolg gemeldet werden. Der Test auf `fcca9c4a` muss für die neuen Verhaltenserwartungen auf dem wirklichen Fehlerpfad rot sein. Behalte Null-Effekt-Autorisierung, eine einzige Unit bei doppeltem Install, geschützten Schlüssel sowie einen realen User-Manager-Lauf mit PID/comm und bereinigtem Ende. Required Hosted Gates für den finalen SHA terminal beobachten; Skips als Skips ausweisen und erforderliche Abdeckung anderweitig belegen.
- **Stop-Kriterium:** REJECT beibehalten, solange ein fremder Wert mit eingebettetem Connector-Marker akzeptiert wird, Install rc=0 trotz fehlgeschlagenem Enable liefern kann oder die Enable-Regression auf `fcca9c4a` grün bleibt.

## END

END_DONE codex-r19c: verdict=REJECT open=Teilzeichenfolgen-Ownership akzeptiert Fremdwert; Install verschluckt Enable-Fehler; Enable-Red-first auf fcca9c4a fehlt | Der echte Produktprozess startet und der Erfolgsfall aktiviert die Unit, aber die Gegenproben zeigen falsche Ownership-Akzeptanz und Erfolg trotz deaktivierter Unit.
