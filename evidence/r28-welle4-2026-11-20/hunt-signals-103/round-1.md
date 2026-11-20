# BUG-HUNT mission-hunt-signals-103 — PostgreSQL/Valkey metrics adapter ohne Plan (reine Befundung)

- Mission: `/var/tmp/mission-hunt-103.md`
- Rolle: WORKER (Bug-Hunt, keine Produktaenderung, keine Commits im Produkt, kein PR)
- Datum: 2026-11-20
- Karte: `t-20261117-hunt-signals-103` (0428-103) — „postgres-/valkey-Adapter ohne Plan"
- Abtafung: reine Befundung nach AGENTS §3.3.5 hunt-fuellregel + §5.3; KEIN Produktcode, KEIN Test, KEIN .github/**, KEIN Planning-Board
- Produktbasis (develop, real via `git ls-remote origin refs/heads/develop`): `96f2ae11a25a508998c44a9854ef17f8fa15c112`

## PLAN

1. Realitaetsabgleich: planning-repo remote verifizieren (baseharbor-plan -> github mcpdev80), develop-HEAD ls-remote, lesereferenz per `git show origin/develop:<pfad>` (kein Produkt-Checkout/Worktree)
2. Vertrag lesen (`plan.py show`), beweisbasis (befund-1.md), dep-risk-103-104, vor-akten der CLOSED karten 101/102 lesen
3. Bestandsaufnahme postgres/valkey metrik-pfad: capability/reference.go (RequiresAdapter), integration_contract.go (Collectable() + non-collection rule), runtime_observability.go (reconcileRuntimeProviderObservability)
4. Check exporter/adapter: `git grep` exporter/exporter/compose in deploy/assets; keine compose-quelle, kein compose-dienst
5. Check perses-dashboard-seam: perses_dashboards_valkey.go + perses_selection.go (verifiziert, dass postgres/valkey als unavailable deklariert sind, kein fabricated panel)
6. Check destroy-cleanup: app-scoped PruneOwnedProviderInstances vs shared_backends (kein registry-cleanup)
7. Befund in evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md (baseharbor-plan main) schreiben; commit; origin/main-verifizierung; END-post

## Zone- und Basis-Zeugen

Planning-repo verifiziert (wrong-zone check, Mission 2026-11-07):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Produkt-basis (develop, real remote `origin`, URL github.com/mcpdev80/baseharbor.git; NUR dieser remote-name wird genutzt, `git remote -v` als erste git-action verifiziert):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor remote -v
origin	git@github.com:mcpdev80/baseharbor.git (fetch)
origin	git@github.com:mcpdev80/baseharbor.git (push)
$ git ls-remote origin refs/heads/develop
96f2ae11a25a508998c44a9854ef17f8fa15c112	refs/heads/develop
```

Lesereferenz ohne produkt-checkout/checkout-chaos: `git show origin/develop:<pfad>` (bestaetigt, exit 0). Der quarentaene stale-ref checkout `workers/baseharbor` stand auf `lane-0428-094-config-fail@4f2906c6` (VERALTET); remote-HEAD `96f2ae11` wird ausschliesslich via ls-remote/zurückgezogener ref gelesen. Kein Worktree angelegt, kein Produkt-Commit, kein remote-branch.

origin/main HEAD bei beginn: `34a52c98926d6d8ec837b77344ce2125f8b16cf9`; origin/main HEAD vor END-post: `ea5e7417133eba5b9a4935b400d235caaa5fa23d` (plan-evidence nur).

## Evidence-pfad auf origin/main (vor END-post, Mission 2026-11-05)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree origin/main evidence/r28-welle4-2026-11-20/hunt-signals-103/
(tree: kein eintrag; verzeichnis noch NICHT auf origin/main)
```

Der pfad ist neu; wird mit dem einzigen evidence-commit angelegt. (Bezug: vor-end-verifizierung unten.)

## Funde

### F1 — postgres/valkey metrics sind im develop-Stand NIE collectable; der Adapterpfad existiert nicht

Anker: `internal/capability/reference.go:35` / `:48`, `integration_contract.go:73`, `runtime_observability.go:101`(application, NICHT provider).

- postgres (`baseharbor/postgresql`) und valkey (`baseharbor/valkey`) deklariern ihr metrics-signal als `Status: ObservabilityRequiresAdapter`, `Mode: ObservabilityAdapter`, `Verification: ObservabilityVerifyNone`, `Protocol: openmetrics` (`reference.go:35` / `:48`).
- `ProviderObservabilitySignal.Collectable()` (`integration_contract.go:73`) gibt NUR `true` bei `Status == ObservabilitySupported`. RequiresAdapter => `Collectable()==false` => das signal ist per vertrag NICHT collectable.
- Die integration_contract validierung (`integration_contract.go:243-249`) FORCERT sogar die deklaration: `signal.Status == ObservabilityRequiresAdapter` REIET `Mode != ObservabilityAdapter && != ObservabilityCombined` als fehler — es gibt also keine erlaubte native sammlung, nur den adapter-feld-pfad.
- Der runtime-pfad schreibt KEIN metrics-signal: `reconcileRuntimeProviderObservability` (`runtime_observability.go:229-269`) bestueckt die signals-map ausschliesslich mit `logs` (`:251`) und `traces` (`:254`). Die einzige `SignalMetrics`-schreibung im file (`:101`) ist `reconcileApplicationMetricsSource` — das ist das workload/prometheus-signal, NICHT der postgres/valkey-provider.
- Kein exporter, kein compose-dienst, kein scrape-pfad in deploy/assets (`git grep exporter|openmetrics|scrape /metrics deploy/** assets/**` = leer; nur application-endpoint-doku `cmd/baha/app_init_summary.go:205`). Der adapter-feld-pfad (postgres-exporter/valkey-exporter) ist im develop-Stand ein leerer namensraum — kein code, kein dienst, kein plan.

Was geschieht im fehlerfall beim nutzer: Eine capability-app mit postgres/valkey hat ein deklariertes metrics-signal (`openmetrics`/`/metrics`), das die registry nie als collectable annimmt und das kein backend abfragt. In Perses (`observability.List`) erscheint die quelle als missing-signal; der prometheus-poll (`VerifyProviderSources`) prueft keinen postgres/valkey-backend. Das ist kein funktionsbruch (DB funktioniert), sondern die in v0.4.28 angepeilte DB-/Valkey-metrik ist undefiniert: es gibt kein collectables signal, keinen exporter, kein dashboard.

### F2 — new (round-1): Die DB-/Valkey-Perses-dashboards existieren, aber ausschliesslich als „unavailable" — der Adapter bleibt eine dokumentierte Luecke statt eines fehlenden features

Anker: `internal/metrics/perses_dashboards_valkey.go:187/195/226/265`, `internal/capability/perses_selection.go:235/319`, `perses_selection_test.go:41-44`.

- **Neu in round-1:** `internal/metrics/perses_dashboards_valkey.go` existiert in develop. Es ist eine standalone-metrik, die PER Kontrakt NICHTs fabriciert:
  - `persesValkeyUnavailableReason` (`:187`): „Valkey has no native metrics signal in BaseHarbor (observability status RequiresAdapter); the dashboard is explicitly unavailable and no exporter is installed".
  - `persesValkeyDashboardCatalog()` (`:195`) liefert exakt einen eintrag mit `Unavailable: true` und diesem `Reason` — kein `panels`-objekt, kein panel.
  - `persesValkeyPanelJSON()` (`:226`) marshallt fuer `entry.Unavailable` den resource-kind `DashboardUnavailable` (`PersesValkeyUnavailableKind`, `:51`) — kein panel-json.
  - `PersesValkeyDashboardAvailability()` (`:265`) liefert den verdict `PersesValkeyDashboardUnavailable = "unavailable"` (`:298`).
- **PostgreSQL:** `internal/metrics/perses_dashboards.go` (das #1597-inventory) ist in develop NICHT vorhanden; postgres wird in der valkey-datei nur als `postgresql-targets`-referenz genannt (`:21/40`). Die karte `postgres-targets`/`postgresql-targets` hat KEINEN dashboard-catalog-eintrag. `perses_selection_test.go:43-44` TESTET ausdrucklich, dass `"postgresql-targets"` NICHT im catalog erscheint: „postgresql has requires-adapter (no native signal); no template may exist".
- `perses_selection.go:235/319` dokumentiert die regel: exporters ohne natives signal (postgres/valkey requires-adapter) sind absent und duerfen nie provisioniert werden.

Was geschieht im fehlerfall beim nutzer: Die DB-/Valkey-metriken werden in Perses als `DashboardUnavailable` deklariert (kein empty panel, kein falscher scrape-target) — also ehrlich als „nicht verfuegbar", nicht als defizit. Das bestaetigt Befund 1: der zustand ist eine bewusst dokumentierte `RequiresAdapter`-defizit, NICHT eine regressed-funktion. Die karte 103 benennt genau diese defizit als „ohne Plan": dashboard-existenz ja, adapter-existenz (exporter/collectablesignal) nein.

### F3 — destroy-cleanup: app-scoped postgres/valkey wird bereinigt, shared-backends NICHT (Registry-Eintraege verbleiben)

Anker: `internal/application/runtime_observability.go:269`, `registry.go:319`, `shared_backends_resources_runtime.go:384/392/399`.

- App-scoped postgres/valkey: `reconcileRuntimeProviderObservability` ruft beim ensure `PruneOwnedProviderInstances(provider, SourceApplicationProvider, ScopeApplication, m.Name, keep)` (`:269`). Das ist der bereits funktionierende app-scoped cleanup (aus der vorherigen karte befrundet, hier bestaetigt).
- Shared backends (shared-postgreSQL / shared-valkey): der shared-destroy laeuft ueber `shared_backends_resources_runtime.go:384` (`compose.DestroyProjectRemoveOrphans`) + `:392/:399` (`os.RemoveAll`) — KEIN `observability.*`-aufruf, kein registry-cleanup. Ein wechsel von app->shared (oder shared->app) hinterlaesst registry-eintraege des vorherigen typs (shared-postgreSQL hat keine app-`PruneOwnedProviderInstances`-kategorie, da `Scope=platform` nie geschrieben wird).
- Hinweis: das metrics-signal ist fuer postgres/valkey ohnehin non-existent (F1), also bleibt hier fuer metrics nichts verwaisten; die `logs`/`traces`-eintraege des app-scoped providers werden ueber Prune bereinigt. Der shared-pfad ohne cleanup betrifft primaer die provider-log/trace-signalen von shared-backends (fortfuehrung der befund-1.md aus befund 3, hier auf shared-/app-grenze praezisiert).

Was geschieht im fehlerfall beim nutzer: Ein target mit shared-valkey/shared-postgreSQL, das spaeter auf app-scoped umstellt (oder umgekehrt), haengt registry-signalen der alten grenze nach — perses/poll koennen ein signal materialisieren, fuer das kein backend mehr existiert.

## Befundlos (ausdrucklich belegt)

Die mission verlangt quelle/pfad/fehlverhalten mit zeugen fuer die pruefgebiete; hier der befund „kein produkt-defekt in X":

- **alert-/signal-rule-registrierung (befund 4 der befund-1.md):** unveraendert im develop-Stand — keine alert-/rule-registrierung fuer postgres/valkey oder andre quellen (`git grep alertmanager|alert_rule|alerting` = nur tls.alerterror-teststellen; `spec/capabilities/metrics/v1.md:48` schliesst alerting aus). Kein neuer befund; die defizit ist system-level (fehlende alert-ebene), keine neue karte noetig (an karte 073/075/080/082).
- **k8s-core / perses als provider:** unveraendert — k8s-provider nicht implementiert, perses auf develop nur als kartenplan. Kein neuer befund.
- **application-workload-signal:** unveraendert (`reconcileApplicationMetricsSource` schreibt workload-metrics ueber prometheus; `observability.List` filtert class==application). Kein neuer defizit.

## repo-rule compliance

- KEIN produktcode geaendert. KEIN test geaendert. KEIN .github/** geaendert (owner-scope). KEIN planning-board geaendert. KEIN offener PR.
- KEIN produkt-checkout/checkout-change: alle produkt-lesungen liefen ueber `git show origin/develop:<pfad>` gegen den realen develop-HEAD. Kein worktree angelegt (tmpfs-chaos vermieden), kein remote-branch, kein produkt-commit.
- KEINE subagenten (§4.8). KEINE sleep-/wait-blöcke. Kein `git add -A`.
- Nur evidence in baseharbor-plan (kein .evidence/ im produkt, kein main-branch-write im produkt).
- Realitaets-zeugen ausschliesslich via `git ls-remote`/zurueckgezogener ref; der quarentaene stale-ref checkout `workers/baseharbor` (stand `4f2906c6`, lane `lane-0428-094-config-fail`) wurde NICHT als zeuge genutzt.

## cleanliness (container/netzwerke/volumes/state-verzeichnisse)

- Vorher: `docker ps -a --format '{{.Names}}\t{{.State}}'` = leer; `docker network ls` = bridge/host/none; `docker compose ls -a` = keine projekte.
- Nachher: identisch (dieser task startete KEINE container/netzwerke/volumes/state-dirs; reine les-/git-/build-arbeit, keine deployment-/compose-aufrufe).
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet.

## FUND -> KARTE (Coordinator)

- F1 (postgres/valkey metrics never collectable, adapter-pfad existiert nicht) — `FUND-FUER-KARTE: postgres/valkey metrics adapter ohne Plan | reference.go:35/:48, integration_contract.go:73/243, runtime_observability.go:229-269 | deklariertes openmetrics-signal ohne collectables-backend/exporter/dashboard; DB-/Valkey-metriken in v0.4.28 undefiniert`
- F2 (DB/Valkey-perses-dashboards nur als DashboardUnavailable, postgres ohne catalog-eintrag) — `FUND-FUER-KARTE: DB/Valkey-Perses-dashboards nur als unavailable deklariert | perses_dashboards_valkey.go:187/195/226/265, perses_selection.go:235/319 | adapter-existenz (exporter/collectablesignal) fehlt; dashboard-existenz ja, defizit bewusst dokumentiert — deckt defizit der karte 103 ab statt defizit-funktion`
- F3 (shared-backends destroy ohne registry-cleanup) — `FUND-FUER-KARTE: shared-postgres/valkey destroy haengt registry-signalen an | shared_backends_resources_runtime.go:384/392/399 | app->shared/wechsel hinterlaesst verwaiste registry-signalen`

## END

END_DONE mission-hunt-signals-103.md — postgres/valkey metrics adapter ohne plan (0428-103) querschnitten: F1 metrics nie collectable (RequiresAdapter => Collectable()==false, runtime schreibt kein provider-metrics-signal, kein exporter/compose/srape), F2 NEW DB/Valkey-perses-dashboards nur als DashboardUnavailable (valkey:187/195/226/265; postgres: kein catalog-eintrag, testet `perses_selection_test.go:41-44`), F3 shared-backends destroy ohne registry-cleanup; alert-/rule-ebene undefiniert (befundlos, karte 073/075/080/082); basis develop@96f2ae11 (ls-remote), evidence in baseharbor-plan origin/main, KEIN produkt-commit, keine container/netze angelegt.
