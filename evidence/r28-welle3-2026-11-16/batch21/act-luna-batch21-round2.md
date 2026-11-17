# CODEX-REVIEW FOLLOW-UP / ROUND-2 AKTE — 0428-100

Date: 2026-11-17. Role: Worker. Card 0428-100 (workload-only-registration).
Corrects Luna batch21 CHANGES REQUESTED on PR #1676, head `ea7d0b2f`.

## 1. Candidate before this work

- PR #1676, card 0428-100: `ea7d0b2fde78f2fc6e7efc1bb9929b289dbe28cd`, base `develop`, DRAFT (`isDraft=true`).
- Round-1 candidate added only an early-return guard in `VerifyProviderSourcesAt` (lines 137–144) and direct-verifier tests. Luna found this bypasses verification instead of registering a source through the real deploy path.
- Round-1 CI run [44000884721] (exact head `ea7d0b2f`) completed SUCCESS.

## 2. Reproduction on the real deploy path (exact develop baseline `e6cce9c73`)

Reproducer drives `EnsureProviderFiles` (the shared Prometheus provider materialization) for a workload-only app:

```go
m := application.New("workload-only", "dev", false, false, false)
files, err := EnsureProviderFiles(ctx, serviceissuer.New(t), m)
```

Captured `runtime-sources.json` BEFORE the fix:

```json
{"version":"baseharbor.prometheus-runtime-sources/v1","project":"bh-local-shared","scope":"shared","sources":[]}
```

Zero sources. The registration call site that emits a source lives in `internal/application/runtime_observability.go`
`reconcileManagedRuntimeObservability` (called from `EnsureRuntime`, `runtime_postgres.go:131`). For a workload-only app
this function ran but registered **only** postgres/valkey application-provider sources — there were none — so no metrics
source was ever written to the observability registry. `EnsureProviderFiles` then reads the registry via
`observability.ListMetrics` (`internal/metrics/prometheus_files.go:234`) and writes an empty snapshot.

Confirmed on develop that `VerifyProviderSourcesAt` at `e6cce9c73` already returns nil on an empty `ListMetrics` via
`if err != nil || len(sources) == 0 { return err }` — the round-1 "fail-closed" was not reproducible (Luna finding c).
The real gap is the empty snapshot / absent registration, not a verifier crash.

## 3. Fix — real deploy-path registration

`internal/application/runtime_observability.go`:

- `reconcileManagedRuntimeObservability` now calls a new `reconcileApplicationMetricsSource(m, project, logsEnabled, tracesEnabled)` after the postgres/valkey reconciliation.
- `reconcileApplicationMetricsSource` registers **one application-scoped, application-provider metrics source**
  (`prometheus:<project>`, `Class=SourceApplicationProvider`, `Scope=ScopeApplication`, `OwnerApplication=m.Name`,
  `Target=runtime://<project>/workload`, `Path=/metrics`, `Protocol=openmetrics`) via the same direct `SignalSource`
  + `ReconcileSignals` construction that `ReconcileRuntimeComponentObservability` uses (`runtime_component_observability.go:97-168`). This satisfies the metrics-source contract (`SignalSource.Validate()` requires network + absolute openmetrics path) without fabricating a scrape backend.
- Registered **only** when `MetricsPolicy.Enabled && MetricsPolicy.Collect[MetricsSourceApplicationProvider]`; a disabled policy is a no-op and never fabricates a target. This preserves fail-closed for apps that declare sources but materialize none (the existing guard in `VerifyProviderSourcesAt` line 142 is untouched).

Root cause: a workload-only app (no SQL/Valkey, no runtime broker, no runtime metrics permission) reached
`EnsureRuntime` but registered zero observability sources because registration was gated on service backends and on the
broker (`RequiresRuntimeBroker` = Secrets or Runtime.Permissions). The new hook closes that gap for the owning app.

## 4. Regression tests (CI-selected package, exact test IDs)

All in `internal/metrics` and `internal/application`, covered by CI `go test ./internal/...` (`.github/workflows/ci.yml`,
`go test ./contracts/... ./internal/... ./spec/...`). Do not add a separate trigger — these packages are already in the
selected group.

- `TestReconcileManagedRuntimeObservabilityWorkloadOnlyRegistersSource` (`internal/application/observability_workload_registration_test.go`) — drives the real deploy hook and asserts the app's own source is registered (positive).
- `TestWorkloadOnlyRegistersSharedSourceOnDeploy` (`internal/metrics/workload_only_source_test.go`) — materializes the shared provider via `EnsureProviderFiles` and asserts the snapshot carries `prometheus:<project>` owned by the app (positive deploy-path assertion).
- `TestServiceAppStillRegistersOnDeploy` (`internal/metrics/workload_only_source_test.go`) — asserts a service app still registers its source through the same path (compatibility regression).

## 5. Evidence witnesses (this work)

- Commit `0b8cecb058efb7dc7678071a3113bc8786890d2d` on `lane-0428-100-workload-only-registration` (base `develop`).
- Local: `go test ./internal/application/ ./internal/metrics/` → PASS (disk-backed TMPDIR under `workers/.tmp/wt100-tmp`; `/tmp` is tmpfs at ~80% and `go test` failed with disk quota there).
- CI run [44006498757] on exact head `0b8cecb05`, event `pull_request`: overall `completed/success`. Go draft jobs
  `PR · Draft Go · packages` (unit tests), `cli-0..cli-3` completed SUCCESS. Draft-policy matrix jobs are skipped by
  design (draft PR). Run started from the push; monitored to terminal (Eigenes-Run-Pflicht).

## 6. PR / branch state

- PR #1676: `isDraft=true`, `state=OPEN`, `base=develop`, `head=lane-0428-100-workload-only-registration`. Verified before AND after push (still draft, isDraft unchanged).
- Branch head after push (ls-remote): `0b8cecb058efb7dc7678071a3113bc8786890d2d`.
- No `.github/**` edit, no merge, no ready_for_review, no force-push, no subagent (§4.8).

## 7. Repo-rule compliance

- Go: `gofmt -l` clean; `go build ./...` ok; `go vet ./internal/metrics/ ./internal/application/` ok; local `go test` PASS.
- Write-set scoped to `internal/application/runtime_observability.go` + two new test files. No `#1665` paths touched
  (`app_status_result.go`, `perses_infra_dashboards*.go`, `perses_prometheus_datasource.go`).
- Evidence only in `baseharbor-plan`; no product-repo writes.
- Todos in all three places (evidence PLAN list, `workers/todos/0428-100-workload-only-registration.json`, GUI-todos `0428-100-*.json`).

## 8. STOP / return for review

No stop criteria hit. The real deploy reproducer showed the claimed failure (empty snapshot) and the fix registers a
source through the existing deploy path. The source contract was resolved by tracing the proven
`ReconcileRuntimeComponentObservability` construction. #1665 paths untouched.

END — worker round-2 complete; PR #1676 head `0b8cecb05`, draft, CI run [44006498757] success. Awaiting CODEX-REVIEW (Luna) re-review on the new exact head.
