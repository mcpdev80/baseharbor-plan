# Befund-Akte: hunt-alerting

- Lane: mission-hunt-alerting (session 2efa2a49, coordinator d4212c96)
- Datum: 2026-11-17 CET
- Ziel der Mission: reine Befundung (keine Produkteuerung) eines Querschnitt ALERTING + RUNTIME-OBSERVER auf develop
- develop-PIN: 6cf121524da34ca11bc07ead0ab3c568d29e9c80 (ls-remote witness)
- Status: ABGESCHLOSSEN (nach HUNT-FREIGABE 2026-11-17); kein Produkt-Zweig, kein Commit, kein Push, kein PR angelegt

## PLAN

- Mission lesen und Geltungsbereich pruefen
- Coordinator-Haltstatus gegen develop verifizieren (HUNT-HOLD / HOLD)
- Release-Stand v0.4.27 verifizieren; HUNT-FREIGABE 2026-11-17 festhalten
- develop@6cf121524 pinnen (ls-remote witness), lokale baseharbor-Worktree syncen
- (a) metrics.rules permission-deklaration vs. Verwender: wer liest sie tatsaechlich
- (b) provider-/observer-pfade runtime://: wer hat probe-adapter, wer nicht (nur inventarisieren, file:line; Karte 108 Territories BERUEHREN aber NICHT bewerten)
- (c) alert-notification-owner aus Karte 073-acceptance: existiert ein Owner im Code
- (a)+(c) als Befund dokumentieren, existing befund-1.md ergaenzen
- Sauberkeit (cleanliness) festhalten, Evidence auf origin/main publishen
- END an Coordinator posten

## Fakten / Belege (Geltungsbereich + Pin)

- Mission /var/tmp/missions/mission-hunt-alerting.md: reine Befundung, Decke ab (a) metrics.rules permission-deklaration vs. Verwender, (b) provider-/observer-pfade runtime://, (c) alert-notification-owner (Karte 073-acceptance).
- HUNT-HOLD 2026-11-15 und HOLD 2026-11-09 in coordinator/BUG-HUNT.md waren anfangs maßgeblich (Halt zuerst dokumentiert).
- HUNT-FREIGABE 2026-11-17 (Owner-Wort, gegenstandslos machend) in coordinator/BUG-HUNT.md: v0.4.27 um 02:48Z released (tag 6c40fab4-Peel-Kette, release-world), Owner-Freigabe wieder auf bug hunts zu gehen (~04:10Z, 0.4.28-Fenster). Halte 2026-11-09/15 hochaufgehoben.
- develop ls-remote origin/develop = 6cf121524 (baseharbor). Lokale baseharbor am 2026-11-17 auf origin/develop resettet, sauber.
- baseharbor-plan origin/main HEAD = 71ae0f7c (planning repo verified via ls-remote, NOT die workers/-Nestkopie).

## (a) metrics.rules permission-deklaration vs. Verwender — wer liest sie tatsaechlich?

Ergebnis: Es gibt KEINE literalen „metrics.rules". Die Deklaration ist `Metrics.Sources` (`MetricsSourceRequirement{Name,Service,Port,Path}`), die Zugrags-/Scope-Entscheidung `Runtime.Permissions`. Alert-/Rule-/Notification-Code existiert im develop-stand NICHT (siehe (c)). Wer die Deklaration tatsaechlich liest:

Deklarations-Leser (intent):
- internal/application/manifest.go:61-74 — Typdefinition; manifest_parse.go:477 fuegt Sources aus YAML hinzu.
- internal/metrics/prometheus_shared.go:232-235 — `HasMetricsSources` / `HasRuntimeMetricsPermissions`; prueft Intent vor Realisierung.
- internal/metrics/prometheus_files.go:27-28 — iteriert `m.Metrics.Sources` fuer Source-Map.
- internal/applicationbackup/recovery_discovery.go:145-146 — haengt `m.Metrics.Sources` bei Recovery an.

