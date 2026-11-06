---
id: t-20261106-r27-remote-up-cli-path
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: w264-remote-up-cli
kanban_status: active
kanban_lane: active
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: []
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
---

- [ ] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/active #view/active #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** w264-remote-up-cli · **Priority:** normal  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Owner:** w264-remote-up-cli  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Purpose

Ferngesteuerte Apps lassen sich anlegen/planen/prüfen (plan/status/doctor belegt), aber der
Start-Pfad (`baha app up`) ist über die Remote-Schiene nicht vollständig bedient: Befund-
dateien app_remote_lifecycle.go:34 (Gate) und runtime_explorer_machine.go:55; dev-seitig
fehlt der CLI-Startpfad für bindings-ferne Apps (round-3-Akte, w243/w262 Zeugnisse
evidence/r27-welle5-2026-11-06/remote-control-smoke/round-3.md).

## Acceptance

- `baha app up` (und --confirm-candidate-Pfad) funktioniert gegen eine per Connector gebundene
  App auf Docker UND Podman; doctor meldet danach health OK ohne Befundzeile für den Up-Gap.
- Tests: rote-first-Zelle gegen aktuellen Stand; echte VM-Transkripte (vm-lock, einer-nach-anderer).
