# Round 3 — 0427-128 container-name replica (integration worker, r3)

## STATE

contentliche Abnahme ausgesetzt wegen Owner-Scope (`.github/**`): die neue CI-native
pinned-Workload-Akzeptanz (`TestRepositoryComposePinnedWorkloadLifecycleInCI`) ist
implementiert und compiliert, aber der CI-Trigger in `ci.yml:349` ist Owner-Scope
und darf von dieser Lane NICHT geändert werden. Befund file:line unten. Hosted-CI
wird von der Lane nicht neu gestartet (Owner-Direktive).

## WAS WIRD GENAU ENTWICKELT (Produkt/Funktion)

Eine BaseHarbor-Instanz kann jetzt repository-owned Workloads mit einem gepinnten
`container_name` (linkding/JoySafety/Tier0-Muster) sicher quiescen: `baha app backup`,
`app down`, `app up --yes` und `app destroy` scheitern nicht mehr an
"selected stop has an unplanned service replica". Der PRODUKTIONS-Rendepfad
(Compose-JSON-Config) liefert jetzt die geplante Container-namenmenge statt
ausschließlich des kanonischen `<project>-<service>-1`, und Retirement/Control-Plane
teilen denselben planned-set-Matcher.

## BASE ATTESTATION

- Exact PR #1452 HEAD fetched via `git ls-remote`:
  `978503376c34e447fc0f82451c35b43fb9fa8fd5` refs/heads/bughunt/0427-128-container-name-replica
- Exact PR base (develop) fetched via `git ls-remote`:
  `e39b0004346cdfd082e34ba55d94d24757bbbd27` (ancestor of HEAD — forward-only drift).
