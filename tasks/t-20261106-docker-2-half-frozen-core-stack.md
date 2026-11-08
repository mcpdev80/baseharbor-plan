---
id: t-20261106-docker-2-half-frozen-core-stack
card_number: "0427-114"
card_short_title: "docker-2 Core half-frozen"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-ops-114
kanban_status: closed
kanban_lane: closed
kanban_summary: "A new owning card for the docker-2 local Core that is half-frozen: Core containers (postgres, openbao, keycloak) are running ~4h…"
kanban_title: "0427-114 · docker-2 Core half-frozen"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/coordinator-host-ops.md"]
---

- [x] t-20261106-docker-2-half-frozen-core-stack · Operations: docker-2  Core half-frozen (compose.yaml missing, phase=sql_failed, containers running ~4h) blocks Core install #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord-ops-114  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/coordinator-host-ops.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-ops-114  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

A new owning card for the docker-2 `local` Core that is half-frozen: Core containers (postgres, openbao, keycloak) are running ~4h but the Core compose.yaml is absent from disk and the installation.json is at phase=sql_failed, so `baha up --control-plane-only` fails the fail-closed canonical-owner verification. This is a host-state finding, not a matrix-lane repair duty.

## Scope

- In scope: file the finding with witness (docker ps, target state dir listing, installation.json phase), hand to coordinator for an owning card; explicit NO-repair of host state in a matrix lane.
- Out of scope: tearing down or repairing the docker-2 Core in this lane; touching the shared bh-*shared* stack or any foreign lane state.

## Acceptance

- The finding carries a docker ps witness, the target state dir listing, and the installation.json phase line.
- The coordinator accepts it as an owning card; this lane performs no host repair.

## Required checks

- None required from this lane (finding-only; no product code touched).

## Dependencies and file ownership

- Owned files or areas: none.
- Shared files: the docker-2 Core runtime and the shared local backend; out of this lanes write-set.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- Filed by w269 (coordinator ec2254ac, 2026-11-06): the half-frozen docker-2 Core is a stale holdover (likely w252 window), not created by this lane. Evidence in evidence/r27-welle5-folge-2026-11-06/vm-integration-runs/docker-2-finding.md.

owner-direktive 2026-11-07 ACCEPT nach bestaetigtem health-check: docker-2 kern-dienste up 17h, container-2-container+name-resolve OK, half-frozen behoben (orphan w169+frozen w266dn downed, bh-local preserved). ops-card, kein merge noetig.
