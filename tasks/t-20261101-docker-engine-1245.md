---
id: t-20261101-docker-engine-1245
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: worker-ornith-1245
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1250"]
sources: ["mcpdev80/baseharbor#1250"]
blocker: "Merge blockt am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum) — KEIN Required-Check von #1245/#1250. Lifecycle-Gates (Targeted HA docker, ci.yml) GRUEN auf head 78fe0a54 (CI run 41306532173). Ha-Blocker-Klasse bestaetigt; claim publiziert nach Heilung plan.py check (plan-hygiene @74ce5e4)."
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md]
---

- [ ] t-20261101-docker-engine-1245 · resolve the ACTIVE Docker context (rootless + rootful) without a hardcoded uid socket #task #release/v0-4-27 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith-1245  
    **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
    **Blocker:** Merge blockt am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum) — KEIN Required-Check von \#1245/\#1250. Lifecycle-Gates (Targeted HA docker, ci.yml) GRUEN auf head 78fe0a54 (CI run 41306532173). Ha-Blocker-Klasse bestaetigt; c…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md)  
    <!-- /generated:card -->
  <!-- generated:card -->
  **Owner:** worker-ornith-1245
  **PR:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250) (work/docker-endpoint-context-ornith, head 78fe0a54 — byte-identisch zu #1245 HEAD 262f069f)
  **Blocker:** Merge blockt am Voll-Cluster-Nachweis (Targeted Integration, etcd DNS/quorum); Lifecycle-Gates GRUEN.
  **Evidence:** [proof](https://github.com/mcpdev80/baseharbor-plan/blob/master/evidence/board-2026-11-01/docker-engine-1245/evidence.md)
  <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Owner:** worker-ornith-1245  
**Priority:** not set  
**PRs:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/pull/1250)  
**Source:** [baseharbor#1250](https://github.com/mcpdev80/baseharbor/issues/1250)
<!-- /generated:links -->

## Ziel

BaseHarbor findet den Docker-Endpoint, unter dem eine Instanz läuft (rootful wie rootless), zuverlässig — auflösesstatt hartcodiertem `/run/user/<uid>/docker.sock` die aktive Docker-Context-Wahl der CLI.

## Umfang

- In Scope: internal/runtime/docker_engine*.go, internal/providers/runtime/podman/provider_status_test.go, cmd/baha/runtime_restart_integration_test.go.
- Out of Scope: CI-Workflows, anderer Lanes Evidence, #1231/#1232 (Dokumentation alsSibling-Lanes).

## Akzeptanz

- A1: exakter Head von #1245 hat PR Selected Checks + Selected Runtime ohne Fehler; Runtime-Qualifizierung gelaufen.
- A2: ein Test beweist rootless UND rootful Endpoint-Erkennung ohne hartcodierten uid-Pfad.
- A3: #1231/#1232 dokumentiert (geschlussfolgert aus Ancestry).

## Pflicht-Checks

- Lifecycle-Gates (atomic/docker/lifecycle, runtime-qualifiziert) — GRUEN auf head 78fe0a54 (CI run 41306532173).
- Voll-Cluster-Nachweis (Targeted Integration) ist KEIN Pflicht-Check dieser Lane.

## Abhängigkeiten und File-Ownership

- Own: internal/runtime/docker_engine.go (sole owner, mission verified facts).
- Shared: durch die owning Task koordinieren.

## Handoff

Merge nur Owner/Maintainer-Autorität. Kandidat (MR #1250, byte-identisch zu #1245 HEAD) bereit; einziges offenes Thema der nicht-pflichtige Voll-Cluster-Nachweis. #1231/#1232 bleiben offene Sibling-Lanes.
