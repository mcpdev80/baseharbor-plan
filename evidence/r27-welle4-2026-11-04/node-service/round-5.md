# Node connector Runde 5 — Eigentum und Installationsfehler

- Task: `t-20261018-r27-node-service`
- PR #19, Branch `work/r27-node-service`
- Start-Head: `2fe4aef3757d73eb73ab11a82af7a39d72321075`
- Geforderter Red-first-Head: `fcca9c4a295625062827343263de5b2ddaff4d62`

## PLAN-Checkliste

1. Den SHA-genauen Reviewbefund, den Remote-Stand und den erlaubten Connector-Dateiscope festhalten.
2. Regressionen für exakte Unit-Identität, vier fremde Marker-/Konfliktwerte und Nullwirkung ergänzen.
3. Eine injizierte Enable-Fehler-Regression im echten `serviceRun install`-Aufrufpfad ergänzen.
4. Die neuen Regressionen auf fcca9c4a ausführen und die wörtlichen roten Assertion-Ausgaben sichern.
5. Eigentumsprüfung auf exakte kanonische Namen und Installationsfehler als typisierten Setup-Fehler korrigieren.
6. Lebenszyklus-, Nullwirkungs-, Schlüssel- und Setup-Regressionen sowie `go test ./... -count=1`, `go build ./...`, `go vet ./...`, `gofmt -l cmd internal` ausführen.
7. Auf demselben PR-Zweig committen/pushen, Hosted Checks und Skips bis terminal beobachten und exakte SHA-/Ancestry-/Diff-Belege eintragen.

## Review-19c RED-FIRST

Wird vor der Produktkorrektur ergänzt: neue Regressionen auf exakt `fcca9c4a295625062827343263de5b2ddaff4d62`, einschließlich wörtlicher Fehlschlagzeilen.

## Umsetzung und Ergebnisse

Noch ausstehend.