Verwender/Realisierer (consume die Deklaration):
- internal/metrics/prometheus.go:319-322 — liest Service/Scheme/Port/Path eines `binding.Metrics` (Prometheus-Provider).
- internal/telemetry/realization.go:187, internal/logs/realization.go:219, internal/identityprovider/keycloak_realization.go:145 — `HasMetricsSources || HasRuntimeMetricsPermissions` steuert `metricsEnabled`.
- internal/runtimebroker/compose_render.go:201,242,308, internal/runtimebroker/retirement.go:44 — `HasRuntimeMetricsPermissions` schaltet Metrics-Netzwerk/Volume.
- internal/hostresource/application.go:90, internal/capability/lifecycle.go:235-260 — Intent-Auflösung/Binding.

Permission-Deklaration: `RuntimePermission{Capability,Services,Operations}` (manifest.go:47), prueft `HasRuntimeMetricsPermissions` gegen `capability.MetricsV1.ID` (internal/application/metrics_policy.go:127). Quelle der Wahrheit ist die Manifest-Deklaration; die read-side prueft nur Vorhandensein (`> 0` / Capability-Match), es gibt KEINEN gegenlesebasierten „Wer liest mich"-Check.

## (b) provider-/observer-pfade runtime:// — wer erzeugt/consumiert, wer hat probe-adapter

`observability.RuntimeTarget(project,service)` erzeugt `runtime://<project>/<service>` (internal/observability/registry.go:259-263). Nur die LOGS-Pfade konsumieren sie (`ParseRuntimeTarget` in internal/logs/render.go:270, internal/logs/overrides.go:132, internal/logs/query.go:110/150, internal/application/runtime_observability.go:185). Tempo/OTel/Keycloak/Metrics konsumieren runtime:// NICHT.

Erzeuger von runtime:// + Signal-Registration (`RegisterProviderSignals`, 5 Call-Sites):
1. internal/telemetry/realization.go:196 — OTelCollector, ID `opentelemetry-collector:<project>`, Klasse platform-provider, Signal `collector-metrics` @ otel-collector:8888 (registry.go:196).
2. internal/logs/realization.go:232 — Loki, ID `loki:<project>`, class platform/application-provider, Signal `loki-metrics` @ loki:3100.
3. internal/identityprovider/keycloak_realization.go:158 — Keycloak, ID `keycloak-metrics`, owner=App, Signal `keycloak-metrics` @ keycloak:9000.
4. internal/application/runtime_observability.go:159 — runtime executor, ID `<provider>:<project>:<service>`, class application-provider, Signals logs+traces mit `runtime://`-Target (registry.go:152).
5. internal/traces/tempo.go:403 — Tempo, ID `tempo:<project>`, class platform/application-provider, Signal `tempo-metrics` @ tempo:3200.

Probe-adapter / VerifyBackend-Vorhandensein (aus capability/reference.go, autoritativ):
- OTel collector: metrics Supported, VerifyBackend (reference.go:104) — Adapter da.
- Loki: metrics Supported, VerifyBackend (reference.go:132); logs runtime VerifyBackend (133). logs/query.go:78 `VerifyProviderSources` probe. Adapter da.
- Tempo: metrics Supported, VerifyBackend (reference.go:146); traces VerifySpan (tempo.go:579 `VerifyTrace`). Adapter da.
- Keycloak: metrics Supported VerifyBackend (160); logs runtime VerifyBackend (161). Adapter da.
- PostgreSQL (reference.go:35) + Redis (reference.go:48): metrics = `ObservabilityRequiresAdapter` + Mode `ObservabilityAdapter`, Verification `ObservabilityVerifyNone`. KEIN backend-adapter; Adapter fehlt (adapter-mode, keine native Metriken).
- Prometheus: metrics `ObservabilityUnsupported`, VerifyNone (reference.go:109) — aber metrics/prometheus_verify.go:109 `VerifyProviderSources` probe. Prometheus ist Sammler, nicht Collectable-Self.
- OpenBao/Caddy/SeaweedFS: alles Unsupported/VerifyNone — kein adapter.

