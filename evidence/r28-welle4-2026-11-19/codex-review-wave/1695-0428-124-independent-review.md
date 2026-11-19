# Independent read-only review — PR #1695 / 0428-124

Reviewed 2026-11-19.

- Head `4f0d5e9f7036aed3d54b67e2f79096b43db9f29c`; base `da76c5cf9c963207038d5599bd130b89ecb1e8a4`; current develop `558dc42d0c8c9d798fcdf5938be2ea14e432b754`.
- Exact-head run `44478473607` passed PR Selected Checks, all six Go unit shards, build/vet/gofmt, Trusted Plan, source format and workflow policy. Runtime/native/release checks were skipped by plan. Branch has diverged from current develop (three commits on each side); description cites stale SHA `cc25c17e1`.
- No edits/comments/merge by this review.

## Findings

1. `ProviderCompositionState` (`internal/metrics/prometheus_files.go:208-213`) treats effective count zero as “all provider sources have Verification=none”, including when there are no provider sources. `ProviderSourcesCompositionState` (`prometheus_verify.go:166-175`) returns that status without checking the source list length; CLI prints it unconditionally (`cmd/baha/app_metrics.go:199-203`). Apps with no provider sources or app-only metrics can receive a false null-provider-target/OTLP-Tempo status. Guard empty source composition and test empty/provider-less input.
2. For all-none sources, the CLI prints the same `[STATE]` twice: `CompositionStateError` at `app_metrics.go:189-195`, then the unconditional status output at 199-203. Existing test checks only `Contains`; assert single output and correct cases.

The task’s prepared r3 lane should fix and retest after a monotonic refresh to current develop.
