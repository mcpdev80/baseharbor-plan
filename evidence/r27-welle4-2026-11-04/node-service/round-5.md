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

## Review-19c RED-FIRST — exakt fcca9c4a

Arbeitskopie: detached worktree `/tmp/w141-connector-r5-fcca` auf exakt `fcca9c4a295625062827343263de5b2ddaff4d62`; nur die neu hinzugefügten Regressionen wurden in die Testdateien kopiert. Produktquellen blieben auf diesem alten Kopf unverändert. Für den Go-Cache und temporäre Builddateien verwendete ich `baseharbor-plan/evidence/r27-welle4-2026-11-04/scripts/w141-r5/`, nachdem die Umgebungscache-Versuche unter `/home/marcel/gocache-root` (read-only) und `/tmp` (`disk quota exceeded`) vor Testausführung scheiterten.

Befehl:

```text
GOCACHE=<evidence>/scripts/w141-r5/gocache TMPDIR=<evidence>/scripts/w141-r5/tmp GOMAXPROCS=2 go test -p 2 -vet=off ./internal/nodeservice -run '^(TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity|TestForeignUnitInstallHasNoManagerOrStoreEffects)$' -count=1
```

Wörtliche rote Ausgabe:

```text
--- FAIL: TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity (0.00s)
    --- FAIL: TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity/foreign_prefix (0.00s)
        nodeservice_test.go:519: noncanonical unit "foreign-baseharbor-node-connector.podman.container" must be rejected, got <nil>
    --- FAIL: TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity/foreign_suffix (0.00s)
        nodeservice_test.go:519: noncanonical unit "baseharbor-node-connector.podman.container.evil" must be rejected, got <nil>
    --- FAIL: TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity/same_marker_different_rest (0.00s)
        nodeservice_test.go:519: noncanonical unit "foreign-baseharbor-node-connector.evil.container" must be rejected, got <nil>
    --- FAIL: TestValidateSelfOwnedUnitRequiresExactCanonicalIdentity/conflicting_identity (0.00s)
        nodeservice_test.go:519: noncanonical unit "baseharbor-node-connector.docker.container/baseharbor-node-connector.podman.container" must be rejected, got <nil>
--- FAIL: TestForeignUnitInstallHasNoManagerOrStoreEffects (0.00s)
    --- FAIL: TestForeignUnitInstallHasNoManagerOrStoreEffects/foreign-baseharbor-node-connector.podman.container (0.00s)
        nodeservice_test.go:544: noncanonical unit must fail at ownership validation, got <nil>
    --- FAIL: TestForeignUnitInstallHasNoManagerOrStoreEffects/baseharbor-node-connector.podman.container.evil (0.00s)
        nodeservice_test.go:544: noncanonical unit must fail at ownership validation, got <nil>
    --- FAIL: TestForeignUnitInstallHasNoManagerOrStoreEffects/foreign-baseharbor-node-connector.evil.container (0.00s)
        nodeservice_test.go:544: noncanonical unit must fail at ownership validation, got <nil>
    --- FAIL: TestForeignUnitInstallHasNoManagerOrStoreEffects/baseharbor-node-connector.docker.container/baseharbor-node-connector.podman.container (0.00s)
        nodeservice_test.go:544: noncanonical unit must fail at ownership validation, got <nil>
FAIL
FAIL	github.com/mcpdev80/baseharbor-node-connector/internal/nodeservice	0.003s
FAIL
```

Befehl:

```text
GOCACHE=<evidence>/scripts/w141-r5/gocache TMPDIR=<evidence>/scripts/w141-r5/tmp GOMAXPROCS=2 go test -p 2 -vet=off ./cmd/baseharbor-node-connector -run '^(TestServiceInstallRejectsForeignUnitBeforeSideEffects|TestServiceInstallReturnsTypedErrorWhenEnableFails)$' -count=1
```

Wörtliche rote Ausgabe:

```text
--- FAIL: TestServiceInstallRejectsForeignUnitBeforeSideEffects (0.22s)
    --- FAIL: TestServiceInstallRejectsForeignUnitBeforeSideEffects/foreign-baseharbor-node-connector.podman.container (0.07s)
        main_test.go:155: foreign unit must be rejected before install, got <nil>
    --- FAIL: TestServiceInstallRejectsForeignUnitBeforeSideEffects/baseharbor-node-connector.podman.container.evil (0.05s)
        main_test.go:155: foreign unit must be rejected before install, got <nil>
    --- FAIL: TestServiceInstallRejectsForeignUnitBeforeSideEffects/foreign-baseharbor-node-connector.evil.container (0.05s)
        main_test.go:155: foreign unit must be rejected before install, got <nil>
    --- FAIL: TestServiceInstallRejectsForeignUnitBeforeSideEffects/baseharbor-node-connector.docker.container/baseharbor-node-connector.podman.container (0.04s)
        main_test.go:155: foreign unit must be rejected before install, got <nil>
--- FAIL: TestServiceInstallReturnsTypedErrorWhenEnableFails (0.04s)
    main_test.go:192: install must fail when enabling the unit fails
FAIL
FAIL	github.com/mcpdev80/baseharbor-node-connector/cmd/baseharbor-node-connector	0.256s
FAIL
```

## Umsetzung und Ergebnisse

Noch ausstehend.
