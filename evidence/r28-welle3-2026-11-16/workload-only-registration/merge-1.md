# CODEX-REVIEW — batch22 object 2 / PR #1676

Date: 2026-11-17. Role: CODEX-REVIEW, exact candidate `0b8cecb058efb7dc7678071a3113bc8786890d2d`. No base refresh, product push, new run, GitHub review mutation, or merge was performed after the findings below.

## Candidate and witnesses

- Card 0428-100, PR #1676, branch `lane-0428-100-workload-only-registration`, OPEN and ready.
- Current PR base before any refresh: `develop@e6cce9c73b8edddeff98fa858e83e4b08e8836ef`. Following object 1, current develop is now `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54`; this PR is behind and will need a normal merge of the new develop head after correction/re-review.
- Exact-head run [44007626272](https://github.com/mcpdev80/baseharbor/actions/runs/44007626272) completed SUCCESS on `0b8cecb058efb7dc7678071a3113bc8786890d2d`. `PR Selected Checks` is SUCCESS from integration 15368. This run is valid evidence for its then-current base only; it does not qualify a later merge commit.
- Exact PR diff has five files: `internal/application/runtime_observability.go`, `internal/application/observability_workload_registration_test.go`, `internal/metrics/prometheus_verify.go`, `internal/metrics/prometheus_verify_workload_test.go`, and `internal/metrics/workload_only_source_test.go`. No #1665-owned path is touched.
- Round-2 evidence `round-2.md` reports the real baseline reproducer: `EnsureProviderFiles` wrote shared `runtime-sources.json` with `sources: []` on develop `e6cce9c73`, and identifies `reconcileManagedRuntimeObservability` as the registration hook.

## Verdict — CHANGES REQUESTED

The production registration hook is now present, but the candidate still includes the round-1 verifier early-return workaround and its regression tests do not demonstrate the required connected deploy path.

1. **Fail-closed verifier bypass remains.** The PR diff still includes `internal/metrics/prometheus_verify.go` adding an early return for manifests with no declared metrics sources and no runtime metrics permission. This contradicts the batch21 recipe and the round-2 evidence claim that there is no early-return workaround in the verifier. The missing source must be fixed by registration, while the verifier retains its fail-closed behavior for required sources.
2. **No end-to-end deploy-path snapshot and positive verification regression.** `TestReconcileManagedRuntimeObservabilityWorkloadOnlyRegistersSource` calls the real hook and checks registry contents, but does not materialize/inspect `runtime-sources.json` or call `VerifyProviderSourcesAt`. `TestWorkloadOnlyRegistersSharedSourceOnDeploy` manually calls `observability.Update(workloadOnlySourceContract(...))` before `EnsureProviderFiles`; it therefore bypasses the production registration hook and can pass if that hook is disconnected or broken. It does not assert positive verification. The two test fragments do not establish the mission-required single path from deploy registration through snapshot to successful verification.
3. **Service compatibility test bypasses the service registration path.** `TestServiceAppStillRegistersOnDeploy` also manually inserts the mirrored source with `observability.Update` before snapshot materialization; it does not call the existing service-app deploy registration path or prove that it still registers through that path.

### Correction recipe and stop condition

1. Remove the early-return change from `internal/metrics/prometheus_verify.go`; preserve the existing required-source fail-closed behavior. Keep the real registration fix in `internal/application/runtime_observability.go`.
2. Replace the manual registry insertion in the workload-only regression with the real deploy registration orchestration, then materialize and inspect shared `runtime-sources.json` and call the positive verifier path on that result. Assert the registered source ID/owner/scope and a successful verification.
3. Drive the service-app compatibility case through its existing real registration path and assert the expected source registration remains unchanged. Keep the regressions in the currently selected package group and state exact test IDs and trigger.
4. Stop if the real deploy path cannot be invoked safely by the package test or if the intended `runtime://<project>/workload` source contract is uncertain; return the concrete blocker to the coordinator. Do not touch #1665-owned paths or `.github/**`.
5. After correction and re-review, merge current develop `8db0d9bd` into the lane with a normal merge commit, push by explicit refspec without force, observe the new exact-head `pull_request` run to terminal SUCCESS, and recheck `PR Selected Checks` from integration 15368, clean mergeability, and the exact diff before any merge.

No local tests were run by this reviewer. The worker's run 44007626272 is recorded above and is not being relabeled as evidence for the pending corrected/current-base candidate.
