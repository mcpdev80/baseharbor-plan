# Perses signal inventory — akte

**Card:** t-20261114-r28-perses-signal-inventory (0428-090 "Audit real observability signals")
**Type:** READ-ONLY inventory (produkt-LES; produkt-aenderungen VERBOTEN). Ergebnis = akte im Plan-Repo.
**Base:** Core `develop` = `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (verified remote HEAD; equals mission pin)
**Branch provenance:** this akte is authored from Core `develop` HEAD `0e9ccb582`; that SHA is an ancestor of every file read here.

> Evidence provenance (Owner rules): evidence lives ONLY in baseharbor-plan, never in the product repo. Base verified via `git ls-remote`/fresh remote ref, never via the quarantined workers/baseharbor checkout. No `.github/**` edited, no reruns/workflow_dispatch. No subagents.

## 1. Ziel / Scope

Inventarisiere ALLE Signale, die BaseHarbor heute aussendet/erhebt (Metriken, Logs, Traces, Alerts; Quellen: internal/, cmd/, docs/, existing dashboards/scrape-konfigurationen) auf develop 0e9ccb582. Je Signal: Name/Sinn+Pfad, Port/Endpoint, Auth-Grenze, Datei:Zeile. Luecken (was ein Perses-Dashboard braucht, aber nicht existiert) und Doppelungen markieren. Zitierte Quellen: baseharbor-Source + context7 (Perses) + Web (Prometheus/OpenTelemetry/Valkey-Exporter).

## 2. Was Perses braucht (Kontext, Source: context7)

- Perses = GitOps-fahres Dashboard-Tool; Dashboards als Code (percli Go SDK). Referenz: `/perses/perses`.
- Ein minimales Dashboard braucht MINDESTENS ein `panel` + ein `layout` (docs/api/dashboard.md, perses/perses).
- Dashboard-Spezifikation: `display`, optional `datasources` (Map; Key = Referenz, Value = Datasource-Def), `variables`, `panels` (Map; Key = Panel-Referenz), `layouts`, `duration`, `refreshInterval`, `timezone`, `links`.
- Panel: `kind: "Panel"` + `spec.plugin`, `spec.queries[]`. Die `query.kind` muss zum Panel/Datasource passen, z. B. `PrometheusTimeSeriesQuery` für `TimeSeriesQuery` (docs/api/dashboard.md).
- PromQL-Query-Beispiel (docs/dac/go/query.md): `query.PromQL("max by (container) (container_memory_rss{...})")`.
- Datasource: z. B. `promDs.Prometheus(promDs.HTTPProxy("https://demo.prometheus.com"))`.
- **Folgerung:** ein Perses-Dashboard braucht i. A. (a) einen Prometheus-/Loki-/Tempo-Datasource-Ref, (b) mind. ein Panel mit `spec.queries` und (c) ein `layout`. Ohne diese drei Elemente ist kein Dashboard valide.

## 3. Signale — Metriken (Prometheus)

### 3.1 Managed Prometheus (Provider) — Collect, nicht Export
BaseHarbor betreibt einen Prometheus (`docker.io/prom/prometheus:v3.14.0`, internal/metrics/prometheus.go:21-22), der Targets scrapet. PromQL-Endpunkte werden intern genutzt:
- `/api/v1/query` (queryUp) — internal/metrics/prometheus_verify.go:286-289
- `/api/v1/targets?state=active` — internal/metrics/prometheus_verify.go:68-70
- `/-/reload`, `/-/ready` — internal/metrics/prometheus_verify.go:24, 40-45
- Port `9090` intern (Container-UPSTREAM); veröffentlichter Port = dynamisch via `allocatePort()` (internal/metrics/prometheus_files.go:276-284), ENV `BASEHARBOR_PROMETHEUS_PORT`, Endpoint `https://127.0.0.1:<port>` (internal/metrics/prometheus_render.go:25-41).
- Auth-Grenze: MTLS via HTTP-Gateway; web-config.yml mit `client_auth_type: RequireAndVerifyClientCert` für MTLS (internal/metrics/prometheus_files.go:560-563); optional Basic-Auth UI (`BASEHARBOR_PROMETHEUS_HEALTH_AUTHORIZATION`) nur in `dev` + `observability.managementUI` (internal/metrics/prometheus_files.go:286-304).

### 3.2 Application scrape target (`baseharbor-applications`)
Job `baseharbor-applications` via `file_sd_configs` (`internal/metrics/prometheus_render.go:192-216`). Labels je Ziel (Targets-JSON): `baseharbor_application`, `baseharbor_environment`, `baseharbor_source`, `baseharbor_metrics_path`, `baseharbor_metrics_scheme`.
- **Das ist das einzige von BaseHarbor real generierte Metrik-Signal.** `Verify()` pollt `up{job="baseharbor-applications",baseharbor_application=..,baseharbor_environment=..,baseharbor_source=..}` (internal/metrics/prometheus.go:344-347).
- Quelle: die Workloads selbst müssen `/metrics` (OpenMetrics, mTLS) anbieten; BaseHarbor registriert nur das Target (Bind). Kein eigener App-Metriken-Exporter im Core.

### 3.3 Provider scrape target (`baseharbor-providers`)
Job `baseharbor-providers` (internal/metrics/prometheus_render.go:218-228). Labels: `baseharbor_provider`, `baseharbor_source`, `baseharbor_source_class`, `baseharbor_metrics_path`.
- `provider--<token>.json` / `provider-secure--<token>.json` (internal/metrics/prometheus_files.go:39-45). mtls-Signale bekommen einen dedizierten `baseharbor-provider-secure-<token>`-Job mit `scheme: https` + `tls_config` (internal/metrics/prometheus_render.go:229-251).

### 3.4 Verifizierte Signale in der Referenzkatalog (`internal/capability/reference.go`)
Nur die mit `Status: supported` werden real gesammelt/exportiert:
- OTel Collector Exporter: `collector-metrics`, metrics, native, `/metrics` Port **8888** (reference.go:104). Quelle: collector telemetry prometheus exporter `host:0.0.0.0 port:8888` (internal/telemetry/otlp.go:603-610).
- Loki Exporter: `loki-metrics`, metrics, native, `/metrics` Port **3100** (reference.go:132). Loki-Config `http_listen_port: 3100` (internal/logs/render.go:20).
- Tempo Exporter: `tempo-metrics`, metrics, native, `/metrics` Port **3200** (reference.go:146). Tempo `http_listen_port: 3200` (internal/traces/tempo.go:634).
- Keycloak Exporter: `keycloak-metrics`, metrics, native, `/metrics` Port **9000** (reference.go:160).

### 3.5 Nicht-sammelt / Adapter
- PostgreSQL/Valkey: `metrics`, `requires-adapter` (reference.go:35, 48) → kein nativer Export; Sammelstatus fehlt.
- OpenBao/Caddy/SeaweedFS/External-OTLP: keine Observability.Signals deklariert.

## 4. Signale — Logs

### 4.1 Loki (Provider) — Collect + Query
Loki (`docker.io/grafana/loki:3.7.8`, internal/logs/driver.go:17). `auth_enabled: false` (internal/logs/render.go:17), `path_prefix: /loki`, Port **3100** (internal/logs/render.go:20). Query-API (internal/logs/query.go):
- `/ready` (internal/logs/query.go:24)
- `/loki/api/v1/series` (internal/logs/query.go:230)
- `/loki/api/v1/query_range` (internal/logs/query.go:287)
Push (Alloy→Loki, mTLS): `https://loki:8443/loki/api/v1/push` (internal/logs/render.go:101). HA-Cluster-Port `7946` (internal/logs/render.go:61).

### 4.2 Alloy (Log-Collector) — Collect
Alloy (`docker.io/grafana/alloy:v1.19.2`, internal/logs/driver.go:18). Syslog-Receiver (`loki.source.syslog`, rfc5424), `address = 0.0.0.0:<SyslogPort>` (internal/logs/render.go:182-186); `SyslogPort` pro Registration dynamisch allokiert. Journal-Modus braucht keinen Host-published Syslog-Listener (internal/logs/render.go:436).

### 4.3 Signal-Registrierung (internal/observability/registry.go)
Signale werden in `<dataDir>/observability/signals.json` persistiert. `RegisterProviderSignals` validiert nur deklarierte, `collectable` Provider-Signale (internal/observability/registry.go:180-238). Protokolle: `stdout-stderr`, `syslog-rfc5424`, `journald`, `otlp` (internal/observability/registry.go:105-108).

## 5. Signale — Traces

### 5.1 OTel Collector (Transport)
`docker.io/otel/opentelemetry-collector-contrib:0.161.0` (internal/telemetry/otlp.go:31). OTLP-Receiver HTTP `0.0.0.0:4318`, mTLS mit optionalem client_ca (internal/telemetry/otlp.go:596-615). Export `otlp_http/tempo` → `http://tempo:4318` (internal/telemetry/otlp.go:618-621). Veröffentlichter Port dynamisch, ENV `BASEHARBOR_OTLP_PORT`, Endpoint `https://127.0.0.1:<port>` (internal/telemetry/otlp.go:656-663).

### 5.2 Tempo (Storage/Query)
`docker.io/grafana/tempo:3.1.0` (internal/traces/tempo.go:27). Tempo-Query-Frontend `http_listen_port: 3200`, gRPC `9095` (internal/traces/tempo.go:634-635; internal/traces/tempo_ha.go:19). Query-Endpoint `/api/traces/<traceID>` (internal/traces/tempo.go:594). Veröffentlichter Port dynamisch, ENV `BASEHARBOR_TEMPO_PORT` (internal/traces/tempo.go:500-511).

## 6. Alerts
- **Keine Alert-/Routing-Logik im Core gefunden.** Kein Prometheus `rules:`/`alerting:` in render.go, kein Loki-Tempo-Alerting, keine `promtool check rules`.
- Alerting-Owner undefiniert: die Karte verlangt den realen Rule-Evaluator/Notification-Owner im Vertrag; er ist hier NICHT implementiert. Kein `datasources`- oder Dashboard-Alerting sichtbar.
- **LUECKE:** Alerting ist nicht realisiert.

## 7. Luecken (Perses-Dashboard fehlt komplett)
1. **Kein Persistenz-Ordner** `dashboards/` und kein Perses-Dashboard-JSON/YAML anywhere im Repo (grep bestätigt, excl. .github).
2. **Kein `panel`+`layout`** vorhanden (Perses-Mindestanforderung, docs/api/dashboard.md).
3. **Kein Prometheus/Loki/Tempo Datasource-Ref** in einem Dashboard definiert.
4. **`up`-Metriken** existieren real (internal/metrics/prometheus.go:344), sind aber keinem Panel zugeordnet.
5. **Alerting** nicht implementiert (siehe 6).
6. **PostgreSQL/Valkey metrics** = `requires-adapter`, kein nativer Export → Dashboard-Feld unabdeckbar ohne Adapter.

## 8. Doppelungen
1. **`MetricsSource` ↔ `SignalSource`:** dualer Metadaten-Typ in internal/observability/registry.go (MetricsSource:120-154, SignalSource:57-73). `MetricsSource` bleibt "focused compatibility type" (Kommentar:120-121) — Redundanz dokumentiert, kein Bug.
2. **`provider-secure-*`-Jobs vs. `baseharbor-providers`:** mtls-Provider-Metriken doppelt erfasst (einmal global job, einmal separater secure-job) — intentional (per-source tls_config), Redundanz bewusst (internal/metrics/prometheus_render.go:218-251).
3. **Prometheus-Metriken-Ref** in referenzkatalog (reference.go:118) und exporter (internal/telemetry/otlp.go) — kein Double, nur verschiedene Schichten.

## 9. Quellen
- baseharbor develop `0e9ccb582` (remote HEAD)
- context7: /perses/perses — docs/api/dashboard.md (Dashboard/Panel/Query-Spezifikation), docs/dac/go/query.md (PromQL-Beispiel)
- Web (Referenz): OpenTelemetry Collector Prometheus Exporter (`telemetry.metrics.readers.pull.exporter.prometheus`), Prometheus `file_sd_configs` + `up`, Grafana Loki HTTP API (`/loki/api/v1/query_range`), Tempo Query API (`/api/traces`), Valkey/Redis Prometheus exporter — Kontext, nicht implementiert.
