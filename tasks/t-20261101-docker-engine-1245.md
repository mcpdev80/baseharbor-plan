---
id: t-20261101-docker-engine-1245
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: "worker-ornith1.5 (Ornith; session 35cdb02e-a3b3-4e6d-86f9-1cbb35822587)"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1250]
sources: []
blocker: "Merge blockt ausschliesslich am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum) — KEIN Required-Check von #1245/#1250 (Pflicht = Lifecycle-Gates, die GRUEN). Ha-Blocker-Klasse bestaetigt durch CI run 41306532173 (Targeted HA docker GRUEN, BLOCKER Voll-Cluster) und eigenen Repeat. claim publiziert 2026-11-01 nach Heilung von plan.py check (lane plan-hygiene @74ce5e4)."
resolution: ""
evidence: [evidence/board-2026-11-01/docker-engine-1245/evidence.md]
---

- [ ] t-20261101-docker-engine-1245 · resolve the ACTIVE Docker context (rootless + rootful) without a hardcoded uid socket #task #release/v0-4-27 #status/accepted #view/accepted #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith1.5 (Ornith; session 35cdb02e-a3b3-4e6d-86f9-1cbb35822587)  
    **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
    **Blocker:** Merge blockt ausschliesslich am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum) — KEIN Required-Check von \#1245/\#1250 (Pflicht = Lifecycle-Gates, die GRUEN). Ha-Blocker-Klasse bestaetigt durch CI run 41306532173 (Targeted HA…  
    **Evidence:** [proof 1](evidence/board-2026-11-01/docker-engine-1245/evidence.md)  
    <!-- /generated:card -->
  <!-- generated:card -->
  **Owner:** worker-ornith1.5 (Ornith; session 35cdb02e)
  **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250) (work/docker-endpoint-context-ornith, head 78fe0a54 — byte-identisch zu #1245 HEAD 262f069f)
  **Blocker:** Merge blockt am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum) — kein Required-Check von #1245/#1250. Lifecycle-Gates (Targeted HA docker, ci.yml) GRUEN auf head 78fe0a54 (CI run 41306532173).
  **Evidence:** [proof](https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md)
  <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Owner:** worker-ornith1.5 (Ornith; session 35cdb02e-a3b3-4e6d-86f9-1cbb35822587)  
**Priority:** not set  
**PRs:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
**Source:** 
<!-- /generated:links -->

## Goal

BaseHarbor finds the Docker endpoint an instance runs on reliably, rootful as well as rootless, by resolving the active Docker context like the docker CLI instead of a hardcoded per-user socket.

## Scope

- In scope: internal/runtime/docker_engine*.go, internal/providers/runtime/podman/provider_status_test.go, cmd/baha/runtime_restart_integration_test.go.
- Out of scope: CI workflow files, other lanes' evidence, #1231/#1232 (documented as sibling engine-probe lanes).

## Acceptance

- A1: exact HEAD of #1245 has PR Selected Checks + Selected Runtime without error; the runtime qualification actually ran for the changed path.
- A2: a test proves rootless AND rootful endpoint detection without a hardcoded uid path (regression against docker_engine.go:85).
- A3: #1231/#1232 documented as closed-by-ancestry OR independent green candidate.

## Required checks

- Lifecycle gates (atomic/docker/lifecycle, runtime-qualified) — green on head 78fe0a54 (CI run 41306532173).
- Native control-plane HA full-cluster (Targeted Integration) is NOT a required check for this lane.

## Dependencies and file ownership

- Owned files / area: internal/runtime/docker_engine.go (sole owner, mission verified facts).
- Shared files: coordinate through the owning task.

## Handoff

Merge is Owner/Maintainer authority only. The candidate (MR #1250, byte-identical to #1245 HEAD) is ready; only the non-required full-cluster proof is outstanding. #1231/#1232 remain open sibling lanes.
