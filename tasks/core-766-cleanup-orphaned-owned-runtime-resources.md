---
id: core-766
areas: [lifecycle]
type: bug
release: v0.4.x
version: ""
parent: v0.4.x
owner: marcel
depends_on: [core-893, core-895, core-896, t-20261027-r27-cutover-pr3]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#766"]
source_updated: "2026-10-15T16:51:08Z"
labels: [kind/bug, area/runtime, area/security, area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-766 · Cleanup: remove orphaned owned runtime resources #task #release/v0-4-x #status/active #view/active #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** marcel  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261027-r27-cutover-pr3](t-20261027-r27-cutover-pr3.md)  
**Owner:** marcel  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#766](https://github.com/mcpdev80/baseharbor/issues/766)
<!-- /generated:links -->

## Goal

Full installation destroy removes orphaned BaseHarbor-owned runtime projects even when deployment state is gone, verifies ownership, and preserves foreign resources and intentionally retained data.

## Scope

- Bug: `baha destroy --all --yes` can report `Registered deployments: 0` while BaseHarbor-owned projects still exist. The full-destroy flow removes resources reachable from deployment/provider/state metadata, then only audits residual containers (`destroyTargetBestEffort`: `ListRuntimeContainers` → `targetOwnedRuntimeContainers` → fail `runtime-audit`). Orphans such as `bh-local-<app>-<env>`, `bh-local-dev-gateway-dev` or stale shared modules (runtime broker/workload, dev gateway, OpenBao/PostgreSQL/Prometheus/SeaweedFS, shared Valkey) are detected but never destroyed.
- Required (full installation destroy only): after normal semantic/state cleanup, discover residual projects from runtime containers; restrict candidates to the Target-owned namespace (`bh-<target>-*`); per project use the provider-neutral ownership API `ListOwnedProjectResources(project)` → `DestroyOwnedProjectResources(project, resources)` → verify empty; then the final runtime audit; keep state only if owned resources cannot be removed/verified. Never target non-BaseHarbor projects; do not rely on missing Compose/Quadlet files.
- Triage (2026-10-15): removal requires verified installation/Target/resource ownership; a BaseHarbor-looking name or an unknown discovered Target never grants destruction authority. Verify retained workload data versus unwanted networks, foreign-resource preservation and deduplicated preservation output on Docker and Podman. Scoped or historical cleanup receipts do not close these criteria. Related lifecycle work was #872/#881.
- Comment (2026-10-08, Docker rootless, v0.4.23): `baha up --yes --plain` → `baha app destroy --yes` → `baha destroy --all --yes` outside the repo leaves volume `bh-local-baseharbor-demo-dev_demo-app-state` (preserved app data) and network `bh-local-baseharbor-demo-observability` with no named residue in the output; recovery file `PRESERVED` reported twice. Required: inventory managed orphan names after registry deletion, distinguish intentionally preserved workload data from unwanted orphan networks, never remove foreign resources, report all residuals explicitly, deduplicate preservation messages; regression: full destroy after app destroy on Docker and Podman.

## Acceptance

- `destroy --all --yes` removes orphaned app/runtime-broker projects even with zero registered deployments.
- Orphaned shared/provider/dev-gateway projects are removed when ownership labels identify them as BaseHarbor-owned.
- Foreign projects are untouched.
- Provider-neutral for Docker and Podman through RuntimeProvider ownership APIs.
- Residual resources are verified after deletion.
- XDG state is removed only after the runtime audit is clean.
- Intentionally preserved workload data is distinguished from unwanted orphan networks; all residuals are reported explicitly; preservation messages are deduplicated.
- The source's "lands directly in active v0.4.21" item is historical.

## Required checks

- Focused tests and `go vet`; regression full destroy after app destroy on Docker and Podman.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies.

## Handoff

- Assigned to mcpdev80; no current claim.
