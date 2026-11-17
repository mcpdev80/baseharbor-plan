# BUG-HUNT mission-hunt-signals.md — Signallandschaft develop (reine Befundung)

- Mission: `/var/tmp/missions/mission-hunt-signals.md`
- Rolle: WORKER (Bug-Hunt, keine Produktaenderung, keine Commits im Produkt)
- Datum: 2026-11-17
- Lane-Worktree (nur Lesereferenz): `workers/.models/flash/wt/hunt-signals`, Branch `hunt-signals/develop-1df7c343`, detached auf Produkt-Basis
- Modellkanal: Flash-Sitz (w150-ahnlich, Owner-Direktive Pool)

## PLAN

1. Realitaetsabgleich: develop-HEAD ls-remote, Plan-Repos-Pfad verifizieren, Worktree anlegen
2. Bestandsaufnahme: alle telemetry-/observability-Quellen im develop-Stand finden
3. Check (a): metrics/telemetry-source-Registrierung pro Quelle mit file:line
4. Check (b): alert-/signal-rule-Registrierung pro Quelle mit file:line, Fehlstellen markieren
5. Check (c): Registrierungspfade der Dienste untereinander vergleichen, Abweichungen festhalten
6. Befunde als `evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md` in baseharbor-plan schreiben, Commit, origin/main-Verifizierung
7. Sauberkeit: container/netz-liste vorher/nachher, cleanliness-Zeile, END-Post

## Zone- und Basis-Zeugen

Planning-Repo-Verifizierung (wrong-zone check, Mission 2026-11-07):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git HEAD refs/heads/main
531975cffeaff972a04cab5faba5fba758855d1b	HEAD
531975cffeaff972a04cab5faba5fba758855d1b	refs/heads/main
```

Produkt-Basis (develop, nur CLOSED/merged Inhalt; Mission nennt 1df7c343, Remote-HEAD ist inzwischen einen Merge weiter):

```
$ git ls-remote origin refs/heads/develop   # baseharbor
8db0d9bdf8d9ae77db94c9ddce9c209001c4da54	refs/heads/develop
$ git merge-base --is-ancestor 1df7c343 origin/develop && echo yes
yes
```

Die Akte zitiert `file:line` gegen `1df7c343` (Mission-Pin). Der einzige Develop-Fortschritt danach, `8db0d9bdf` (PR #1666, config fail-loud), aendert NUR `internal/deployment/{target.go,config_fail_loud_test.go}` — kein Signallandpfad, alle Befunde gelten unveraendert fuer beide SHA. Bestaetigt per:

```
$ git diff --name-only 1df7c343 origin/develop
internal/deployment/config_fail_loud_test.go
internal/deployment/target.go
```

Kein PR, kein Produkt-Commit. Arbeitsbaum der Lane: 0 Aenderungen (`git status --porcelain` = leer auf 1df7c343).

## Evidence-Pfad auf origin/main (vor END-Post, Mission 2026-11-05)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
6e27aad9f6fcbbebbc6dd0890705b9b182f710cd	refs/heads/main
$ git ls-tree origin/main evidence/r28-welle3-2026-11-16/hunt-signals/
100644 blob 47868841c2a1be20b3e232d635fbccdd416582cc	evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md
```

## Nachtrag: Disk-Lage (Fund, keine eigenmachtige Aenderung)

/tmp/opencode (tmpfs 13G) stand waehrend dieser Lane bei 80% (2.6G frei); eine Worktree-Anlage dort schlug mit "Disk quota exceeded" fehl, und ein mv-Versuch beschadigte einen Teilbaum. Lane-Worktree liegt daher unter `workers/.models/flash/wt/hunt-signals` (Legitimation: die dortigen Vorgaenger-Lanes nutzen genau diesen Pfad). Beschleunigend waere eine Aueraeumrunde der alten /tmp/opencode/w*-wt-Baeume (~2.8G) — Coordinator-Entscheidung, diese Lane hat nichts geloescht.

## Befund 1 — Die registrier-pfade sind ueber alle provider heterogen

