# fix-1 (r3) — 0428-123 regvisibility: ListMetrics/List 5-arg on develop head (requestedEnvironment)

- Card: t-20261119-hunt-metrics-registration-visibility-only (0428-123)
- PR: mcpdev80/baseharbor#1693 · zweig `lane-0428-123-regvisibility`
- This run: r3 continuation of the same card (Owner-freigabe: resume, kein zweiter 123-Lauf).
- Session: `c5d271cb` (w123-0428-123-regvisibility, laptop), Modell `worker-ornith1.5-laptop` uber AgentGateway verifiziert.
- Evidence provenance: baseharbor-plan `origin/main`.
- Product develop witness (ls-remote): `fac01c77276ca2bf1e20cd0b7334bda5dd43e353` (2026-11-19 15:07:47 +0100, #1692).
- Base attestation (BASE ATTESTATION): cut-from SHA `deeeb64778b3f6109d3a8e49fd652d490901e89c` (= PR #1693 base-ref = #1685). witnesses: `git merge-base --is-ancestor origin/develop HEAD` → 0 (develop ancestor); `git merge-base --is-ancestor deeeb6477 HEAD` → 0 (base ancestor). develop head is NOT an ancestor of the old candidate head (that is why the hop was required).

## Situation (why r3 is a re-hop, not a product fix)

- develop moved `observability.List` and `observability.ListMetrics` to the 5-arg form with a new `requestedEnvironment string` parameter over #1691 and #1692.
- The candidate branch `lane-0428-123-regvisibility` was cut from the old base `deeeb6477` (4-arg signature). On the new develop head the metrics/observability packages do not compile: `List` is called with 6 args where 7 are required.
- The four in-scope call sites the PR zweig invokes viert-argtig:
  - internal/metrics/prometheus_files.go:240
  - internal/metrics/prometheus_files.go:451
  - internal/metrics/prometheus_verify.go:141
  - internal/metrics/runtime_retirement.go:56
  - plus internal/application/runtime_observability_trace_source_test.go:162 and internal/metrics/regvisibility_regression_test.go:54/127.

## What changed in this run

Candidate `d751c83b` was hopf-monotonically merged onto develop head `fac01c772` (commit `489bf3c0`, no conflict), then two in-scope call sites updated to the 5-arg form:

- internal/observability/registry.go (1 line): `ListMetrics()` internal `List(SignalMetrics, …)` call threaded the new `requestedEnvironment` parameter. Build fix inherited from develop's 5-arg `List` signature — without it the package does not compile. No behavior change: the same environment filter that runs on the outer `List` call now also runs on the app-class sub-call, so no duplicate scrape-targets and no cross-environment exposure are introduced.
- internal/metrics/regvisibility_regression_test.go (2 call sites): pass the registered source's real environment dimension. The source ID `application:metrics:demo:dev:api` has environment dimension `"dev"`; pass `"dev"` as `requestedEnvironment` instead of an empty-string filler so the fail-closed requested-environment filter keeps the load-bearing app-class source.

## Acceptance semantics (verified)

- (a) `ScopeApplication` is the only filter stage: `List` filters app-scoped sources via `SourceMatchesEnvironment(source, requestedEnvironment)` (registry.go ~572); `ListMetrics` surfaces the load-bearing app-class source only for `placement.Scope == ScopeApplication`.
- (b) no duplicate scrape-targets: the app-class source is appended alongside the provider sources; no identical ID is emitted twice (Verification == none sources are skipped).
- (c) no cross-environment exposure: an environment sees only sources whose environment equals `requestedEnvironment` (case-insensitive trim equal; empty requestedEnvironment excludes app-scoped sources).
- The develop-inherited internal `List` call fix is documented here as a finding, not justified by an inline code comment alone: it is required for compilation and is behavior-neutral (the filter already applies at the outer call).

## Verification (all local, same run)

- go build ./... — PASS
- go vet ./internal/metrics/... ./internal/observability/... — PASS
- go test ./internal/metrics/... ./internal/observability/... -count=1 (full suites) — PASS (ok metrics, ok observability)
- go test targeted -run "^Test(Reg|Visib|Metrics|List)" — PASS
- bash scripts/source-readability-audit.sh — PASS (registry.go 785 lines < 800; podman baseline 843 <= 878 ratchet)
- bash scripts/ci-fast-check.sh — PASS (workflow policy PASS, 275 tests OK, no candidate-added validation checks)

## Provenance / candidate

- Merge head: `489bf3c0025d9d2bc2a421d83ea83c09122124ae` on develop `fac01c772`.
- Final candidate: `f3c1bf43bf1a682c29145bf0dade48b319d8e481` pushed to `lane-0428-123-regvisibility` (remote head verified = same SHA).
- Only my two commits on top of develop: the develop-merge and the in-scope fix. No foreign commit in the ancestor list.
- develop commit-time for reference: `2026-11-19T15:07:47+01:00` (vs run start 15:40).

## repo-rule compliance

- Write-set: only registry registration path files (internal/observability/registry.go, internal/metrics/regvisibility_regression_test.go). No `.github/**` touched (Owner scope).
- No subagents (§4.8). One PR carries product code + tests; required checks from base-plan remain the merge requirement; candidate-added checks are advisory.
- Monotonic hop (git merge, no rebase, no force); base attestation witnesses recorded.

## CI run (PR Selected Checks, §4.6)

- To be recorded with terminal PR Selected Checks aggregate after the pushed candidate runs.
