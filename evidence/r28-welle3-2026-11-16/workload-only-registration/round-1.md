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

Root cause: a workload-only app (no SQL/cache/secrets/object-storage/capabilities)
never materializes the runtime executor (`requiresRuntimeObjectStorageExecutor`
returns false), so the shared platform-provider metrics source that would populate
`runtime-sources.json` is never registered. In the shared Prometheus placement the
retained snapshot stays `sources:[]`.

- Workload-only app: `application.New("workload-only","dev",false,false,false)`,
  `HasObjectStorage==false`, `HasRuntimeCapabilityPermission(ObjectStorageS3V1)==false`.
- `requiresRuntimeObjectStorageExecutor(m)` returns false -> executor never runs.
- Placement scope for a default app == `capability.ScopeShared`.
- `observability.ListMetrics(placement, []string{app.Name}, true, true)` on an
  empty registry returns 0 sources.
- `internal/metrics/prometheus_verify.go` `VerifyProviderSourcesAt`:
  `sources, err := observability.ListMetrics(...)` then the strict guard
  `if err != nil || len(sources) == 0 { return err }` (line ~143) is the
  fail-closed site. The datasource builder at
  `internal/metrics/perses_prometheus_datasource.go` `persesPrometheusDatasourceSources`
  (line 276, only present on the 0428-082 lane; NOT in develop) carries the same
  over-agmissive guard with the mission's exact message "no materialized
  Prometheus sources".
- Empirically confirmed on develop: an empty registry yields 0 sources; a
  workload-only app must verify with zero sources (nothing to verify), while an
  app that DECLARES application metrics sources but materializes none must still
  fail closed.

## Fix

In `VerifyProviderSourcesAt` (internal/metrics/prometheus_verify.go), add an
explicit workload-only early return BEFORE the strict guard: when the app
declares no metrics sources and has no runtime metrics permission, there is no
source to verify, so return nil (valid success). The strict fail-closed guard
below is preserved for apps that request application metrics sources but
materialize none. Minimal, one-file, in the real registration/verification path
(no second resolver, no retrospective snapshot-baking route).

Verified: `go test ./internal/metrics/` passes (4 new workload tests + all
existing), `go test ./internal/application/ ./internal/observability/` pass,
`go build ./...`, `go vet ./internal/metrics/`, `gofmt -l` clean.

## CI uptake

`internal/metrics/prometheus_verify.go` is covered by CI "Source & Quality"
(job at .github/workflows/ci.yml:124, `go test ./... ./internal/... ./spec/...`),
which runs the new tests in `internal/metrics/prometheus_verify_workload_test.go`
automatically. No .github/** change needed (Owner scope).

## END state (0428-100)

- Branch: lane-0428-100-workload-only-registration, HEAD ea7d0b2fd, develop
  ancestor, only my commit on the branch.
- PR #1676, base develop, head lane-0428-100-workload-only-registration.
  isDraft=true BEFORE and AFTER the push cycle (Owner/Frost directive;
  ready_for_review forbidden).
- CI run 44000884721 completed/success. Go unit (cli-0..3, packages, owner),
  go-build, go-vet, Source format, Workflow policy all pass.
- Evidence published to baseharbor-plan origin/main:
  evidence/r28-welle3-2026-11-16/workload-only-registration/round-1.md
  blob 2d676422c59 (verified present on origin/main before END).
- Write-set: internal/metrics/prometheus_verify.go + new test file only.
  Did NOT touch cmd/baha/app_status_result.go,
  internal/metrics/perses_infra_dashboards*.go,
  internal/metrics/perses_prometheus_datasource.go (scope guard).
- Worktree cleaned, compose/projects down.
