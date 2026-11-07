---
id: t-20261106-r27-remote-up-cli-path
card_number: "0427-116"
card_short_title: "CLI start path for Prov-bound"
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: 0427-116-cli-path
kanban_status: blocked
kanban_title: "0427-116 · CLI start path for Prov-bound"
kanban_lane: blocked
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: [mcpdev80/baseharbor#1407]
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
blocker: "ErrDeploymentOwnerMissing wird auf docker UND podman am kopf 86f96a... reproduziert; die karte wartet auf die LANDUNG von 0427-117 (owner-inherit fix auf develop). naechster trigger: 117 merged develop."
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md"]

---

- [ ] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/blocked #view/blocked #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** 0427-116-cli-path · **Priority:** normal  
    **PR:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407)  
    **Blocker:** ErrDeploymentOwnerMissing wird auf docker UND podman am kopf 86f96a... reproduziert; die karte wartet auf die LANDUNG von 0427-117 (owner-inherit fix auf develop). naechster trigger: 117 merged develop.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Required by:** [t-20261106-r27-remote-up-podman-owner-missing](t-20261106-r27-remote-up-podman-owner-missing.md)  
**Owner:** 0427-116-cli-path  
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

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

bahn hat basis konfliktfrei auf develop 934be499b aufgefrischt (head 86f990a6) und die beiden zellen ausgefuehrt — ergebnis ist der owner-seam-fehler, nicht ein neuer defekt dieser karte.
