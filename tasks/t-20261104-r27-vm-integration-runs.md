---
id: t-20261104-r27-vm-integration-runs
card_number: "0427-107"
card_short_title: "real Docker and Podman Integr"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-107-docker2-bughunt
kanban_lane: blocked
kanban_summary: "The real Docker and Podman integration suites run on the rebuilt test hosts against core, demo, console and connector, and each…"
kanban_status: blocked
kanban_title: "0427-107 · real Docker and Podman Integr"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261018-r27-node-service, t-20261104-r27-vm-rebuild-integration]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: "stale claim from 11-04 wave (lane-0427-107-docker2-bughunt no longer exists; hunt docker2 finished via hp3/podman2 dossiers). Work needs either a fresh integration-run mission or owner decision; not on any live lane."
resolution: ""
evidence: []
wait_reason: ""

---

- [ ] t-20261104-r27-vm-integration-runs · Operations: real Docker and Podman integration runs with core, demo, console and connector #task #release/v0-4-27 #status/blocked #view/blocked #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-107-docker2-bughunt · **Priority:** high  
    **Blocker:** stale claim from 11-04 wave (lane-0427-107-docker2-bughunt no longer exists; hunt docker2 finished via hp3/podman2 dossiers). Work needs either a fresh integration-run mission or owner decision; not on any live lane.  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261104-r27-vm-rebuild-integration](t-20261104-r27-vm-rebuild-integration.md)  
**Required by:** [t-20261107-r27-runtime-broker-oras-missing-edge-readiness](t-20261107-r27-runtime-broker-oras-missing-edge-readiness.md)  
**Owner:** lane-0427-107-docker2-bughunt  
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

wieder active gesetzt: w288 faehrt gerade die podman-seite der matrix (0/4 war der stand von w269). offene zweigruende bleiben: (1) connector-zelle ist TWO-HOST-flow — R2 erlaubt einer Bahn nur EINEN host, wartet auf deine regelentscheidung; (2) demo-zelle braucht auf dem host das r27-w150-demo-repo + provisioniertes managed backend (sql/redis/s3) — provisioning-lane folgt, sobald ein sitz frei ist. docker-seite: 2/4 gruen (core+console PASS), akte auf main.

owner-freigabe 05:0xZ: zwei-rechner-ausnahme fuer die fertigstellende bahn — w288 haelt baha-podman + baha-docker-2 gleichzeitig und uebernimmt damit auch die demo-provisionierung (bisher als externer blocker gemeldet). status gruende damit beseitigt: connector-zelle = ausgehend freigeben, demo-zelle = einrichtung teil dieses auftrags.

kein blocker mehr: braucht ein nachweis mehrere Maschinen, werden mehrere bereitgestellt (owner-regel 05:2xZ, RUNBOOK R2). w288 haelt baha-podman + baha-docker-2 und faehrt: podman-matrix (4 zellen) -> demo-einrichtung auf docker-2 (r27-w150-demo-repo + managed backend sql/redis/s3) -> connector-zelle im zwei-rechner-ablauf. bisherige zeugen: docker-seite 2/4 gruen (core+console PASS, akte round-1.md + docker-2-finding.md auf main).

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

akte round-3-docker-podman2.md auf origin/main (c5b947df); lane hat eigene compose auf beiden hosts downgemacht (0 lane-container ps-zeugnis).

owner-direktive 2026-11-07: #107 -> ACTIVE. podman-2 host-blocker behoben (ip_forward). realer docker+podman integration-lauf wird jetzt gefahren (coord host-ops + 021 CI runtime cells + 003/118 outputs).

#107 host-config erledigt (ip_forward). native VM-laeufe fuellen #110/#003 pods. KEINE aktive worker-bahn => wait, nicht active. trigger: #110 podman cells durch.

owner-direktive: hand-festival docker-2 — greenfield+brownfield+alle wizards, KEIN HA, nur befundung ohne produkt-aenderungen. lane 2cc3a33a.
