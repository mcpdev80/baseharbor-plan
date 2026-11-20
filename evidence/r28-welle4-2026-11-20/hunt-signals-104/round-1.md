# Bug-Hunt 0428-104 — Drei Quellen ohne Destroy-Cleanup (reine Befundung, Round 1)

- Mission: `/var/tmp/mission-hunt-104.md`
- Rolle: WORKER (Bug-Hunt, keine Produktaenderung, keine Commits im Produkt, kein PR)
- Datum: 2026-11-20
- Karten-ID: t-20261117-hunt-signals-104 (card_number 0428-104), Release v0.4.28, repos [mcpdev80/baseharbor]
- Basis-Attestierung: develop HEAD `96f2ae11a25a508998c44a9854ef17f8fa15c112` (via `git ls-remote lane-origin refs/heads/develop`)
- Referenzpin der Vorgaengerkarte (befund-1): `1df7c343c334ffb17954a249f69690570e94ee8d` — IS ancestor of current develop HEAD (GitHub API `compare 1df7c343...96f2ae1`: behind_by 0, ahead_by 200, status "ahead")
- Worktree (nur Lesereferenz): `/tmp/opencode/x104-hunt-wt`, `--no-checkout`-Klon von develop, remote `origin` = `https://github.com/mcpdev80/baseharbor.git`
- Arbeitsbaum der Lane: 0 Aenderungen im Produkt (reine Lese-/git-Arbeit), keine container/netzwerke/volumes angelegt

## PLAN

1. Realitaetsabgleich: Planning-Repo-Pfad verifizieren, develop-HEAD ls-remote, Leseklon in eigener Zone
2. Vertrag (card t-20261117-hunt-signals-104) + Vorgaenger-evidence (befund-1.md, dep-risk-103-104.md) + baseharbor/AGENTS.md lesen
3. Bestandsaufnahme: alle Signal-Quellen und ihre Registry-Remove-/Reconcile-Pfade im develop-Stand (develop@96f2ae1)
4. Check destroy-cleanup: welche der vier Befund-3-Quellen (Keycloak, Runtime-Broker, Runtime-Executor, Shared PostgreSQL/Valkey) loeschen Registry-Eintraege beim Destroy — mit datei:zeile + wortlichem Zeugnis
5. Abgleich gegen befund-1-Pin 1df7c343: was hat sich seit der Vorgaengerkarte veraendert (insb. 0428-166 ID-Kollision)?
6. Funde in evidence/r28-welle4-2026-11-20/hunt-signals-104/round-1.md in baseharbor-plan schreiben
7. Sauberkeit: docker/ps-Zeugnis vorher/nachher, cleanliness-Zeile, END-Post

## Zone- und Basis-Zeugen

