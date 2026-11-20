---
id: t-20261120-r28-bughunt-uid-app-slice
kanban_title: 0428-159 · bughunt uid app identity
card_number: "0428-159"
card_short_title: "bughunt uid app identity"
type: task
areas: [cli, application, security]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w159-pr0428-159-uidhunt
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-uid-app/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---
- [x] t-20261120-r28-bughunt-uid-app-slice · uid-app-identitaet gegen rename und re-import befunden #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/application #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** w159-pr0428-159-uidhunt  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-uid-app/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w159-pr0428-159-uidhunt  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
## Ziel

Bug-Hunt-Schnitt H-V10 auf dem frisch gemergten uid-app-pfad (#1578, merge d5c11753ea43):
woher die stable uid kommt, ob rename/re-import sie erhaelt, und was bindings und
status-/desk-ansicht dabei mitmachen. Reine befundung, keine produktaenderung.

## Pruefschnitte

1. Symlink-Enthaltung an jedem Ort, der einen Component-Pfad aufloest (S1).
2. 'unique components' gegen registry und footprint (S2).
3. maschinelle CLI-Registrierung (machine_coverage.go, handschriftlich) gegen den echten Kommando-Baum (S3).
4. wizard- und mcp-Pfade gegen denselben Validierungshelfer wie der source-model-Zweig (S4).

## Akte

evidence/r28-welle4-2026-11-19/bughunt-uid-app/round-1.md
