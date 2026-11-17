# CODEX-REVIEW-3 — PR #1676

Date: 2026-11-17. Role: CODEX-REVIEW, owner-authorized, exact candidate `178b8a00aa72acd11c29499038834bdbcc0fb038`.

## Identity, base and run

- Live PR #1676 is OPEN, ready (`isDraft=false`), base `develop`, mergeable, `mergeStateStatus=CLEAN`; head `178b8a00aa72acd11c29499038834bdbcc0fb038` matches both `refs/heads/lane-0428-100-workload-only-registration` and `refs/pull/1676/head` from `git ls-remote`.
- `develop` is `2581000b5fdb78f4af577fc13ce1205ca32a84e8`; `git merge-base --is-ancestor origin/develop origin/lane-0428-100-workload-only-registration` passed.
- Exact-head `pull_request` run [44022175082](https://github.com/mcpdev80/baseharbor/actions/runs/44022175082) completed `success` on the exact head. PR `Selected Checks` completed `SUCCESS` at [job 133835834779](https://github.com/mcpdev80/baseharbor/actions/runs/44022175082/job/133835834779).

## Contract and guardrails

Applied card 0428-100's snapshot-only contract ruling: for a workload-only app with no declared endpoint, retain logical source identity in the runtime source snapshot; do not invent an endpoint; exclude it from file_sd and provider-network projections; skip verification only for this metadata. Endpoint-backed sources retain normal verification and fail-closed behavior.

1. **file_sd absence — PASS.** `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy` drives the real `EnsureRuntime -> EnsureProviderFiles` path, asserts source ID/owner/`runtime://` target in `runtime-sources.json`, then scans generated `ProviderFiles.TargetsDir` JSON and fails if the workload identity appears.
2. **network absence and service compatibility — PASS.** The same workload-only test calls `assertNoWorkloadComposeNetwork` over the generated Compose file. `TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy` positively asserts that a service-app fixture still has its metrics provider network in generated Compose.
3. **verification query count — PASS.** New in-package `TestVerifyProviderSourcesSkipsOnlySnapshotMetadata` calls the unexported `verifyProviderSourcesAt` recording seam. It proves exactly one normal backend query is issued, containing the endpoint-backed source ID and excluding the snapshot-only workload ID.
4. **snapshot identity — PASS.** The real deploy-path test checks that the shared `runtime-sources.json` retains the workload source identity, owner and symbolic target.
5. **delta/API scope — PASS.** PR diff against current develop contains the expected runtime-source registration, file_sd/network exclusion, verifier skip, and associated tests. Delta since prior reviewed head `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c` also includes develop's `cmd/baha/app_init_uid_app_slice_test.go`; the added production helper is unexported (`verifyProviderSourcesAt`), not a test-only public API. No `.github/**`, `security.go`, or neighboring 0428 lanes changed.

Review-role file integrity: `internal/metrics/workload_only_source_test.go` remained at blob `d910e472c18fe7d0ddf90b8321446e9959a10d32`; `internal/metrics/prometheus_verify_workload_only_test.go` remained at blob `5a03b6d2d3b0eb69de505dcda271310a2ded3875`. The mission's third named path `internal/metrics/prometheus_verify_test.go` is absent from the candidate tree; the new in-package test is `prometheus_verify_workload_only_test.go`. No candidate file was edited by this review session.

## Verdict — APPROVE

All five review gates pass on the exact candidate; exact-head CI and merge-base freshness are verified. Proceeded to CODEX-MERGE as authorized, with `--match-head-commit 178b8a00aa72acd11c29499038834bdbcc0fb038`. Merge witness is appended below after remote verification.

## CODEX-MERGE witness

- Executed `gh pr merge 1676 --repo mcpdev80/baseharbor --squash --match-head-commit 178b8a00aa72acd11c29499038834bdbcc0fb038`; no admin/bypass flags.
- GitHub reports PR #1676 `MERGED` at `2026-11-17T05:16:49Z`; squash merge commit `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`.
- `git ls-remote origin refs/heads/develop` returned exactly `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`; `gh pr view` independently reports the same mergeCommit and original exact head.
- No release, tag, deployment, or GitHub review mutation.
