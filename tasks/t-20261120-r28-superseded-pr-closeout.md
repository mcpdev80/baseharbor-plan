---
id: t-20261120-r28-superseded-pr-closeout
kanban_title: 0428-169 · superseded PR closeout
card_number: "0428-169"
card_short_title: "superseded PR closeout"
type: maintenance
areas: [release]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w169-pr0428-169-closeout
kanban_status: active
kanban_lane: active
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-superseded-pr-closeout · close superseded PRs with ancestry proof #task #release/v0-4-28 #status/active #view/active #area/release #kind/maintenance
    <!-- generated:card -->
    **Owner:** w169-pr0428-169-closeout  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w169-pr0428-169-closeout  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Die 10 veralteten Pull Requests aus dem PR-Inventory (0428-160, Befund SUPERSEDED/TODC)
werden geschlossen — jeder einzelne mit Ancestry- oder Blob-Nachweis, nicht mit Verweis auf
die Liste. Grundlage ist Owner-Direktive 2026-10-28 (veraltete Staging-PRs und integrierte
Drafts nach Ancestry-Nachweis schließen) und §3.8.

## Liste (aus der Akte, Stand des Audits)

1627, 1620, 1597, 1594, 1665, 1645, 1588, 1587, 1585, 1582.

#1591 stand ebenfalls auf dieser Liste, ist aber inzwischen GEMERGT (merge-commit
83b19dce24ee, 2026-11-20T02:29:42+01) — es gehört in keine close-Aktion mehr, sondern ist
ein Beleg dafür, warum die Liste nicht ungeprüft übernommen werden darf.

## Vertrag

- Je PR: `gh api repos/mcpdev80/baseharbor/pulls/<n>` (state, draft, head.sha, base), dann
  ein Nachweis in einer Zeile: entweder `git merge-base --is-ancestor <head> origin/develop`
  = JA (Inhalt ist schon drin), oder `git diff --name-only <head> origin/develop -- <PR-Dateien>`
  = leer (Inhalt blob-identisch), oder — nur wenn beides NEIN — ein Satz, WARUM der Ansatz
  veraltet ist, mit der Karten-/PR-Nummer, die ihn ersetzt.
- Schließen erst NACH dem Nachweis, mit einem Kommentar, der den Nachweis enthält.
- Kein Branch-Löschen, kein Force-Push, kein Merge, keine Inhaltliche Änderung.

## Stop-Kriterium

Ein PR, dessen head Inhalt trägt, der auf develop NICHT vorhanden und NICHT ersetzt ist,
wird nicht geschlossen, sondern gemeldet (Nummer, Datei, Zeile, was fehlen würde). Zwei
solche Fälle sind ein Hinweis, dass das Inventory von 2026-11-19 zu alt ist — dann STOP.


## Akte

https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md
