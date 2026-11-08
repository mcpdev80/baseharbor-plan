# Round 2 — 0427-172: exact fix diff + regression coverage

## Scope
Bug hunt 0427-172 (Rotkarte, highest priority). `TestUpNameResumesThroughCommandEntrypoint` failed globally in the hosted go-test `./../..` matrix: the package's TestMain bootstrap-trust-plane adoption aborted the whole run for a torn teardown/sequence — a dead-owner marker naming a `w169-ci-bootstrap-*` target whose Core was never actually provisioned.

## Files changed
- `cmd/baha/runtime_integration_test_support_test.go`
  - `destroyOrphanedBootstrapMarkers` (the dead-owner adoption path): before attempting the destroy, call `orphanBootstrapTargetHadFootprint` to confirm the orphan's target owned a provisioned Core. If it did NOT, consume the claim cleanly (remove marker, return nil).
  - Added `backgroundInventoryCtx()` — bounded background context for the footprint inventory (ambient test cancellation never aborts a teardown-class check).
  - Added `orphanBootstrapTargetHadFootprint(ctx, provider, target) (bool, error)` — returns true iff the target owned runtime project files (compose.yaml + env) OR owned containers/resources on the engine; returns false for a phantom (nothing provisioned), error for an unverifiable target root.
  - Added `ownedFootprintOnEngine(ctx, provider, target, dataDir) (bool, error)` — confirms a target with no compose files truly owns nothing on the engine.
- `cmd/baha/runtime_integration_cleanup_coverage_test.go`
  - Added `TestBootstrapAdoptionConsumesOrphanWithNoProvisionedCore`: dead-owner marker + config naming a w169-ci-bootstrap-* target but NO compose files -> adoption returns nil and removes the marker.
  - Added `TestBootstrapAdoptionKeepsMarkerWhenCoreExists`: dead-owner marker + config + compose file (Core provisioned) -> adoption returns an error and KEEPS the marker (fail-closed against a real residual).

## Fail-closed safety (preserved, not loosened)
- Live-owner protection: unchanged. `bootstrapProcessAlive` gates adoption before this path is reached — a still-running Core is never adopted, never inspected for reclaim.
- Genuine residual: Core was provisioned (footprint=true) -> destroy runs -> if owned resources remain after destroy, or a provider/engine error occurs while something WAS up -> non-nil error, marker kept, run aborted.

## Durable CI evidence
- New tests are pure unit tests (no real runtime daemon required): the footprint check inspects local compose files; the destroy fails on missing engine binding, which is the expected "fail-closed" branch.
- Picked up by:
  - `ci.yml` job `release_source_preflight`, step "Run release-source tests", line 123: `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`
  - `ci.yml` job `validate`, step "Run unit and package tests", line 341: `go test ./...`
- Both run on PR activity (`pull_request` types to develop/main, line 12-16).
- No `.github/**` file was edited (Owner scope). No workflow change required.

## Local verification
- `go vet ./cmd/baha/`: PASS
- `gofmt -l cmd/baha/`: clean
- `go test ./internal/deployment/... ./internal/runtime/...`: PASS (internal/deployment 64s, internal/runtime all subpackages)
- `go test ./cmd/baha -run 'TestBootstrap|TestUpName|TestControlPlane'`: PASS
- New regression tests both PASS; the failing reproduction (phantom orphan) now PASSES instead of aborting the run.
- Full cmd/baha package: run was CPU-starved by concurrent lanes on the shared host (multiple lanes run `go test ./cmd/baha` simultaneously); targeted groups green. A clean full-package signal is pending host load.

## TODO (remaining)
- Get a clean full cmd/baha green run for the evidence log.
- Cut branch from develop HEAD (>=20902f0a6), commit ONLY these two files, ls-remote witness (own commits only), push.
- Hosted CI run on develop-nearby head; record run name in round-1.md §4.
- Cleanliness: confirm no stray docker/podman compose projects left by this lane.
- END post to shared inbox.
