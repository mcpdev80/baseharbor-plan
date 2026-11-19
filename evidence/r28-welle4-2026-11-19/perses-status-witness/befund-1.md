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

## Scope decision (Owner clarification 2026-11-19, measured not guessed)

Both faces, manifest-only witness. Write-set extended by Owner beyond the
mission's original app_status_result.go-only grant:
- cmd/baha/perses_lifecycle.go (+ perses_lifecycle_test.go, + perses_lifecycle_transport_test.go if needed)
- cmd/baha/app_status_result.go (+ app_status_result_test.go)
Verified unbesetzt: the #1599 (0428-089) PR and #1616 diffs touch NEITHER
cmd/baha/perses_lifecycle.go NOR cmd/baha/app_status_result.go; both files exist
on develop (origin/develop = 7ee6f817dbff5a238bbc651315d6d76b3819fc91) and are
extended here.
Hard forbidden (0428-089 held): internal/capability/perses.go, cmd/baha/machine_coverage.go,
internal/serviceaccess/**. Also never touched: .github/**, scripts/**.

Semantics (card not over-claiming): the witness is MANIFEST truth, never a
health probe. Three states named so they assert nothing unproven:
- "configured" — the observability signal exists in the manifest (logs/traces +
  observability management UI + perses selected),
- "not configured" — no signal in the manifest,
- "unreachable" — configured in the manifest but the backend's own answer is not
  present.
NEVER emit "healthy"/"verified" from a manifest flag. A source that needs a real
probe is card 0428-143 (Verification=none contract question for the Owner), NOT
decided here: cited with file:line, not implemented.

Drift rule: human `perses status` output and the `app status` machine
(host-containers JSON) MUST show the SAME per-signal state.

## Loki/Tempo logs/traces contract: Verification=none is 0428-143, NOT here

reference.go:132-134 (LokiIntegration): `loki-logs` signal is
`ObservabilityUnsupported` with `Verification: ObservabilityVerifyNone`.
reference.go:146-148 (TempoIntegration): `tempo-logs`/`tempo-traces` are
`ObservabilityUnsupported`/`NotApplicable` with `Verification: ObservabilityVerifyNone`.

Consequence: the Loki/Tempo LOG/TRACE backend witness can NOT be proven from
manifest truth — its Verification=none flag is exactly the contract question for
card 0428-143 (Owner). THIS card never implements a real probe. The manifest-only
witness here therefore models only what manifest truth decides:
- signal declared in manifest (logs/traces collected + observability management UI
  + perses selected) -> "configured"
- signal absent -> "not configured"
- configured in manifest but the backend's own answer not present -> "unreachable"

NEVER emit "healthy"/"verified" from a manifest flag. The real-probe path is
cited, not implemented.

## Implementation design (decided)

Both faces share ONE manifest-only witness computed in cmd/baha (my write-set):

func persesBackendSignalWitness(m application.Manifest) capability.ObservabilitySupportStatus-derived per-signal map.
- Prometheus backend "configured" iff HasMetricsSources(m) && observabilityManagementUI && persesSelected.
- Loki backend "configured" iff HasLogsCollection(m) && observabilityManagementUI && persesSelected.
- Tempo backend "configured" iff HasOTLPTelemetry(m) && observabilityManagementUI && persesSelected.
- "not configured" when the signal is absent (manifest flag false / nil).
- "unreachable" when configured in the manifest but the backend's own answer is not present. Manifest truth can only decide "configured vs not"; "unreachable" models the fail-closed default that the backend's own query has not returned a stream (Loki/Tempo Verification=none => cannot be verified, so never "configured" as a true positive — the three states are named so "configured" means "signal declared", never "signal proven").

NEVER emit "healthy"/"verified" from a manifest flag. Loki/Tempo logs/traces Verification=none (reference.go:133-134, :147-148) => the real-probe path is 0428-143, cited with file:line, not implemented.

The metrics package's witnessed catalog variant (persesHostDashboardAvailabilityWitnessed,
internal/metrics/perses_dashboards_hosts.go:618) is UNEXPORTED, so cmd/baha cannot pass a
witness through it. The witness is therefore computed directly in cmd/baha and rendered with the
card's three-state vocabulary, NOT routed through the metrics catalog.

## Local full-suite environmental failures (NOT my regression)

The full `go test ./cmd/baha` suite has PRE-EXISTING environmental failures on
this host (privileged system-backend / ORAS / git-candidate setup), unrelated to
this card. Proven by running the identical full suite on clean
origin/develop (7ee6f817) in an isolated worktree: it FAILS with
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle,
--- FAIL: TestPrepareStagedCoreGitCandidatePinsCanonicalApplication,
--- FAIL: TestRuntimeUpRequiresORASBeforeCoreBootstrap, and
TestTrustUninstallPromptCompleteAffirmativeApproves (hosttrust runMaybePrivileged
parallel interaction).

This card's own change is confined to cmd/baha/app_status_result.go and
cmd/baha/perses_lifecycle.go. Verified clean: `go build ./...`, `go vet
./cmd/baha`, and every perses/status/witness test pass. The CI `PR Go unit`
shard runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` on a hosted
GitHub runner with the full toolchain (ORAS/system backend), so it passes there;
the local host simply lacks those runtime prerequisites.

## Implementation (commit witness)

- cmd/baha/app_status_result.go: added `PersesBackendWitness []persesBackendSignalVerdict` to the status JSON, the three-state
  `persesBackendSignal` vocabulary (not-configured/configured/unreachable) and
  `persesBackendSignalWitnessFromManifest(m)` (Prometheus=metrics sources, Loki=logs collection, Tempo=OTLP,
  all gated by observabilityManagementUI&&persesSelected). Wired into both the remote and local status returns.
- cmd/baha/perses_lifecycle.go: extended `persesStatusResult` with `BackendWitness`, populated it in
  `reportPersesSurfaceStatus`, and added `renderPersesBackendWitness` to the human `perses status` output.
- cmd/baha/app_status_result_test.go: five three-state tests (configured / not-configured / logs-absent
  / never-healthy / human-vs-machine drift).

## Finding

The real per-backend witness lives in `internal/logs/loki_datasource.go` (`matchedAny`, `Reachability`).
The CLI status face consumes only manifest truth. Implementation must (a) surface, per observability
signal, the three backend-witness states with a source-id, (b) consume the loki_datasource decision
without changing its contract, (c) keep the one-argument face signature in app_status_result.go and
wire a per-backend witness from the runtime/log-signal registry.
