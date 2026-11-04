# CODEX-REVIEW PR #1373 — Runde 3

- Rolle: REVIEW (kein Merge)
- Kandidat: `mcpdev80/baseharbor`, PR #1373, `work/r27-execution-journal`
- Geprüfter Head: `0d89a13e63a61fe027e458b36fbda255d37f53dc`
- PR-Basis: `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`
- Urteil: **REJECT**

## PLAN / Prüfung

1. PR, Kandidaten-SHA, Remote-Branch, Basis und Write-set frisch messen.
2. Handler- und Store-Persistenz gegen den Vertrag und die Ordnungstests lesen.
3. Deduplizierung, Reconnect, Auth-Expiry, Payloadschutz und Retention prüfen.
4. Betroffene Tests 20-mal mit Race Detector ausführen und den synchronen Aufruf kontrolliert zurückbauen.
5. Paket-/Build-/Vet-/Formatprüfungen sowie Hosted-Gates terminal prüfen.

## Kandidat und Scope

- PR #1373 ist offen, Head stimmt exakt mit `0d89a13e63a61fe027e458b36fbda255d37f53dc` überein.
- `git diff --name-only 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1...HEAD` enthält genau:
  - `internal/machinehttp/execution_duplicate_reject_test.go`
  - `internal/machinehttp/execution_reconnect_test.go`
  - `internal/machinehttp/execution_request_identity_test.go`
  - `internal/machinehttp/handler.go`
  - `internal/machinehttp/handler_test.go`
  - `internal/machinehttp/store.go`
- Kein `.github`-Pfad und keine Datei außerhalb `internal/machinehttp/`.
- Keine bestehenden Testfunktionen wurden im Diff entfernt.
- PR-Basis ist noch `2ea2c6f1…`; Live-`develop` ist inzwischen `e444ae117173dcf84e7aa8b17f73c020d3e2923c`, ein Commit voraus. Dieser Commit ändert ausschließlich `contracts/managementaccess/v1/` und die DE/EN-Credential-Access-Dokumente. Der aktuelle Diff gegen Live-`develop` bleibt auf dieselben sechs MachineHTTP-Dateien begrenzt; PR ist dadurch 1 Commit behind.
- Wörtliches `ls-remote`:

```text
e444ae117173dcf84e7aa8b17f73c020d3e2923c	refs/heads/develop
0d89a13e63a61fe027e458b36fbda255d37f53dc	refs/heads/work/r27-execution-journal
```

## Befunde

### 1. Synchroner Aufruf vorhanden, aber der verlangte Endzustandsbeweis fehlt

`internal/machinehttp/store.go:190-206` schreibt den akzeptierten Request-Commit synchron vor Rückgabe von `createRequest`; `appendJournalLineLocked` führt `Write`, `Sync` und `Close` aus (`store.go:391-415`). `handler.go:206-211` ruft `runExecution` synchron auf. Damit läuft `start`, Executor und terminaler Übergang vor Rückkehr aus `handleExecute`.

Der angegebene Expectation-Test beweist aber nur die **Zusage vor Executorstart**: `execution_request_identity_test.go:153-159` liest `request_id` und `input_sha256` im Executor und prüft, dass der rohe Testwert nicht persistiert ist. Er prüft weder terminalen Zustand vor Handler-Rückkehr noch den terminalen Journal-Eintrag. `TestRequestIdentityIndexSurvivesJournalReopen` (`execution_request_identity_test.go:99-115`) wartet nach dem Handler-Aufruf mit Polling bis zu einer Sekunde auf `ExecutionSucceeded`; das besteht auch bei Hintergrundausführung.

**Eigene Rückbau-Gegenprobe:** Ich änderte lokal im isolierten Kandidaten-Worktree `handler.go:211` vorübergehend zu `go h.runExecution(...)` und führte die originalen Tests `TestJournalCommitReadableBeforeExecutorStarts` und `TestRequestIdentityIndexSurvivesJournalReopen` aus. Ergebnis: beide PASS (`ok .../internal/machinehttp 0.775s`). Der Originaltest wird bei Rückbau also nicht rot. Die Änderung wurde bytegenau zurückgenommen; der Worktree blieb sauber.

### 2. Fehler beim terminalen Persistieren werden verschluckt

`executionStore.update` rollt den In-Memory-Zustand bei Append-/Sync-/Close-Fehler zurück und gibt den Fehler zurück (`store.go:303-317,391-415`). `handler.go:214-232` verwirft dagegen die Fehler von `start`, `progress`, `fail` und `succeed`; insbesondere kann `succeed` fehlschlagen und `runExecution` trotzdem normal zurückkehren. Der Handler hat zu diesem Zeitpunkt bereits die 202-Antwort codiert (`handler.go:201-211`). Damit belegt der synchrone Aufruf allein nicht, dass ein terminaler Zustand dauerhaft geschrieben wurde; bei Speicherfehler kann die Anfrage zurückkehren, ohne terminales Journal-Ergebnis und ohne weitergereichten Fehler. Es gibt keine Handler-Regression, die diesen Fehlerfall abdeckt.

### 3. Sleep-Polling bleibt in den neuen Testkörpern

`execution_request_identity_test.go` wurde im Vergleich zu `develop` neu hinzugefügt und enthält `time.Sleep(time.Millisecond)` in den Poll-Schleifen bei Zeilen 67, 101 und 111. Diese warten auf Executorstart bzw. terminalen Zustand und lassen die Tests auch mit der zurückgebauten Hintergrundausführung bestehen. Der Reihenfolge-Test verwendet außerdem ein Timeout (`:168-175`), prüft dabei aber nur die Zusage vor Executorstart. Das ist kein belastbarer Test für den synchronen Endzustand.

