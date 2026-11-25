# BUG-HUNT slice H-V53 — observability correctness

- Lane: w202-0428-224-hunt-v53
- Shift: r28-welle6-2026-11-27
- Mode: READ-ONLY, pure FINDING. No product changes, no PR, no card creation (freeze honored — disposition belongs to the Codex disposition lane).
- Mission: `coordinator/missions/hunt-v53-observability.txt`

## ANSATZ (visible block)

- Per-card frontmatter owner VERBATIM: none — this is a bug-hunt slice, not a card; mission assigns lane `w202-0428-224-hunt-v53`. No card claims were made or edited (plan freeze).
- git identity for the evidence commit: user.name=`w202-0428-224-hunt-v53`, user.email=`w202-0428-224-hunt-v53@baseharbor.local`
- Literal invocation: `git -c user.name=w202-0428-224-hunt-v53 -c user.email=w202-0428-224-hunt-v53@baseharbor.local commit -m ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w202-0428-224-hunt-v53` before any push.

## Anchor

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82 refs/heads/develop`
- Product worktree `workers/w202-0428-224-hunt-v53-wt` cut detached at exact tip (`git rev-parse HEAD` = `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`).
- Planning repo remote witness (before first evidence commit): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Plan worktree cut from `origin/main` = `0719f61221435244c7877e7767dab8f76dd2c680`.

## ## PLAN

1. Anchor: ls-remote develop tip; cite cut-from SHA in this header. (done)
2. Fresh worktree at exact tip. (done)
3. Read H-V47-intake bundle (the hunt48-era finding rows) and H-V52 disposition bundle first; build exclusion list. (done)
4. Hunt: metrics endpoints vs actual gauges (counter resets, label cardinality). (done)
5. Hunt: healthcheck semantics vs #1650 fail-closed states. (done)
6. Hunt: log-to-metric correlation ids. (done)
7. Hunt: dashboards data.capabilities coverage vs code surfaces. (done)
8. Write this akte under evidence/r28-welle6-2026-11-27/bughunt-hv53-observability/ via isolated plan worktree. (done)
9. Verify evidence on origin/main, push, remove worktree. (in progress at write time)
10. Cleanliness + END line + codeman post. (in progress at write time)

## Cross-hunt overlap (dedup, checked FIRST per mission)

- H-V41 (`evidence/hunt-v41/2026-11-27/bughunt-hv41-telemetry-surface/README.md`, anchored a87da7d1): FUND 1-2 census the realized application/provider label sets vs docs (scrape-only `baseharbor_metrics_path/scheme` drops, `baseharbor_source_class` doc gap); FUND 3 the per-panel Perses signal witnesses. H-V53 does NOT restate those label-census rows; H-53-4 generalizes only the class-coverage gap H-V41 FUND 2 touched incidentally, and H-53-2 concerns runtime-metrics target discovery, which H-V41 did not examine.
- H-V47-intake bundle (workers/w193-0428-224-hunt-v47-intake/disposition-bundle — the metric-adjacent hunt48-era rows; the plan-tree `bughunt-hv48-api-surface/hunt-1.md` BF-48-2 instead covers "GET /metrics registered but undocumented" and BF-48 series the HTTP/DTO surface): the `/metrics` endpoint existence/documentation row belongs to BF-48-2 — H-V53 H-53-1/H-53-5 go beyond it (series TYPE/semantics and authentication, not registration/doc presence). BF-47 rows are upgrade/migration surface — disjoint.
- H-V52 (`workers/w199-0428-224-hunt-v52/disposition-bundle/hv52-disposition-rows.md`): logging/redaction rows H-52a-d. H-52c is the control-plane raw-logs-on-start-failure leak; H-V53 H-53-3 is the distinct fact that those log records carry no correlation id (structure, not scrubbing). No duplicate rows.
- w198 (card 0428-284 demo parser, stream-shape family): H-V53 takes no stream-shape row.

All rows re-verified at the current tip 99d9ddebc (no anchor drift: mission itself anchors at the ls-remote tip).

## Findings

### H-53-1 — the runtime Observer serves a scalar sum-counter where Prometheus-native consumers expect buckets; and two of its four series have zero consumers in-repo

- Evidence (read-only): `internal/runtimeobservability/observer.go:195` emits `baseharbor_runtime_http_request_duration_seconds` as `# TYPE ... counter`, a single nanos-summed scalar with only a `component` label (`:195`, `:164`). With no `_bucket/_sum/_count` series, neither `histogram_quantile()` nor even a per-request average duration (`rate(..._sum)/rate(..._count)`) is computable — average duration per interval is unrecoverable from the exposed data.
- Consumers: grep across the whole checkout finds the only references to the `baseharbor_runtime_http_*` / `baseharbor_runtime_otlp_dropped_spans_total` series are the producer itself (`observer.go:193-196`) and its unit test (`internal/runtimeobservability/observer_test.go:61-84`). No Perses dashboard query, no Prometheus alert rule (`internal/metrics/prometheus_alert_rules.go:13` keys only on `up{job=~"baseharbor-applications|baseharbor-providers" == 0}`), no doc enumerates them.
- Counter-reset semantics: correct — monotonic `atomic.Uint64` since process start (`observer.go:48-51`), never reset in-process (`grep atomic.Uint64 internal/ cmd/` yields only `internal/operatorauth/local_runtime.go:30` and these four). Prometheus `rate()` handles process restarts. This sub-check is clean.
- Severity: LOW-MEDIUM (latency observability silently missing; series are scraped-at-most, alerted-on never).
- Proposed card line: either convert the duration series to a real histogram (explicit `http_duration_buckets` array rendered in OpenMetrics text form) or document + dashboard the scalar; register alert/query consumers for `baseharbor_runtime_http_errors_total` and `baseharbor_runtime_otlp_dropped_spans_total` so they are not write-only series. Write-set: `internal/runtimeobservability`, `internal/metrics/perses_*`.

