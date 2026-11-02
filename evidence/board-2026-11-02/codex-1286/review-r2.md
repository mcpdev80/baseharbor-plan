# PR #1286 — Codex Review Runde 2

ROLLE: REVIEW
Urteil: REJECT
Reviewer: OpenAI Codex, unabhängige Session; Session-ID und genaue Modellkennung nicht verfügbar, kein Horde-Task zugewiesen.
Kandidat: 9e94a00ae647dbd47c851ac57d13d11216bba2dd; develop: 9a93865a935624045e96a503da0a3a1c2f7d1559. Vor und nach Review via ls-remote bestätigt. Vollständiger PR-Diff und logsmap/evidence.md gelesen.

## Kriterien

1. Exact path: PASS. Nur `internal/logs/render.go` wird über `path == ...` erfasst; nur planner und dessen Tests geändert.
2. Fail-closed: PASS für neue und verschachtelte Pfade; Tests prüfen jeweils unresolved und Fehlermeldung. Mixed-Test deckt render.go plus `internal/foo.go` ab, nicht ausdrücklich render.go plus eine andere internal/logs-Datei; dafür ist die Kombination aus den Einzeltests und der Planner-Logik ein Indiz, aber kein direkter Regressionstest.
3. Alter irreführender Prefix-Kommentar entfernt. Der neue Kommentar über Gate-Abdeckung ist jedoch sachlich falsch (siehe Befund).
4. Vier Regressionen vorhanden, positive und negative Assertions sind sinnvoll, mit obiger Mixed-Test-Einschränkung.
5. Actions-Run 41449999815: PR Selected Checks SUCCESS (Job 125293659676, App 15368, exakt obiger SHA); Trusted Plan und pr-planner-tests SUCCESS.
6. Beweisklasse promotable: keine überprüfbare Simulation oder sonstiger Nachweis in der vorgelegten Evidence; vor Merge nach RUNBOOK.md:166 erforderlich.

## Blockierende Befunde und Rezept

Die Pfadzuordnung fordert nur `source-contracts` (`go test ./internal/application/... ./contracts/...`), `cli-guided-tests` (`go test ./cmd/baha -run '^TestGuided'`), `cli-vet` und `cli-build` für cmd/baha und `cli-gofmt` (`gofmt -l cmd/baha`). Keine dieser Anforderungen führt `go test ./internal/logs/...` aus; das geforderte cli-gofmt prüft internal/logs nicht. Der Kommentar behauptet dagegen, das gebundene Format-Gate decke internal/logs ab. Die Evidence erwähnt eine lokale Logs-Paketprüfung und andere Workflows, belegt aber nicht, dass diese bei dem durch den Planner qualifizierten PR verpflichtend laufen. Der #1283-Diff ändert Regex-Verhalten in render.go; Build und Tests anderer Pakete belegen die Verhaltensabdeckung nicht. Ein exakter Pfad begrenzt die Freigabe, beweist aber nicht, dass jede künftige Änderung dieses Pfads durch diese Prüfungen abgedeckt wird.

Worker: das tatsächlich erforderliche, reproduzierbare Logs-Paket-Gate an den Planner binden (gegebenenfalls im vertraglich zulässigen Scope als ausführbare CI-Validierung ergänzen), relevanten Regex-Verhaltenstest einschließlich der Änderung belegen und den Format-Gate-Kommentar korrigieren. Negativtest render.go plus neue internal/logs-Datei ergänzen. Den finalen SHA mit erforderlichen Checks und Beweisklasse promotable gemäß RUNBOOK.md:166 belegen; falls Gate-Erweiterung außerhalb des Write-Sets liegt, STOP und Auftrag klären. Anschließend erneutes unabhängiges Review. Kein Merge durchgeführt.
