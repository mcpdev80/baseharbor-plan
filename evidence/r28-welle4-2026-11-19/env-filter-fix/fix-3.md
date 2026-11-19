# 0428-121 — Route-2 FAIL-CLOSED environment filter (fix-3)

Status: **DONE** — CI terminal SUCCESS, pushed to `lane-0428-efilter`.

## What was fixed

Route-2 first commit `4f4b3d7a6` made `SourceMatchesEnvironment` *compare*
the source's derivable environment against the caller's `requestedEnvironment`
(case-normalised). That was functionally correct — the FAIL-OPEN leak was
closed. But it failed the repo's own source-readability gate: `registry.go`
was **877 lines**, over the repo limit of 800.

fix-3 (`d1fcfdf6b`) extracts the environment-derivation helpers into a
dedicated `internal/observability/environment.go` so `registry.go` drops to
**731 lines**. Behaviour and API are unchanged; only the file cut changed.

## Evidence (machine-witnessed)

- **CI run**: `44487090323`, head_sha `d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e`,
  head_branch `lane-0428-efilter`, created `2026-11-19T08:22:46Z`,
  conclusion **success**.
  - Every required PR job SUCCESS: `PR · Source format`,
    `PR · Validation · go-build`, `PR · Validation · go-vet`,
    `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,packages}`,
    `PR · Validation · identity-provider-package-tests`, `PR · Exact Candidate`,
    `PR · Runner Interface`, `PR · Demo Pin`, `PR · Focused Python`.
  - `PR · Source format` was the ONE job that FAILED on `4f4b3d7a6`
    (run `44485086467`): its own log quoted the cause verbatim —
    `source readability: internal/observability/registry.go has 877 lines
    (limit: 800)`. It passes on `d1fcfdf6b`.
- **Local re-check after extraction**:
  - `gofmt -l .` → empty (clean).
  - `bash scripts/source-readability-audit.sh` → all three checks PASS
    (Go file size `PASS (<= 800 lines)`, function span `PASS`, regression
    ratchet `PASS`), exit 0.
  - `go build ./...` → exit 0.
  - `go vet ./internal/observability/` → exit 0.
  - `go test ./internal/observability/ ./internal/metrics/ ./internal/logs/
    ./internal/application/ ./internal/identityprovider/` → all `ok`.
- `wc -l internal/observability/*.go`:
  - `environment.go` 157, `registry.go` 731, `registry_test.go` 399,
    `envfilter_route2_test.go` 269.

## Commit receipts

- `d1fcfdf6b` `refactor(0428-121 r2b): move environment derivation into environment.go`
  — 2 files, +157/−147; `environment.go` created, `registry.go` 877→731 lines.
- Parent history (monotone, no rebase):
  - `d1fcfdf6b` ← `4f4b3d7a6` ← `da76c5cf9` (develop, #1696).
- `git merge-base --is-ancestor origin/develop HEAD` → YES (clean monotone hop).
- Push: `4f4b3d7a6..d1fcfdf6b HEAD -> lane-0428-efilter`
  (`--force-with-lease`; lane-exklusiv, single owner).

## The comparing rule (unchanged by fix-3)

```go
func SourceMatchesEnvironment(source SignalSource, requestedEnvironment string) bool {
	requestedEnvironment = strings.TrimSpace(requestedEnvironment)
	environment, ok := SourceEnvironment(source)
	if !ok {
		return false
	}
	return strings.ToLower(environment) == strings.ToLower(requestedEnvironment)
}
```
Central guard in `List` (registry.go, app-caller only):
```go
if placement.Scope == capability.ScopeApplication && source.Scope == capability.ScopeApplication && !SourceMatchesEnvironment(source, requestedEnvironment) {
	continue
}
```
`requestedEnvironment` is threaded from the owning application's
`manifest.Environment` through `List` / `ListLogs` / `ListTraces` /
`ListMetrics` / `ListApplicationMetrics`.

## W-belege (file:line) — requestedEnvironment threading

| Site | file:line | value passed |
| --- | --- | --- |
| provider logs | `cmd/baha/app_logs.go:140` | `prepared.manifest.Environment` |
| provider traces | `cmd/baha/app_traces.go:249` | `prepared.manifest.Environment` |
| runtime metrics | `internal/metrics/prometheus_files.go:240` | `m.Environment` |
| shared-runtime metrics | `internal/metrics/prometheus_files.go:452` | `m.Environment` |
| verify provider metrics | `internal/metrics/prometheus_verify.go:141` | `m.Environment` |
| verify app metrics | `internal/metrics/prometheus_verify.go:152` | `m.Environment` |
| runtime retirement metrics | `internal/metrics/runtime_retirement.go:56` | `m.Environment` |
| override logs | `internal/logs/overrides.go:105` | `m.Environment` |
| registration logs | `internal/logs/registration.go:35` | `providerLogSources(p, regs, m.Environment)` ← `lifecycle.go:88`, `state.go:169` (both hold `m`) |

## Regression guard (`envfilter_route2_test.go`, 6 cases, all PASS)

- `TestRoute2SameAppProdStageProdCaller` — same app in prod AND stage: prod
  caller yields only the prod source, stage caller only the stage source.
- `TestRoute2EmptyRequestedEnvironmentFailsClosed` — `""` requested env
  excludes every app-scoped source (explicit fail-closed).
- `TestRoute2ProviderEnvMatch` — provider with canonical project name visible
  to the matching env caller, excluded from a mismatched env caller.
- `TestRoute2UnresolvableAppSourceFailsClosed` — bare-ID + hyphenated
  (`bh-local-demo-prod-west`) + reserved-token (`prometheus`) all fail closed.
- `TestRoute2MutationEnvDropExcludes` — mutation control: changing the caller's
  requested env from `prod`→`stage` drops the prod source (exclusion is
  structural, not accidental).
- `TestRoute2SharedSourceStaysVisibleForSharedCaller` — environment-agnostic
  shared source stays visible to a shared-platform caller.

## Note on full-suite failures (NOT introduced by this change)

The remaining `go test ./...` failures (`cmd/baha`, `internal/controlplaneruntime`,
`internal/database`, `internal/development`) are environment/infra — missing
`BASEHARBOR_TEST_DATABASE_URL`, runtime-executor not configured, native git
archive OOM-killed under pressure. They fail identically on develop
(`da76c5cf9`) and are unrelated to the route-2 change.