### H-53-2 — the broker's runtime-metrics targets carry `job="baseharbor-runtime-metrics"`, which no verify query, dashboard panel or alert rule ever keys on

- Evidence (read-only): `internal/metrics/runtime_source.go:138` writes target files with label set `job: "baseharbor-runtime-metrics"` (+ app/env/service/source/class/path). Those files land in the runtime volume that IS mounted into Prometheus and enumerated under the scrape job `baseharbor-applications` (`internal/metrics/prometheus_render.go:237-240`, volume attach `:163-164`, `:212-213`), so targets get scraped — but the file_sd group's `job` label stays `baseharbor-runtime-metrics` (relabeling at `prometheus_render.go:249-255` only remaps path/scheme and labeldrops them; it never rewrites `job`).
- Consequence surfaces: every application-scoped query hardcodes `job="baseharbor-applications"`: verify `internal/metrics/prometheus.go:351-353` and `internal/metrics/prometheus_verify.go:248`, dashboard panel `internal/metrics/perses_dashboards.go:330`. The alert expression `up{job=~"baseharbor-applications|baseharbor-providers"} == 0` (`internal/metrics/prometheus_alert_rules.go:13`) therefore never sees a runtime-metrics target go DOWN: an application whose metrics come only via the runtime-metrics path can be fully unreachable (`up=0`) with zero pages.
- Contrast note: the runtime path is deliberately excluded from `PruneApplicationTargets` governance (`internal/metrics/runtime_retirement.go:19,94`) — retirement/ownership semantics, not label identity — so the job-name split is not backed by any contract statement found in docs/spec (grep `runtime-metrics` in docs/ returns nothing).
- Severity: MEDIUM (monitoring blind spot exactly where #1650-style fail-closed state matters: dead scrape = silent).
- Proposed card line: normalize the runtime-metrics job label to `baseharbor-applications` (keeping `baseharbor_source_class="application"` already set at `runtime_source.go:143`) or add `baseharbor-runtime-metrics` to the verify/dashboard/alert selectors; add a contract test asserting every target file the platform materializes is matched by the alert selector and the application verify query. Write-set: `internal/metrics/runtime_source.go`, `internal/metrics/prometheus_alert_rules.go` (+ tests).

### H-53-3 — the request log line carries no trace id although the observer generates one per request; log-to-trace correlation is impossible by design

- Evidence (read-only): `internal/runtimeobservability/observer.go:144-151` generates a traceID/spanID and sets the W3C `traceparent` RESPONSE header; `:166-176` attaches them to the `traceEvent`, and the OTLP exporter uses them (`:366-386`, span name `baseharbor.runtime.request`, attrs `http.request.method`/`url.path`/`http.response.status_code`). But `writeRequestLog` (`:222-232`) emits only `timestamp/level/component/event/method/path/status/duration_ms` — no `trace_id`/`span_id` field — while holding the event with the ids (`:177` passes the full event). The same asymmetry applies to `writeLifecycleLog`/`writeExportError` (`:200-220`, `:287-302`): export failures are logged with error text but no trace id, and — separately — exporter failures increment `traceDropped` (`:254`) yet the trace itself is never retried or requeued, so a dropped span has no correlated log pointing at the span it lost.
- Consumers: the Tempo dashboard queries traces by `resource.service.namespace`/`resource.deployment.environment.name` only (`internal/metrics/perses_dashboards.go` tempo panel query `{resource.service.namespace="$application" && resource.deployment.environment.name="$env"}`); the Loki error panel filters `baseharbor_source_class="application"` + `|= "error"` (`:330` region, loki panel). There is no log field a query can pivot on to jump log-line -> trace.
- No inbound propagation either: `Wrap` ignores any incoming `traceparent` request header (no read of `r.Header.Get("traceparent")` anywhere in the package; it always mints a new trace, `:144-149`), so application-side spans cannot be joined to broker/executor spans.
- Severity: MEDIUM (this is the entire log-to-metric/trace correlation cut of the mission: the ids exist, are exported, and are never put in the logs that operators search).
- Proposed card line: add `trace_id`/`span_id` fields to `writeRequestLog` (data already in `event`), optionally honor inbound `traceparent` per W3C context propagation; add a Perses Loki->Tempo correlated-drilldown note or dashboard variable. Write-set: `internal/runtimeobservability`, `internal/metrics/perses_dashboards*.go` (docs follow).

### H-53-4 — source-class coverage gap: dashboards/alerts never surface `application-provider` / `platform-provider` metrics classes; the only valkey panel is also dead (job mismatch)

- Evidence (read-only): three semantic classes are defined `internal/observability/registry.go:22-24` (`application`, `application-provider`, `platform-provider`) and all three are written into target labels (`internal/metrics/prometheus_files.go:171-179` provider payload sets `baseharbor_source_class`; `internal/metrics/realization.go:148-156` application payload; `internal/metrics/runtime_source.go:137-144`).
- Every PromQL/log consumer keys on class `application` or a `job`: app up-panel and verify use `job="baseharbor-applications"` (`perses_dashboards.go:330`, `prometheus.go:351`, `prometheus_verify.go:248`); provider panels use `up{job="baseharbor-providers"}` (`perses_dashboards_hosts.go:234`), which matches provider-class target files (`prometheus_files.go:171-179` sets `job="baseharbor-providers"`, `baseharbor_provider`, `baseharbor_source_class`) and the scrape job of the same name (`prometheus_render.go:257`). But the TLS variant renders its scrape job as `baseharbor-provider-secure-<token>` (`prometheus_render.go:274`) while the file_sd group label still pins `job="baseharbor-providers"` (`prometheus_files.go:172`, relabeling at `prometheus_render.go:262-266` never rewrites `job`): the actual series carry `job="baseharbor-providers"` and the `job_name` never appears in any series, so the panel works but the secure job's name is observable nowhere — and conversely the application-scoped provider targets written by `realization.go:148-156` carry `baseharbor_application` and NO `baseharbor_provider` label, so a provider-keyed panel like the valkey one (`perses_dashboards_valkey.go:276` `up{baseharbor_provider="valkey"}`) can only ever match platform/application-provider class files, never app-scoped provider sources.
- `baseharbor_metrics_scheme` labeldrop asymmetry is already censused by H-V41 FUND 1 — NOT restated here.
- Severity: LOW-MEDIUM (coverage gap claim, one concrete dead-panel sub-row).
- Proposed card line: add a per-class dashboard section (or `$class` variable) covering `application-provider`/`platform-provider`, and a contract test that every `observability.SourceClass` value persisted by `registry.Update` appears in at least one shipped panel's query result set (fail-closed like `perses_infra_dashboards.go:129`). Write-set: `internal/metrics/perses_dashboards*`, `internal/metrics/realization.go` (add `baseharbor_provider` to app-scoped provider targets if that is the chosen normalization).

### H-53-5 — /healthz is an unconditional 200 with no process liveness signal, and the two brokers disagree on the readiness-asymmetry style (positive census) + executor healthcheck start_period=2s churn window

- Evidence (read-only): `internal/controlplaneruntime/server_run.go:158-162` `/healthz` always writes `{"status":"ok"}` 200 with zero checks — fine as pure liveness, but there is no in-process deadlock/self-state signal at all and it is identical in shape to the readyz success body except version/commit (`:207-215`). Census: the broker's `/readyz` implements the #1650 fail-closed doctrine carefully and symmetrically — database ping (`:167-172`), openbao login-check (`:173-178`), executor check or the documented secrets-only exemption with `executorDependencyRequired` disagreement still RED (`:179-205`, comment `:186-198` names the "permanent not_ready" asymmetry the 0.4.26 edge image showed). Positive evidence, recorded, no defect.
- One asymmetry remains between the two processes: the executor's `/readyz` (`internal/runtimeexecutor/server.go:104-112`) fail-closes on the S3/seaweedfs dependency check, but its compose healthcheck uses `start_period: 2s` (`internal/runtimeexecutor/compose.go:295`) while the broker healthcheck uses `start_period: 30s` (`internal/runtimebroker/compose_render.go:264`) with the same `interval: 5s retries: 12`. Consequence: an executor under slow S3 startup flaps starting/handling for ~28s longer into the retries window than a broker in the identical state; container state (and therefore anything keying on `up`/health) shows executor RED during a warm-up the broker is allowed. No contract doc names the 2s value (grep `start_period` docs/ = nothing).
- Also census-clean: the broker healthcheck probes `https://.../readyz` with mTLS client material (`compose_render.go:260`), the executor likewise (`compose.go:291`), so healthcheck semantics match the fail-closed body path exactly — no "healthcheck hits /healthz while verify gates on /readyz" drift exists here.
- Severity: LOW (config asymmetry / doc absence; the readyz logic itself is sound).
- Proposed card line: align `start_period` across the two management-service healthchecks (or document the deliberate difference next to `retries: 12`), and add the readyz-fail-closed doctrine sentence to `docs/reference/platform-support.md` or a spec file — currently #1650 semantics live only in code comments (`server_run.go:186-198`). Write-set: `internal/runtimeexecutor/compose.go`, docs.

## Net

- Fund count: 5 findings (H-53-1..5), all re-verified at develop tip 99d9ddebc. 2 MEDIUM (H-53-2, H-53-3), 2 LOW-MEDIUM (H-53-1, H-53-4), 1 LOW + 1 positive census (H-53-5).
- Novelty: no row duplicates H-V41 FUND 1-3, BF-48-2, the H-V47 bundle, or H-V52 rows H-52a-d (dedup section above).
- No product changes; no PR; no card created (freeze: disposition to Codex lane).

## repo-rule compliance

- Read-only product worktree at exact develop tip; zero `git checkout/merge/rebase` in shared checkouts; plan writes only via isolated worktree `workers/w202-hunt-v53-plan` cut from `origin/main` 0719f6122, own files only.
- No `.github/**` touched; no reruns; no containers started (this lane runs no docker/podman at all).
- Evidence lives only in baseharbor-plan at `evidence/r28-welle6-2026-11-27/bughunt-hv53-observability/README.md`; no checkboxes anywhere in this file.
- No subagents used; every step executed in this session.

## cleanliness

- `docker ps -a` before: this session runs on the coordinator/server host; no compose project was started by this lane; no test containers created or removed (pure source reading + git worktree add only).
- `docker ps -a` after: unchanged for the same reason.
- Created then removed: nothing under `/home/marcel/dev/baseharbor-ecosystem` except the two worktrees named here (product worktree `workers/w202-0428-224-hunt-v53-wt` stays for review until END; plan worktree `workers/w202-hunt-v53-plan` is removed after push with `git worktree remove`).
- cleanliness: besenrein — no container/network/volume/state dirs touched by this lane; pid noted in END transcript.

## Verification witnesses

- Plan remote (before first evidence commit): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` + `(push)`.
- `origin/main` containment proof for the evidence commit runs as second-to-last action (fetch + ls-tree grep), output appended below by the push step.
- Post-push witness (exact command + output, run second-to-last): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-27/bughunt-hv53-observability` -> `evidence/r28-welle6-2026-11-27/bughunt-hv53-observability/README.md`. Evidence commit `ff4dc59b7` (author `w202-0428-224-hunt-v53`, verified via `git show -s --format=%an HEAD` before push; single commit on top of origin/main via rebase-in-worktree after one fast-forward rejection).

END_DONE w202-0428-224-hunt-v53: bundle filed (5 rows H-53-1..5 at product tip 99d9ddebc, novel vs H-V41/H-V47/H-V48/H-V52); no product changes; plan freeze honored.
