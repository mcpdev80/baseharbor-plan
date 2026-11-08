# 0427-144 · Foreign records stall wizard — round 1

Task: t-20261108-bughunt-wizard-foreign-records · Lane: w144-flash (mission-144) · Source dossier: [hp1.md BF-6](../vm-bughunt/hp1.md)

## PLAN

- Realitaetsabgleich: baseharbor develop HEAD, baseharbor-plan main, Kartenakte und hp1-Befund BF-6 lesen.
- Worktree anlegen, Base-Attestation (SHA + Ancestor-Nachweis) sichern.
- Fundstelle reproduzieren: Provider-Aufloesung, die fremde records anspricht (datei:zeile), mit Probe-Test.
- Minimal-Fix nach Acceptance-Disjunktion: KONKRETEN Konflikt mit naechstem Schritt melden (Ast 2), Wizard-SelectionView toleriert requirement-lokale Luecke.
- Regressionstest mit zwei apps auf gemischtem Hintergrund, in CI-erfaschter Gruppe verdrahtet.
- Lokale Checks (build/vet/fokussierte Tests/Lesbarkeit), PR gegen develop HEAD mit Ancestry- und Cleanliness-Zeugen.
- Hosted CI-Lauf bis TERMINAL beobachten, Ergebnis hier festhalten.
- Evidence finalisieren, publizieren, END melden.

## Fundstelle und Reproduktion

- `cmd/baha/application_provider_plan.go:46` baut die Fremdkonsumenten-Schlüssel als `deployment/<DeploymentID>` und ruft `application.ResolveUnionFootprint`; `internal/application/provider_union.go` verpackte den Aufloesungsfehler eines Konsumenten als `fmt.Errorf("consumer %s: %w", ...)`. Die Klassifikation in `cmd/baha/app_core_requirement.go` (`classifyApplicationResolutionError`) verlor damit die Konsumenten-Zuordnung und lieferte das generische "Reconcile the existing Target provider binding" ohne Eigentuemer und naechsten Schritt — genau der hp1 BF-6 Stillstand: eine http-only App wird durch die abgelaufene Referenz einer fremden Aufzeichnung blockiert.
- Reproduktion mit Probe-Test (Zwei-App-Hintergrund: fremde App mit `DesiredProviderPreferences` auf die nicht mehr registrierte Instanz `postgresql/shared/environment-dev-91df0423`, Quellrepository geloescht, deren Record `Observed.State=configured`; davon unabhaengige http-only App): vor dem Fix bricht `appProviderChoicesWithView` mit `consumer deployment/22222222-2222-4222-8222-222222222222: provider resolution missing-dependency for / (instance "postgresql/shared/environment-dev-91df0423")` und die klassifizierte Meldung nennt nur die generische Binding-Reconcile-Anweisung.

## Fix (Ast 2 der Disjunktion: konkreter Konflikt mit naechstem Schritt)

- `internal/application/footprint.go`: `ResolutionError` traegt das fehlende `Consumer`-Feld (JSON `consumer`).
- `internal/application/provider_union.go`: füllt `resolution.Consumer` auf dem Schlüssel `deployment/<ID>`, bevor es als Konsumentenursache verpackt wird; die Konsumenten-Fussabdrucks-Aufloesung behaelt ihre Ziel-Trennung bei der Fehlerzuordnung.
- `cmd/baha/app_core_requirement.go` (`classifyApplicationResolutionError`): ein fehlende-Abhaengigkeit-Fehler, der einem `deployment/`-Konsumenten gehoert, wird als Ursache `provider_stale_consumer_dependency` klassifiziert; die namentliche Ressource ist der Konsumentenschluessel, und der naechste Schritt nennt die fremde Aufzeichnung, ihre Realisierung und die konkrete Wiederherstellung (Provider-Instanz dort neu aufloesen oder die verwaiste Referenz bereinigen), statt der generischen Bindungs-Anweisung. Eine echte gleichartige Referenz bleibt bei der bisherigen Ursache.
- `cmd/baha/app_provider_choice.go` + Wizard/Edit-Flaechen: SelectionView (Wizard `choicesForSelection`, Edit-Choices-Autoritaet)fasst einen requirement-lokalen `missing`-Fehlschlag als sichtbaren unresolved-Grund mit Kandidaten auf, statt die Auswahl zu verletzen; fremde Konsumenten und andere Fehlerformen brechen weiterhin mit dem konkreten typisierten Fehler, genau wie plan/preview. Die 0427-150 Live-Nachloesung (`liveCanonicalChoiceInstances`, `appProviderChoicesWithPreferences`) bleibt unveraendert wirksam.
- `cmd/baha/app_edit.go`: die Wiederherstellung gespeicherter Praeferenzen bestaetigt nur Instanzen, die dieselbe SelectionView-Oberflaeche anzeigt; eine nicht angebotene Instanz blockiert die Sitzung nicht, die plan/apply-Oberflaeche nennt ihren konkreten Konflikt.

## Kandidat

