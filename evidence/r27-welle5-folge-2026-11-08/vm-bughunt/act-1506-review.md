# CODEX-REVIEW 0427-174 — PR #1506

ROLLE: REVIEW
Kandidat: `fb21a02eec29890c793ae3da5e8ab7d3567fa829`
PR: https://github.com/mcpdev80/baseharbor/pull/1506
Kartenvertrag: `t-20261108-bughunt-permission-lies-foreign-install`
URTEIL: KORREKTUR

## PLAN

1. Verifiziere live PR-Head, PR-base, develop-Head, Diff und exakten Hosted-Lauf.
2. Prüfe die Owner-Fehlerklassen und die leere-Target-Regressionszelle.
3. Verfolge Permission-denied-Fehler durch CLI-Auflösung und den Owner-loan-Recheck.
4. Vergleiche Testpakete mit den tatsächlich ausgewählten CI-Jobs und Triggern.
5. Veröffentliche das SHA-genaue Urteil mit Korrekturrezept.

## Vertrag und Diff

Der Kartenvertrag fordert getrennte Ergebnisse: unreadable/denied wird `ErrDeploymentOwnerAccessDenied` mit Dateipfad und Reparaturhinweis; leerer/ungültiger Target-Name bleibt Usage-Fehler; nur ein echter fremder Owner bleibt `ErrDeploymentOwnerForeign`. Die PR ändert genau vier Dateien unter `internal/deployment/`: `deployment_store.go`, `deployment_owner_loan.go`, neue `deployment_owner_load_seam.go`, neue `deployment_owner_access_denied_test.go`. Keine `.github/**`-Datei ist geändert.

