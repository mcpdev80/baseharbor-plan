# Bug-Hunt slice H-V41: telemetry/observability surface

- Shift: r28-welle6-2026-11-27
- Card lane: w174-0428-224-hunt-v41
- Mode: READ-ONLY, pure FINDING, no product changes
- Host: a87da7d1 (develop tip, worktree `workers/w174-0428-224-hunt-v41-wt`)

## Anchor

- `git ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `a87da7d179e08d43e8987885c38ab459ff1d887d`
- Worktree cut at exact tip `a87da7d1` (detached HEAD, verified via `git rev-parse HEAD` in worktree).

## Scope

Three slices off the telemetry/observability surface:

1. Metrics endpoints + label cardinality vs docs (0428-290 context).
2. Perses backend signal witnesses vs actual probes (0428-249/Perses chain).
3. Log redaction claims vs code (secrets leakage classes).

## Findings

### FUND 1 (info): metrics realized labels vs the log-source contract label set differ by design

- file: `internal/metrics/prometheus.go:351` - the `Verify` scrape query keys `up{job="baseharbor-applications",baseharbor_application,baseharbor_environment,baseharbor_source}`.
- file: `internal/metrics/realization.go:148` - realized `baseharbor-applications` target labels: `job`, `baseharbor_application`, `baseharbor_environment`, `baseharbor_service`, `baseharbor_source`, `baseharbor_source_class`, `baseharbor_metrics_path`, `baseharbor_metrics_scheme`.
- file: `internal/metrics/prometheus_render.go:249` - `baseharbor-applications` scrape config relabels `baseharbor_metrics_path -> __metrics_path__` and drops `baseharbor_metrics_(path|scheme)` via `labeldrop` (lines 254-255).
- file: `internal/metrics/prometheus_render.go:262` - the `baseharbor-providers` scrape config drops only `baseharbor_metrics_path`, never `baseharbor_metrics_scheme`.
- Contrast: `internal/observability/registry.go:18` documents the three semantic source classes; `docs/architecture/runtime-log-source-contract.md:70` documents the Loki collector-normalization label set (`baseharbor_application, baseharbor_environment, baseharbor_source_class, baseharbor_provider, baseharbor_service`).
- Assessment: not a defect. The metrics path carries two extra scrape-only labels (`baseharbor_metrics_path`, `baseharbor_metrics_scheme`) that are used for `__scheme__`/`__metrics_path__` remap and dropped before series retention. The `baseharbor-providers` job never sets `baseharbor_metrics_scheme` (provider target payload `internal/metrics/prometheus_files.go:171` omits it), so the asymmetric `labeldrop` is consistent, not a leak. Documented here for the metrics-vs-docs label reconciliation.
- Proposed card: none (documentation reconciliation, optional).

### FUND 2 (info): metrics source class label `baseharbor_source_class` is present on application targets but the docs do not enumerate it

- file: `internal/metrics/realization.go:154` - application target carries `baseharbor_source_class: application` (via `application.MetricsSourceApplication`).
- file: `internal/metrics/runtime_source.go:143` - runtime-metrics target carries `baseharbor_source_class` too.
- Contrast: `docs/releases/v0.4.8.md:78` documents "labels series with application/environment/source identity" - it does not enumerate `baseharbor_source_class` explicitly.
- Assessment: not a defect; `baseharbor_source_class` is a real semantic tag (matches the log-source contract) and is a positive label-cardinality control (it lets a single dashboard scope by class). Documented for completeness of the label-cardinality reconciliation.
- Proposed card: none.

### FUND 3 (info): Perses infra dashboard signal witnesses are per-panel series, not a generic up{} probe

- file: `internal/metrics/perses_infra_dashboards.go:60` - the builder answers each panel's OWN series query (one `/api/v1/query` per panel) through the `persesInfraProbe` seam.
- file: `internal/metrics/perses_infra_dashboards.go:119` - `httpClientSeriesProbe.querySeries` -> `queryUp` over the materialized management endpoint.
- file: `internal/metrics/perses_infra_dashboards.go:129` - `VerifyPersesInfraDashboard` fails closed when every panel's series is missing (`MissingSignalCount() == len(Signals)`).
- file: `internal/metrics/perses_backend_status.go:85` - `PersesBackendAnswersStatusWithProbe` returns `configured_unverified` unless every panel's own series returned rows.
- Contrast: `internal/metrics/perses_infra_dashboards.go:81` documents that the standard node_exporter name is `node_cpu_seconds_total` and that this dashboard ships NO `node_*` series - the four infra panels realize `up`, `scrape_samples_post_metric_relabeling`, `scrape_samples_scraped`, `scrape_duration_seconds` (lines 86-90).
- Assessment: not a defect. Signal witnesses are real per-panel PromQL against the live backend; unobserved panels are an explicit visible "No Data" gap, never a silent fill. Matches Luna batch17 findings 2/3. Documented as positive evidence the named probe path is genuinely wired.
- Proposed card: none.

### FUND 4 (info): OTLP workload binding never delivers secret material through env values

- file: `internal/application/telemetry_binding.go:73` - `OTEL_EXPORTER_OTLP_ENDPOINT` = host endpoint; `OTEL_EXPORTER_OTLP_HEADERS` retained only for `ProviderExternalOTLP`.
- file: `internal/application/telemetry_binding.go:56` - for managed collector, `OTLP_HEADERS` is deleted and `OTLPTLSHostCAEnv`/`OTLPTLSHostClientCertEnv`/`OTLPTLSHostClientKeyEnv` are NOT delivered to external (line 62-64).
- Contrast: `docs/spec/bindings/secure/v1.md` workload-projection boundary lists `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_CERTIFICATE` as the only projected OTEL vars; private keys are projected through protected file mounts, never env.
- Assessment: not a defect. Authorization headers and TLS CA are not written to the portable env; `parseExternalHeaders` rejects CR/LF/NUL and non-printable bytes (`internal/telemetry/external_auth.go:41`). Documented as positive evidence against the secrets-leakage class.

## Net

- Fund count: 4, all info-level, all "documented-but-no-defect" reconciliations.
- No blocking security defect in the telemetry/observability surface on the a87da7d1 develop tip.
- No product changes made (read-only hunt). No proposed card required beyond optional documentation reconciliation (Funds 1-2).

## repo-rule compliance

- Read-only worktree at exact develop tip; no product files edited.
- Evidence lives only in baseharbor-plan; no `.evidence/` dir in the product repo.
- No CI run, no workflow edit (Owner scope).
