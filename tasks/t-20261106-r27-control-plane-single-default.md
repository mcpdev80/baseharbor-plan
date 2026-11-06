---
id: t-20261106-r27-control-plane-single-default
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Die develop-Kontrollebene faehrt im Default als Einzel-Instanzen (ein Postgres, ein OpenBao), weil die Entwickler-Umgebung laut…"
kanban_title: "Control plane: default deployment must be SINGLE instances (per-service one postgres/one openbao, no HA ensemble); HA only as explicit opt-in"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261106-r27-control-plane-single-default · Control plane: default deployment must be SINGLE instances (per-service one postgres/one openbao, no HA ensemble); HA only as explicit opt-in #task #release/v0-4-27 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Die develop-Kontrollebene faehrt im Default als Einzel-Instanzen (ein Postgres, ein OpenBao),
weil die Entwickler-Umgebung laut Owner genau so gemeint ist. Heute zeigt der Auslieferungs-Standard ein
HA-Ensemble (3 OpenBao-Mitglieder + Balancer). Die Einzel-Form wird Default; HA bleibt als
explizit waehlbares Profil erhalten.

## Scope

- In scope:
- Out of scope:

## Proof / Befund (coord-Nachmessung 2026-11-06 14:1xZ, origin/main develop)

- Owner-Direktive woertlich: "openbao ist da insgesamt 4 mal zu sehen ist der aufbau als ha das
  waere komplett falsch es sollte default sein das nichts ha ist sondern einzeln".
- Produktbeleg: internal/runtime/assets/compose.yaml definiert offenbao-member-1/2/3 (Zeilen
  268/297/326) + haproxy (356) + postgres-etcd 1-3 (Zeilen 10/23/36) — das mitgelieferte
  Standard-Template IST das HA-Ensemble.
- Go-Seite kennt bereits beide Formen: internal/runtime/control_plane_profile.go
  (OpenBaoMembers 68-73, validateSingleControlPlane 75) — Einzel-Pfad existiert, ist aber nicht
  der Default des Assets.
- Live-Zeuge: baha-docker `docker ps` nach devenv-smoke-Aufbau: bh-local-shared-openbao-member-1/2/3
  + -admin + haproxy = 4-5 Tresor-Container; identisch bh-w169-ci-ctxa (CI-Kontext).

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
