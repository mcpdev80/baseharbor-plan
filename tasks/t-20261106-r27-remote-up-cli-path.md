---
id: t-20261106-r27-remote-up-cli-path
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: coord-welle5 (wartend)
kanban_status: blocked
kanban_lane: blocked
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: [mcpdev80/baseharbor#1407]
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
blocker: "urteil 1407b REJECT: karten-acceptance verlangt lauffaehige zellen auf BEIDEN familien; podman-seite haelt am befund ErrDeploymentOwnerMissing (eigene karte t-20261106-r27-remote-up-podman-owner-missing, korrektur-lane laeuft), docker-VM-zelle pending (hostbelegung). trigger: owner-fehbehebung gelandet + docker-zelle nachgezogen + base auf aktuellen develop."

---

- [ ] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/blocked #view/blocked #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (wartend) · **Priority:** normal  
    **PR:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407)  
    **Blocker:** urteil 1407b REJECT: karten-acceptance verlangt lauffaehige zellen auf BEIDEN familien; podman-seite haelt am befund ErrDeploymentOwnerMissing (eigene karte t-20261106-r27-remote-up-podman-owner-missing, korrektur-lane laeuft), docker-VM-z…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Required by:** [t-20261106-r27-remote-up-podman-owner-missing](t-20261106-r27-remote-up-podman-owner-missing.md)  
**Owner:** coord-welle5 (wartend)  
**Priority:** normal  
**PRs:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407)  
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