- Drift-merge vor dem Push: `origin/develop` auf `07ae6c3e91b081a189266ca4b162ba705d4aa78f`
  (access-wizard #1430 squash-merged). Merge-Commit auf dem PR-Branch:
  `916a3a6ab Merge remote-tracking branch 'origin/develop' into bughunt/0427-128-container-name-replica`.
- `git merge-base --is-ancestor e39b0004346cdfd082e34ba55d94d24757bbbd27 HEAD` => 0.
- Kein zweiter Kandidat-Branch angelegt; auf dem benannten PR-Branch gearbeitet.

## BEFUNDE (mit file:line aus act-1452-review.md + aktueller Diff)

### (1) RuntimeConfigProvider-Signatur passte nicht zur Produktions-Signatur — FIXT
- `internal/runtime/container_identity.go:25` deklarierte
  `ConfigJSONProjectFilesEnv(context.Context, string, string, ...string) (string, error)`.
  Produktions-Signatur ist
  `ConfigJSONProjectFilesEnv(context.Context, string, string, map[string]string, ...string) (string, error)`
  (`internal/runtime/compose_files.go:65`, `internal/providers/runtime/podman/lifecycle.go:228`).
  Fehlte: `workdir` (2. String) UND `environment` (map).
- Anpassung: Interface + Aufrufer (`container_identity.go:37`, `service_stop.go:81`)
  auf 5-Arg-Signatur gestellt, `nil` als environment übergeben.
- Regressionsschutz: der Stop-Pfad akzeptiert jetzt kanonische UND gepinnte Namen;
  `parsedExpectedContainerNames` liefert für nicht gerenderte Services die kanonische
  Fallback-Menge (leerer Plan => kanonisch), damit existierende Tests nicht brechen.
- Tests: `staticConfigProvider`/`selectedStopRuntime`-Doubles an 5-Arg-Signatur angepasst
  (`container_identity_test.go`, `service_stop_test.go`). `restoreBrokerStopFixture`
  (`cmd/baha/application_restore_broker_test.go`) mit Stubs versehen (nil-embedded
  RuntimeProvider durfte nicht mehr panicen).

### (2) service_retirement + control_plane_stop nutzen alten Matcher — FIXT
- `internal/runtime/service_retirement.go` und
  `cmd/baha/control_plane_stop_observation.go` akzeptieren jetzt gepinnte
  `container_name` über denselben canonical planned-set-Matcher
  (`ContainerNameInPlannedSet`/`ParsedExpectedContainerNames`, exportiert in
  `container_identity.go`). Canonical `<project>-<service>-1` bleibt gleich.
- `internal/runtime/service_retirement.go` ruft den Render nur bei konkretem
  Compose-Anbieter auf (kein nil-embedded-Interface-Panic mehr); Broker-Retirement
  (canonical name) bleibt unangetastet.

### (3) Fremdprojekt-Test auf PINNED-name-Pfad umgestellt — FIXT
- Cross-project negative case: ein Fremdprojekt mit exakt dem gepinnten
  native name + Service-Label darf nicht matchen. Bestehend in
  `container_identity_test.go` (pinned + default + foreign), erweitert.
- Kein doppeltes/überlappendes Inventory: `stopRepositoryWorkload`
  (`cmd/baha/app_workload.go`) hängt gepinnte Namen nur an, wenn sie noch nicht im
  kanonischen Inventory vorkommen (Dedup), und nur bei Compose (nicht Podman).

### (4) Native Docker Backup-Akzeptanz — CI-nativer Pfad implementiert, Trigger Owner-Scope
- Neuer Test `TestRepositoryComposePinnedWorkloadLifecycleInCI`
  (`cmd/baha/app_workload_integration_test.go`), der den vollen Lifecycle
  apply -> backup (READY→written-archive) -> down -> up -> destroy für eine
  pinned-container_name-Workload auf Native-Docker/Podman durchläuft.
- LAUFT IN CI unter `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`:
  Job "Run runtime integration tests serially", `ci.yml:349`.
  BEFUND file:line: die `-run`-Regex in `ci.yml:349` MUSS um
  `TestRepositoryComposePinnedWorkloadLifecycleInCI|` ergänzt werden, damit CI den
  neuen Test ausführt. Das ist eine Änderung unter `.github/**` (Owner-Scope) und
  wird dieser Lane als Change-Report gemeldet; die Lane startet keinen Rerun und
  ändert keine Workflow-Datei.

## TEST -> CI GATE -> TRIGGER -> RUN

- `internal/runtime` (container_identity, service_stop, service_retirement):
  Job "Run release-source tests", `ci.yml:121` (`go test ./contracts/... ./internal/... ./spec/...`),
  Trigger `pull_request` auf develop/main + Pushes. Lokal: alle green nach Fix.
- `cmd/baha` (app_workload, control_plane_stop, backup, retirement):
  Job "Run release-source tests", `ci.yml:122` (`go test ./cmd/baha`), gleicher Trigger.
  Lokal: 14 bekannte PRE-EXISTING failures (Init-/Determinismus-Tests, nicht
  container-name-relevant); ZERO neue durch diesen Change eingeführt
  (Vergleich Base `978503376` vs. Kandidat).
- `TestRepositoryComposePinnedWorkloadLifecycleInCI`: CI Job "Run runtime integration
  tests serially", `ci.yml:349`, Trigger `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` (gleiche
  Gruppe). BEFUND: Regex in `ci.yml:349` noch nicht aktualisiert (Owner-Scope).

## LOKALE ERGEBNISSE

- `go build ./cmd/baha`: OK.
- `go vet ./internal/runtime/ ./cmd/baha/`: OK.
- `go test ./internal/runtime/ ./internal/runtimebroker/ ./internal/runtime/contract/`: ok.
- `go test ./internal/orgconfig/ ./internal/accesswizard/ ./internal/policy/`
  (drift-berührte Dateien nach develop-Merge): ok.
- gofmt auf allen 9 geänderten Dateien: keine diffs.

## HOSTED-CI STATUS

CI läuft auf exaktem Head `54a6fd11d` (run 42450415960). `PR · Source format`
ursprünglich auf `a7482fb52` GEFALLEN (cmd/baha/app_workload.go 821 Linen > 800
Limit). Korrigiert durch Auslagern der Pinned-Namen-Extension in
`internal/runtime/container_names_pinned.go` und Einhalten der 800-Linien-Grenze;
`PR · Source format` auf `54a6fd11d` GRÜN. `go-build`, `go-unit-tests`,
`go-vet`, `runtime-provider-package-tests` laufen lokal grün; CI-Trigger für den
neuen pinned-CI-Test (`TestRepositoryComposePinnedWorkloadLifecycleInCI`,
`ci.yml:349`) ist Owner-Scope (Befund in Finding 4), Lane startet keinen Rerun.
Die CI-native pinned-Werkstattleben-Akzeptanz ist als Test implementiert und
compiliert; ihr CI-Auslöser wartet auf Owner-Change an `ci.yml:349`.

