---
id: t-20261018-r27-remote-rollout
card_number: "0427-053"
card_short_title: "apply a new candidate without"
areas: [providers]
type: task
release: v0.4.28
version: ""
parent: v0.4.28
priority: normal
owner: ""
kanban_lane: closed
kanban_summary: Apply an explicitly selected next version through native Docker Compose or Podman Quadlet/systemd using existing…
kanban_status: closed
kanban_title: "0427-053 · apply a new candidate without"
depends_on: [t-20261017-release-0-4-27-updates, t-20261017-release-0-4-28-updates, t-20261018-r27-artifact-resolution, t-20261018-r27-journal-wiring, t-20261018-r27-mutation-lock, t-20261018-r27-remote-podman-web, t-20261018-r27-stage-versions, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: true
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-owner-close-inherited-work.md"]
---

- [x] t-20261018-r27-remote-rollout · Remote lifecycle: apply a new candidate without losing the previous owner #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/providers #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-owner-close-inherited-work.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [t-20261018-r27-promote](t-20261018-r27-promote.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Apply an explicitly selected next version through native Docker Compose or Podman Quadlet/systemd using existing lifecycle/provider owners. Retain previous applied metadata/material and resource ownership until the result is reconciled; this is not a guarantee that old/new containers coexist or that update is atomic/zero-downtime. Record desired/applied/observed versions separately on failure/restart. Preserve SQL/cache data, consumer verification, permission and exact consequence consent. Runtime-native behavior and supported limits are visible. No generic rollout controller, scheduler, canary, destructive automatic rollback or reimplementation of Kubernetes deployments. Application schema migrations and compatibility are app-owned; image rollback and verified backup are not schema-compatibility proof.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/app_remote_lifecycle.go; internal/application/remote_managed_snapshot.go; bounded remote transition files/tests. Serialize after both web admission slices; preserve immutable previous snapshots rather than overwriting them. Registration remains public-surfaces.

## Required checks

Focused candidate transition/failure/crash/recovery tests against actual production orchestration; one bounded Docker and one bounded Podman changed-candidate gate with SQL/cache data preservation, actual consumer access and cleanup. Reuse unchanged web proof only through the existing verifier. No full matrix or self-approved waiver.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Release boundary decision — 2026-11-13

Advanced revision replacement, last-good recovery and restart/reconciliation for repeated remote rollouts move to v0.4.28. Initial remote apply, status and destroy as shipped in v0.4.27 are not deferred; no promise of zero-downtime update/automatic rollback in release notes.

No implementation/acceptance is inferred; original stable card_number remains unchanged. Complete this through the normal v0.4.28 Coordinator/Worker/Codex merge process and current native tests.

## Owner-directed closure — 2026-11-14

The Owner stated that this work was already performed and explicitly directed acceptance. See the [Owner decision](../decisions/2026-11-14-owner-close-inherited-work.md). This closure does not claim independently reproduced tests or newly verified CI evidence.