- Repository: https://github.com/mcpdev80/baseharbor · PR: https://github.com/mcpdev80/baseharbor/pull/1501
- Branch: `fix/0427-144-foreign-records-resolution` · Kandidat SHA: `a6bb99bfa1727b2231c3b226a7069c33abe96a51` (ein Commit, PR-Diff: 8 Dateien, +333/−22)
- Base-Attestation: entwickelt auf develop `7af8d440e9a4dd1b633fdc44e4093109fe44ae37`; nach Landen von 0427-150 (#1490, Merge-Commit `20902f0a6ab016fd8fe6a501751e1becc5f334dd`) neu aufgezogen — der Kandidat enthaelt aktuelles `origin/develop` als Vorfahren (`git merge-base --is-ancestor origin/develop HEAD` = 0).
- Cleanliness: `git log --oneline origin/develop..HEAD` = genau `a6bb99bf fix(0427-144): report foreign provider records as actionable conflicts`; keine `.github/**` Aenderungen; Write-Set: `cmd/baha/app_core_requirement.go`, `cmd/baha/app_edit.go`, `cmd/baha/app_edit_apply_result.go`, `cmd/baha/app_provider_choice.go`, `cmd/baha/app_wizard_controller.go`, `cmd/baha/app_foreign_records_regression_test.go` (neu), `internal/application/footprint.go`, `internal/application/provider_union.go`.
- ls-remote-Zeuge (Publikation): `20902f0a6ab016fd8fe6a501751e1becc5f334dd refs/heads/develop` und `a6bb99bfa1727b2231c3b226a7069c33abe96a51 refs/heads/fix/0427-144-foreign-records-resolution`.
- 0427-150-Koordination: der Landeckonflikt mit #1490 wurde durch Rebase auf das enthaltende develop geloest; die gemeinschaftlichen Wahl-Oberflaechen-Signaturen (`appProviderChoicesWithView(manifest, snapshot, selection, preferences, selectionView)`) fusionieren beide Mechanismen, die 0427-150 Testdateien bleiben unveraendert und gruen.

## Regressionstest und CI-Verdrahtung

- Neu: `cmd/baha/app_foreign_records_regression_test.go` mit `TestForeignRecordDoesNotBlockHttpAppSelection` (zwei apps, gemischter Hintergrund; http-only Auswahl bleibt moeglich), `TestForeignRecordUnionReportsConcreteConflictWithNextStep` (Plan/Verify-Bereich nennt Konsumentenschluessel, abgelaufene Instanz und naechsten Schritt) und `TestForeignRecordStaleReferenceDoesNotPoisonUnrelatedUnionPlan` (saubere Toleranz fuer die fret-App, kein Blocker, keine generische Meldung).
- CI-Aufnahme: der Test laeuft im regularen `go-unit-tests`-Job der Workflow-Datei `.github/workflows/ci.yml:123` (`BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`) ohne Pfadfilter, also bei jeder Auswahl dieses Jobs; die PR-Auswahl startet die Gruppe ueber die betroffenen Pfade `cmd/baha/**` und `internal/**` gemaess `scripts/pr-gate-map-v1.json`. Kein zuschaetzlicher Trigger noetig, keine `.github/**` Aenderung.

## Lokale Pruefungen (Worktree, Kandidat)

- `go build ./...`, `go vet ./cmd/baha/ ./internal/application/`, `gofmt -l`: sauber.
- `go test ./cmd/baha/ -run TestForeignRecord -count=1`: ok (3/3).
- `go test ./cmd/baha/ -run 'TestForeignRecord|TestAppProviderChoices|TestProviderStale|TestAppWizardController|TestAppEditHydrates' -count=1` (Auswahl-, Wizard-, Edit- und 0427-150-Stale-Gruppe, Kandidat auf aktuellem develop): ok bis auf die environmentale Native-Zelle unten. `TestAppEdit`-Gruppe separat: nur die Native-Zelle unten.
- `go test ./internal/application/ ./internal/capability/`: ok.
- `bash scripts/source-readability-audit.sh`: PASS.
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`: SHA — faellt auf reinem develop `20902f0a` (isolierter Zeugen-Worktree, identische Fehlerzeile "existing native network lacks a protected Core or shared backend owner") wie auf dem Kandidaten; environmentale Native-Runtime-Voraussetzung dieses Hosts, keine Kandidatenregression. Ebenso die Logs-/Env-Tests, die nur ohne `BASEHARBOR_LOGS_ENABLED=false` lokal starten; der CI-Job setzt die Variable (`ci.yml:123`).

## Hosted CI

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/42528721531 (CI · Source & Quality · PR #1501 · attempt 1 · Kandidat `a6bb99bf`). Beobachtet bis terminal: **completed / success** (erstellt 22:08:32Z, abgeschlossen 22:18:38Z), vom Worker selbst überwacht (Eigenes-Run-Pflicht).
- Alle ausgefuehrten Jobs grün: Workflow policy, PR · Trusted Plan, PR · Source format, PR · Focused Python, PR · Native impact selection, go-build, go-vet, cli-gofmt, go-unit-tests ( traegt `go test ./cmd/baha` und damit die neue Regression), wizard-controller-tests, wizard-provider-choice-tests, wizard-app-edit-tests, Native destroy retry docker und podman. Nicht betroffene Jobs ( Consumer Pins, Demo Pin, Exact Candidate, Public Contracts, Runner Interface, Selected Runtime, Native Keycloak/Core, Targeted HA, Release Source Preflight, validate) sind regelkonform `skipping`, nicht umgefaerbt.
- PR-Zustand nach terminalerobservation: OPEN, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`. Merge ist Sache der Abschlussabnahme, nicht dieser Lane.

## repo-rule compliance

- Plan → Preflight → Apply → Verify getrennt; keine Mutationspfade geaendert, nur Zuordnung und Anzeige der Aufloesung.
- Keine `.github/**` Aenderung, ein Kandidaten-Branch, kein Force des PR-Ziels, keine Subagenten, nur gezielte `git add` der Write-Set-Dateien.
- Tests in bestehender CI-Gruppe ohne neue Workflow-Datei ausgefuehrt; Ergebnis unten mit Run-Zeuge.

END: Kandidat `a6bb99bfa1727b2231c3b226a7069c33abe96a51` auf PR #1501 gegen develop, gehosteter Lauf 42528721531 terminal success, Evidence publiziert.
