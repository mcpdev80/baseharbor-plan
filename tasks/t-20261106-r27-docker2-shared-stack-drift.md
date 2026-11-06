---
id: t-20261106-r27-docker2-shared-stack-drift
title: "Ops: baha-docker-2 shared stack runs with absent compose.yaml and phase=sql_failed"
release: v0.4.27
priority: normal
type: task
areas: [platform, ops]
owner: ""
kanban_status: planned
kanban_lane: ready
depends_on: [t-20261017-release-0-4-27-updates]
prs: []
repos: [mcpdev80/baseharbor]
---

- [ ] t-20261106-r27-docker2-shared-stack-drift · Ops: reconcile baha-docker-2 shared stack (running containers, missing compose.yaml, sql_failed phase) #task #release/v0-4-27 #status/planned #view/ready #area/ops #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Purpose

w269's integration matrix found on baha-docker-2 (205): bh-local-shared-* containers (postgres,
openbao, keycloak) running ~4h while the target's compose.yaml is absent from disk and
installation.json sits at phase=sql_failed — a half-reconciled state plausibly left by an earlier
state-recovery/disaster cell. The stack must be truthfully reconciled (finish or tear down and
rebuild) so future installs on this host start from a clean, evidence-consistent base.

## Acceptance

- Host audit shows either a fully consistent shared stack (compose.yaml present, doctor healthy,
  phase complete) or container=0 with journal release — no mixed state.
- Root cause pinned to the lane/run that removed or never wrote compose.yaml (journal + akte cross-check).
