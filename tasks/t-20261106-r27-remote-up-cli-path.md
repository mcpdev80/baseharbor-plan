---
id: t-20261106-r27-remote-up-cli-path
card_number: "0427-116"
card_short_title: "CLI start path for Prov-bound"
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: w285-pr1407-docker-cell
kanban_status: review
kanban_title: "0427-116 · CLI start path for Prov-bound"
kanban_lane: review
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: [mcpdev80/baseharbor#1407]
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md"]

---

- [ ] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/review #view/review #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** w285-pr1407-docker-cell · **Priority:** normal  
    **PR:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Required by:** [t-20261106-r27-remote-up-podman-owner-missing](t-20261106-r27-remote-up-podman-owner-missing.md)  
**Owner:** w285-pr1407-docker-cell  
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

kandidat c87c8b644cc auf develop dddf0d7823f; alle gehosteten checks success (skipped nach pfadregel), lauf 42320398007 terminal; docker-zelle meldet echten defekt ErrDeploymentOwnerMissing -> folgt auf karte t-20261106-r27-remote-up-podman-owner-missing

kandidat c87c8b644cc auf develop dddf0d7823f; alle gehosteten checks success (skipped nach pfadregel), lauf 42320398007 terminal; docker-zelle meldet echten defekt ErrDeploymentOwnerMissing -> folgt auf karte t-20261106-r27-remote-up-podman-owner-missing
