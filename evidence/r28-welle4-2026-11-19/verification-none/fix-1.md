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
