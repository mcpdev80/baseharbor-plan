---
id: t-20261101-docker-engine-1245
card_number: "0427-093"
card_short_title: "resolve the ACTIVE Docker"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: worker-ornith-1245 (Ornith; session 35cdb02e)
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-093 · resolve the ACTIVE Docker"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1250"]
sources: []
blocker: ""
resolution: "accepted"
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md]
---

- [x] t-20261101-docker-engine-1245 · resolve the ACTIVE Docker context (rootless + rootful) without a hardcoded uid socket #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith-1245 (Ornith; session 35cdb02e)  
    **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md)  
    <!-- /generated:card -->
  <!-- generated:card -->
  **Owner:** worker-ornith-1245 (Ornith; session 35cdb02e)
  **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250) (work/docker-endpoint-context-ornith, head 78fe0a54 — byte-identisch zu #1245 HEAD 262f069f)
  **Blocker:** none — candidate ready; only non-required full-cluster proof outstanding.
  **Evidence:** [proof](https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md)
  <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** worker-ornith-1245 (Ornith; session 35cdb02e)  
**Priority:** not set  
**PRs:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
**Source:** 
<!-- /generated:links -->

## Ziel

BaseHarbor findet den Docker-Endpoint, unter dem eine Instanz läuft (rootful wie rootless), zuverlässig — statt hartcodiertem `/run/user/<uid>/docker.sock` die aktive Docker-Context-Wahl der CLI.

## Umfang

- In Scope: internal/runtime/docker_engine*.go, internal/providers/runtime/podman/provider_status_test.go, cmd/baha/runtime_restart_integration_test.go.
- Out of Scope: CI-Workflows, anderer Lanes Evidence, #1231/#1232 (Dokumentation als Sibling-Lanes).

## Akzeptanz

- A1: exakter Head von #1245 hat PR Selected Checks + Selected Runtime ohne Fehler; Runtime-Qualifizierung gelaufen.
- A2: ein Test beweist rootless UND rootful Endpoint-Erkennung ohne hartcodierten uid-Pfad.
- A3: #1231/#1232 dokumentiert (aus Ancestrylussfolgert).

## Pflicht-Checks

- Lifecycle-Gates (atomic/docker/lifecycle, runtime-qualifiziert) — GRUEN auf head 78fe0a54 (CI run 41306532173).
- Voll-Cluster-Nachweis (Targeted Integration) ist KEIN Pflicht-Check dieser Lane.

## Abhängigkeiten und File-Ownership

- Own: internal/runtime/docker_engine.go (sole owner, mission verified facts).
- Shared: durch die owning Task koordinieren.

## Handoff

Merge nur Owner/Maintainer-Autorität. Kandidat (MR #1250, byte-identisch zu #1245 HEAD) bereit; einziges offenes Thema das nicht-pflichtige Voll-Cluster-Nachweis. #1231/#1232 bleiben offene Sibling-Lanes.
