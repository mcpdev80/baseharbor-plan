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
