---
id: t-20261120-r28-bughunt-source-symlink-slice
kanban_title: 0428-158 · bughunt source symlink slice
card_number: "0428-158"
card_short_title: "bughunt source symlink slice"
type: task
areas: [cli, application, security]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w158-pr0428-158-symhunt
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-source-symlink/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---
- [x] t-20261120-r28-bughunt-source-symlink-slice · source-model- und symlink-flaeche befunden #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/application #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** w158-pr0428-158-symhunt  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-source-symlink/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w158-pr0428-158-symhunt  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
## Ziel

Bug-Hunt-Schnitt H-V9 auf der frisch gemergten Flaeche: 0428-059 source model slice
(merge 15727ca88) und die Symlink-Enthaltung (#1706, merge 97abbe157). Reine Befundung,
keine Produktaenderung. Funde gehen als eigene Karten zurueck an den Coordinator.

## Pruefschnitte

1. Symlink-Enthaltung an jedem Ort, der einen Component-Pfad aufloest (S1).
2. 'unique components' gegen registry und footprint (S2).
3. maschinelle CLI-Registrierung (machine_coverage.go, handschriftlich) gegen den echten Kommando-Baum (S3).
4. wizard- und mcp-Pfade gegen denselben Validierungshelfer wie der source-model-Zweig (S4).

## Akte

evidence/r28-welle4-2026-11-19/bughunt-source-symlink/round-1.md

jagd H-V9 BEFUNDBLOS, vier szenen je mit datei:zeile (S1 entwicklungResolveWorkspace/resolveContainedWorkspaceDirector, S2 internal/development/source.go:174-176 uniqueness, S3 machine_coverage.go :95/:133/:189 gegen den kommando-baum, S4 wizard/mcp-validierungs-helfer), akte 5917 bytes auf main 1c01f635, checkboxen null, besenrein. Fund→Karten-pflicht: kein fund, keine neue karte. Der inhaltliche wert: der 059-und-#1706-merge ist damit von zwei seiten befunden (destroy-pfade durch 157, quelle/pfade durch 159-vorgaenger 158)
