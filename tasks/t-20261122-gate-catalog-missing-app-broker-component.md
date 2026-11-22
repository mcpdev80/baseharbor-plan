---
id: t-20261122-gate-catalog-missing-app-broker-component
card_number: "0428-242"
card_short_title: "app_broker not in gate catalog"
type: bug
areas: [testing, ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ffe7611b (Codeman lane, OWNER-FREIGABE scripts/** 22.11) / coord (zeugnis)
kanban_status: active
kanban_lane: active
kanban_summary: "Make broker diagnostics provable in hosted CI: scripts/pr-gate-coverage.json carries 65 cmd/baha path entries but no entry…"
kanban_title: 0428-242 · app_broker not in gate catalog
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1763]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45011815553"]
---

- [ ] t-20261122-gate-catalog-missing-app-broker-component · Gate catalog: no coverage component for cmd/baha/app_broker.go #task #release/v0-4-28 #status/active #view/active #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** ffe7611b (Codeman lane, OWNER-FREIGABE scripts/\*\* 22.11) / coord (zeugnis) · **Priority:** high  
    **PR:** [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45011815553)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261121-static-gate-registration](t-20261121-static-gate-registration.md), [t-20261122-runtime-broker-health-unhealthy](t-20261122-runtime-broker-health-unhealthy.md)  
**Owner:** ffe7611b (Codeman lane, OWNER-FREIGABE scripts/** 22.11) / coord (zeugnis)  
**Priority:** high  
**PRs:** [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763)  
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

VON DER #1763-LANE BELEGT (head c698d1310, run 45011815553 SUCCESS, alle vier runtime-reihen SKIPPED). Die einzige loesung liegt in scripts/pr-gate-coverage.json: ein component analog cmd/baha/app_* (ab datei ~142) der app_broker.go auf die data-capabilities-native gaete mappt. File:line in akte runtime-broker-0428-240/ready-round-1.md. Owner-aktion, keine lane.

UMGESTELLT von 'blocked auf owner' auf 'active Codeman': der owner hat am 22.11 scripts/** fuer die Codeman-front FREIGEGEBEN. Ein vorgang = (A) katalogeintrag cmd/baha/app_broker.go in pr-gate-coverage.json (muster: path+surfaces data.capabilities docker+podman) + (B) fail-loud-Waechter (validate-pr-gate-coverage.py / pr-native-gate-plan.py): geaenderte UNKATALOGISIerte datei => exit!=0 mit fehlender katalognummer + naechster handlung, NIE leere matrix=gruen. + (C) test-faelle katalogisiert vs unkatalogisiert. Bezug #1763 native matrix. KEINE broker-/runtime-/github-datei (Codex Runner domain).