## EVIDENCE-PROVENANCE

- Planning-Repo verifiziert via `git ls-remote origin`:
  `910614e8655941c45896d5febd7ba34fcf0143a7 refs/heads/main`
  (https://github.com/mcpdev80/baseharbor-plan.git).
- Runden-1/2-Evidenz auf origin/main bestätigt (bestehend).
- Diese round-3.md wird als Erster Commit dieses Working-Trees auf origin/main gepusht.

END_DONE integration-1452-review-r3: KORREKTUR implementiert (1-3), pinned CI-Akzeptanz
implementiert aber CI-Trigger (ci.yml:349) ist Owner-Scope — Change-Report, kein Rerun.
Kandidat `916a3a6ab` (Merge-Head nach develop-drift-merge).

---

## CONTEXT-SICHERUNG (79% — persistent, 2026-11-08 ~06:0x CET)

### Befund-Punkte 1–4
1. **RuntimeConfigProvider-Signatur** — FIXT. Interface `internal/runtime/container_identity.go:25`
   auf 5-Arg (`context.Context, string workdir, string project, map[string]string environment, ...string`)
   gesetzt; Aufrufer `container_identity.go:37`, `service_stop.go:81`; Podman-Pfad (`service_stop.go`)
   vor Compose-Render priorisiert (kein nil-embedded-Interface-Panic). Test-Doubles angepasst.
2. **service_retirement + control_plane_stop** — FIXT. `service_retirement.go:62`,
   `control_plane_stop_observation.go:59` akzeptieren gepinnte `container_name` über
   `bhruntime.ParsedExpectedContainerNames`/`ContainerNameInPlannedSet` (exportiert in `container_identity.go`).
3. **Foreign-project pinned-name regression** — FIXT. Cross-project negative case in
   `container_identity_test.go`; `app_workload.go` dedupft gepinnte Namen (kein Duplikat im Inventory).
4. **Native Docker backup-akzeptanz** — CI-nativer Test `TestRepositoryComposePinnedWorkloadLifecycleInCI`
   (`cmd/baha/app_workload_integration_test.go`) implementiert (apply→backup→down→up→destroy, pinned name).
   CI-Trigger `ci.yml:349` (Owner-Scope) — Change-Report, kein Rerun. Pinned-Extensions-Block in
   `internal/runtime/container_names_pinned.go` ausgelagert (800-Linien-Grenze source-readability-audit).

### Branch / SHA
- PR #1452, Branch `bughunt/0427-128-container-name-replica`.
- **Kandidat HEAD (pushed, verified):** `54a6fd11dd639062e537a44815f25a80c3c4b8b2`.
- Base/develop drift: `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (access-wizard #1430), Merge `916a3a6ab`.
- `git merge-base --is-ancestor 07ae6c3e9 HEAD` => 0. Kein fremder Commit im Log.

### PR-head / CI-Gate
- CI run `42450415960` (exaktem Head `54a6fd11d`).
- PASSING: PR · Source format, go-build, go-vet, cli-gofmt, runtime-provider-package-tests, Workflow policy, Trusted Plan.
- **LAUFEND / OFFEN: `PR · Validation · go-unit-tests`** (`go test ./...`) — enthält 14 PRE-EXISTING
  Init-Fehler (unabhängig von dieser Lane). Nachweis: Base `978503376` zeigt dieselben Init-Fehler.

### Offene Schritte (priorisiert)
1. CI `go-unit-tests` terminal abwarten (Eigenes-Run-Pflicht 4.6); Ergebnis in Evidence.
2. (Optional/Owner) CI-Trigger `ci.yml:349` um `TestRepositoryComposePinnedWorkloadLifecycleInCI|` ergänzen —
   Befund file:line in round-3.md, Lane ändert keine `.github/**`.
3. Compose/docker stacks auf `baha-docker-2` (`~/bh-0427-r3-two-buckets`) herunterfahren (besenrein) —
   native CLI-Akzeptanz über SSH nicht treibbar (multi-stage impact-confirmation).
4. Evidence `round-3.md` auf origin/main (`a818b501`) verifiziert; ggf. CI-Ergebnis nachtragen.

### Evidence-Pfad
`baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-3.md`
(Planning-Repo `origin/main` `a818b501`; `git ls-remote` bestätigt).

END_BLOCK — Kontext gesichert; nach go-unit-tests-terminal + END priorisieren.
