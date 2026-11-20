---
id: t-20261120-r28-pr-inventory-audit
kanban_title: 0428-160 · pr inventory audit
card_number: "0428-160"
card_short_title: "pr inventory audit"
type: task
areas: [cli, application, security]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
resolution: ""
evidence: []
prs: []
created: 2026-11-20
wait_reason: ""

---
- [ ] t-20261120-r28-pr-inventory-audit · offene pull-requests des fensters inventurieren #task #release/v0-4-28 #status/planned #view/ready #area/application #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
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
## Ziel

Inventur aller offenen Pull-Requests des 0.4.28-Fensters ( basics-check meldet 25 gegen sollwert 12): je PR zustand,
kopf-alter, basis-abstand, schreib-konflikt und ein urteil in genau drei kategorien. Reine verifikation, KEINE
produktaenderung, KEIN schliessen von PRs (das ist meine aktion).

## Pruefschnitte

1. Symlink-Enthaltung an jedem Ort, der einen Component-Pfad aufloest (S1).
2. 'unique components' gegen registry und footprint (S2).
3. maschinelle CLI-Registrierung (machine_coverage.go, handschriftlich) gegen den echten Kommando-Baum (S3).
4. wizard- und mcp-Pfade gegen denselben Validierungshelfer wie der source-model-Zweig (S4).

## Akte

evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md