Der PR-API-Base ist `develop@b3a8042d18ea60f162a32a51df34a499cad6a237`, aber der Kandidaten-Commit hat Parent `20902f0a6ab016fd8fe6a501751e1becc5f334dd`; `merge-base(origin/develop, origin/pr-1506)` ist ebenfalls `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Der aktuelle develop-Head ist kein Ancestor des Kandidaten. Zwischen diesem Merge-Base und develop liegen Änderungen in `cmd/baha`-Dateien, nicht in `internal/deployment`. Das Review bezieht sich auf den exakten PR-Commit; ein Lauf auf der Integration mit aktuellem develop ist noch nicht belegt.

## Befunde

1. **Blockierend — der Permission-denied-Fehler verschwindet im benannten CLI-Auflösungspfad als „nicht registriert“.** Bei `internal/deployment/deployment_list.go:73-78` konvertiert die best-effort Liste jeden Ownerfehler in eine Warnung vom Typ `missing`. `cmd/baha/app_context.go:235-240` nutzt diese Liste für `baha app status NAME`; die Auswertung bei `:266-309` verarbeitet nur Warnungen des Typs `incomplete` und endet ohne Treffer mit „has no registered deployment“. Ich baute `baha` separat aus develop und aus dem exakten Kandidaten und führte beide mit derselben isolierten Fixture aus: ein `local`-Target mit Deployment-Record und `installation.json`-Modus `000`. Im Repository-Kontext ohne NAME meldet develop „foreign installation“, der Kandidat die neue Permission-denied-Meldung samt Pfad und `permission denied`. Mit explizitem `app status fixture-app` melden beide Binaries jedoch „application … has no registered deployment on target local“. Damit wird der fehlgeschlagene Eigentümercheck weiterhin als Abwesenheit dargestellt. **Rezept:** Access-denied-Warnungen durch `resolveRegisteredApplication` erhalten und als Access-denied zurückgeben, statt sie wie fehlende Records zu behandeln. In `cmd/baha` eine `runWithIO`-Regression mit benanntem App-Einstieg und derselben Permission-denied-Fixture hinzufügen; sie muss `ErrDeploymentOwnerAccessDenied`, den Installationspfad und den Reparaturhinweis ausgeben und darf weder „not found“ noch „foreign“ melden. **Stoppkriterium:** benannter und repository-basierter CLI-Einstieg zeigen für dieselbe Permission-Fixture dieselbe Access-denied-Klasse; Record bleibt unverändert.

2. **Blockierend — die Owner-loan-Revalidierung faltet fehlgeschlagene Reads weiterhin in `ErrDeploymentOwnerForeign`.** `internal/deployment/deployment_owner_loan.go:98-106` ruft direkt `coreinstallation.Load(targetRoot)` auf; jeder Fehler außer `os.ErrNotExist` führt zu `ErrDeploymentOwnerForeign`. Der neue Loader-Testseam wird dort umgangen. Wenn während der Loan-Revalidierung eine Berechtigungs- oder sonstige Lesestörung eintritt, ist damit keine echte fremde Installation nachgewiesen. **Rezept:** die Revalidierung durch denselben klassifizierenden Loader führen und Permission-/I/O-Fehler als Access-denied bzw. konkrete unveränderte Fehler propagieren; nur nachweislich geladene, fremde Owner-Identität als Foreign klassifizieren. Eine deterministische Permission-Injektion während genau dieses Rechecks muss zeigen, dass der Vorgang fail-closed endet, weder Foreign/Missing vortäuscht noch den Loan gewährt. **Stoppkriterium:** jeder fehlgeschlagene Recheck endet unterscheidbar und verweigert die Autorisierung; echte foreign-identity bleibt Foreign.

3. **Korrektur — der Foreign-Fallback ist breiter als „nur echter fremder Hash“.** `internal/deployment/deployment_store.go:149-163` ordnet jeden Fehler von `coreinstallation.Load`, der weder `os.ErrNotExist` noch ein erkennbarer `fs`-Fehler ist, `ErrDeploymentOwnerForeign` zu. `internal/coreinstallation/installation.go:73-100` kann auch nicht-FS-Fehler für ungeschützten Modus, ungültiges JSON oder inkompatiblen/ungültigen Zustand liefern. Die neue Foreign-Gegenprobe verändert ausschließlich `Spec.Target` eines geladenen Zustands (`deployment_owner_access_denied_test.go:158-181`); sie belegt den geladenen Target-Mismatch, nicht die Abgrenzung zu defektem oder unentscheidbarem Zustand. **Rezept:** echte geladene fremde Identität als Foreign erhalten; ungültigen, beschädigten oder nicht klassifizierbaren Ladezustand als eigenen fail-closed Fehler behandeln, nicht als erwiesene Fremdinstallation. Regressionen: gültig fremder Owner bleibt Foreign; defektes JSON/unsicherer Dateimodus wird nicht als Foreign oder Missing gelesen und verweigert ohne Mutation. **Stoppkriterium:** ausschließlich eine erfolgreich geladene, positive Owner-Abweichung kann `ErrDeploymentOwnerForeign` erzeugen.

4. **Test-/CI-Abdeckung:** Die drei neuen Tests `TestDeploymentOwnerAccessDeniedIsNotForeign`, `TestDeploymentOwnerMissingStillMissingAndForeignStillForeign` und `TestDeploymentOwnerEmptyTargetUsageError` laufen in `internal/deployment`. Hosted Job `PR · Validation · deployment-package-tests` (run `42546637296`, job `128932988609`) führt über die vertrauenswürdige `scripts/pr-check-runner.py`-Zuordnung für `deployment-package-tests` (`:170-175`) `go test ./internal/deployment -count=1 -json` aus. Trigger war `pull_request` auf den exakten Head `fb21a02eec29890c793ae3da5e8ab7d3567fa829`; der Job ist terminal erfolgreich. Damit sind die vorhandenen Paketregressionen dauerhaft erfasst. Es gibt in diesem Lauf aber keinen `cli-package-tests`-Job und keinen CLI-Entry-Regressionstest für den in Befund 1 reproduzierten Verlust. Ein Test unter `cmd/baha/*_test.go` wird durch die bestehende Planner-Regel für CLI-Testdateien an `cli-package-tests` gebunden (`scripts/pr-gate-plan.py:1273-1280`); der Workflow-Dispatcher kennt diesen Check unter `.github/workflows/ci.yml:964-970`. Neue CLI-Regressions müssen auf diesem PR-Trigger tatsächlich ausgewählt und bestanden sein.

## Lokale Gegenprobe

Beide Binaries wurden frisch aus develop und dem exakten PR-Head gebaut. Die Permission-Fixture verwendete `BASEHARBOR_STATE_DIR=/tmp/opencode/0427-174-fixture/state`, `BASEHARBOR_TARGET=local`, Deployment-ID `11111111-1111-4111-8111-111111111111` und `installation.json` Modus `000`.

```text
Develop binary, `baha app status` im Fixture-Repository:
Error: deployment state directory is not owned by the installation under its Target; foreign installation cannot own this deployment

PR binary, gleicher Befehl und gleicher Zustand:
Error: deployment state directory for its Target is not readable; the Core installation.json is not accessible to this user — check owner and permissions before its state is loadable: open /tmp/opencode/0427-174-fixture/state/targets/local/runtime/installation.json: permission denied

PR binary, `baha app status fixture-app` aus dem Nicht-Repository-Verzeichnis mit demselben Zustand:
Error: application "fixture-app" has no registered deployment on target "local"
```

Auf dem PR-Checkout liefen die drei neuen Pakettests gezielt mit `go test ./internal/deployment -run '^(TestDeploymentOwnerAccessDeniedIsNotForeign|TestDeploymentOwnerMissingStillMissingAndForeignStillForeign|TestDeploymentOwnerEmptyTargetUsageError)$' -count=1 -v`: alle drei PASS. `TestDeploymentOwnerEmptyTargetUsageError` belegt `ValidateTargetName("")` und `ListDeployments("")` auf Paketebene, aber keine CLI-Entry-Route.

## Hosted status

Run `42546637296` ist `completed/success` auf genau `fb21a02eec29890c793ae3da5e8ab7d3567fa829`, Event `pull_request`. `deployment-package-tests` job `128932988609`, `source-contracts` job `128932988656`, `cli-build` job `128932988696`, `cli-vet` job `128932988678`, `cli-guided-tests` job `128932988620`, native destroy-retry Docker job `128932988675`, native destroy-retry Podman job `128932988638` und `PR Selected Checks` job `128934631319` sind erfolgreich. Native Keycloak/Core sowie mehrere nicht ausgewählte Jobs sind `skipped`, nicht bestanden oder als grün zu zählen. Der relevante Paketjob ist grün; er deckt die fehlende CLI-Regression nicht ab.

## Urteil und Korrekturrezept

**KORREKTUR.** Der direkte Owner-Check trennt den beobachteten Permission-denied-Fall korrekt von Missing und Foreign; die empty-target-Paketregression bleibt Usage-Fehler, und ein geladener Target-Mismatch bleibt Foreign. Die Abnahme scheitert aber daran, dass der benannte CLI-Pfad Access-denied als „not found“ verbirgt und der Owner-loan-Recheck Lesefehler weiter als Foreign fehlklassifiziert. Zusätzlich ist der Foreign-Fallback breiter als die Kartenaussage.

Korrigiere `internal/deployment/deployment_list.go`, `cmd/baha/app_context.go`, `internal/deployment/deployment_owner_loan.go` und `internal/deployment/deployment_store.go`: Access-denied-Warnungen bis zum CLI-Ergebnis erhalten, alle Rechecks klassifizieren/propagieren statt Fehler als Owner-Beweis zu behandeln, und Foreign nur nach positiver Identitätsabweichung zurückgeben. Ergänze command-entry-, loan-recheck-, malformed-state- und leere-Target-Regressions. Erforderliche Zuordnung: Deployment-Paketregressionen → `deployment-package-tests` → Pull-Request-Auswahl für `internal/deployment`; CLI-Entry-Regressionen → `cli-package-tests` → Pull-Request-Auswahl für `cmd/baha/*_test.go`. Stop, wenn ein Fehler- oder Abwesenheitszustand weiter als Foreign/Missing/„not found“ durchgereicht wird, eine Verweigerung Daten ändert oder der Test nicht im bezeichneten Job tatsächlich läuft.

Vor weiterer Abnahme auf den aktuellen PR-Base `develop@b3a8042d18ea60f162a32a51df34a499cad6a237` integrieren und den exakten neuen Head mit ausgewählten Checks prüfen. Der aktuelle erfolgreiche Lauf beweist ausschließlich den alten PR-Head und dessen Paketregressionen.

END_DONE 0427-174-review: KORREKTUR — Kandidat `fb21a02eec29890c793ae3da5e8ab7d3567fa829`; Evidence auf baseharbor-plan origin/main zu veröffentlichen.

## Planning validation

`python3 scripts/plan.py check` was attempted and failed before evaluating this act: `scripts/plan.py:650 short_ref` raised `ValueError: not enough values to unpack (expected 2, got 1)` while generating a task PR link from existing vault metadata. This review did not modify task metadata. `git diff --check` passed, and the act contains no checkbox syntax.
