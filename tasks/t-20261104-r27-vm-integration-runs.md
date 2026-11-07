---
id: t-20261104-r27-vm-integration-runs
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: w269-vm-integration-runs
kanban_lane: blocked
kanban_summary: "The real Docker and Podman integration suites run on the rebuilt test hosts against core, demo, console and connector, and each…"
kanban_status: blocked
kanban_title: "Operations: real Docker and Podman integration runs with core, demo, console and connector"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261018-r27-node-service, t-20261104-r27-vm-rebuild-integration]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: "zwei von vier zellen brauchen maschinen, die es unter den geltenden regeln fuer eine einzelne Bahn nicht gibt: (1) connector-zelle ist ein TWO-HOST-Flow (core auf host A, node auf host B) — R2 erlaubt einer Bahn genau EINEN host gleichzeitig; (2) demo-zelle braucht auf baha-docker-2 (205) das r27-w150-demo-repo plus ein provisioniertes managed backend (sql/redis/s3) — beides fehlt dort. ergebnis bisher: core+console PASS (SINGLE default Core READY, doctor OK, status read-only), docker-podman-matrix 2/4 gruen. naechster trigger: (a) owner-entscheid, ob eine zwei-host-bahn ausdruecklich zwei locks halten darf (R2-ausnahme) oder zwei bahnen koordiniert werden, (b) provisioning-laeuft auf 205"
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-vm-integration-runs · Operations: real Docker and Podman integration runs with core, demo, console and connector #task #release/v0-4-27 #status/blocked #view/blocked #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** w269-vm-integration-runs · **Priority:** high  
    **Blocker:** zwei von vier zellen brauchen maschinen, die es unter den geltenden regeln fuer eine einzelne Bahn nicht gibt: (1) connector-zelle ist ein TWO-HOST-Flow (core auf host A, node auf host B) — R2 erlaubt einer Bahn genau EINEN host gleichzeit…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261104-r27-vm-rebuild-integration](t-20261104-r27-vm-rebuild-integration.md)  
**Required by:** [t-20261107-r27-runtime-broker-oras-missing-edge-readiness](t-20261107-r27-runtime-broker-oras-missing-edge-readiness.md)  
**Owner:** w269-vm-integration-runs  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The real Docker and Podman integration suites run on the rebuilt test hosts against core, demo, console and
connector, and each combination leaves a pass/fail line with the exact revisions used, so release qualification
is based on executed runs instead of skipped gates.

## Scope

- In scope: executed integration runs per host and per repository with recorded revision pairs, cleanup of what
  each run creates, and a finding on the owning feature card for every product defect the run exposes.
- Out of scope: host rebuild (t-20261104-r27-vm-rebuild-integration), workflow and runner definitions (shared
  GitHub runners), Proxmox and productive services, release promotion or tagging, weakening a test to pass.

## Acceptance

- Eight combinations are executed (two hosts x core, demo, console, connector) and each leaves a run line with
  host, repository, source revision and result.
- A skipped or simulated run does not count; the evidence holds the command and its output.
- Product defects are filed on their own cards; this card closes when the runs themselves work.
- A worker executes the runs; the coordinator verifies on disk and publishes.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- Lage 2026-11-04 (Koordinator, plattenfest): der NEGATIVE nachweis ist auf der Rechnerseite erfuellt
  (Ablehnung ohne wirkung, anwendung bleibt nicht ausgeliefert, rueckgabewert eins), der POSITIVE zyklus ist
  ohne den gemeinsamen stapel derzeit NICHT herstellbar. grundlage und folgenarbeit stehen auf
  t-20261104-r27-private-integration-path. diese karte bleibt offen, bis dieser pfad existiert.

## Release gate: SINGLE default / explicit HA opt-in (Owner, 2026-11-06)

- Governing contract: `t-20261106-r27-control-plane-single-default`. The Docker and Podman integration runs must demonstrate that an unmodified production default startup creates ONE instance per required control-plane service, with no implicit HA members or load balancers.
- Additionally execute an explicitly selected HA positive run on each runtime. Archive both topologies, health and restart results, rendered Compose configuration, container inventory, product SHA, and verifiable command transcripts.
- Fail closed: implicit HA in the default, an unverified topology, or SKIP means FAIL/BLOCKED and must not qualify the release. Never execute these tests on the Codeman server `baha-runner-docker-2`.

akte auf plan main: evidence/r27-welle5-folge-2026-11-06/vm-integration-runs/round-1.md + docker-2-finding.md; neue defektkarte t-20261107-r27-runtime-broker-oras-missing-edge-readiness ist von mir schema-gefixt (b8fe933e) und in arbeit
