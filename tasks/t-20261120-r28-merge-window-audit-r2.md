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
owner: w164-pr0428-164-windowakte
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---
- [x] t-20261120-r28-merge-window-audit-r2 · die merges nach karte 150 auf blob-identitaet pruefen #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #area/coordination #kind/task
    <!-- generated:card -->
    **Owner:** w164-pr0428-164-windowakte  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w164-pr0428-164-windowakte  
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

## Hinweis des Coordinators, 2026-11-20 02:0x

B2 prueft zusaetzlich das RULESET, nicht den alten brancheschutz: 'gh api repos/mcpdev80/baseharbor/rulesets' zeigt ruleset 25223521 'develop - required checks' mit enforcement=ACTIVE (das aeltere 23754541 ist disabled). Meine feststellung 'develop hat keinen brancheschutz' kam aus '/branches/develop/protection' — diese API sieht rulesets NICHT, also war es ein messfehler durch die falsche API, an eine worker-session weitergegeben, und CODEX hat den merge von #1693 zu Recht verweigert. Melde bitte mit, welche offenen PRs an genau dieser regel haengen (mergeable_state=behind bei sonst gruener CI), damit ich die hopfreihenfolge danach setzen kann.

audit geliefert und von mir nachgemessen. B2 (urteil am merged sha): die fuenf merges #1578 #1580 #1595 #1706 #1707 haben KEIN verdict ammerged sha — meine eigene scharfe gegenprobe (datei muss 'Verdict:' UND den sha enthalten) bestaetigt das muster, nur #1693 traegt durch meine merge-aktion jetzt einen merged-sha-vermerk (1693-0428-123-merge.md, 'Verdict: MERGED 6b8188df26a1'). B3 (doppelarbeit): staerker als gemeldet — cmd/baha/app_status_result.go lebt in DREI verschiedenen versionen ueber die offenen PRs: blob 4052832c2d in #1606/#1615/#1645, 4bca9d58b1 in #1623/#1625, 0e5d91961b in #1614; develop traegt f963601a56, also weicht ALLE funf ab. Das ist kein stilfrage: whichever PR zuerst gemergt wird, bestimmt die datei, und die anderen vier bekommen konflikte. B1 (blob-identitaet je merge) und B4 (brett-wahrheit: kein review/draft-mismatch mehr) ohne befund. akte 11181 bytes auf main 81ed0cca, checkboxen null. FOLGE, die ich ziehe: (a) owner-draht-punkt 'merge-regel fuer Karten ohne verdict am merged sha' hat jetzt eine zahl: null von fuenf; (b) fuer app_status_result.go setze eine integrations-reihenfolge, bevor der naechste der fuenf PRs gemergt wird

Werkzeug-Hinweis: die Ablaufe dieser Karte werden von Coordinator-Skripten getragen; Werkzeug-Details und -Fehler laufen im Tooling-Repo https://github.com/mcpdev80/codeman-coordinator-tooling, nicht als Produktkarten.
