# CODEX-REVIEW — Luna batch 9

**ROLLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

Exact heads and pull-request runs refreshed from the live GitHub API. The 4 candidates were reviewed against their preceding correction evidence and current exact diffs. Detailed per-candidate akten follow.

| PR | Exact head | Exact-head `pull_request` run | Verdict |
|---|---|---|---|
| #1578 | `6f07aef2c68ba5eb3c2361d8f0bf1dccc676025c` | `43838767406` SUCCESS | APPROVE CONTENT |
| #1591 | `08fc5ad310e181394f6cef51d91ba8df42b2b446` | `43830046439` SUCCESS | APPROVE CONTENT (format-only continuity) |
| #1614 | `80d4df52e913e4472334a5f257fe868d26d5976e` | `43840657678` FAILURE (`cli-1`) | REQUEST CHANGES / exact-head CI hold |
| #1610 | `601f3c3af26a7aec00551f8d37899c30918b9939` | `43829552274` FAILURE (Go package-selection jobs) | REQUEST CHANGES |

## #1578 — `t-20261114-r28-cli2-uid-environment`

**Base:** `lane-0428-uid-app` @ `22c545d8242f8cfc2acff2a5152ab5ea4f07d170`. PR remains open/draft. Exact-head run `43838767406` is completed SUCCESS; the API associates it with the reviewed SHA. Exact PR file list now contains only `internal/deployment/environment_identity.go`, `internal/deployment/environment_identity_test.go`, and the two `internal/environment` files; the orphaned `cmd/baha/command_target_env.go` is absent.

The r5 correction addresses both prior findings. The source-present rename path re-stats and reads the destination inside `WithDeploymentRegistryWriteLock`; a different identity returns `ErrEnvironmentAlreadyExists`, while the same identity converges. The regression `TestRenameDoesNotClobberConcurrentDestinationCreator` is reported in `round-5.md` as failing on `9c5bc09a` and passing 5/5 on this candidate. The out-of-scope CLI file has been removed. This revalidation under the common lock protects against the package's concurrent `GetEnvironment`/rename writers, which share that lock.

**Verdict: APPROVE CONTENT** for this exact candidate. Preserve the domain-only scope and do not treat this content review as dependency acceptance or merge authorization. Review evidence: `cli2-uid-environment/act-1578-review-r5.md` and `cli2-uid-environment/round-5.md`.

## #1591 — `t-20261114-r28-cli2-env-registry`

**Base:** `lane-0428-uid-target` @ `ae0602e02882619dea151dc82d62b98b72481566`. PR remains open/draft. Exact head is `08fc5ad310e181394f6cef51d91ba8df42b2b446`; exact-head run `43830046439` is completed SUCCESS. GitHub commit metadata shows the sole delta after `3d1841bab3f5c933a16f1116ece4105cc68bdcee` is `format(deployment): gofmt environment_association_test.go`, touching only that test file with 15 additions/15 deletions and no semantic changes.

The underlying r2 correction from `4d14741ee` to `3d1841bab` validates persisted association kind and ID at the authoritative read and register/deregister mutation paths, fails closed, and preserves malformed records byte-for-byte on rejected mutations. The test evidence in `cli2-env-registry/round-2.md` covers those paths. The current patch is formatting-only, so it preserves that reviewed content.

**Verdict: APPROVE CONTENT (format-only continuity)** for this exact candidate. This does not accept dependent tasks or authorize merge. Review evidence: `cli2-env-registry/act-luna-r1.md`, `cli2-env-registry/round-2.md`, and live commit comparison `3d1841bab..08fc5ad31`.

## #1614 — `t-20261114-r28-cli2-app-status`

**Base:** `lane-0428-059-cli2-source-model` @ `818d572b982a69e2caebd5474a4ba270ed21fd41`. PR remains open/draft. Exact-head run `43840657678` is completed FAILURE; job `PR · Draft Go · cli-1` failed while package and other CLI shards succeeded. The logged failures are `TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse` (`control_plane_stop_impact_test.go:150`) and `TestRemoteMutationArgumentsFailClosed` (`management_remote_mutation_test.go:58`). These routes predate the final commit `80d4df52e`, whose patch changes only acceptance-gate test setup in `app_edit_apply_test.go` and `management_core_git_candidate_test.go`; it does not modify the failing implementation or test files. The worker's `round-3.md` reports both tests green in isolation and in its full local shard on this SHA.

This evidence points toward a shared-state/test-isolation or runner-specific failure rather than a defect introduced by the final test-only commit, but does not prove that classification: the exact hosted `pull_request` run is red, and the log shows actual assertions, not an infrastructure startup error. No independent hosted baseline comparison establishes whether the failure predates this candidate.

**Verdict: REQUEST CHANGES / CI HOLD.** Do not mark accepted while the exact-head run is red. Establish the failure on the PR base/current candidate with isolated state, or correct the test isolation/setup if run ordering leaks state; then obtain a green exact-head `pull_request` run. Do not change the unrelated core files inside this card without a contract/scope change. Stop if the failure reproduces as a real production behavior defect outside the card's write-set; report file:line for owner triage.

Review evidence: `cli2-app-status/round-3.md`; live PR #1614 file list, exact head, run and `cli-1` logs. No local product tests were run by this reviewer.

## #1610 — `t-20261114-r28-perses-tempo-source`

**Base:** `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`. PR remains open/draft. Exact-head run `43829552274` is completed FAILURE. The source/routing validation passes, but the `packages` and all four CLI Go shard jobs fail before tests with:

```text
Draft Go package selection failed: changed Go package not discoverable: github.com/mcpdev80/baseharbor/internal/metrics/testdata/perses-tempo-datasource/upstream
```

The candidate adds eight upstream witness files under `internal/metrics/testdata/.../upstream/` with `.go` suffixes. The current changed-package selector treats that directory as a Go package, then cannot discover/build it as one. This is a candidate/CI-selection integration defect, not a flaky test or external runner artifact; the run had no test lines because selection stopped first. The r4 content corrects the prior Perses model/query envelope findings, but the candidate cannot satisfy the required CI path in its current layout.

**Verdict: REQUEST CHANGES. Recipe:** rename the embedded upstream source copies to non-package suffixes (for example `.go.txt`) and update the `//go:embed` paths, leaving Go source outside any `testdata` directory as data. Do not edit `.github/**` from this lane; CI selector/workflow changes are owner-scope. Keep the pinned SHA-256 witness validation and serialization tests. Verify the package selector now discovers only `internal/metrics`, rerun the focused Perses tests and obtain an exact-head `pull_request` SUCCESS on the corrected SHA. Stop if satisfying the selector requires workflow ownership changes; report the required workflow file/line to the coordinator.

Review evidence: `perses-tempo-source/act-luna-r3.md`, `perses-tempo-source/round-4.md`; live PR #1610 file list, exact head, run and failed Go-job logs. No local product tests were run by this reviewer.

## repo-rule compliance

- Read-only product review; no product files, PR metadata, review state, CI, or release state were changed.
- No merge, GitHub approval mutation, or task-state change was performed.
- Planning-only evidence is published separately on `baseharbor-plan` `main`.
