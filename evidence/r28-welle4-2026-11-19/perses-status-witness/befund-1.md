# Befund 1 — perses status backend-witness: data-path audit

Card: t-20261119-r28-perses-status-backend-witness (0428-142)
Worker: laptop-142-statuswitness
Base SHA: 7ee6f817dbff5a238bbc651315d6d76b3819fc91 (contains #1616 c296086c Loki datasource adapter)

## Data path (what exists)

- `internal/logs/loki_datasource.go` already computes the per-backend backend-witness.
  - `persesLokiDatasourceQuery` (line 323) returns `matchedAny bool` after running one Loki stream query per authorized provider log source.
  - `buildPersesLokiDatasourceWithProbe` (line 206) maps `verified` -> `Reachability` one of `PersesLokiReachabilityUnverified` / `PersesLokiReachabilityVerified`.
  - `BuildPersesLokiDatasource(m)` (line 188) is the probe-less build path used by production; always `unverified` unless a probe observed a match.
  - `VerifyPersesLokiDatasourceHealth` (line 360) is the fail-closed real-query path.

## The gap (product-loch, not a round-fehler)

The CLI `perses status` command (`cmd/baha/perses_lifecycle.go`, `persesStatusCommand` line 73,
`reportPersesSurfaceStatus` line 213) renders only `persesStatusResult{State, Enabled, Version}`:
human output `fmt.Fprintf(out, "Perses state: %s\n", result.State)` (line 91). `State` comes from
`application.PersesLifecycleStatus` -> `capability.PersesStatusNow`, i.e. manifest declaration truth
(`not_configured` / `configured_unverified`). It never reports per-source backend witness
(matched / no-match / unreachable) nor a source-id.

`cmd/baha/app_status_result.go` carries `Perses *capability.PersesStatus` (manifest-only) and
`HostContainersDashboards` (host/container catalog). The catalog is built via the one-argument
face `metricsprovider.PersesHostDashboardAvailability(resolvedHostSignalStatus)` (lines 152, 255),
which passes a zero `PersesBackendSignalWitness{}`. `persesHostDashboardAvailabilityWitnessed`
(lines 563-574) then answers `loki` from `witness.LokiProven` and `tempo` from `witness.TempoProven`
— both always false with the zero witness — so Loki and Tempo report "unavailable" with a reason
naming their own missing signal (lines 579-590). The one-argument CLI face carries no Loki/Tempo
signal input, so Loki and Tempo stay unavailable even though `loki_datasource.go` already decides
per source. This is exactly the defect the mission describes.

## Acceptance target (from card)

- `perses status` (and the status face) must name, per observability signal, one of the three states
  (backend reached AND stream matched / reached but no match / not reachable) WITH a source-id, instead
  of the blanket "unverified"/"unavailable".
- The three label-witness code locations (internal/logs/render.go:145/163/296, internal/telemetry/otlp_payload.go:28,
  internal/metrics/perses_dashboards_hosts.go:243-245) already carry the source-id/label material.
- The one-argument API of `app_status_result.go` must NOT be changed signature-wise; the witness must be
  wired from the already-existing `loki_datasource.go` decision.

## Scope boundary (from mission Schreibmenge, before first line)

`git diff --name-only origin/develop` is EMPTY (clean tree) — proves the working tree equals origin/develop
before editing. Allowed edits: `cmd/baha/app_status_result.go` + `cmd/baha/app_status_result_test.go`
(and only the status-output file in cmd/baha/ if the status-text lives there). Forbidden (other lanes):
`internal/capability/perses.go`, `cmd/baha/machine_coverage.go`, `internal/serviceaccess/perses_config_render.go`,
`internal/metrics/prometheus_*.go` (0428-089 #1599, 0428-123 #1693).

## Finding

The real per-backend witness lives in `internal/logs/loki_datasource.go` (`matchedAny`, `Reachability`).
The CLI status face consumes only manifest truth. Implementation must (a) surface, per observability
signal, the three backend-witness states with a source-id, (b) consume the loki_datasource decision
without changing its contract, (c) keep the one-argument face signature in app_status_result.go and
wire a per-backend witness from the runtime/log-signal registry.
