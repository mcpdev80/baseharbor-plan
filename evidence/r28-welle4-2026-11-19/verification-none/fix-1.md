# fix-1 — Prometheus composition: explicit 'null effective targets after composition' counter

- Card: `t-20261119-hunt-metrics-verification-none-blind` (0428-124), hunt-918 Befund 6
- Role: Worker (session worker-ornith1.5)
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Base develop head: `ec592fd3852328439ae9de8763c816ae9dd88dcc` (ls-remote witness in END)
- Branch: cut from `ec592fd3852328439ae9de8763c816ae9dd88dcc`, ancestry proven in END

## PLAN

- Read hunt-918 context, claim card, ls-remote develop, cut branch from exact head
- Red regression: composition with a single verification:none source produces zero effective scrape-targets with no counter/state message
- Fix: documented counter at the composition point reporting 'null effective targets after composition' with reason; do NOT remove the correct verification:none skips
- Regression: existing workload-only/verification tests still pass; new counter test passes with the explicit state message
- build, vet, gofmt; monotonous Hopf exact-head run to terminal; push; wire CI for the new metrics test
- Evidence + END + GUI todos

## Finding (befund 6, red)

- The Prometheus provider composition in `internal/metrics/prometheus_files.go` skips every `verification:none` metrics source in TWO places:
  - `syncProviderTargets` (line 65) — `if source.Verification == capability.ObservabilityVerifyNone { continue }` creates no file_sd scrape-target
  - `providerMetricNetworks` (line 163) — `if source.Verification == capability.ObservabilityVerifyNone { continue }` adds no scrape network
- Each individual skip is CORRECT (a workload emits to the OTLP/Tempo receiver, not a Prometheus scrape endpoint). The commit `bcae1e8c1261c9e44db03fe285a5d090c532dfcd` added these skips.
- The blind spot (befund 6): the composition has NO counter/assertion. When every provider source is `verification:none` (or there are no backend sources at all), the composition silently yields ZERO effective scrape-targets with no explicit state message. An operator sees no counter/warning that the Prometheus placement has no active scrape targets and why.

## Expected (green)

- The composition reports an explicit state: 'null effective targets after composition' with the reason (all sources verification:none), as a counter/warning, NOT as a hard failure that removes the correct skips.

## Scope boundaries (mission + card)

- Touch only the Prometheus composition in `internal/metrics/` (target/network composition + counter).
- Do NOT touch: `internal/observability/registry.go` (registry, ~123), env-filter, writer/log-source (~122), consent-folds (119r3 running).
- Do NOT remove the `verification:none` skips (they are correct).
- No `.github/**` edits (Owner scope). No merge, no force, no subagent.

## CI mapping (verified via `scripts/pr-gate-plan.py`)

- Diff-base: `ec592fd38` (develop) -> `84911f99e` (branch head), single-parent, `--integration == head`.
- `coverage_status: resolved`, `broad_required: false`.
- `selected_gates: []` (pure Go logic, no native runtime impact).
- `required_validation_checks` (what CI actually runs at `84911f99e`):
  - `go-build` => `go build ./...`
  - `go-unit-tests` => `go test ./... -count=1` (this selects `internal/metrics`, so the new `verify_none_red_test.go` runs under CI)
  - `go-vet` => `go vet ./...`
- No `.github/**` change needed: the new test rides the existing `go test ./...` unit gate, so it is durable CI evidence.
- Affected source files only: `internal/metrics/{prometheus.go, prometheus_files.go, prometheus_verify.go}` + `cmd/baha/app_metrics.go` (CLI [STATE] surface) + `internal/metrics/verify_none_red_test.go`.

## Verification (local, exact head cc25c17e1 — after rebase onto develop deeeb6477)

### Local
- `go build ./...` => exit 0
- `go vet ./...` => exit 0
- `go test ./internal/metrics/...` => ok (existing workload-only + verify suites still pass)
- `go test ./cmd/baha/ -run 'Metrics|Observab'` => ok (metrics/observability CLI surface incl. verify path)
- New counter tests: `TestRedAllVerificationNoneHasNoCompositionCounter`, `TestVerificationNoneCompositionReportsNullTargetState`, `TestEnsureProviderFilesCompositionStateCarriesState` => PASS
- `gofmt -l internal/metrics/` => clean

### Hosted CI (run 44462738608, URL https://github.com/mcpdev80/baseharbor/actions/runs/44462738608)
- Head: `cc25c17e17d989710923b93d7e629b14a3c0a3e0` (PR #1695, base develop)
- Run conclusion: **success** (terminal; all non-skipped jobs pass)
- Relevant jobs: `PR · Validation · go-build` success · `PR · Validation · go-vet` success · `PR · Go unit · owner` success · `PR · Go unit · packages` success (selects internal/metrics) · `PR · Go unit · cli-0..3` success · `PR · Native gate plan` success · `PR · Focused Python` success · `PR · Source format` success · `PR · Trusted Plan` success · `Workflow policy` success. Native/release gates skipped (not applicable to pure Go change).
- CI gate mapping (via `scripts/pr-gate-plan.py`): `coverage_status=resolved`, required checks `go-build`/`go-unit-tests`/`go-vet` (`go test ./...` selects internal/metrics, so the new test runs under CI). No `.github/**` change needed.

### Branch provenance
- Base: `ec592fd3852328439ae9de8763c816ae9dd88dcc`; develop at time of work: `deeeb64778b3f6109d3a8e49fd652d490901e89c` (only 115-docs added, no conflict).
- Single commit `cc25c17e1` rebased onto `origin/develop`; `git merge-base --is-ancestor origin/develop HEAD` => YES; `git diff --stat origin/develop HEAD` => only the 4 intended files, no foreign commits.
- PR: https://github.com/mcpdev80/baseharbor/pull/1695 (base develop, head lane-0428-124-metrics-verification-none, not a draft).
