---
id: t-20261104-r27-vm-rebuild-integration
card_number: "0427-108"
card_short_title: "reproducible rebuild of the"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "coord-welle4 (lanes w116, w117)"
kanban_lane: closed
kanban_summary: "Both test hosts are rebuilt from their own setup scripts instead of patched by hand, and afterwards the real Docker and Podman…"
kanban_status: closed
kanban_title: "0427-108 · reproducible rebuild of the"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261104-r27-vm-integration-runs.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md"]
superseded_by: t-20261104-r27-vm-integration-runs

---

- [x] t-20261104-r27-vm-rebuild-integration · Operations: reproducible rebuild of the Docker and Podman test VMs and real cross-repo integration runs #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (lanes w116, w117) · **Priority:** critical  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261104-r27-vm-integration-runs.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md)  
**Owner:** coord-welle4 (lanes w116, w117)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Both test hosts are rebuilt from their own setup scripts instead of patched by hand, and afterwards the real
Docker and Podman integration suites run against core, demo, console and connector with compatible source
references, so release qualification rests on executed runs rather than skipped gates.

## Scope

- In scope: scripted rebuild and full cleanup of the Docker test VM and the Podman test VM (pure test
  environments, Owner authorization 2026-11-04), functional proof of each runtime, then executed integration
  runs of core, demo, console and connector on both hosts with recorded revision pairs.
- Out of scope: Proxmox hosts and any productive service, GitHub workflow and runner definitions (shared GitHub
  runners only), release promotion or tagging, and weakening any test to make a host pass.

## Acceptance

- Each host rebuild is reproducible: the run uses the host setup script, and any deviation is recorded as a
  script diff on the host, not as an undocumented manual step.
- Shared stacks are preserved; every destructive action is preceded by the recorded three-point check.
- Runtime is proven per host: version, a rootless run without sudo, a port mapping test, and a build cache test.
- The integration runs are executed on the hosts, not simulated on the coordinator: core, demo, console and
  connector each produce a pass/fail line per host with the exact source revision used.
- Product defects found by the runs are filed on their own feature card; they do not block this card, which
  closes when the hosts and the runs themselves work.
- A worker executes this; the coordinator dispatches and verifies on disk.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Handoff

- Owner directive 2026-11-04 (16:0x): test VMs are pure test environments, full cleanup and rebuild authorized,
  prefer reproducible rebuild over manual repair, Proxmox and productive services untouched, then run the real
  Docker/Podman integration tests with core, demo, console and connector, in parallel to the PR fixes.
- Lanes w116 (Docker host) and w117 (Podman host) execute the rebuild phase. A second pair of lanes executes
  the integration phase once both hosts report functional.

## Progress 2026-11-04
- Podman host: rebuilt from its own setup script by lane w117, functional proofs recorded (rootless run, port
  mapping, rc=0 lines) and the lane's own containers removed while every shared stack stayed up. The only
  remaining unhealthy item on that host is the external backup-recovery broker deployment, documented there as a
  blocker with cause and next trigger; it is not owned by this card.
- Docker host: lane w116 is executing the same rebuild now.
- Integration phase (core, demo, console, connector against a functional host) starts after w116 reports.

## Scope split 2026-11-04
- This card is the host phase only: rebuild both test hosts from their setup scripts and prove each runtime
  works. It does not depend on feature cards.
- The executed cross-repo integration runs live in t-20261104-r27-vm-integration-runs, which carries the feature
  dependencies.

## Version finding 2026-11-04 (coordinator, on disk)
- Both test hosts ship an installed `baha` in `~/.local/bin/baha` reporting **BaseHarbor 0.4.23**
  (baha-docker: dated 2026-10-08; baha-podman: reinstalled 2026-11-04 14:54 by its setup script).
- Current develop is ecbb8854 (v0.4.27 line). Any run that resolves `baha` from PATH therefore tests a binary
  four releases behind, and a green result would be worthless.
- Required by the rebuild phase: the host setup script must build and install `baha` from the source revision
  under test, and record `baha --version` plus that revision. The integration phase is blocked until both hosts
  show the matching version.
- Related pin to fix in the same pass: baseharbor-demo `baseharbor-core.ref` still points at 212ae90e.

## Ops probe result 2026-11-04 (second Codex instance, owner-requested test)
- The instance reported BLOCKED and wrote no evidence file: no stacks rebuilt, `baha` still 0.4.23
  (revision 9514a768be) on the Podman host. Useful facts, but the operating task belongs to a worker lane.
- Verified by the coordinator on the host: the backup-recovery broker container no longer exists (it was
  removed as lane-owned during the first Podman pass); host memory is tight (about 2.4 GB available of 7.9 GB),
  which matches the earlier exit 137. Historical logs additionally show a TLS handshake without a client
  certificate — recorded here as a possible product finding for the runtime-executor path, not something the
  VM lane fixes.
- Consequence: the Podman rebuild is re-commissioned for a worker lane with these findings in its brief, and the
  broker stack must come back from its own definition before backup/recovery tests count.

## Security finding 2026-11-04 — nicht bestätigt, Blocker aufgehoben
- Ein als Klartext-GitHub-Token gemeldeter Fund in `.codex/auth.json` auf dem Docker-Testrechner ist
  aufgeklärt: Die Datei `/home/marcel/.codex/auth.json` gehört zum OpenAI-Codex-Werkzeug selbst
  (Eigentümer `marcel`, Modus `600`, kein Weltleserecht). In den fünf BaseHarbor-Repositories existiert kein
  Commit dieses Dateipfads.
- Bewertung: kein Befund aus diesem Ökosystem, keine Entwertung oder Rotation eines Tokens veranlasst, nichts
  gelöscht. Der Hinweis, vorgefundene Anmelde-Dateien nur als Metadatum zu behandeln und zu melden, bleibt als
  Regel bestehen (AGENTS 5.6); er hat hier korrekt funktioniert.
- Damit ist der PAT-Blocker dieses Kartenzweigs aufgehoben. Andere technische Blocker (Schlüsselkarten-Stapel
  im Absturz, Datenbankanbindung der Prüfläufe) bleiben unberührt und werden weiter verfolgt.
