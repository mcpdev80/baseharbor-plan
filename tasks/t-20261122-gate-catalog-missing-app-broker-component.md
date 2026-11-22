---
id: t-20261122-gate-catalog-missing-app-broker-component
card_number: "0428-242"
card_short_title: "app_broker not in gate catalog"
type: bug
areas: [testing, ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: wait
kanban_lane: wait
kanban_summary: "Make broker diagnostics provable in hosted CI: scripts/pr-gate-coverage.json carries 65 cmd/baha path entries but no entry…"
kanban_title: 0428-242 · app_broker not in gate catalog
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "scripts/pr-gate-coverage.json traegt keinen component fuer cmd/baha/app_broker (65 cmd/baha, 0 app_broker); PR 1763 head c698d1310 hat damit leere native gate-plan matrix und keinen runtime-beleg"
resolution: ""
evidence: []
---

- [ ] t-20261122-gate-catalog-missing-app-broker-component · Gate catalog: no coverage component for cmd/baha/app_broker.go #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting:** scripts/pr-gate-coverage.json traegt keinen component fuer cmd/baha/app\_broker (65 cmd/baha, 0 app\_broker); PR 1763 head c698d1310 hat damit leere native gate-plan matrix und keinen runtime-beleg  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make broker diagnostics provable in hosted CI: `scripts/pr-gate-coverage.json` carries 65 `cmd/baha` path entries but no
entry matching `app_broker`, so a PR that only changes `cmd/baha/app_broker.go` plans an EMPTY native matrix and its runtime
diagnostic path is never exercised by a hosted job.

## Measured evidence

- `git show develop:scripts/pr-gate-coverage.json` → `cmd/baha` appears 65 times, `app_broker` 0 times (2026-11-22).
- PR #1763 run `45009251403` at exact head `b38838e1c30` is SUCCESS, trusted plan job `137167667713` reports the native gate
  plan selected an empty matrix, and `PR · Native matrix` is SKIPPED. A skipped gate is not evidence.

## Acceptance

1. One catalog component maps `cmd/baha/app_broker.go` to the gates that must run when broker diagnostics change.
2. A follow-up PR that only edits that file triggers at least one executed native or selected runtime row (witnessed by job
   id), or the plan explicitly documents why unit sentinels are sufficient.
3. No lane edits `scripts/**`: this is an Owner-scope catalog change, tracked here so the finding is not lost.

## Boundaries

`scripts/pr-gate-coverage.json` (Owner scope) plus its validation script. No product files in this card.

DER EINE FEHLENDE SCHRITT FUER #1763 RUNTIME-BELEG (owner-scope scripts/**): #1763 head c698d1310 hat 'Native gate plan matrix empty', selected runtime skipped, kein runtime-zeugnis fuer die broker-diagnose. Loesung liegt NICHT bei der lane - scripts/pr-gate-coverage.json braucht einen component-Eintrag, der cmd/baha/app_broker.go auf die data-capabilities-native-gaete mappt. Damit der owner es direkt setzen kann: genuegt ein eintrag analog der bestehenden cmd/baha/app_*-muster (datei ~142 ff), 'path':'cmd/baha/app_broker.go' plus dieselbe gate-liste wie die anderen cmd/baha-dateien.

owner-scope stueck, damit #1763 runtime-beleg bekommt. Gemessen an head c698d1310 durchgang 45011815553: 'Native gate plan matrix EMPTY', selected runtime skipped - die broker-diagnose hat KEINEN gehosteten runtime-zeugen. Loesung = ein component-eintrag in scripts/pr-gate-coverage.json der cmd/baha/app_broker.go auf die data-capabilities-native gaete mappt (analog der cmd/baha/app_* muster ab datei ~142). Kein lanen-zugriff (scripts/**).
