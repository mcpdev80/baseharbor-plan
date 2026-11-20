---
id: t-20261120-r28-merge-window-audit-r2
kanban_title: 0428-164 · merge window audit r2
card_number: "0428-164"
card_short_title: "merge window audit r2"
type: task
areas: [ci, coordination]
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
- [ ] t-20261120-r28-merge-window-audit-r2 · die merges nach karte 150 auf blob-identitaet pruefen #task #release/v0-4-28 #status/planned #view/ready #area/ci #area/coordination #kind/task
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

Zweite Fenster-Integritaetspruefung fuer die merges NACH karte 0428-150: #1578 (merge d5c11753e), #1580 (merge bbc937c8f1), #1706 (merge 97abbe157), #1595 (merge 15727ca88). Reine verifikation, keine produktaenderung, kein PR.

## Pruefschnitte

1. B1 blob-identitaet je merge: diff PR-head gegen merge-commit; nicht leer = fremde zeilen im merge, mit datei:zeile.
2. B2 urteil-am-merge-sha: pro merged sha eine CODEX-urteilsdatei in evidence/*/codex-review-wave/ oder ausdruecklich nicht (heute vier faelle).
3. B3 doppelarbeit: paare offener PRs mit derselben datei in dieselbe richtung (bestaetigung/Widerlegung #1614 gegen #1645).
4. B4 brett-wahrheit: karten mit status review/closed gegen den echten PR-zustand (draft, merged, state) — der fall, den ich heute dreimal von hand zurueckziehen musste.

## Akte

evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md