Planning-Repo-Verifizierung (wrong-zone check, Mission 2026-11-07):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git HEAD refs/heads/main
34a52c98926d6d8ec837b77344ce2125f8b16cf9	HEAD
34a52c98926d6d8ec837b77344ce2125f8b16cf9	refs/heads/main
```

Produkt-Basis (develop, ls-remote):

```
$ git ls-remote lane-origin refs/heads/develop   # (Klon: remote = github.com/mcpdev80/baseharbor)
96f2ae11a25a508998c44a9854ef17f8fa15c112	refs/heads/develop
```

Befund-1-Pin-Verifizierung (GitHub API, kein Full-Clone noetig):

```
$ curl -s https://api.github.com/repos/mcpdev80/baseharbor/compare/1df7c343...96f2ae1
status:"ahead"  behind_by:0  ahead_by:200
```

1df7c343 liegt 0 Commits hinter dem aktuellen develop-Kopf — IS also ein Ancestor des aktuellen develop HEAD. Alle Befunde der Vorgaengerkarte gelten weiter fuer develop@96f2ae1; zwischen den beiden SHA liegen 200 Commits (siehe Abgleich unten).

## Funde

### F1 — Destroy-Cleanup-Laecke (Befund 3) besteht auf develop@96f2ae1 fort: 3 von 4 Quellen loeschen ihre Registry-Eintraege nicht

Der Grundbefund der Karte ("Drei Quellen ohne Destroy-Cleanup") ist auf dem aktuellen develop-Stand BESTAETIGT. Die Signalregistrierung läuft über `observability.RegisterProviderSignals` / `ReconcileSignals`; das Gegenstueck beim Destroy ist `observability.Remove` bzw. `ReconcileProviderSignals` mit leerem `desired`. Vier von acht Quellen loeschen korrekt (Loki, Tempo x2, OTel), vier nicht:

Registrieren (Ensure-Pfaden), mit datei:zeile auf develop@96f2ae1:

- `internal/logs/realization.go:237` — Loki — `RegisterProviderSignals` — ID `"loki:"+p.Project`
- `internal/traces/tempo.go:403` — Tempo — `RegisterProviderSignals` — ID `"tempo:"+p.Project`
- `internal/telemetry/realization.go:196` — OTel Collector — `RegisterProviderSignals` — ID `"opentelemetry-collector:"+Project`
- `internal/identityprovider/keycloak_realization.go:115`/`:205` — Keycloak — `registerKeycloakSignals()` -> `RegisterProviderSignals` — ID `"keycloak:"+r.files.Project` (pro-Source-ID `provider_registration.go:32`)
- `cmd/baha/app_broker.go:137` — Runtime-Broker — `ReconcileRuntimeComponentObservability` -> `ReconcileSignals` — ID `"runtime-broker:"+brokerProject`
- `cmd/baha/app_broker.go:279` — Runtime-Executor — `ReconcileRuntimeComponentObservability` -> `ReconcileSignals` — ID `"runtime-executor:"+executorFiles.Project`

Destroy-/Retirement-Pfaden mit REGISTRY-CLEANUP (Witness):

- `internal/logs/lifecycle.go:172`: `_ = observability.Remove("loki:" + p.Project)` — PASST zu `logs/realization.go:237`
- `internal/traces/tempo.go:458` und `:490`: `_ = observability.Remove("tempo:" + p.Project)` — PASST zu `traces/tempo.go:403`
- `internal/telemetry/otlp.go:525`: `_ = observability.Remove("opentelemetry-collector:" + files.Project)` — PASST zu `telemetry/realization.go:196`

Destroy-/Retirement-Pfaden OHNE REGISTRY-CLEANUP (der Befund 3,Witness):

- **Keycloak** `internal/identityprovider/keycloak_realization.go:462` (`func (r *localKeycloakRealization) Destroy`) — ruft `r.lifecycle.Destroy` (`:481`) und `os.RemoveAll(files.Dir)` (`:484`), aber KEIN `observability.Remove`/`ReconcileSignals`. Die Ensure-Seite schreibt aber die Source bei `:115`/`:205` (`RegisterProviderSignals` mit ID `"keycloak:"+r.files.Project`). Der `placement.Scope != capability.ScopeApplication`-Rueckgang bei `:479` macht den Destroy fuer Shared-Keycloak ohnehin zum No-op — fuer App-Scoped-Keycloak ist die Source registriert, wird aber beim Destroy nicht bereinigt.
- **Runtime-Broker/Executor**: die Registry-Eintraege werden in den Ensure-Pfaden `cmd/baha/app_broker.go:137`/`:279` geschrieben; der Executor-Destroy `internal/runtimeexecutor/compose.go:232-247` (`DestroySharedAt`) loescht nur `DestroyProject` + `os.RemoveAll(files.Dir)` (`:246`), kein Registry-Cleanup. Der Broker-Retirement-Pfad `cmd/baha/runtime_destroy_all.go` (z.B. `:365-368`) ruft `ReleaseApplicationProviderRegistryAt` (`:388`) auf, entfernt aber KEINE observability-Source. Witness: `git grep` nach `observability.Remove`/`ReconcileSignals` in `cmd/baha/app_broker.go`, `internal/runtimeexecutor/compose.go`, `cmd/baha/runtime_destroy_all.go` = leer.
- **Shared PostgreSQL/Valkey**: vollstaendiger Shared-Destroy laeuft ueber `cmd/baha/runtime_destroy_all.go:459` -> `internal/application/shared_backends_resources_runtime.go:367-400` (`DestroyShared...`); Witness `git show HEAD:...shared_backends_resources_runtime.go | grep -E "observability\.Remove|ReconcileSignals|ReconcileProviderSignals"` = leer. App-scoped Provider werden durch `PruneOwnedProviderInstances` (`internal/application/runtime_observability.go:141-171`, aufgerufen `runtime_postgres.go:131`) bereinigt — diese bereits funktionierende App-scoped-Bereinigung ist BEIM ZUGRIFF, nicht betroffen (nur dokumentiert, nicht veraendert).

Schadensbild (Frage: was geschieht im Fehlerfall beim Nutzer?): ein Target mit mehrfachem deploy/destroy-Zyklus traegt stale Keycloak/Broker/Executor-Source-Eintraege, die `observability.List`/`ListMetrics` (`internal/observability/registry.go`) als scrape-Ziele materialisieren — Prometheus haenge tote Targets (up=0), `VerifyProviderSources` kann zeitweise fails, Perses-Witnesses (Karten 078/080/082) zeigen Signale ohne existierendes Backend. Die ID am Project haengt (`"runtime-broker:"+project`, `"keycloak:"+project`), also bleiben Eintraege auch nach app-Umbenennung/Env-Wechsel haften.

### F2 — 0428-166/1712 hat die ID-Kollision (Befund 1a) behoben; der Cleanup-Pfad ist aber NICHT mitgefixt, sondern nur noch kritischer

Zwischen befund-1-Pin `1df7c343` und develop-`96f2ae1` liegt der Merge von **0428-166** (`fix(0428-166): fail-closed on Keycloak signal-id normalization collision`, PR #1712, Commit `96f2ae1`). Die Aenderungen beruehren:

- `internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/keycloak_signal_collision_test.go` (NEU), `keycloak_signal_golden_test.go` (NEU), `keycloak_signal_registration_test.go` (NEU)
- `internal/observability/migration.go` (NEU): `ReconcileLegacySignals` re-bookt die pre-scoping Legacy-ID `"keycloak-metrics"` auf `"keycloak:"+project`, ohne sie zu droppen — undokumentierte, aber existierende Migration
- `internal/observability/registry.go`, `provider_registration.go`, `internal/application/runtime_observability.go`

Der alte Befund-1a-Fall (zwei Keycloak-Instanzen schreiben gegen dieselbe unscoped-ID und loeschen sich gegenseitig, `Remove` beim Destroy loescht beide) ist damit durch fail-closed Normalisierung auf der Ensure-Seite behoben. ABER: genau die Destroy-Seite, die den Cleanup machen muesste, ist unveraendert leer (F1). Die Migration in `migration.go:58` macht den Fall sogar schärfer: eine Legacy-ID `keycloak-metrics` (project-unabhaengig) ist im destroy-cleanup-Fall potenziell noch problematischer als die jetzt scoped-ID, weil ein Remove ohne owner/ID-Pruefung mehrere Instanzen treffen koennte. Der Cleanup-Pfad muss also spaeter MINDESTENS die Migration mitbedenken.

### F3 — Kein zerstoerter/abdeckender Test fuer den fehlenden Cleanup

Witness: `git grep -inE "Remove|ReconcileSignals" internal/identityprovider/*_test.go internal/runtimeexecutor/*_test.go internal/application/runtime_observability_test.go | grep -iE "keycloak|executor|broker|destroy"` findet nur `os.Remove` (Datei) und `observability.Remove` in `keycloak_legacy_migration_integration_test.go` (Tests der Migration, nicht des Destroy-Cleanups). Es existiert KEIN Test, der assertiert, dass Keycloak/Broker/Executor-Source-Eintraege beim Destroy aus der Registry verschwinden — die Laecke ist also nicht nur implementierungs-, sondern auch testabdeckungsseitig offen.

## Abgleich mit der Vorgaengerkarte (befund-1, pin 1df7c343)

- Befund 1 (registrier-pad-/ID-Raum-Heterogenitaet): durch 0428-166/1712 (F2) teilbehoben — Keycloak-ID jetzt project-scoped + fail-closed, Migration `migration.go` vorhanden.
- Befund 2 (application-Klasse fehlt in Registry): unveraendert — `observability.List` filtert `class==application` weiterhin aus (keine Aenderung in registry.go seit Pin).
- **Befund 3 (drei/vier Quellen ohne Destroy-Cleanup): BESTAETIGT auf develop@96f2ae1** — keine Aenderung der Cleanup-Pfade seit Pin.
- Befund 4/5 (alert/rule-Ebene fehlt; k8s-core/worker/perses nicht implementiert): unveraendert (nur `internal/metrics/perses_prometheus_alerts.go` auf unmerged Kandidaten; develop-seitig keine alert-rule-Registrierung).

## repo-rule compliance

- Keine Produktdateien veraendert, keine Tests, keine `.github/**`, kein Planning-Board.
- Kein PR, kein Commit im Produkt, kein workflow_dispatch/rerun.
- Kein Subagent, kein `git add -A`, keine sleep-/wait-Bloecke.
- Reine Lese-/git-Arbeit gegen einen `--no-checkout`-Klon in eigener Zone (`/tmp/opencode/x104-hunt-wt`); der quarantinierte Checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor` (anderer Lane, Branch `lane-0428-174-develop-runtime-red`, untracked dirs) wurde NICHT fuer Evidence genutzt.
- Remote-Zeugen nur ueber `git ls-remote` (github.com/mcpdev80) + GitHub API `compare`; kein zitat des quarantinierten Refs.

## Sauberkeit / Teardown

- Vorher (docker, dieser Host): `docker ps -a --format '{{.Names}}\t{{.State}}'` = leer; `docker network ls` = bridge/host/none; `docker compose ls -a` = leer.
- Nachher: identisch.
- Diese Lane hat KEINE container/netzwerke/volumes/state-verzeichnisse angelegt; keine deployment-/compose-Aufrufe; reine Lese-/git-/curl-Arbeit.
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet; /tmp/opencode/x104-hunt-wt Klon wird mit END aufgeraeumt.

## END

END_DONE mission-hunt-104 (0428-104, Drei Quellen ohne Destroy-Cleanup): reine Befundung auf develop@96f2ae1 (ls-remote-zeugnis + ancestry 1df7c343 IS ancestor). Fund F1 BESTAETIGT: Loki (`logs/lifecycle.go:172`), Tempo (`traces/tempo.go:458/490`), OTel (`telemetry/otlp.go:525`) loeschen Registry beim Destroy; KEYCLOAK (`keycloak_realization.go:462/481/484`, Ensure bei `:115/205`), RUNTIME-BROKER/EXECUTOR (`app_broker.go:137/279`, Destroy `runtimeexecutor/compose.go:232-247`, Retirement `runtime_destroy_all.go:388`) und SHARED POSTGRES/VALKEY (`runtime_destroy_all.go:459` -> `shared_backends_resources_runtime.go:367-400`) loeschen NICHT — Witness: `git grep observability.Remove|ReconcileSignals` = leer in den Destroy-Pfaden. Fund F2: 0428-166/1712 (PR #1712) hat ID-Kollision auf Ensure-Seite behoben + Migration `migration.go`, Cleanup-Pfad aber unangetastet -> spaeter minimal kritisch. Fund F3: kein Test deckt den fehlenden Cleanup ab. Evidence auf baseharbor-plan main, kein Produkt-Commit.
