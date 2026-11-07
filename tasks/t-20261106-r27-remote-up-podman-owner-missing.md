---
id: t-20261106-r27-remote-up-podman-owner-missing
title: "Remote app up on Podman family fails with ErrDeploymentOwnerMissing"
release: v0.4.27
priority: high
type: bug
areas: [cli, remote]
owner: w286
kanban_status: active
kanban_lane: active
depends_on: [t-20261017-release-0-4-27-updates, t-20261106-r27-remote-up-cli-path]
prs: []
repos: [mcpdev80/baseharbor]
---

- [ ] t-20261106-r27-remote-up-podman-owner-missing · Remote up: podman-family deployment owner missing (ErrDeploymentOwnerMissing) #task #release/v0-4-27 #status/active #view/active #area/cli #area/remote #kind/bug
    <!-- generated:card -->
    **Owner:** w286 · **Priority:** high  
    **Needs:** [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
**Owner:** w286  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Purpose

w273 ran the pure-client remote `baha app up` cell at candidate head 2651a5c9869 on baha-podman-2
(vm-locked, journal claim 22:00->release 22:08Z): deployment reports ErrDeploymentOwnerMissing while the
Docker family passes the identical scenario (w264 round-2, baha-docker cell green). The connector-routed
up path apparently does not record or resolve the deployment owner for the podman runtime family.

## Acceptance

- Same-scenario cell on baha-podman passes (up -> doctor health OK); owner record present and resolvable.
- Root cause with file:line in the akte; regression cell red-first.