Das Muster-Fund 097 (keycloak registrierte sein deklariertes metrik-Signal nie) war kein Einzelfall: die Signalregistrierung laeuft ueber DREI verschiedene, unkoordinierte Pfade mit vier verschiedenen ID-Formaten. Die Registry selbst ist dokumentarisch generisch (`internal/observability/registry.go:180 RegisterProviderSignals`, `:274 PruneOwnedProviderInstances`, `:318 UpdateSignal`, `:338 ReconcileSignals`, `:367 Remove`).

Quellen, Pfad, ID-Format, Ankernummer (develop@1df7c343):

- `internal/telemetry/realization.go:196` — OTel Collector — RegisterProviderSignals — ID `"opentelemetry-collector:"+Project` (`:178/:197`) — Scope immer Shared/PlatformProvider (`:199`)
- `internal/logs/realization.go:232` — Loki — RegisterProviderSignals — ID `"loki:"+placement.Project` (`:233`)
- `internal/traces/tempo.go:403` — Tempo — RegisterProviderSignals — ID `"tempo:"+p.Project` (`:404`)
- `internal/identityprovider/keycloak_realization.go:158` — Keycloak — RegisterProviderSignals — ID `"keycloak-metrics"` OHNE Project-Suffix (`:159`)
- `internal/application/runtime_observability.go:86` — PostgreSQL/Valkey — RegisterProviderSignals — ID `fmt.Sprintf("%s:%s:%s", provider, project, service)` (`:71`)
- `cmd/baha/app_broker.go:137` — Runtime Broker — ReconcileRuntimeComponentObservability (`internal/application/runtime_component_observability.go:29`, schreibt via `:168 ReconcileSignals`) — ID `"runtime-broker:"+brokerProject` (`:138`)
- `cmd/baha/app_broker.go:279` — Runtime Executor — ReconcileRuntimeComponentObservability — ID `"runtime-executor:"+executorFiles.Project` (`:280`)

Abweichungen (befundwuerdig, Muster wie 097):

- Befund 1a: Keycloak ist die EINE Quelle, die ihr metrik-Signal ohne Project-Kontext registriert (`"keycloak-metrics"`, `keycloak_realization.go:159`). Loki/Tempo/Collector haengen das Project an (`"loki:"+Project` usw.). Die Registry dedupliziert bei `RegisterProviderSignals` nach `(ID, Provider)` (`internal/observability/registry.go:244-249`). Bei zwei nebeneinander liveunden Keycloak-Instanzen auf einem Target (app-scoped + shared, oder app-A + app-B mit getrennten Grenzen) schreiben beide gegen dieselbe ID und entfernen sich gegenseitig; das `Remove` beim Destroy loescht zusaetzlich beide Registrierungen auf einmal (`registry.go:367`). Das ist ein anderer Lebenszyklus als bei allen anderen Providern.
- Befund 1b: Broker und Executor gehen den EINZIGEN ReconcileSignals-Pfad (`runtime_component_observability.go:168`) und sind damit die einzigen Provider mit `Enabled`-Semantik aus `runtime_observability.go`-Policy-Kombination; die Registry-Seite ist fuer sie identisch zu Provider-Signalen, aber der ID-Raum (`"runtime-broker:"+Project`) kollidiert nicht mit dem Provider-Namensschema `"%s:%s:%s"` (`runtime_observability.go:71`), das fuer postgres/valkey gilt (`postgresql:project:postgres`, `valkey:project:valkey`).
- Befund 1c: Der Scope der Registrierung haengt pro Quelle an verschiedenen Stellen ab: OTel hart auf Shared+Platform (`realization.go:199`), Loki/Tempo/Keycloak leiten Class aus `placement.Scope` ab (`logs/realization.go:211-214`, `traces/tempo.go:382-385`, `keycloak_realization.go:141-144`), Broker ist IMMER application-provider und Executor IMMER platform-provider-shared (`app_broker.go:140/:282`). Ein Konsistenztest ueber "quelle X hat scope Y" existiert nirgends — `internal/observability/registry.go` hat keine Provider-bezogene Validierung ueber Scope/Class-Kombinationen.
- Befund 1d: PostgreSQL/Valkey sind die einzigen Provider mit deklariertem, collectable-nahem metrik-Signal, das NIEMALS in die Registry geschrieben wird: `reconcileRuntimeProviderObservability` (`internal/application/runtime_observability.go:58-99`) bestueckt die `signals`-Map ausschliesslich mit `logs` (`:81`) und `traces` (`:84`) — das deklarierte `metrics`-Signal (`reference.go:35`, Status `RequiresAdapter`, damit per `integration_contract.go:73-75` nicht collectable) fehlt in der Map vollstaendig. Das ist in sich konsistent (nicht-collectable-Signale duerfen nicht registriert werden, `registry.go:203-207` weist sie sonst zurueck) — aber die Adapter-Seite (postgres-exporter/valkey-exporter) existiert im develop-Stand nirgends (kein Code, kein compose-Dienst, `git grep -iln exporter origin/develop` = nur Coreless/Otel-Teststellen), und die `RequiresAdapter`-Deklaration hat KEINEN getrackten Folgeauftrag: kein Task, keine Karte, kein Hinweis im Code auf eine Exporter-Lane. Der Zustand ist also kein Regressions-Fund, sondern eine dokumentationswuerdige Dauerluecke mit 097-Anschluss: eine capability-first-Deklaration ohne Registrierung UND ohne Plan.

