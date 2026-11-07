---
id: t-20261106-r27-remote-up-cli-path
card_number: "0427-116"
card_short_title: "CLI start path for Prov-bound"
title: "Remote app up: CLI start path for provider-bound remote apps"
release: v0.4.27
priority: normal
type: task
areas: [cli, remote]
owner: lane-0427-116-remote-up-cli-r5
kanban_status: active
kanban_title: "0427-116 · CLI start path for Prov-bound"
kanban_lane: active
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-smoke-docker-podman]
prs: [mcpdev80/baseharbor#1407]
sources: ["mcpdev80/baseharbor#777"]
repos: [mcpdev80/baseharbor]
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md"]

---

- [ ] t-20261106-r27-remote-up-cli-path · Remote app up: CLI start path for provider-bound remote apps #task #release/v0-4-27 #status/active #view/active #area/cli #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-116-remote-up-cli-r5 · **Priority:** normal  
    **PR:** [baseharbor#1407](https://github.com/mcpdev80/baseharbor/pull/1407)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Required by:** [t-20261106-r27-remote-up-podman-owner-missing](t-20261106-r27-remote-up-podman-owner-missing.md)  
**Owner:** lane-0427-116-remote-up-cli-r5  
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

blocker '#117 landing' ERFUELLT (1419 merged develop beb923fe6 11:33Z); deps release-updates+vm-smoke closed. owner-direktive war conditional auf 117 -> jetzt bereit, seat-refill.

<<<<<<< HEAD
r3 request-changes: KEIN Erfolg-fall (err==nil) ueber echtes CLI baha app up auf Docker UND Podman; nur podman-negativ + interne direkt-aufrufe. ask-3 verweis auf #117 falsch (#117 = fail-closed owner-negativ, kein erfolg-transkript). r4 in FRISCHER lane = echter konfliktfreier einsatz auf dem freien sitz.
=======
## Owner-PR-Pruefung — 2026-11-07

- **PR #1407** head `5900dc6b71a2adfec1842164066475061a44d616` ist offen, mergeable und hat PR-CI [42374201283](https://github.com/mcpdev80/baseharbor/actions/runs/42374201283) SUCCESS.
- Der vorhandene Review-Befund verlangt zusaetzlich, dass `app up` nachweislich erfolgreich endet (nicht nur kein lokaler Core-Bootstrap), und einen echten Connector-gebundenen Docker- **und** Podman-Up+Doctor-Gesundheitsnachweis; Podman-Installation-Owner-Befund ist separat zu klaeren. PR-Gruen allein schliesst das nicht. Bis zur echten Abnahme in **review** belassen; kein Merge durch diesen Board-Abgleich.
>>>>>>> origin/main

head c4d528645 drift-frei (develop 812c99c88 Vorfahr), delta nur 116-dateien, CI run 4238139371 terminal PASS. CODEX-REVIEW ausgelöst.

CODEX-REVIEW r4 = REQUEST-CHANGES an head c4d528645: belegt nur fail-closed (upErr!=nil ohne live connector), KEIN echter successfull baha app up + healthy doctor auf Docker UND Podman, native HA/Runtime jobs skipped. run 42381393714 nur go-unit PASS. Review veroeffentlicht act-1407-r4.md (plan 4d00f0ee9). Korrektur r5 an c977fe82.
