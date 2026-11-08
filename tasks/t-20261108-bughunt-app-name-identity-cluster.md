---
id: t-20261108-bughunt-app-name-identity-cluster
card_number: "0427-149"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w149-nameid
kanban_status: active
kanban_lane: active
kanban_summary: "Eine namensaesung im registry: registrieren prueft kollision (expliziter fehler statt stiller zweiter uuid), name-basierte…"
kanban_title: 0427-149 · app init Owner-Naht regression
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md"]
---
- [ ] t-20261108-bughunt-app-name-identity-cluster · Bug Hunt v0.4.27: Namens-Zwillinge sperren alles #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w149-nameid · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w149-nameid  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Eine namensaesung im registry: registrieren prueft kollision (expliziter fehler statt stiller zweiter uuid), name-basierte befehle loesen eindeutig oder nennen den konkreten ausweg (uuid), edit/show/plan/destroy funktionieren in allen dupel-zustanden; regressionen (dup-register, dup-edit, dup-destroy) in der lifecycle gruppe.

## Problem (Fund H-P3, datei-/#beleg in der Akte)
app edit meldet "application machine: denied" sobald eine zweite app mit gleichem NAME+environment existiert; app init registriert stumm duplikate unter NEUER uuid; app create erzeugt oeffnungen die kein name-basierter befehl mehr oeffnet/loescht; show/plan NAME-rat gibt einen flag der die kollision nicht loest. Quelle Hunt H-P3 BF-01/02/05/10 (blocker-kandidat).

## Acceptance
Eine namensaesung im registry: registrieren prueft kollision (expliziter fehler statt stiller zweiter uuid), name-basierte befehle loesen eindeutig oder nennen den konkreten ausweg (uuid), edit/show/plan/destroy funktionieren in allen dupel-zustanden; regressionen (dup-register, dup-edit, dup-destroy) in der lifecycle gruppe.

## Dependencies and file ownership
Keine. Write-set: app registry namensaesung + app edit/init/create/show/plan/destroy.
