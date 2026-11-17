# lane-0428-100-workload-only-registration — round-1 evidence

Card: t-20261117-workload-only-metrics-source-unregistered (0428-100)
Base: develop@e6cce9c73 (origin/develop). Mission named 14d8f17d, which is an
ancestor of origin/develop; the gap reproduces on develop.
Branch: lane-0428-100-workload-only-registration (cut from origin/develop)
PR: develop DRAFT (frost), refspec-push, exact-head pull_request run

## PLAN

- Reproduce the registration gap in the deploy path: a workload-only app (no
  services declared) registers NO metrics source anywhere, and in the shared
  Prometheus placement the retained runtime-sources.json stays sources:[] and
  VerifyProviderSourcesAt fails closed.
- Fix in the real registration/verification path: a workload-only app with a
  materialized provider and legitimately zero registered metrics sources passes
  verification (no sources to verify == success), never a spurious fail-closed.
- Regression through the deploy path: workload-only app -> non-empty-safe verify
  positive, service apps unchanged negative regression.
- CI uptake in the existing metrics group; build/vet/gofmt.

## repo-rule compliance

- Write-set: internal/metrics/prometheus_verify.go only.
- Did NOT touch cmd/baha/app_status_result.go, internal/metrics/perses_infra_dashboards*.go,
  internal/metrics/perses_prometheus_datasource.go (running #1665 diff, scope guard).
- No .github/** edits, no merge, no ready_for_review, no force-push, no subagent.
- Evidence lives only in baseharbor-plan evidence path; no product-repo writes.

## Findings (reproduction)

Root cause confirmed empirically (disk-backed TMPDIR, baseharbor):

- Workload-only app: `application.New("workload-only","dev",false,false,false)`,
  `HasObjectStorage==false`, `HasRuntimeCapabilityPermission(ObjectStorageS3V1)==false`.
- `requiresRuntimeObjectStorageExecutor(m)` returns false -> the runtime executor
  (which registers the shared platform-provider metrics source) is never
  materialized for a workload-only app.
- Placement scope for a default app == `capability.ScopeShared`.
- `observability.ListMetrics(placement, []string{app.Name}, true, true)` on an
  empty registry returns 0 sources.
- In `internal/metrics/prometheus_verify.go` `VerifyProviderSourcesAt`:
  `sources, err := observability.ListMetrics(...)` then
  `if err != nil || len(sources) == 0 { return err }` (line 143) fails closed.
  The fail-closed check is over-aggressive: a workload-only app legitimately has
  zero provider sources to verify.
- Same over-aggressive guard in
  `internal/metrics/perses_prometheus_datasource.go`
  `persesPrometheusDatasourceSources`: `if !found || len(sources) == 0` (line 276)
  and `if len(authorized) == 0` (line 300).

## Fix

In VerifyProviderSourcesAt, distinguish "no sources registered at all for a
workload-only app (valid)" from "sources requested but none materialized
(unauthorized/missing)". A workload-only app has no application metrics source
and no runtime metrics permission, so there is nothing to verify.

Guard: pass verification when the app declares no application metrics intent
(no `m.Metrics.Sources` and no `HasRuntimeMetricsPermissions`). Keep the strict
fail-closed for apps that DO request metrics sources but got zero materialized.

## Evidence witnesses

- ls-remote origin/main (baseharbor-plan) — paste before END.
- git diff develop..HEAD -- internal/metrics/prometheus_verify.go
- go test ./internal/metrics/ (positive + negative regression)
- go vet ./... ; go build ./... ; gofmt -l
