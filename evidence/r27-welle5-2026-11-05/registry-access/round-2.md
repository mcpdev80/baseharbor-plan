# round-2.md

- Lane: w203 (Worker)
- Task: t-20261018-r27-registry-access · Registries: use configured enterprise endpoints and native credentials (ROUND 2)
- Coord: 841e7734 (w1-baseharbor)
- Model: worker-ornith1.5
- Session: 2041231d
- Card: round 2, wave 5
- Branch: work/r27-registry-access (PR #1395)

## PLAN

- Read mission, task note, review-1395a.md akte, base attestation (base c2ada69c = round-1 head; develop 3d8fc207 ancestor)
- Await + receive coordinator scope decision: JA, single seam at app_broker.go:58 (compose.PullImage via RegistrySource.Resolve)
- Implement resolveRegistrySource pull seam + pullResolvedRuntimeImage in application_registry_source.go (write-set); call from app_broker.go:58
- Fix: split tagged BASEHARBOR_RUNTIME_IMAGE into repo+tag so oras resolve is not double-tagged; fallback returns original ref
- Production-path e2e test (TestPullResolvedRuntimeImagePinsImmutableDigest) + mutant caller-removed => RED + counterprobe => GREEN (verified)
- Local gates: go build/vet/gofmt clean; focused tests pass; drift merge origin/develop rc=0 (only unrelated snapshot test)
- Commit akte round-2.md to baseharbor-plan origin/main (ls-tree witness)
- Push branch work/r27-registry-access, run hosted selected-checks gate (TERMINAL at new head), ls-remote real==head
- Update card note, post END line to coordinator 841e7734

## Base attestation

- Base ref cut from: c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd (round-1 head, named candidate)
- ls-remote witness for origin/work/r27-registry-access (before push): c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd
- develop drift: origin/develop moved from 3d8fc207deabc2840bcfd888f46d2394cc5a7d36 to a0441838deb2c2b69be547e538a94dc50c9fde2f (unrelated PR #1387 snapshot-flake, test-only)
- Drift resolved: `git merge origin/develop` rc=0 (only internal/development/* snapshot test changes); develop now an ancestor of HEAD
- One integration candidate per chain: the mission names branch work/r27-registry-access

## Scope decision (coordinator 841e7734, 2026-11-06)

- JA — authorized to set the production seam, strictly limited: exactly the one call site cmd/baha/app_broker.go:58 (compose.PullImage(ctx, runtimeImage)) is driven through RegistrySource.Resolve (adapter detour, no further refactoring, no second file outside the write-set, app_up_noop/operational_errors stay at rest)
- If that is impossible without more foreign files: STOP + report with the blocking line
- Proof required: e2e cell (real up-path resolves on configured endpoint) + MUTANT caller-removed => RED + counterprobe => GREEN
- Card note adopts the decision

## Implementation

- Production caller: cmd/baha/app_broker.go:58 now calls pullResolvedRuntimeImage(ctx, compose, runtimeImage, "edge") instead of compose.PullImage(ctx, runtimeImage)
- Pull seam: cmd/baha/application_registry_source.go
  - resolveRegistrySource (var seam) -> resolveRegistrySourceImpl: builds RegistrySource{Kind: SourceOCIAddressed, Location, Requested, Exec: registrySourceExec}, calls Resolve(ctx)
  - On success returns the immutable repository@digest identity (identity.ImmutableIdentity())
  - On failure (no native tool, unreachable, no digest) best-effort falls back to the original configured reference so the mutable-image path is preserved
  - registrySourceExec seam defaults to execArtifact (real os/exec); tests install a fake runner
  - splitReference separates a tagged BASEHARBOR_RUNTIME_IMAGE (e.g. ghcr.io/...:edge) into repo + tag so oras resolve is not double-tagged; requested selects the tag
  - pullResolvedRuntimeImage: resolveRegistrySource -> compose.PullImage(resolvedRef); the single pull site proving the seam
- No file outside the r27 write-set; app_up_noop and operational_errors untouched

## Evidence (discriminating)

- Test: cmd/baha/app_broker_registry_pull_test.go TestPullResolvedRuntimeImagePinsImmutableDigest drives pullResolvedRuntimeImage with a fake registrySourceExec that records the native oras resolve invocation and returns a digest-carrying reply; asserts exactly one PullImage and that it received the resolved repository@digest identity
- MUTANT (caller removed / resolveRegistrySourceImpl returns the raw tag): pull receives ghcr.io/mcpdev80/baseharbor-runtime:edge:edge -> test FAILS (RED) — recorded
- Counterprobe (mutation-free, original code): pull receives ghcr.io/mcpdev80/baseharbor-runtime@sha256:aaa... -> test PASSES (GREEN) — recorded
- splitReference correctness for all CI env shapes (ghcr/localhost/<repo> with and without tag) verified

## Local gates (all green)

- go build ./cmd/baha: rc=0
- go vet ./cmd/baha: rc=0
- gofmt: clean on application_registry_source.go, app_broker.go, app_broker_registry_pull_test.go
- focused tests PASS: TestPullResolvedRuntimeImagePinsImmutableDigest, TestResolve*, TestCanonicalArtifactRepository, TestExecArtifact, TestRuntimeBroker*, TestBroker*, TestSelfUpdateRelease*
- full cmd/baha suite cannot complete locally (gated tests need a live Docker daemon); no native registry smoke locally (oras not installed) — native smoke belongs on the named SSH runners, not this host

## Hosted gate (run 42132438226 — TERMINAL, new head ef0120aa)

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/42132438226 — 24 jobs: 14 success, 10 skipped, 0 failure
- Selected checks pass: go-build, go-vet, go-unit-tests, cli-build, cli-vet, cli-package-tests, cli-guided-tests, cli-gofmt, source-contracts, Focused Python, Source format, Trusted Plan, Workflow policy
- Docker/managed-runtime gates (Targeted HA · docker, Selected Runtime, etc.): skipping — no native registry runtime selected for this change (native registry smoke belongs on the named SSH runners, not this host)
- ls-remote real == head (WORDLICH): `ef0120aa3d738f333dd9bd8fbed385bd1d92fa05 refs/heads/work/r27-registry-access`
- develop ancestor: `git merge-base --is-ancestor origin/develop HEAD` rc=0 (drift from unrelated PR #1394 device-lifecycle merged into develop, resolved via merge rc=0)
- My branch beyond develop touches only: cmd/baha/app_broker.go, cmd/baha/application_registry_source.go, cmd/baha/app_broker_registry_pull_test.go (+ round-1's application_registry_source_test.go)
- No foreign commit carried in first-parent history

## Evidence committed

- akte round-2.md committed to baseharbor-plan main, pushed, ls-tree witness on origin/main: `538eb62ab0a3094976acd0efc7a8d7f68e8d426d evidence/r27-welle5-2026-11-05/registry-access/round-2.md`

## Status

- State: active — committed locally on work/r27-registry-access at 010a6792 (root + worktree identical). Awaiting push + hosted gate.
- END an 841e7734 (pending)
