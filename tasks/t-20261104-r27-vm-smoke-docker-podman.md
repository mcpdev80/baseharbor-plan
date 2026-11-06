---
id: t-20261104-r27-vm-smoke-docker-podman
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: coord-welle5 (Lane w212, freigegeben)
kanban_lane: blocked
kanban_summary: "A workstation enrolls once against a real BaseHarbor installation and the node service installs, starts, restarts and is removed…"
kanban_status: blocked
kanban_title: "Operations: real-VM smoke test of enrollment and node service on Docker and Podman hosts"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261018-r27-node-service]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: "Infra: baha-podman nicht erreichbar (SSH-banner-timeout, coord-nachmessung deckt sich mit lane + compose-befund 11-06); docker-half ok (kein baha installiert). Mission-Zeile 'baha-runner-*' stammte aus lane-lektuere, datei nennt korrekt baha-docker/baha-podman. Trigger: podman-VM wiederherstellung (owner-infra)."
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-vm-smoke-docker-podman · Operations: real-VM smoke test of enrollment and node service on Docker and Podman hosts #task #release/v0-4-27 #status/blocked #view/blocked #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w212, freigegeben) · **Priority:** high  
    **Blocker:** Infra: baha-podman nicht erreichbar (SSH-banner-timeout, coord-nachmessung deckt sich mit lane + compose-befund 11-06); docker-half ok (kein baha installiert). Mission-Zeile 'baha-runner-\*' stammte aus lane-lektuere, datei nennt korrekt ba…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
**Owner:** coord-welle5 (Lane w212, freigegeben)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

A workstation enrolls once against a real BaseHarbor installation and the node service installs, starts, restarts and is removed on both a Docker host and a Podman host, using real VMs rather than only in-process tests. An operator gets reproducible smoke evidence that the two features work on the runtimes the product actually supports.

## Scope

- In scope: one worker lane executes scripted smoke runs over owner-provided SSH access to the Docker VM and the Podman VM; enrollment happy path plus one-use rejection; node service package install/start/restart/uninstall without Go on the node; captured logs and a machine-readable summary per host and runtime.
- Out of scope: CI or runner changes (owner-owned), release promotion or tagging, long-lived infrastructure, new product interfaces beyond the two predecessor cards, secrets handling on the VMs beyond what the existing access already provides.

## Acceptance

- Executed by a worker lane, not by the coordinator; the lane reports its own observed run end to end for both hosts.
- Both runtimes are covered: Docker VM and Podman VM, each with its own log set.
- Enrollment is proven callable end to end on a real host: first use succeeds, second use of the same code is refused.
- Node service lifecycle is proven on a real host without Go installed: install, start, restart keeps behavior, uninstall leaves no orphan unit.
- Every claim in the evidence is backed by command output captured in the run; the reproduction script lives in the evidence scripts path so the run can be repeated.
- Any failure found is filed as a concrete finding with the exact command and output, then fixed by the owning feature card before this card can close.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Handoff

- Predecessors: t-20261018-r27-device-enrollment and t-20261018-r27-node-service must have a reviewable candidate each; this card runs against those candidate builds.
- Owner directive 2026-11-04: real VM smoke test required for this feature pair; execution belongs to a worker lane. SSH host access is provided by the owner environment and is never configured by the lane itself.
