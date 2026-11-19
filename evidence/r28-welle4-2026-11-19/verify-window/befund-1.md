# Befund 1 — Live verify window (card 0428-138)

Mission `mission-live-verify-window.md`: verifiziert das **gemeinsame Ergebnis** der heutigen Merges auf `develop` — nicht die Einzelabnahmen. Read-only gegen das Produkt-Repo. Keine Produkt-/Workflow-/Script-/Teständerung, kein Rerun, kein Push, kein Merge, kein Subagent.

## Basis-Attestation

- Develop head (base of this verification): `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- `ls-remote origin refs/heads/develop` (fresh read-only clone, zone `/var/tmp/bah-verify-138`):
  `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- `origin/main` = `af33577a8cf6d27e6b33904f0077b3fd0b7cb987`. `origin/main` ist der Upstream-Base von `develop`, **kein** direktes Vorfahre von `develop` (develop trägt die heutigen Commits); die provenance-nötige Zeile ist hier der develop-head als Verify-Base.
- `git log --first-parent -12 origin/develop` (Kopf):
  - `da76c5cf9` feat(cli,docs): Warning marker in every acknowledging stage; EN docs i18n rename (0428-126) (#1696)
  - `21161b101` fix(0428-125): bind environment into runtime-metrics target file key/resource id (#1694)
  - `7d3438364` fix(0428-120): MCP/HTTP edit path fails loud on partial provider-change (#1688)
  - `de5324658` fix(0428-118): remove DIAG_EXEC stdout leak from app edit partial path (#1689)
  - `97a840e54` fix(observability): register application metrics signals (0428-117 lineage)
  - `8dccd4fe1` i18n: localize Achtung to Warning (0428-093 lineage)
  - `aadee4520` fix: drop phantom prometheus workload logs (#1680)
- Merge-Kette der heutigen PRs auf develop (first-parent): `#1696 ← #1694 ← ... ← #1688 ← #1689 ← #1685` (0428-115 twophase-doc). Der develop-tree enthält heute alle gemergten Inhalte; verifiziert wird der Kopf `da76c5cf9`.

## Prüftabelle

| Prüfung | Befehl wortgleich | Lauf-ID / Host-Zeug (Dauer) | Resultat + Grund | Betroffene Karte |
| --- | --- | --- | --- | --- |
| metrics: runtime target envkey (0428-125) | `go test -count=1 ./internal/metrics/...` (develop head `da76c5cf9`, Zone `/var/tmp/bah-verify-138`, 2026-11-19T10:08:48Z) | lokal, `ok github.com/mcpdev80/baseharbor/internal/metrics 0.243s` | PASS | 0428-125 (#1694) |
| metrics: Prometheus target-dir namespace regression | `go test -count=1 -run 'PrometheusConfigUsesExplicitRuntimeTargetDirectories|ProviderTargetFileNameIsStableAndNamespaced' ./internal/metrics/... -v` | lokal, 2026-11-19 | `--- PASS: TestPrometheusConfigUsesExplicitRuntimeTargetDirectories`, `--- PASS: TestProviderTargetFileNameIsStableAndNamespaced` | 0428-125 |
| observability: registry + signals (0428-117) | `go test -count=1 ./internal/observability/...` | lokal, `ok ... 0.007s` | PASS | 0428-117 / observability |
| identity: keycloak signal registration (metrics lineage) | `go test -count=1 ./internal/identityprovider/...` | lokal, `ok ... 8.991s` | PASS | metrics/observability |
| application: app edit partial path (0428-118) | `go test -count=1 ./internal/application/...` | lokal, `ok ... 4.523s` | PASS | 0428-118 (#1689) |
| app edit DIAG_EXEC stdout leak (0428-118) | `go test -count=1 -run 'DiagExec|EditApply' ./cmd/baha/...` | lokal, `ok github.com/mcpdev80/baseharbor/cmd/baha 4.259s` | PASS | 0428-118 |
| registration: MCP/HTTP partial = fail-loud (0428-120) | `go test -count=1 -run 'TestCore921' ./cmd/baha/...` | lokal, `ok github.com/mcpdev80/baseharbor/cmd/baha 9.344s` | PASS | 0428-120 (#1688) |
| enrollment/consent boundary races (0428-102) | `go test -count=1 ./internal/targetenrollment/...` | lokal, `ok ... 0.180s` | PASS | 0428-102 |
| cli2 app paths / warning marker (0428-126, 0428-093) | `go test -count=1 -run 'Warning|Attention|ProviderImpact|Acknowledg|ProviderChange' ./cmd/baha/... -v` | lokal, `ok github.com/mcpdev80/baseharbor/cmd/baha 68.920s`, 24 PASS | PASS | 0428-126 (#1696), 0428-093 |
| Go vet, alle Touch-Pfade | `go vet ./internal/metrics/... ./internal/observability/... ./internal/application/... ./internal/identityprovider/... ./cmd/baha/...` | lokal, exit 0 | PASS | alle |
| Hosted cell: Runtime · Docker Core @ develop | gh API: run `44473347792` (job `135387947884` "Native single-default · Docker") @ `da76c5cf9` | GitHub Actions, terminal SUCCESS | PASS | develop-common |
| Hosted cell: Runtime · Podman Core @ develop | gh API: run `44473347848` (job `135387923962` "Native single-default · Podman") @ `da76c5cf9` | GitHub Actions, terminal SUCCESS | PASS | develop-common |
| PR CI: Go unit + build + vet, metrics lanes | gh API run `44465054273` (0428-125) / `44471319498` (0428-126): `PR · Go unit · cli-0/1/2/3`, `packages`, `go-build`, `go-vet` | GitHub Actions, terminal SUCCESS | PASS | 0428-125/126 |
| PR CI: Go unit + build + vet, 0428-124 lane | gh API run `44478473607`: `PR · Go unit · cli-0/1/2/3`, `packages`, `go-build`, `go-vet` | GitHub Actions, terminal SUCCESS | PASS | 0428-124 |
| PR CI: 0428-131 en-docs-warning | gh API run `44478483899`: Go unit cli-0/1/2/3, packages, go-build, go-vet | GitHub Actions, terminal SUCCESS | PASS | 0428-131 |

## Gegenprobe (bekannt grüner Referenzpfad)

Referenz laut Mission: die develop-Zellen `Runtime · Docker Core` / `Podman Core` waren auf `21161b101` und `da76c5cf9` SUCCESS.

- `da76c5cf9` (current develop head): `gh run view 44473347792` → `✓ Native single-default · Docker in 7m54s` (alle Schritte ✓), `gh run view 44473347848` → `✓ Native single-default · Podman in 9m55s` (alle Schritte ✓). Host GitHub-hosted shared runner, terminal SUCCESS auf dem verify-base.
- `21161b101`: `gh run list --commit 21161b101` → run `44467228786`/`44467228776` (`Runtime · Podman/Docker Core`). Die native single-default Jobs wurden dort mit `0s` **nicht ausgelöst** (kein single-default Impact auf diesem Tree); die übergeordneten Runs terminierten `success`. Damit konsistentes Grün: auf `21161b101` war der native Gate-Trigger empty (Metrics-Dateien noch nicht im single-default-Impact-Scope), auf `da76c5cf9` läuft das Gate grün.
- Lokale Gegenprobe auf demselben Kopf: `cmd/baha` provider-change / acknowledgment regression suite (24 Tests, u.a. `TestApplicationImpactRejectsAcknowledgementAfterHiddenCredentialChange`, `TestRuntimeImpactRequiresTwoCurrentAcknowledgements`, `TestTargetDefinitionRequiresTwoCurrentAcknowledgements`, `TestOrdinaryYesNeverAcknowledgesProviderEffects`) alle PASS — deckt dieselbe acknowledgment-attention-Semantik ab, die 0428-126 (`readProviderImpactAcknowledgements` leadet die Single-Confirmation-Stage) verändert hat.

## Mapping: heutige Merge-Pfade → Gates

- observability/metrics — `internal/metrics/` (runtime_source.go, prometheus.go/verify.go, realization.go) + `internal/observability/` (registry.go): Go unit (`internal/metrics`, `internal/observability`), PR CI `Go unit · packages`, hosted Docker/Podman Core.
- logs/registration — `cmd/baha/app_registration_921.go` (0428-120) + `internal/identityprovider/` keycloak signal registration (metrics lineage): Go unit `cmd/baha` (`TestCore921*`), `internal/identityprovider`.
- enrollment/consent — `internal/targetenrollment/` (0428-102): Go unit `internal/targetenrollment`, PR CI `Go unit · packages`.
- cli2-app-pfade — `cmd/baha/` provider-change/warning-marker (0428-126, 0428-093): Go unit `cmd/baha` (cli-0/1/2/3), PR CI Go unit.

## CI-Abdeckung / Wiederholbarkeit (Befund)

- `develop`-Push triggert nur die native single-default-impact Gates `Runtime · Docker Core` / `Runtime · Podman Core` (`scripts/ci-single-default-impact.sh`, Workflow-Auslöser `push: [develop]`), iff die heutigen Merges den native/single-Core- oder Enrollment-Footprint berühren. Go-Unit-Matrix (`go test ./...` in `ci.yml`, Job `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,packages,owner}` + `go-build` + `go-vet`) läuft unter dem PR-Workflow `CI · Source & Quality`.
- Die heute betroffenen Pfade (metrics/observability/registration/enrollment/cli2) sind durch die PR-Go-unit-Matrix abgedeckt (wiederholbar über PR-CI). Die lokal ausgeführten Tests laufen unter demselben Trigger; kein eigener lokaler/VM-nur-Test, den es in die CI einspielen müsste.
- Kein fehlender Wiederholbarkeits-Befund: für alle geprüften Pfade existiert ein PR-CI-Go-unit-Job. Gemappte hosted Zelle pro develop-Kopf = Docker/Podman Core (SUCCESS @ da76c5cf9).

## Cleanliness

- Nur read-only Klon unter `/var/tmp/bah-verify-138` (`--filter=blob:none`, kein Produkt-Tree berührt).
- Keine Container/Compose/Netzwerke/Volumes gestartet (kein runtime-test-Pfad in dieser Mission).
- Cleanup: `/var/tmp/bah-verify-138` wird mit der letzten Aktion entfernt.
- cleanliness: prior-liste = Klon existent nach Clone; nachher = `/var/tmp/bah-verify-138` + `*.py`-Hilfs skripte unter `/var/tmp` entfernt.

## Schlusszeile

`qualified for release-qualification: ja` — das gemeinsame Ergebnis der heutigen Merges auf develop-Kopf `da76c5cf9` ist grün: lokale Go unit/vet auf allen Touch-Pfaden PASS, die hosted Runtime Docker/Podman Core Zellen laufen auf genau diesem SHA terminal SUCCESS, und die PR-CI Go-unit-Matrix (cli-0/1/2/3, packages, go-build, go-vet) für die betroffenen Lanes (0428-124/125/126/131) ist terminal SUCCESS. Kein fehlender Wiederholbarkeits-Befund; kein Workflow-/Produkt-/Test-Scope berührt.

## Repo-rule compliance

- Read-only gegen das Produkt-Repo; kein `.github/**`, kein Produkt-Code, kein Test, kein Script geändert.
- Kein `workflow_dispatch`, kein Rerun, kein Push, kein Merge, kein Kartenstatuswechsel.
- Kein Subagent (§4.8); alle Schritte in dieser Session.
- Isolation: Klon nur unter `/var/tmp`, kein Scratch im Ecosystem-Root.
- Planning-Evidence liegt in `baseharbor-plan/`, nie im Produkt-Repo.

## END

`END DONE mission-live-verify-window`: common develop-window result of today's merges verified green on `da76c5cf9`.
