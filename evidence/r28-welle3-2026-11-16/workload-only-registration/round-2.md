# round-2 akte — card 0428-100 (workload-only-registration)

Date: 2026-11-17. Role: worker. Card 0428-100. Corrects Luna batch21 CHANGES REQUESTED on PR #1676.

## Candidate

- PR #1676, card 0428-100: exact head `0b8cecb058efb7dc7678071a3113bc8786890d2d`, base `develop`.
- Status: `isDraft=false` (marked ready with `gh pr ready 1676 --repo mcpdev80/baseharbor`), state OPEN, base=develop.
- Round-1 head was `ea7d0b2f` (early-return workaround only); corrected here.

## (1) Reproduction + snapshot capture on the real deploy path (baseline develop `e6cce9c73`)

Reproducer drove `EnsureProviderFiles` (shared Prometheus provider materialization, `internal/metrics/prometheus_files.go`) for a workload-only app:

```go
m := application.New("workload-only", "dev", false, false, false)
files, err := EnsureProviderFiles(ctx, serviceissuer.New(t), m)
```

Captured `runtime-sources.json` BEFORE the fix:

```json
{"version":"baseharbor.prometheus-runtime-sources/v1","project":"bh-local-shared","scope":"shared","sources":[]}
```

Zero sources. The registration call site is `internal/application/runtime_observability.go`
`reconcileManagedRuntimeObservability` (called by `EnsureRuntime`, `runtime_postgres.go:131`). For a
workload-only app it ran but registered only postgres/valkey application-provider sources — there were none — so
nothing was written to the observability registry. `EnsureProviderFiles` then read the registry via
`observability.ListMetrics` (`internal/metrics/prometheus_files.go:234`) and wrote an empty snapshot.

Confirmed on develop that `VerifyProviderSourcesAt` at `e6cce9c73` already returns nil on empty `ListMetrics`
(`if err != nil || len(sources) == 0 { return err }`) — the round-1 "fail-closed" was not reproducible (Luna
finding c). The real gap is the empty snapshot / absent registration, not a verifier crash.

## (2) Fix — real deploy-path registration

`internal/application/runtime_observability.go`:

- `reconcileManagedRuntimeObservability` now calls new `reconcileApplicationMetricsSource(m, project, logsEnabled, tracesEnabled)` after the postgres/valkey reconciliation.
- New function registers **one application-scoped, application-provider metrics source**
  (`prometheus:<project>`, `Class=SourceApplicationProvider`, `Scope=ScopeApplication`, `OwnerApplication=m.Name`,
  `Target=runtime://<project>/workload`, `Path=/metrics`, `Protocol=openmetrics`) via the same direct `SignalSource`
  + `ReconcileSignals` construction that `ReconcileRuntimeComponentObservability` uses
  (`internal/application/runtime_component_observability.go:97-168`). Satisfies `SignalSource.Validate()`
  (network + absolute openmetrics path) without fabricating a scrape backend.
- Registered only when `MetricsPolicy.Enabled && MetricsPolicy.Collect[MetricsSourceApplicationProvider]`; disabled
  policy is a no-op, never fabricates a target. Preserves fail-closed for apps that declare sources but
  materialize none (existing guard in `VerifyProviderSourcesAt` line 142 untouched). No early-return workaround in
  the verifier, no second resolver.

Root cause: a workload-only app (no SQL/Valkey, no runtime broker, no runtime metrics permission) reached
`EnsureRuntime` but registered zero observability sources because registration was gated on service backends and on
the broker (`RequiresRuntimeBroker` = Secrets or Runtime.Permissions). The new hook closes that gap for the owning app.

## (3) Regression tests (CI-selected package, exact test IDs)

`internal/metrics` and `internal/application`, covered by CI `go test ./contracts/... ./internal/... ./spec/...`
(`.github/workflows/ci.yml`); no new trigger added (package already in the selected group).

- `TestReconcileManagedRuntimeObservabilityWorkloadOnlyRegistersSource` (`internal/application/observability_workload_registration_test.go`) — drives the real deploy hook; asserts the app's own source is registered (positive).
- `TestWorkloadOnlyRegistersSharedSourceOnDeploy` (`internal/metrics/workload_only_source_test.go`) — materializes the shared provider via `EnsureProviderFiles`; asserts the snapshot carries `prometheus:<project>` owned by the app (deploy-path positive).
- `TestServiceAppStillRegistersOnDeploy` (`internal/metrics/workload_only_source_test.go`) — asserts a service app still registers through the same path (compatibility regression).

## (4) Witnesses

- Commit `0b8cecb058efb7dc7678071a3113bc8786890d2d` on `lane-0428-100-workload-only-registration` (base `develop`).
- Local: `go test ./internal/application/ ./internal/metrics/` PASS; `gofmt -l` clean; `go build ./...` ok; `go vet` ok.
  (disk-backed TMPDIR under `workers/.tmp/wt100-tmp`; `/tmp` is tmpfs at ~80% and `go test` failed there with disk quota).
- CI run **44007626272** on exact head `0b8cecb05`, event `pull_request` (triggered after marking the PR ready):
  overall `completed/success`. Key jobs `PR Selected Checks`, `PR · Go unit · packages`, `cli-0..cli-3`, `owner`
  all `success`. No failure. Run started from the push and monitored to terminal (Eigenes-Run-Pflicht).

## Repo-rule compliance

- Write-set scoped to `internal/application/runtime_observability.go` + two new test files. No `#1665` paths touched
  (`app_status_result.go`, `perses_infra_dashboards*.go`, `perses_prometheus_datasource.go`).
- No `.github/**` edit, no merge, no ready_for_review beyond the single required `gh pr ready`, no force-push, no subagent (§4.8).
- Evidence only in `baseharbor-plan`; no product-repo writes. Todos in `workers/todos/0428-100-workload-only-registration.json`.

## Return for review

No stop criteria hit. Real deploy reproducer showed the claimed failure (empty snapshot); fix registers a source
through the existing deploy path; source contract resolved by tracing the proven
`ReconcileRuntimeComponentObservability` construction. #1665 paths untouched.

END — worker round-2 complete; PR #1676 ready, head `0b8cecb05`, CI run 44007626272 success. Awaiting Luna re-review on new exact head.
