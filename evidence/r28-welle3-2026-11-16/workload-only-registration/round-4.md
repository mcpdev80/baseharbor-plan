# 0428-100 round-4 — snapshot-only projection guardrails

Date: 2026-11-17. Card 0428-100. Product PR #1676.

## Contract

Per the owner ruling recorded in the task Handoff, a workload-only app has a logical runtime identity in shared snapshot metadata only. It is not a Prometheus scrape target, file_sd target, or provider-network attachment. Real endpoint-backed sources continue through normal verification.

## Product head

- Branch: `lane-0428-100-workload-only-registration`
- Commit: `178b8a00aa72acd11c29499038834bdbcc0fb038`
- Develop base included: `2581000b5fdb78f4af577fc13ce1205ca32a84e8`
- PR: https://github.com/mcpdev80/baseharbor/pull/1676 (OPEN, non-draft, mergeable at verification)

## Evidence added

- `internal/metrics.TestWorkloadOnlyRegistersSharedSnapshotOnDeploy`: actual `EnsureRuntime -> EnsureProviderFiles`; confirms app-owned logical snapshot source and absence from provider file_sd and Compose network projection; calls the public verifier successfully.
- `internal/metrics.TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy`: confirms service-app network projection remains attached and normal deployment verification succeeds.
- `internal/metrics.TestVerifyProviderSourcesSkipsOnlySnapshotMetadata`: injects an endpoint-backed source and records the verifier's real query path; asserts exactly the real source is queried and the snapshot-only logical ID is not.
- `internal/metrics.TestProviderFilesUsePinnedPrometheusAndHardenedSharedNetwork`: fixture now declares a real metrics source, preserving coverage of the normal metrics network.

## Local verification

At commit content immediately before commit `178b8a00`:

- `go test ./internal/metrics -run 'Test(WorkloadOnlyRegistersSharedSnapshotOnDeploy|ServiceAppKeepsRuntimeSourceRegistrationOnDeploy|VerifyProviderSourcesSkipsOnlySnapshotMetadata)$' -count=1` — PASS.
- `go test ./internal/application ./internal/metrics` — PASS.
- `go build ./cmd/baha` — PASS.
- `go vet ./internal/application ./internal/metrics` — PASS.
- `git diff --check` — PASS.

## Exact-head CI and review

- Exact-head PR run: https://github.com/mcpdev80/baseharbor/actions/runs/44022175082 on `178b8a00` is **terminal `completed/success`** (`status=completed`, `conclusion=success`, `head_sha=178b8a00aa72acd11c29499038834bdbcc0fb038`). Executed gates all `success`: Go unit owner/cli-0/1/2/3/packages, go-build, go-vet, Focused Python, Source format, Trusted Plan, Native gate plan. Expensive native/release/exact-candidate gates skipped by trusted-plan selection; no red jobs.
- Round-4schnittmenge (shared-file conflict resolved): external probe helper + temporary `wdiagnose_test.go` removed; production `VerifyProviderSourcesAt` probe API reverted to un-exported stand; product diff vs `ecfccbb9b` is test-only. Projection-absence evidence retained in `workload_only_source_test.go` (compose/network-absence via `assertNoWorkloadComposeNetwork` + file_sd-absence + snapshot-presence). Codex in-package recorder-test (`prometheus_verify_workload_only_test.go`, `TestVerifyProviderSourcesSkipsOnlySnapshotMetadata`) untouched and remains the single verification-evidence guardrail-1 witness.
- Guardrail-1 gap closed: workload-only identity stays out of file_sd AND provider-network projection (positive absence in generated Compose), snapshot identity positively preserved, real endpoint-backed sources keep verification.
- No merge, no GitHub review mutation. Independent review-3 requested against the clarified contract.