## Befund 2 — Provider-metrik-Signale sind netzseitig korrekt, aber die application-Klasse fehlt im Konsumenten komplett

`SignalSource.Validate` verlangt fuer metrics ein Netzwerk (`registry.go:97-101` "observability metrics source requires network and absolute path"), und die Provider-Setzer liefern es: Loki `internal/logs/realization.go:225-230` (`placement.Network` aus `internal/logs/state.go:85/:92`), Tempo `internal/traces/tempo.go:398-401` (`p.Network` aus `internal/traces/tempo.go:166/:172`), OTel `internal/telemetry/realization.go:189-194`, Keycloak `internal/identityprovider/keycloak_realization.go:151-156` (`r.files.ConsumerNetwork`), Broker/Executor `cmd/baha/app_broker.go:142-143/:283` — und Prometheus haengt diese Netze auch korrekt in seine Compose-Realisierung (`internal/metrics/prometheus_files.go:249 providerMetricNetworks` -> `internal/metrics/prometheus_render.go:72/:143-145/:167-170`, als `external: true`). Die provider-Klasse ist netzseitig korrekt realisiert. Die Luecke sitzt eine Ebene hoeher, im Konsumenten:

- `observability.List` (`internal/observability/registry.go:399-405`) UEBERGEHT class==application bedingungslos (`case SourceApplication: continue`) und filtert application-/platform-provider-Quellen nach den Flags `includeApplicationProviders`/`includePlatformProviders`.
- Die application-Klasse schreibt NIEMAND in die Registry: Application-Metrik-Targets (`cmd/baha/app_metrics.go:120-143` -> `internal/metrics/prometheus.go:315 -> realization.RegisterTarget`, `internal/metrics/realization.go:132-146`) erzeugen nur file_sd-Dateien (`targetFileName`, job `baseharbor-applications`), nie einen `SignalSource`. Der einzige Registry-Writer mit application-Class ist das Test-Setup (`internal/observability/registry_test.go:116`).
- Folge fuer `VerifyProviderSources` (`internal/metrics/prometheus_verify.go:137-150`): der Poll prueft NUR die (provider-)Quellen aus der Registry. Ein Deployment mit ausschliesslich workload-/application-Metrikquellen hat `len(sources)==0` (`:149`) und die Funktion gibt `nil` — die Metrikpfad-Verifizierung ist in der Realitaets-Haeufigkeit EINER application-only-App ein No-op, obwohl ueber file_sd echte Targets gestreift werden. Genau derselbe Class-Filter haengt an `runtime_retirement.go:56` und den Prometheus-render-Reads (`prometheus_files.go:234/:445`).
- Das Erklaerungsmuster von 097 ("registriert, aber der Konsument sieht es nicht") kehrt sich hier um: die application-Quellen sind korrekte scrape-targets, aber in der Registry nicht registriert — und die Perses-Witnesses (Karten 078/080/082) lesen ausschliesslich die Registry. Was dort als missing-signal erscheint, ist bei application-Metriken systematisch, nicht quellenbezogen.

Anker: `internal/observability/registry.go:399-405`, `cmd/baha/app_metrics.go:120-143`, `internal/metrics/realization.go:132-146`, `internal/metrics/prometheus_verify.go:137-150`.

