---
id: t-20261120-r28-bughunt-source-symlink-slice
kanban_title: 0428-158 · bughunt source symlink slice
card_number: "0428-158"
card_short_title: "bughunt source symlink slice"
type: task
areas: [cli, application, security]
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
---
- [ ] t-20261120-r28-bughunt-source-symlink-slice · source-model- und symlink-flaeche befunden
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
