# fix-2 (r3) — 0428-123 regvisibility: route app-class metrics into the baseharbor-applications job (end-to-end)

- Card: t-20261119-hunt-metrics-registration-visibility-only (0428-123)
- PR: mcpdev80/baseharbor#1693 · zweig `lane-0428-123-regvisibility`
- Session: `c5d271cb` (w123-0428-123-regvisibility, laptop), Modell `worker-ornith1.5-laptop` über AgentGateway verifiziert.
- Evidence provenance: baseharbor-plan `origin/main`.

## Kopf-Folge (d751c83bb → f3c1bf43 → neu)

- d751c83bb (r3): ListMetrics 5-arg auf develop fac01c772 — Commit `d751c83bb047989d5bb4b11bcee1d091cf08d96a`. Run 44546638806 lief auf fac01c772 und ist KEINE Abnahme: der Owner hat 15:08Z festgehalten, dass ein alter Lauf auf älterem Base keine Abnahme ist.
- f3c1bf43 (r3): Commit `f3c1bf43bf1a682c29145bf0dade48b319d8e481`, Base noch fac01c772.
- 4f22bf6e (dieser Lauf): Commit `4f22bf6e92354637367a821318f1dfbd6d1c1515`, Base `1019190d8dc0ecac7693f3461153e76be0e2cb8a` (develop, #1598 Perses lifecycle gemergt 14:56:29Z). Run 44557894265.
- Warum die alten Läufe nicht zählen: f3c1bf43 stand auf fac01c772; develop ist weiter 1019190d8 (#1685 Registry-Änderung, #1598 Perses). queue563-Basisabstand (f3c1bf43 vs origin/develop) berührt nur internal/metrics/prometheus_verify.go, internal/metrics/regvisibility_regression_test.go, internal/observability/registry.go — kein .github/**, kein scripts/test_pr_*|scripts/test_ci_* → kein neuer Hopf nötig, der Lauf unter 1019190d8 ist der gültige Kandidat.

## CI-Beweis (terminal)

- Run-ID: 44557894265, Event pull_request, SHA 4f22bf6e.
- Status terminal: **success**. Aggregate `PR Selected Checks: success`.
- Pflicht-Jobs ausgeführt und grün (kein SKIPPED unter Mandatory): go-build (PR · Validation · go-build: success), go-vet (PR · Validation · go-vet: success), Go unit owner/packages/cli-0/1/2/3 (alle success), Workflow policy success, Native gate plan success, Source format success, Focused Python success.
- Kein ORAS/trust-plane runner-precondition-Fehler: die Runtime-Gates (Targeted HA · docker/podman, Native Keycloak/Core) sind von CI-Policy als skipped markiert, nicht als ausgefallen. SKIPPED != pass, aber hier ist SKIPPED keine Mandatory-Execution; die Mandatory-Jobs sind alle ausgeführt.
- Provenance: git merge-base --is-ancestor origin/develop 4f22bf6e → rc=0; git merge-base --is-ancestor a10e6781 4f22bf6e → rc=0 (a10e6781 = vorheriger Hopf-Kopf). Log enthält nur develop-Commits + zwei eigene Commits (f3c1bf43, 4f22bf6e).

## Die vier Fixes (Datei:Zeile)

1. **Routing — prometheus_files.go** (freigegeben durch Owner). Bisher: syncProviderTargets (:40 prefix 'provider--', :71 "job": "baseharbor-providers", :74 "baseharbor_source_class") schrieb ALLE nicht-none Quellen in provider--<hash>.json. Fix: syncProviderTargets (:89-101) teilt SourceApplication-Klassen ab und schreibt sie über writeApplicationTargetFile (:125) in die eigene <app>--<env>--<source>.json-Datei mit job=baseharbor-applications und baseharbor_application/baseharbor_environment/baseharbor_source/baseharbor_source_class/baseharbor_metrics_path/baseharbor_metrics_scheme. Die Quelle verlässt die provider--<hash>.json-Datei komplett (exactly-once). appTargetFileName (:53) leitet den Pfad aus der ID-Grammatik application:metrics:<app>:<env>:<src>.
2. **Render-Glob — prometheus_render.go:199**. baseharbor-applications job (:195-198, liest NUR *--*--*.json + runtime-targets) umfasst jetzt auch /etc/prometheus/targets/baseharbor-applications-*.json, damit die vom Exporter geschriebene app-target-Datei vom application-job gelesen wird. (prometheus_verify.go:179 app-abfrage 'up{job="baseharbor-applications",baseharbor_application=…}' bleibt der Verifikations-Endpunkt.)
3. **Parity-Guard — prometheus_verify.go:174** (app-loop). Der provider-loop (:185) überspringt bereits ObservabilityVerifyNone; der app-loop bekam dieselbe Zeile, damit eine app-Quelle mit 'none' jetzt einheitlich abgefangen wird und nicht in den wait-for-up-Timeout läuft. Das ist eine Folge des Routing-Fixes; die weitergehende Vertrags-Frage zur Provider/App-Asymmetrie bleibt auf 0428-143 (t-20261119-r28-app-source-verification-none-ignored). Parity-Guard in #1693 als direkte Folge des Routing-Fixes genommen; die weitergehende Vertragsfrage bleibt auf 0428-143.
4. **Tests — regvisibility_regression_test.go**. TestRegVisibilityEndToEndAppTargetInApplicationsJob: dieselbe Quelle erscheint im application-target MIT labels baseharbor_application/baseharbor_environment/baseharbor_source UND NICHT mehr im providers-target (duplicate-freiheit); abgedeckt von der baseharbor-applications verify-abfrage. TestRegVisibilityNoCrossEnvironmentExposure: dev/stage-Sibling-Quelle derselben Application, assertion 'dev sieht nur dev' (cross-environment-exposure). TestRegVisibilityVerificationNoneStaysUnexported: none-Quelle bleibt unexportet.

## Neue Test-IDs + Gate

- TestRegVisibilityRegisteredSourceIsExported, TestRegVisibilityNoCrossEnvironmentExposure, TestRegVisibilityVerificationNoneStaysUnexported, TestRegVisibilityEndToEndAppTargetInApplicationsJob — alle grün unter `go test ./internal/metrics/... -run TestRegVisibility`.
- Gate: `bash scripts/ci-fast-check.sh` → 275 tests OK, Workflow policy PASS, source readability PASS. Package-wide: `go test ./internal/metrics ./internal/observability -count=1` OK.
- CI-Aufnahme: die neuen Tests laufen im existing Go unit owner/packages shard (auto-discovered by `go test ./...`), pull_request-Trigger. Kein .github/**-Change nötig (Owner-scope): kein Change.

## ## PLAN (nummeriert, ohne Markdown-Checkboxen)

1. git fetch origin --prune; remote-Truth selbst lesen (git ls-remote origin refs/heads/develop, gh api pulls/1693 .head.sha/.base.sha/.mergeable_state/.draft).
2. EIN monotoner merge-hopf git merge origin/develop (kein rebase, kein force); nachweis is-ancestor develop=0, is-ancestor f3c1bf43=0, merge-tree conflict-count=0; queue563 diff --name-only f3c1bf43 vs origin/develop (kein .github/**/scripts/test_pr_* → kein neuer Hopf).
3. Die vier Fixes: routing (files.go + render.go), parity-guard im app-loop, end-to-end-assertion + duplicate-freiheit, dev/stage-sibling.
4. go build ./..., go vet ./internal/metrics ./internal/observability, go test ./internal/metrics ./internal/observability -count=1, bash scripts/ci-fast-check.sh VOR push.
5. push (draft=false), EIN exaktkopf-lauf bis terminal (Run 44557894265).
6. Evidence fix-2.md; karte active bis (5) terminal gruen.
7. KEIN merge durch mich (Owner führt die unabhängige Abnahme), KEINE subagenten (§4.8), host besenrein.

## ## repo-rule compliance

- Write-set: nur registry registration path (internal/metrics/prometheus_files.go, prometheus_render.go, prometheus_verify.go, regvisibility_regression_test.go). Kein .github/**, kein scripts/**, kein cmd/baha/**, kein internal/machine/**, kein docs/** (0428-084/089).
- Kein rebase/force/reset; monotoner merge-hopf; base attestet.
- Kein subagenten (§4.8); kein merge durch mich.
- CI-Aufnahme der neuen Tests über bestehenden Go-unit shard + pull_request-Trigger; kein .github/**-Change.

## Host hygiene (cleanliness)

- Vorher: `docker ps` (keine baseharbor-compose container in diesem Lauf), `docker network ls` (leer/non-baha), `docker volume ls` (leer/non-baha).
- Nachher: dieselben drei Listen; kein in diesem Lauf erzeugter container/netzwerk/volume.
- cleanliness: keine baseharbor-compose netzwerke/volumes/container in diesem Lauf erzeugt; ambient-core/ unangetastet.
