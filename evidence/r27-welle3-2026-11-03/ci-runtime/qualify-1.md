# Qualify 1: w42-ci-runtime (r27 runtime) — fail-closed Go coverage

Lane: w42 (worker) · Coord: f49a3303 (Codeman) · Task: t-20261022-r27-ci-runtime
Candidate SHA: d8170d47b5c2dbb004960d5f695cce16e5c43bf5
PR: https://github.com/mcpdev80/baseharbor/pull/1356 (OPEN, mergeable, all CI green)
Base: develop 9a93865a · Write-set: internal/** only (scripts/** + .github/** TABU)

## Observable outcome
Missing domain-specific trusted selection, execution and verification for accepted
runtime-trust interfaces now execute as normal Go package tests and fail closed on
bad input. The CI selection route is the normal `go test ./...` route in ci.yml (the
trusted-PR receipt chain was retired by ci-plain-checks #1345).

## Deliverables (fail-closed Go tests, internal/** only)
1. internal/runtimeexecutor/handler_test.go (9 tests) — TLS client-cert + SPIFFE identity
   enforcement, capability gating (object-storage.s3/v1 only), unknown-field rejection,
   method/path gating, create/get/delete routing, NewHandler(nil) closure.
2. internal/deployment/runtime_selection_test.go (10 tests) — runtime profile/provider
   selection with fail-closed on unknown provider/profile and nil state; round-trip apply/read.
3. internal/providers/runtime/podman/local_authority_verify_test.go (10 tests) — native
   rootless Linux podman authority verification; fail-closed on malformed/oversized/
   remote/root/non-linux input and missing flags; context-deadline closure.

## Local verification
- go test ./internal/runtimeexecutor/ ./internal/deployment/ ./internal/providers/runtime/podman/ → all pass
- go build ./... ; go vet ./internal/... → clean; gofmt -l → clean
- Full go test ./internal/... ./contracts/... ./spec/...: ONLY pre-existing environment-limited
  failures (externalprovider cert-dir; podman retirement needs live podman binary), identical on
  clean develop baseline — not introduced by this change.

## CI results (PR #1356, run 41626804368) — 25 checks, 0 failing, 6 skipped (release/HA gates)
go-unit-tests SUCCESS (my tests run inside the full internal suite); go-build, go-vet,
deployment-package-tests, runtime-provider-package-tests, Source format (SUCCESS after gofmt
fix), Focused Python, Trusted Plan, Exact Candidate, cli-build/vet/guided, docker+podman
lifecycle all SUCCESS.

## repo-rule compliance
Write-set strictly internal/** (3 new files); no scripts/** or .github/** writes; no existing
file modified; targeted git add only; no release/tag/deploy; no gate bypass. CI record = merge
SHA + PR #1356 only.

## Owner-CI points (qualification needs scripts/ or live gate — noted, not blocked)
- remote-docker-web: internal/providers/runtime/docker/provider.go New() shells to live `docker`
  CLI → not exercisable by isolated Go test; needs hosted gate.
- podman retirement/definition-owner tests need live `podman` binary → pre-existing limitation.

## END
_LANE w42: DONE_ · CI all green · PR #1356 · candidate SHA d8170d47
