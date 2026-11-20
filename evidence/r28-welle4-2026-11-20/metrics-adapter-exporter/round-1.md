# 0428-182 — adapter without exporter (metrics source has no producer)

- Mission: `/var/tmp/mission-182.md`
- Rolle: WORKER (produkt-implementation, kein coordinator)
- Datum: 2026-11-20
- Karte: `t-20261120-r28-metrics-adapter-without-exporter` (0428-182) — „adapter without exporter"
- Release: v0.4.28
- Owner: w182-0428-182-metricsadapter (card), lane owner: this session
- Basis develop (real via `git ls-remote origin refs/heads/develop`): `96f2ae11a25a508998c44a9854ef17f8fa15c112`

## PLAN

1. Realitaetsabgleich: planning-repo remote verifizieren, develop-HEAD ls-remote, lesereferenz via `git show origin/develop:<pfad>` (kein produkt-checkout); worktree vom realen develop-HEAD in `/tmp/opencode/lane-0428-182-metrics-wt`.
2. `git grep -n RequiresAdapter` + compose/service-pfad der wert liefern muesste; in die akte die gewaehlte zeile (adapter verdrahten ODER RequiresAdapter entfernen) und WARUM, mit datei:zeile.
3. Fix implementieren: `RequiresAdapter` -> `Unsupported` fuer postgres + valkey metrics mit dokumentiertem code-kommentar in `internal/capability/reference.go` (die metrik ist strukturell nicht sammelbar; kein exporter, kein compose-dienst, runtime schreibt kein provider-metrics-signal).
4. Fail-closed regression: test der ROT wird, wenn eine `RequiresAdapter`-metrics-quelle ohne producer existiert (integration_contract_test).
5. Lokal pruefen: gofmt, readability, `go test`/`go vet`/`go build`; ein letzter commit; gofmt/readability leer.
6. Branch provenance: `git ls-remote` branch = `refs/pull/<n>/head`, `git merge-base --is-ancestor origin/develop HEAD`, `git diff origin/develop...HEAD --name-only`, `git log --oneline origin/develop..HEAD` nur eigene commits.
7. PR (base develop) + CI; job (packages-shard) benennen; run-id + CONCLUSION TERMINAL am exakten head.
8. Evidence auf baseharbor-plan origin/main; origin/main-verifizierung; container/compose DOWN; END-post.

## Zone- und Basis-Zeugen

