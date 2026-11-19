---
id: t-20261119-r28-obs-docs-verified-state-unreachable
kanban_title: "0428-148 · docs: perses 'verified' unerreichbar"
card_number: "0428-148"
card_short_title: "docs: perses 'verified' unerreichbar"
type: task
areas: [docs, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "hunt 0428-147 (akte evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md, haupt d667cce4)"
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-obs-docs-verified-state-unreachable · doku verspricht perses-zustand 'verified' #task #release/v0-4-28 #status/planned #view/ready #area/docs #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-docker-147.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Die observability-how-to fuehrt fuer 'perses status' einen zustand 'verified', den der status-pfad in diesem release nicht zurueckgeben kann. Fund aus einer echten runtime-zelle (baha-docker, develop 558dc42d0), nicht aus doku-lektuere. Ziel: die doku nennt nur zustaende, die der code erzeugen kann — oder der code erzeugt sie nachweislich.

## Scope

- In scope: docs/en/guides/observability-how-to.md (zeile 32 laut fund) und die entsprechende DE-stelle (zeile 28), plus der pfad, der die zustaende erzeugt (cmd/baha 'app perses status').
- Zur einordnung: der wert 'verified' existiert im code an anderer stelle (cmd/baha/app_evidence.go:168/:178) fuer einen ANDEREN kontext — das ist nicht derselbe zustandsraum.
- Out of scope: die 'Verification=none'-vertragsfrage (karte 0428-143, beim owner). Hier geht es ausschliesslich um ein versprochenes ergebnis in der doku.

## Acceptance

- Jede in der doku genannte status-zeile ist im code erzielbar, mit bedingungen-satz.
- Eine regression belegt den gelieferten zustand am echten pfad; bleibt 'verified' in der doku, muss ein test den wert erzeugen.
- documentation-audit laeuft am exaktkopf; selektiert die zuordnung docs/** nicht, ist das der bekannte befuend zu scripts/pr-gate-plan.py (karte 0428-144, owner-scope) — dann in der akte belegen statt 'gruen' behaupten.

## Required checks

- **Modified features:** doku-check (documentation-audit) + die status-regression der observability-pfade.
- **CI integration:** die neue regression muss in ihrem paket vom 'PR · Go unit'-shard ausgefuehrt werden (CI-aufnahmepflicht neuer tests).