Karte 108 (Territories) BERUEHREN, nicht bewertet: Die 5 Erzeuger + reference.go-Descriptor sind die volle Inventar-Grundlage fuer 108 (nur file:line, keine Bewertung).

## (c) alert-notification-owner aus Karte 073-acceptance — existiert ein Owner im Code?

Ergebnis: NEIN. Der develop-stand hat KEINEN Alert-Regel-Evaluator, KEINE Notification-Routing-Konfiguration und KEinen benannten notification-owner.

Quellen:
- Karte 0428-073 (baseharbor-plan/tasks/t-20261114-r28-perses-alerts.md) acceptance: „For alerting, define the real rule evaluator and notification owner in the approved contract... Do not claim native Perses alerting/routing parity without evidence." Status review, owner coord.
- Folgekarte 0428-112 (t-20261117-alert-evaluator-persistence-missing.md) „Alert rule evaluation and persistence missing (declaration-only)", depends_on 073, planned.
- spec/capabilities/metrics/v1.md:45,48 — expliziter non-goal: „alert routing" und „Prometheus-specific recording or alerting rules".
- Produkt-Scan develop: kein `alertmanager_config`/`alerting`/`receivers:`(alert)/`route:`/`RuleEvaluator`/`notification.*owner` in any .go/.yml. Die einzigen `receivers:`-Zeilen sind OTLP-Pipeline-receivers (internal/telemetry/otlp.go:613/647/650/653) und Tempo-distributor receivers (internal/traces/tempo.go:647) — kein alert-notification-owner.

Befund (c): Alert liegt auf declaration-only. Der „real rule evaluator + notification owner" aus 073-acceptance ist in develop NICHT implementiert; 0428-112 dokumentiert die Luecke.

## Fund-Matrix (Befund, keine Bewertung)

| Punkt | Inhalt | Beleg (file:line) | Status |
| --- | --- | --- | --- |
| (a) Deklaration vs. Verwender | Metrics.Sources=Deklaration, Runtime.Permissions=Scope; read-side nur Vorhandensein, kein Wer-liest-mich-Check | manifest.go:61-74, metrics_policy.go:127, prometheus.go:319-322, prometheus_shared.go:232 | gepruft |
| (b) runtime:// Erzeuger/consumer | 5 RegisterProviderSignals-Erzeuger; runtime nur von logs konsumiert; DB-Adapter fehlen (requires-adapter) | registry.go:259, telemetry/realization.go:196, logs/realization.go:232, keycloak_realization.go:158, runtime_observability.go:159, tempo.go:403, reference.go:35/48 | inventarisiert |
| (c) alert-notification-owner | Kein Evaluator/Notification-Routing/owner in develop; declaration-only | metrics/v1.md:45,48, otlp.go:613, tempo.go:647, karte 0428-112 | gepruft |

## Sauberkeit (cleanliness)

- ps-Vorher: keine Container/Netzwerke/Volumes der Lane gestartet
- ps-Nachher (2026-11-17): keine Container/Netzwerke/Volumes der Lane gestartet (bh-local-shared-openbao ist fremde Infrastructure, nicht von dieser Lane)
- cleanliness:-zeile: CLEAN — kein Container, kein Netzwerk, kein Volume, kein Compose-Projekt angelegt; kein Produkt-Zweig, kein Commit, kein Push, kein PR

## Handoff / END

ABGESCHLOSSEN. (a) Deklaration = Metrics.Sources/Runtime.Permissions, read-side prueft nur Vorhandensein (kein Wer-liest-mich-Check). (b) 5 runtime://-Erzeuger, logs konsumiert sie; DB-Metriken adapter-mode ohne backend-adapter. (c) alert-notification-owner NICHT implementiert (declaration-only; 0428-112). Kein Produkt-Zweig/Commit/Push/PR.
