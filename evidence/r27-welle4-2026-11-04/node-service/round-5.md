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

- `internal/nodeservice/nodeservice.go`: `IsSelfOwnedUnitName` akzeptiert nur die exakten kanonischen Identitäten ohne Tag, Docker und Podman. `validateSelfOwnedUnit` nutzt diesen strukturellen Identitätsvergleich.
- `cmd/baseharbor-node-connector/main.go`: `serviceRun` lehnt fremde Unitnamen vor dem Zustands-/Unitverzeichnis und vor jedem `systemctl`-Aufruf ab. Der direkte `--self-owned-unit`-Guard verwendet dieselbe exakte Prüfung. Ein Enable-Fehler kommt als `*ServiceSetupError` zurück; die Meldung benennt die Einheit und erklärt, dass ihr Unit-File verbleibt, eventuell aktiv ist und nicht für Autostart aktiviert wurde.
- `cmd/baseharbor-node-connector/main_test.go`: Tests für kanonische Identität sowie Präfix, Suffix, Marker-Kollision und widersprüchlichen Wert; Service-Install-Gegenprobe stellt Null-Datei-/Reload-Wirkung fest. Der injizierte Enable-Fehler läuft durch `serviceRun install`, prüft typisierten Fehler, nicht aktivierten Status, verbliebenes benanntes Unit-File und fehlenden Erfolgstext.
- `internal/nodeservice/nodeservice_test.go`: fünf Identitätsfälle und Installationsverweigerung mit null Manager-, Metadaten- und Enrollment-Effekten.

### Erhaltene Lebenszyklus-/Schlüssel-Nachweise aus Runde 4

- Die Runde-4-Lebenszyklusbelege bleiben erhalten; siehe `round-4.md` (realer systemd-user-Manager, Produktprozess mit PID/comm, `is-enabled=enabled`, danach sauber gestoppt) und `review-19c.md` (Null-Effekt-Autorisierung, doppelte Installation mit einer Unit, geschützter Schlüssel).
- Die zugehörigen Regressionen wurden nicht entfernt oder abgeschwächt und liefen im vollständigen `go test ./... -count=1` auf dem neuen Kandidaten mit: `TestMissingAuthorizationProducesNilManagerAndStoreEffects`, `TestMissingAuthorizationBlocksReenrollMetadataEffect`, `TestDuplicateInstallCannotCreateSecondUnit`, `TestEnsureEnrollmentPrivateKeyCreatesPrivateKeyOnce` sowie der native Lifecycle-Test, soweit die lokale Umgebung ihn ausführt.
- Hosted-Lauf `41900064793` (neuer SHA `9913ce4770363cead7cc95726816acd4269c0358`): `Actual encrypted transport` und `Managed native enrollment` terminal SKIPPED. Diese zwei Laufzeit-Gates sind nicht als PASS gewertet; die geräte-/managerbezogenen Lebenszyklusbelege aus Runde 4 bleiben die separate Abdeckung.

### Lokale Prüfungen

- Gezielte neue `cmd/baseharbor-node-connector`-Regressionen: PASS.
- Gezielte neue `internal/nodeservice`-Regressionen: PASS.
- `go test ./... -count=1`: PASS; alle Pakete, einschließlich Connector-CLI, Node-Service und Target-Access.
- `go build ./...`: PASS (mit schreibbarem `GOMODCACHE` im Evidence-Scriptpfad).
- `go vet ./...`: PASS (Exit 0).
- `gofmt -l cmd internal`: LEER.
- `git diff --check`: PASS.

### Hosted CI — eigene Läufe, terminal

- CI · Node Connector Quality Run [41900064640](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41900064640), Head `9913ce4770363cead7cc95726816acd4269c0358`: terminal SUCCESS; Job `Test · Vet · Build` `126819771900` PASS (20s).
- Connector Source Conformance Run [41900064793](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41900064793), gleicher Head: terminal SUCCESS; Job `source` `126819771878` PASS (1m13s), einschließlich exact candidate formatting, module checksums, race/conformance suite, vet und CLI build. `Actual encrypted transport` Job `126819774524` und `Managed native enrollment` Job `126819774639` terminal SKIPPED; kein Ergebnis als grün gezählt.
- PR #19 bleibt OPEN und READY, Branch `work/r27-node-service`, Basis `main`; keine Merge-/PR-Statusänderung.

### Git-Belege und Write-Set

- Produktcommit `9913ce4770363cead7cc95726816acd4269c0358` wurde normal gepusht. `git ls-remote origin refs/heads/work/r27-node-service` = `9913ce4770363cead7cc95726816acd4269c0358` (identisch mit `HEAD`).
- `git merge-base --is-ancestor origin/main HEAD`: Exit 0.
- Dieser Runde-5-Commit ändert genau vier Dateien: `cmd/baseharbor-node-connector/main.go`, `cmd/baseharbor-node-connector/main_test.go`, `internal/nodeservice/nodeservice.go`, `internal/nodeservice/nodeservice_test.go`. Gesamter PR-Name-only-Diff gegen `origin/main` enthält sechs Connector-Feldpfade; die zwei weiteren `internal/nodeservice/reenroll.go` und `internal/nodeservice/systemd.go` stammen aus den erhaltenen Vorarbeiten dieser PR. Keine Datei außerhalb des Connector-Felds, kein `.github`.

### repo-rule compliance

- Derselbe zugewiesene Branch/Worktree; kein zweiter Branch/PR, keine Subagenten, kein `.github`-Pfad.
- Vier Dateien aus dem Connector-Bereich in Runde 5 geändert; keine Tests entfernt oder abgeschwächt.
- Red-first lief auf detached `fcca9c4a`; Produktquellen des Alt-Worktrees blieben unberührt.
- Commit/Push und alle ausgewählten Hosted Gates sind terminal; ausgelassene native Checks sind oben explizit als SKIPPED markiert.
