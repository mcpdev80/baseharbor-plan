# Remote smoke readiness, 2026-11-09

## Verified blockers
- [BaseHarbor #1513](https://github.com/mcpdev80/baseharbor/issues/1513) requires local dirty/untracked working-tree delivery, incremental second apply, deletion handling and real remote Docker/Podman READY.
- [Remote PR #1473](https://github.com/mcpdev80/baseharbor/pull/1473) is open. Its implementation continues to select immutable Git SHA/Core-side checkout as a source; this is **not** the agreed developer-local dirty snapshot delivery.
- Previous exact-head CI run [42588777740](https://github.com/mcpdev80/baseharbor/actions/runs/42588777740) failed in Go unit tests: `TestCreateTargetManagedApplicationPersistsImmutableGitSourceSelection` used a zero-service, zero-workload invalid manifest (error: at least one backend service, telemetry binding or explicit Compose workload must be enabled).
- [Commit 301d77a2](https://github.com/mcpdev80/baseharbor/commit/301d77a28bb7694c3dbcccd369f6c5c7e9dc8526) corrects that fixture on the existing remote PR branch; [run 42611750139](https://github.com/mcpdev80/baseharbor/actions/runs/42611750139) was in progress at last check.
- [Policy draft #1514](https://github.com/mcpdev80/baseharbor/pull/1514) contains an independent policy evaluator foundation, **not yet wired to real authorization/candidate ingress**. [Run 42611402466](https://github.com/mcpdev80/baseharbor/actions/runs/42611402466) also in progress at last check.

## What is NOT complete
The existing source packer `internal/development/source_snapshot.go` records source-tree metadata/identities; it does not itself implement a remote authenticated incremental byte-transfer and mutable snapshot admission. OCI transfer adapter `cmd/baha/application_image_transfer.go` exists but has not been proven integrated into remote apply. Real separate developer workstation -> HTTPS Core -> Connector -> READY -> second apply -> update -> destroy is not attested.

## Constraints
No external developer machine/runtime is accessible through this session's GitHub connector; a green unit test or synthetic HTTP fixture must not be represented as actual on-host smoke success. Do not mark release/PR DONE or merge solely on fixture fixes. Integrate accepted predecessor modules rather than creating a parallel protocol or skipping required authorization/consent.

## Follow-up: 2026-11-09 source-transfer implementation
- PR [#1473](https://github.com/mcpdev80/baseharbor/pull/1473) exact head `4da01dfc3ec9631cff23e698d73b6cf16f84de37` now contains authenticated HTTPS source-transfer handlers, delta transfer with SHA-256 manifest and chunk checks, Core immutable snapshot storage, the HTTP apply source-binding path, and revisioned remote publication/rollback logic. Local isolated `go test -race ./internal/sourcetransfer` passed; this is NOT a full-system validation.
- Snapshot capture now excludes local .baseharbor credentials, Docker/AWS/SSH/Kube/Terraform configuration and rejects environment/credential files; see commit [4da01dfc](https://github.com/mcpdev80/baseharbor/commit/4da01dfc3ec9631cff23e698d73b6cf16f84de37).
- A dedicated exact-commit validation ref `runtime-validation/ci/r27-remote-snapshot-4da01d` started [Actions run 42619879783](https://github.com/mcpdev80/baseharbor/actions/runs/42619879783). No success is claimed until it is terminal green.
- PR #1473 currently reports `mergeable_state=dirty` against newer `develop`, so reconciliation is required before merging; do not overwrite concurrent changes.
- **Still outstanding:** actual independent workstation HTTPS Core -> Connector -> Docker/Podman READY, second delta apply, update and destroy live-host smoke. No release/tag/merge and no unconditional READY claim.

## Exact-head CI follow-up after gofmt fix
- Commit [5cf86ddd](https://github.com/mcpdev80/baseharbor/commit/5cf86ddd93ab279bbb826cb7d23333029bd29f38) resolves all four gofmt differences from failed exact-head [run 42619879783](https://github.com/mcpdev80/baseharbor/actions/runs/42619879783).
- Validation ref `runtime-validation/ci/r27-remote-snapshot-4da01d` now points at `5cf86ddd`. [Run 42620209276](https://github.com/mcpdev80/baseharbor/actions/runs/42620209276) has reached the Go unit/package test step and was in progress at last check; do not claim complete PASS yet.
- Smoke CLI can be built from PR #1473 using a separate Git worktree. A real Node/Connector READY proof remains outstanding and requires access to the enrolled target.

## 2026-11-09: Native CI ownership correction (after decision review)
- Reviewed accepted [local delta delivery decision](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md), [native target ownership architecture](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-10-18-r27-native-delivery-and-stages.md) and concluded [0427-117](https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261106-r27-remote-up-podman-owner-missing.md), including round-7 evidence: real CLI apply must refuse ownerless isolated targets, even with a loan marker; do not bypass production owner verification.
- [Run 42626269890](https://github.com/mcpdev80/baseharbor/actions/runs/42626269890) passed package tests then failed five native lifecycle cases with `ErrDeploymentOwnerMissing` because `isolateRuntimeForTest` generated a new `w169-*-iso` Target without an `installation.json` while the real runner selected that same Target (owner loan cannot grant).
- [Commit 65da6552](https://github.com/mcpdev80/baseharbor/commit/65da6552a79d06ee7a0c7dc3026a03ab4875406b) fixes **test fixture only**: native cases now select the genuine package-owned bootstrap installation and verify `VerifyDeploymentOwnerAgainstOwner` before running. Different test applications still have independent project and deployment identities; no production owner check weakened, no fake installation seeded, no unsupported loan scope added.
- Exact head validation: [run 42631181302](https://github.com/mcpdev80/baseharbor/actions/runs/42631181302) in progress on `65da6552` at last check. **Not yet PASS; no live separate workstation-to-Connector READY proof.**