## Befund 3 — Loeschastronomie: drei Quellen ohne Registry-Cleanup im Destroy

Registry-Eintraege werden beim Destroy nicht ueberall entfernt; die ID-Formate der Remove-Aufrufe passen nicht ueberall zu den Registrierungs-IDs:

- `Remove` existiert genau 4x: `internal/logs/lifecycle.go:172` (`"loki:"+p.Project` — passt zu `logs/realization.go:233`), `internal/traces/tempo.go:458` und `:490` (`"tempo:"+Project` — passt zu `traces/tempo.go:404`), `internal/telemetry/otlp.go:525` (`"opentelemetry-collector:"+files.Project` — passt zu `telemetry/realization.go:178/:197`).
- Keycloak hat KEIN `observability.Remove` — weder in `keycloak_realization.go:190-213` (`localKeycloakRealization.Destroy`, nur `lifecycle.Destroy`+`RemoveAll`) noch in `keycloak_files.go:382-408` (`DestroyAllSharedKeycloakAt`, looped nur `DestroyProject`, kein Remove) noch in `cmd/baha/runtime_destroy_all.go:457`. Da die ID project-unabhaengig ist (Befund 1a), koennte ein Destroy nicht mal korrekt aufraeumen, ohne die jeweils andere live-Registration zu loeschen.
- Runtime Broker/Executor: die Registry-Eintraege `"runtime-broker:"+project` (`cmd/baha/app_broker.go:138`) und `"runtime-executor:"+project` (`:280`) werden beim Destroy niemals entfernt — `ReconcileRuntimeComponentObservability` (`internal/application/runtime_component_observability.go:168`) laeuft nur in den Ensure-Pfaden (`app_broker.go:137/:279`); weder `runtimeexecutor.DestroySharedAt` (`internal/runtimeexecutor/compose.go:232-247`) noch der Broker-Retirement-Pfad (`cmd/baha/runtime_destroy_all.go:367`) toucht die Registry. Die Eintraege verbleiben dauerhaft (gilt auch fuer app-Umbenennung/Env-Wechsel, weil die ID am Project haengt).
- PostgreSQL/Valkey: app-scoped faellt unter `PruneOwnedProviderInstances` (`internal/application/runtime_observability.go:98`, nur aus `reconcileRuntimeProviderObservability` beim Runtime-Ensure, aufgerufen `internal/application/runtime_postgres.go:131`). Die Shared-Backends (`internal/application/shared_backends_resources_runtime.go:367-400`, aufgerufen `cmd/baha/runtime_destroy_all.go:459`) haben KEIN Registry-Cleanup — wenn eine app von shared auf managed (oder umgekehrt) wechselt, bleibt der fruehere Registrationstyp (shared postgres hat keine app-`PruneOwnedProviderInstances`-Kategorie, da `Class=platform` nie geschrieben wird) potenziell als Source mit `Scope=application/Class=application-provider` verwaist; der Prune filtert nur `(provider, class, scope, owner)`-Tupel, die sein Ensure-Pfad selbst geschrieben hat.

Konsequenz: ein Target, das mehrfach deploy/destroy-Zyklen durchlaufen hat, traegt stale Signal-Sources, die `observability.ListMetrics` (`prometheus_files.go:234`/`:445`, `prometheus_verify.go:137`) als scrape-Ziele materialisieren — Prometheus kriegt tote targets (up=0), `VerifyProviderSources` kann zeitweise failen, und Perses-Witnesses (Karten 078/080/082) sehen Signale, fuer die kein Backend mehr existiert.

## Befund 4 — (b) alert-/signal-rule-Registrierung existiert im develop-Stand ueberhaupt nicht

Quer ueber develop@1df7c343 existiert keine alert-/rule-Registrierung fuer KEINE Quelle (Muster-Fund 097 verallgemeinert, in die andere Richtung):

```
$ git grep -inE "alertmanager|alert_rule|alerting" origin/develop -- '*.go' '*.yaml' '*.json'
(nur tls.AlertError-Teststellen: internal/runtimeexecutor/client_test.go; renovate.json; keine Produktstellen)
$ git grep -i "perses" origin/develop
origin/develop:internal/identityprovider/keycloak_realization.go:127   (nur Kommentar, kein Code)
$ git ls-tree -r --name-only origin/develop | grep -iE "alert"
(keine Datei)
```

