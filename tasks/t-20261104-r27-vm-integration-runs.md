---
id: t-20261104-r27-vm-integration-runs
card_number: "0427-107"
card_short_title: "Core Demo runtime flow"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: mcpdev80 (awaiting release acceptance)
kanban_lane: wait
kanban_summary: The selected release candidate completes the developer-PC-to-Core-VM journey with Core and Demo on Docker and Podman. Each…
kanban_status: wait
kanban_title: 0427-107 · Core Demo runtime flow
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261104-r27-vm-rebuild-integration]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/43328719841", "https://github.com/mcpdev80/baseharbor/actions/runs/43328719851"]
wait_reason: "The old eight-cell Core/Demo/Console/Connector matrix is out of scope. Keep this card open only until the current pinned Core+Demo candidate has the intended developer-PC-to-VM lifecycle evidence on Docker and Podman; selector-only CI runs do not count as a runtime result."

---

- [ ] t-20261104-r27-vm-integration-runs · Operations: Core + Demo developer-workstation-to-VM flow on Docker and Podman #task #release/v0-4-27 #status/wait #view/wait #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (awaiting release acceptance) · **Priority:** high  
    **Waiting:** The old eight-cell Core/Demo/Console/Connector matrix is out of scope. Keep this card open only until the current pinned Core+Demo candidate has the intended developer-PC-to-VM lifecycle evidence on Docker and Podman; selector-only CI runs…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/43328719841), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/43328719851)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261104-r27-vm-rebuild-integration](t-20261104-r27-vm-rebuild-integration.md)  
**Owner:** mcpdev80 (awaiting release acceptance)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The selected release candidate completes the developer-PC-to-Core-VM journey with Core and Demo on Docker and Podman. Each runtime result records exact Core/Demo revisions and the user-visible lifecycle outcome.

## Scope

- In scope: executed integration runs per host and per repository with recorded revision pairs, cleanup of what
  each run creates, and a finding on the owning feature card for every product defect the run exposes.
- Out of scope: host rebuild (t-20261104-r27-vm-rebuild-integration), workflow and runner definitions (shared
  GitHub runners), Proxmox and productive services, release promotion or tagging, weakening a test to pass.

## Acceptance

- Two runtime journeys are executed: developer workstation → Core on Docker VM, and developer workstation → Core on Podman VM. Each records exact Core/Demo revisions and result.
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

## Kanban-Audit 2026-11-09 — kein technischer Blocker

- Der bisherige `blocker` bezog sich nur auf eine nicht mehr aktive Lane. Eine fehlende Lane ist keine Owner-Entscheidung oder technisch unmoegliche Implementierung: **blocked -> wait**.
- Die direkten technischen Voraussetzungen `device-enrollment`, `node-service`, `vm-rebuild-integration` sowie der private Integration Path sind in den Plan-Karten `closed`/`accepted`. Der alte Nachweisstand `Docker core+console 2/4 PASS` ist historisch; die vollstaendigen acht Kombinationen sind nicht belegt.
- CI-Owner-/Coordinator-Uebergabe steht aus. Nach aktueller Owner-CI-Policy werden Native-/PR-Tests auf GitHub-hosted Docker/Podman-Runnern ausgefuehrt; Cross-Repo-E2E wird in der develop-/Release-Qualifikation geprueft, nicht als zusaetzliches PR-Gate oder manuelle Hardwarepflicht. Die alten VM-Anweisungen in Scope/Acceptance sind historische Ausgangsanforderungen und muessen vor Wiederaufnahme mit der aktuellen CI-Policy abgestimmt werden.
- Nicht `closed`: kein 8/8-Run und keine SHA-genauen allseitigen Integrationsnachweise behauptet. Nicht `active`: kein aktueller Worker nachgewiesen. Wiederaufnahme, sobald Coordinator die CI-Integration/Abnahme explizit uebernimmt.

## Owner closure — 2026-11-13

Owner closure: accepted 2026-11-13. Per the current CI policy, runtime validation is performed by hosted Docker/Podman gates and release qualification; the old eight-cell two-host VM matrix is retired. These links prove the cited repository runs only; they are not represented as one eight-cell cross-repository run.

## Reopened after full v0.4.27 audit — 2026-11-13

The old eight-cell Core/Demo/Console/Connector matrix is out of scope. Keep this card open only until the current pinned Core+Demo candidate has the intended developer-PC-to-VM lifecycle evidence on Docker and Podman; selector-only CI runs do not count as a runtime result.


## Release scope correction — 2026-11-13

This card no longer requires Console or Node Connector cells. The v0.4.27 user journey is driven from the developer workstation against Core running on the selected Docker/Podman VM; the Core executes the app on that same VM. Separate remote-runtime Connector acceptance is v0.4.28.
