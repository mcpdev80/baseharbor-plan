---
id: t-20261018-r27-remote-rollout
areas: [providers]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-artifact-resolution, t-20261018-r27-ci-lanes, t-20261018-r27-journal-wiring, t-20261018-r27-mutation-lock, t-20261018-r27-remote-podman-web]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-remote-rollout · Remote lifecycle: apply a new candidate without losing the previous owner #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/providers #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Replace the current remote retained-publication equality restriction with a bounded candidate transition using existing lifecycle/provider owners. Keep previous applied source/material/ownership until new candidate converges and verifies; commit authoritative revision only afterwards. Failure/restart remains inspectable with no duplicate project or lost data; repair/destroy use the exact retained owner. Provider consequence consent, receiver/material change and actual SQL/cache consumer verification remain mandatory. Initially qualify only the supported Docker/Podman SQL/cache/web footprint; every other unsupported capability stays explicit. No automatic destructive rollback or generic rollout engine.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/app_remote_lifecycle.go; internal/application/remote_managed_snapshot.go; bounded remote transition files/tests. Serialize after both web admission slices; preserve immutable previous snapshots rather than overwriting them. Registration remains public-surfaces.

## Required checks

Focused candidate transition/failure/crash/recovery tests against actual production orchestration; one bounded Docker and one bounded Podman changed-candidate gate with SQL/cache data preservation, actual consumer access and cleanup. Reuse unchanged web proof only through the existing verifier. No full matrix or self-approved waiver.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