Planning-repo verifiziert (wrong-zone check):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Produkt-remote verifiziert (FIRST git action, remote-guard: NUR `origin` mit github.com/mcpdev80, hier korrekt):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor remote -v
origin	git@github.com:mcpdev80/baseharbor.git (fetch)
origin	git@github.com:mcpdev80/baseharbor.git (push)
```

Produkt-basis (develop, real remote `origin`, URL github.com/mcpdev80/baseharbor.git; NUR dieser remote-name):

```
$ git ls-remote origin refs/heads/develop
96f2ae11a25a508998c44a9854ef17f8fa15c112	refs/heads/develop
```

Quarentaene stale-ref checkout `workers/baseharbor` stand auf `4f2906c6` (lane `lane-0428-094-config-fail`), UNVERALTET; NICHT als zeuge genutzt. Kein produkt-checkout: alle produkt-lesungen liefen ueber `git show origin/develop:<pfad>`. Worktree vom realen develop-HEAD:

```
$ git -C /tmp/opencode/lane-0428-182-metrics-wt log -1 --oneline
96f2ae11 fix(0428-166): fail-closed on Keycloak signal-id normalization collision (#1712)
```

## Fund / Entscheidung

Anker: `internal/capability/reference.go:35`, `:48` (postgres + valkey metrics `Status: ObservabilityRequiresAdapter`), `integration_contract.go:73` (`Collectable()` nur bei `Supported`), `integration_contract.go:249` (validierung FORCERT adapter-realisierung fuer `RequiresAdapter`), `runtime_observability.go:229-269` (runtime schreibt NUR `logs`/`traces`, kein provider-metrics-signal), `internal/metrics/perses_dashboards_valkey.go:186` (valkey dashboard ist bewusst UNAVAILABLE, kein panel, kein exporter).

Gewaehlte zeile: **RequiresAdapter entfernen -> Unsupported** (nicht verdrahten).

WARUM (datei:zeile-gebunden):

- `reference.go:35` (postgres metrics) und `reference.go:48` (valkey metrics) deklariern `Status: ObservabilityRequiresAdapter, Mode: ObservabilityAdapter, Protocol: "openmetrics"`.
- Der adapter-feld-pfad ist im develop-Stand ein leerer namensraum: kein exporter, kein compose-dienst, kein scrape-pfad (`git grep exporter|openmetrics|/metrics|scrape deploy/** perses_dashboards.go` = leer; `perses_dashboards.go` existiert in develop ueberhaupt nicht — postgres hat keinen dashboard-catalog-eintrag).
- `integration_contract.go:249` FORCERT fuer `RequiresAdapter` zwingend `Mode == Adapter || Combined` — also eine realisierte adapter-realisierung. Derzeit existiert keine, also ist die deklaration eine versprechen ohne erfuellung: die metrik ist per vertrag NICHT collectable (`Collectable()==false`) und wird von keinem backend abgefragt.
- Der adapter zu verdrahten (exporter + compose-dienst + runtime-reconcile + dashboard) waere der inhalt von #1684 (0428-083), #1645 (0428-091) und 0428-183/184 — alle ausdrucklich verschlossen. Die valkey-dashboards liegen im selben paket `internal/metrics` wie die verschlossene `perses_prometheus_datasource.go`/`perses_datasource_lifecycle.go` (#1684) — dieselbe write-set. Ein verdrahten waere also ein doppelschreiber in eine verschlossene datei.
- Die ehrliche, fail-closed-loesung ist die deklaration zu korrigieren: `RequiresAdapter` -> `Unsupported` mit dokumentiertem comment, dass eine metrics-metrik ohne nativen signal und exporter nicht als adapter-required deklariert werden darf, sondern als unsupported. Das laesst `Collectable()==false` ueber den supported-pfad gueltig (kein adapter-feld-pfad versprochen) und macht die metrik-struktur ehrlich.

## repo-rule compliance

- Write-set disjunkt gewaehlt: NUR `internal/capability/reference.go` (deklaration) + `internal/capability/integration_contract_test.go` (regression). KEIN `internal/metrics/**` (verschlossen, #1684), KEIN `internal/application/perses_runtime.go` (#1684), KEIN `internal/capability/perses.go` (#1645), KEIN `internal/metrics/valkey.go` (0428-183), KEIN `internal/observability/**` (0428-184).
- KEIN `.github/**` geaendert (owner-scope). KEIN produkt-checkout als zeuge (quarentaener stale-ref `4f2906c6` nicht genutzt). KEIN subagent (§4.8). KEIN `git add -A`. KEIN merge, KEIN force-push.
- Branch aus develop-spitze `96f2ae11` (attestiert unten). EIN letzter commit.
- container/compose: kein stack gestartet (reine go-build/test/git-arbeit). cleanliness unten.

## cleanliness

- Vorher: `docker ps -a --format '{{.Names}}\t{{.State}}'` = leer; `docker compose ls -a` = keine projekte.
- Nachher: identisch (dieser task startete KEINE container/netzwerke/volumes/state-dirs; go-build/test/git, keine deployment-/compose-aufrufe).
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet.

## CI-AUFNAHME

- Regression: `TestObservabilityRequiresAdapterSourceHasNoProducer` in `internal/capability/integration_contract_test.go` (new).
- Job: **packages-shard** (unit tests, `internal/...`), CI-trigger: pull_request push (branch lane-0428-182-metrics-adapter) — benennen in der akte, run-id + CONSTRUCTION am exakten head folgt nach push.
- Hinweis owner-scope: falls der packages-shard keine neuen tests laeuft, ist aenderung an `.github/**` noetig (owner-scope); dann EXAKTE aenderung als finding mit file:line hier dokumentieren, NICHT editieren.

## END

END_DONE mission-182.md — 0428-182 adapter without exporter: deklaration korrigiert, RequiresAdapter -> Unsupported fuer postgres+valkey metrics in reference.go:35/:48 (metrik nie collectable, kein exporter/compose/runtime-producer; verdrahten waere doppelschreiber in verschlossene zones #1684/#1645/183/184), fail-closed regression in integration_contract_test.go, CI packages-shard, branch aus develop@96f2ae11, evidence in baseharbor-plan origin/main.