Spezifikation schliesst Alerting explizit aus: `spec/capabilities/metrics/v1.md:48` ("does not imply ... alert routing", "Prometheus-specific recording or alerting rules"). Alert-Kontrakt-Code existiert ausschliesslich auf UNMERGED Kandidaten-Branches: `w073-perses-alerts` (`internal/metrics/perses_prometheus_alerts.go`, fail-closed, PR #—; `BuildPersesAlertEvaluator` `:121`), `lane-0428-075-perses-seam`, `lane-0428-077/080/082/085/086/088/089-r28-perses-*` (alle `develop-contains: NO`, ls-remote/merge-base-Zeugen siehe oben). Fuer den develop-Stand ist die Frage "(b) existiert die alert-/signal-rule-Registrierung?" fuer alle acht Quellen mit NEIN zu beantworten — und zwar nicht als Quelle-Einzelbefund, sondern weil die alert-Ebene des Systems fehlt. Das ist der groesste gemeinsame Nenner von 097: ein deklariertes/angepeiltes Signal ohne Registrierung. Die Kartenkette 073 (alerts) haengt an derselben Luecke, die der 097-Fund fuer metrics gezeigt hat.

## Befund 5 — k8s-core und "worker": im develop-Stand nicht vorhanden; "perses" nur als Plan

- "worker" (workload/application-Metrikquellen): siehe Befund 2 — die Quellen existieren als file_sd-Targets (`cmd/baha/app_metrics.go:120-143`, `internal/metrics/realization.go:132-146`), aber nie als Registry-`SignalSource`; die `List`-Funktion verwirft class==application sogar explizit (`internal/observability/registry.go:399-405`). Systematische Luecke derselben Klasse wie 097 ("Signal vorhanden, aber nirgends gelistet").
- "k8s-core": Der Kubernetes-Runtime-Provider ist deklariert (`internal/runtime/contract/api.go:18 ProviderKubernetes`), aber in develop NICHT implementiert (`internal/runtime/resolver/resolver_test.go:29-32` belegt "kein Provider"). `internal/repositoryinspect/workload_source_kubernetes.go` ist Quellen-Erkennung, keine Registrierung. Eine Signallandschaft "k8s-core" existiert nicht; nichts zu registrieren, nichts zu pruefen.
- "perses": auf develop nur als Kartenplan (075/077/080/082/085/086/088/089, alle UNMERGED). Perses hat KEINEN provider-Descriptor und schreibt selbst nichts in die Registry (`internal/capability/reference.go` ohne Perses-Eintrag; die Perses-Codepfade existieren nur auf den Kandidaten-Branches, `git grep -l perses origin/develop` = ein Kommentar in `keycloak_realization.go:127`). Sobald 082 merged, liest Perses ueber die Registry (`observability.List`); dann greifen Befund 1 (ID-Raum/Keycloak-Kollision), Befund 2 (application-Klasse fehlt) und Befund 3 (stale sources) direkt als Dashboard-Luecken.

## Karte der Quellen (Tabelle)

| Quelle | metrics registriert? | alert-/rule-Registriert (develop)? | registry-Remove? | Anker |
| --- | --- | --- | --- | --- |
| postgres | nein (nur logs+traces; metrics deklariert "requires-adapter", kein Exporter, kein Plan) | nein | app-scoped Prune (`:98`); shared: keiner | `reference.go:35`, `runtime_observability.go:71/81/84/86/98` |
| redis/valkey | nein (wie postgres) | nein | wie postgres | `reference.go:48`, `runtime_observability.go:55` |
| loki | ja (`realization.go:227`) | nein | ja (`lifecycle.go:172`) | `reference.go:132`, `realization.go:225-233` |
| tempo | ja (`tempo.go:400`) | nein | ja (`tempo.go:458/490`) | `reference.go:146`, `tempo.go:398-404` |
| otel-collector | ja (`realization.go:191`) | nein | ja (`otlp.go:525`) | `reference.go:104`, `realization.go:178/196` |
| keycloak | ja (`keycloak_realization.go:153`, Fix 097) | nein | KEINER | `reference.go:160`, `keycloak_realization.go:158-167` |
| runtime-broker | ja (`app_broker.go:144`) | nein | KEINER | `app_broker.go:137-158` |
| runtime-executor | ja (`app_broker.go:285`) | nein | KEINER (`compose.go:232-247`) | `app_broker.go:279-299` |
| application-workload ("worker") | NICHT in Registry (nur file_sd) | nein | keine | `app_metrics.go:120-143`, `registry.go:399-405` |
| caddy / openbao / seaweedfs / mongodb / rabbitmq / external-oidc / external-otlp | nein (deklariert unsupported oder kein Observability-Block, `reference.go:62/76/90`; mongodb/rabbitmq/external-* ohne Observability-Feld) | nein | keine | `reference.go` je Descriptor |
| k8s-core | Provider nicht implementiert | — | — | `contract/api.go:18` |
| perses | kein Provider-Descriptor (nur Kartenplan) | — | — | siehe Befund 5 |

## Sauberkeit / Teardown

- Vorher (dieser Host, lokal, docker): `docker ps -a --format '{{.Names}}\t{{.State}}'` = leer; `docker network ls` = bridge/host/none nur; `docker compose ls -a` = keine Projekte. Diese Lane hat KEINE container/netzwerke/volumes angelegt (keine deployment-, keine compose-Aufrufe; reine Lese-/git-/build-Arbeit).
- Nachher: identisch (siehe END-Akte; `docker ps -a` erneut geleert).
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient containers untouched.
- Worktree-Hinterlassenschaft: Lane-Worktree unter `workers/.models/flash/wt/hunt-signals` (detached + 1 Lane-Lokalanzeige branch `hunt-signals/develop-1df7c343`, NICHT gepusht; kein remote branch angelegt); aufraeumen auf Coordinator-Anweisung (`git worktree remove`), da `/tmp/opencode` tmpfs zur Laufzeit quota-limitiert war (Finding: /tmp ist 80% voll, 2.6G frei — mehrere alte Lane-Worktrees belegen es; kein Eingriff durch diese Lane).

## Befund-Nachlieferung / Kartenwuerdigung (Fund→Karte-Pflicht, Coordinator)

- F1 (ID-Format-Keycloak, Reconcile-Pfad-Heterogenitaet) — Vorschlagkarte: "observability signal-ID-Raum vereinheitlichen (project-suffix vs. flat), Registry-Kollisionstest"
- F2 (application-Klasse fehlt in Registry, `List` verwirft class==application; Perses-Witnesses blind fuer workload-Metriken) — Vorschlagkarte: "observability signal registry: application-class sources (metrics/v1 workload) listen + Verifizierung"
- F1d (postgres/valkey `RequiresAdapter` ohne Exporter und ohne Karte) — Vorschlagkarte: "postgres-exporter/valkey-exporter Lane eroedern oder RequiresAdapter-Deklaration dokumentieren"
- F3 (stale signals nach destroy: keycloak/broker/executor/shared-backends) — Vorschlagkarte: "signal-Registry-Cleanup in destroy-/retirement-Pfaden"
- F4 (alert-Rule-Ebene fehlt im develop vollstaendig; nur unmerged perses-alerts-Kandidaten) — haengt an den bestehenden Karten 073/075/080/082, keine neue Karte noetig, aber develop-Fehlstellendokumentation
- F5 (application-Klasse nie in Registry) — Vorschlagkarte: "metrics/v1 application source vs. signal registry (ListMetric filtert class=application)"

## END

END_DONE mission-hunt-signals.md — Signallandschaft develop@1df7c343 (=origin/develop-Kopf 8db0d9bdf, signalseitig identisch) querschnitten: 5 Befunde (registrierpfad-/ID-Raum-Heterogenitaet inkl. Keycloak-Kollision; application-Klasse fehlt in Registry und damit in jedem Konsumenten;postgres/valkey-Adapter ohne Plan; 3 Quellen ohne Registry-Cleanup im Destroy; alert-/rule-Ebene fehlt develop-weit), Akte in baseharbor-plan origin/main, kein Produkt-Commit, keine container/netze angelegt.