### 4. Kartenfälle, Geheimnisse und Retention

- Gleiche Idempotency-Key-/Request-Inhalte liefern bei Reconnect dieselbe Execution und keinen zweiten Executorlauf (`execution_duplicate_reject_test.go:63-84`, `execution_request_identity_test.go:118-137`).
- Geänderter Inhalt wird typisiert abgewiesen und erzeugt keinen zweiten Record (`execution_duplicate_reject_test.go:9-36,38-61`).
- Expired-Principal- und Terminal-Expiry-Regressionen bleiben erhalten (`browser_security_test.go:17-47`, `terminal_test.go:178-196`). Im MachineHTTP-Paket fand ich keine explizite Revocation-/Renewal-Testfunktion; die kanonische Execution-Journal-Task-Note führt solche Fälle nicht als eigenes Akzeptanzkriterium.
- Das Journal schreibt nur Identität, Request-ID, Input-Digest, Operation, Zustand, Actor/Context und Zeitstempel (`store.go:328-356`), nicht Input/Result/Progress/Error. Größenlimits: 4 MiB pro Segment, höchstens drei Backups, 16 MiB gesamt (`store.go:36-45`). Der Ordnungstest prüft wörtlich, dass `never-persist-this` nicht im Journal steht (`execution_request_identity_test.go:143-159`).

## Laufbelege

- Gezielte Race-Wiederholung für Request-Identity, Reopen, Zusage-vor-Executor, Duplicate/Reconnect: `go test -race -count=20 -timeout 2m ./internal/machinehttp -run '^(TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest|TestRequestIdentityIndexSurvivesJournalReopen|TestJournalCommitReadableBeforeExecutorStarts|TestCreateDuplicateRequestDifferentContentRejects|TestDuplicateAfterStartStillRejects|TestCreateReconnectIdenticalReturnsSameOperation|TestReconnectReturnsSameOperation)$'` → PASS, 13.289s.
- Voller `go test -race -count=20 ./internal/machinehttp` → Timeout nach 600s in `TestRound3BoundedRetentionAndNoPayloads`, während `executionStore.appendJournalLineLocked` auf `fsync` wartete.
- Voller `go test ./internal/machinehttp -count=1` → Timeout nach 600s im selben Retention-Test, bei `fsync`.
- `go test ./cmd/baha` → FAIL nach 504.962s in dieser Sandbox: schreibgeschütztes `/home/marcel/.local/share`, nicht verfügbarer Docker-Socket und TMPDIR/XDG-Pfadabweichungen. Diese Fehler liegen außerhalb der sechs geänderten Dateien; sie zählen hier nicht als grüne Tests.
- `go build ./...` → PASS.
- `go vet ./...` → PASS.
- `gofmt -l` über alle sechs geänderten Go-Dateien → keine Ausgabe.
- `git diff --check` → PASS.
- Hosted Run `41892296752` am exakten Kandidatenkopf: terminal success; 8 Jobs success, 0 failure, 10 skipped, einschließlich `go-unit-tests`, `go-build`, `go-vet` und `PR Selected Checks` success.

## Urteil

**REJECT** für `0d89a13e63a61fe027e458b36fbda255d37f53dc`. Die synchrone Implementierung ist vorhanden, aber die Pflichtprüfung belegt nur den anfänglichen Commit und wird von der geforderten Rückbau-Gegenprobe nicht rot. Zusätzlich werden terminale Persistenzfehler in `runExecution` ignoriert. Das sind substantielle Lücken gegenüber der geforderten Zusage-plus-Endzustand-Garantie. Lokale volle Paketläufe sind außerdem nicht terminal grün; das Hosted Gate ist terminal grün, ersetzt aber die fehlende Mutationssicherheit nicht.

## REZEPT

1. **Datei:** `internal/machinehttp/execution_request_identity_test.go` und `internal/machinehttp/handler.go`. **Änderung:** Den Ordnungstest so ändern, dass er nach Rückkehr aus `ServeHTTP` den terminalen Status aus dem Journal liest; einen per Channel blockierbaren Executor verwenden. Keine Sleep-Poll-Loops als Ersatz. **Testanforderung:** gezielte Tests `-race -count=20` grün; den Aufruf an `handler.go:211` zu `go h.runExecution(...)` zurückbauen und genau diesen Originaltest ausführen. **Stop-Kriterium:** Der Rückbau muss den Test zuverlässig rot machen; bis dahin ist die synchrone Endzustandsgarantie nicht belegt.
2. **Datei:** `internal/machinehttp/handler.go` und erforderliche Store-Test-Seams in `internal/machinehttp/`. **Änderung:** Fehler der terminalen Journal-Übergänge bis zur Handler-Grenze zurückgeben und bei fehlgeschlagenem `Sync`/`Close` keinen erfolgreichen Abschluss bzw. stillen Rückfall auf Running melden. **Testanforderung:** Append-/Sync-Fehler bei `succeed` injizieren; der Handler muss den Fehler/Unsicherheitszustand sichtbar machen und darf keinen erfolgreichen terminalen Commit behaupten. **Stop-Kriterium:** Wenn `runExecution` einen Persistenzfehler weiterhin ignoriert oder der Request ohne sichtbaren terminalen/unsicheren Zustand zurückkehrt, nicht akzeptieren.
