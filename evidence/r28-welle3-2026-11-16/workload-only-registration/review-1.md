# CODEX-REVIEW — R3 / PR #1676

Date: 2026-11-17. Role: CODEX-REVIEW, sequential after WORKER END. No GitHub APPROVE/review mutation and no merge performed.

## Candidate identity and gates

- PR #1676, `lane-0428-100-workload-only-registration`, exact head `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c`, base `develop` at `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54` (included as second parent of merge commit `9ae08086e01739984eb197375dece37c145b8b8e`). Remote ancestry check passed: current develop is ancestor of candidate.
- Own exact-head `pull_request` run [44018836577](https://github.com/mcpdev80/baseharbor/actions/runs/44018836577) completed `success` on the exact head. `PR Selected Checks` completed `SUCCESS`; selected Go unit shards, `go-build`, `go-vet`, source format, trusted plan, focused Python, and workflow policy passed. Native Docker/Podman checks were skipped by trusted impact selection.
- PR remains OPEN and mergeable; mergeStateStatus was CLEAN at review time. CI/base gates pass, but content acceptance does not.
- Reviewed the complete diff from develop to exact head. Changed files: `internal/application/runtime_observability.go`, `internal/metrics/prometheus_files.go`, `internal/metrics/prometheus_verify.go`, `internal/metrics/workload_only_source_test.go`, `internal/observability/registry.go`. No `.github/**`, `security.go`, or #1665-owned files changed.

## Verdict — CHANGES REQUESTED

### Blocking finding: R3 point (4) still has no scrapeable workload target

The new production source at `internal/application/runtime_observability.go` uses `Target: observability.RuntimeTarget(project, "workload")`, `Path: "/metrics"`, `Verification: ObservabilityVerifyNone`. The delta deliberately excludes that source from Prometheus target generation and network projection in `internal/metrics/prometheus_files.go` (`syncProviderTargets` and `providerMetricNetworks`), and skips it in `internal/metrics/prometheus_verify.go`. The test `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy` explicitly asserts the source is absent from every Prometheus file_sd target (`assertNoWorkloadScrapeTarget`) and `VerifyProviderSourcesAt` passes without requiring a scrape sample.

This matches the former R2 description of a symbolic identity “without fabricating a scrape backend,” but it does not meet the explicit R3 point (4) requirement that the metrics target be scrapeable and that verification not be weakened. The source is registered as `SignalMetrics`/`openmetrics` at `/metrics`, yet no scrapeable endpoint is materialized and no `up=1` sample is proven for it. A green CI run validates this implementation, not the missing scrape contract.

### Correction recipe / stop criterion

1. Define and implement a real scrapeable endpoint for the workload source from an existing product contract (actual workload service plus declared/known port and `/metrics` path); resolve the runtime identity to that endpoint before writing provider file_sd. Keep the normal verifier path and require the source's observed `up=1` sample. Do not use `VerificationNone` or omit this metrics source from scrape generation to make the test pass.
2. Update the integrated workload-only regression to assert the concrete resolved host:port/path in generated provider target JSON and prove positive scrape verification. Keep the real `EnsureRuntime -> EnsureProviderFiles -> VerifyProviderSourcesAt` path and service-app compatibility regression.
3. If the product has no endpoint/port contract for this workload shape, STOP+QUESTION and obtain an explicit owner decision to change the card from a scrapeable metrics source to a non-scraped logical registration. That would revise the current R3 requirement; do not merge the current code under the scrapeable-target acceptance wording.
4. After correction, push a new exact head, observe its own `pull_request` run to terminal success, then request a fresh sequential review. Do not reuse run 44018836577 for a changed SHA.

No product edits, local checks, approve, or merge were performed in this REVIEW role. Planning render/check were reported repaired and the card band published by coord; this review verdict is recorded here and in the coordinator inbox post.
