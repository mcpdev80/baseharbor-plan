---
id: t-20261121-base-branch-provenance-loss
card_number: "0428-221"
card_short_title: "0428-221 base provenance loss"
type: bug
areas: [cli, ci]
release: "v0.4.28"
version: ""
parent: ""
owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-221 · 0428-221 base provenance loss
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
created: "2026-11-21T09:35:37Z"
updated: "2026-11-21T09:35:37Z"
---

- [ ] t-20261121-base-branch-provenance-loss · 0428-221 base content of closed-unmerged lane branches must be recovered or the cards reopened #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by the coordinator (2026-11-21, finding-to-card duty AGENTS 3.3.5)

Measured, not inferred: PR #1726 (cards 0428-198 and 0428-204) is CLOSED without merge (`mergedAt` null, `closedAt` 2026-11-21T09:09:20Z, `mergeable` CONFLICTING) while both cards sit `closed` with `resolution: accepted`. The lane head `e45430f2f1b7` carries 11 commits that are absent from develop (`rev-list --count develop..e45430f2f1b7` = 11, `merge-base --is-ancestor` NEIN for all eight sampled commits). Content proof: develop has 0 occurrences of `withoutOperatorAuthTestContext` in `cmd/baha/app_init_wizard.go`, the lane has 2. Four open PRs (#1737 #1738 #1740 #1741) declare that lane as `baseRefName`, so none of them can ever be green against develop, and the 0428-220 supersede I booked on witness `46017060d` had to be withdrawn.

## Acceptance

1. For every closed-unmerged lane branch of this window: either its content is re-landed onto develop (a commit whose tree contains the delta) or the cards that recorded `accepted` are reopened with a note naming the lost commits.
2. A machine check that fails when a card is `accepted`/`closed` while its PR has `mergedAt` null: the state transition must require remote merge witness, per AGENTS 5.2.
3. A machine check that reports, per open PR, whether `baseRefName` head is an ancestor of develop or a live lane (no silent stale-base ancestry).

## Boundaries

Card fields in `baseharbor-plan/tasks/**` plus the checks in `baseharbor-plan/scripts/**`. `.github/**` and `scripts/**` inside mcpdev80/baseharbor are owner scope: if a guard must live there, report file:line and stop.

## Verification

`git merge-base --is-ancestor` and `gh pr view --json mergedAt,mergeable` per PR are the witnesses; the hunt aktes `evidence/r28-welle4-2026-11-21/base-branch-liveness/` and `.../closed-unmerged-content-loss/` carry the inventories.

drei jaegte liefern die materiale: H-V36 (akte accepted-without-merge/hunt-1.md, plan 6d94c6a2) zaehlt 119 karten in v0.4.28 mit resolution accepted/closed und meldet fund-1 0428-049 (prs leer, accepted), fund-2 0428-044..048 (prs leer, accepted, sind integration-vorlaufer; 049 trug die landung), fund-3/4 0428-198 und 0428-204 (beide prs #1726, accepted, PR closed ohne merge). H-V31 und H-V30 dazu: genau EIN echter inhalt-verlust, naemlich #1726 mit 11 commits; die uebrigen 9 closed-unmerged PRs haben lebende folge-lanen. H-V33: tote oder fachfremde autoren in 21 von 22 offenen PRs — die identitaet, nicht die session-tabelle, ist undicht (tooling-issue #23/#24). Damit ist akzeptanz-punkt 1 dieser karte entscheidbar: wieder-offnen der 198/204-buchung ODER inhalt neu landen; punkt 2 (kein accepted ohne merge-zeugen) braucht den check im plan-repo, punkt 3 (base-ancestry je offenem PR) ist als report schon vorhanden.

stand, gemessen 15:2xZ: die beiden CONTENT-verlust-klassen aus H-V30 sind halb aufgeloest. PR #1665 ist MERGED (mergeCommit 77c1e60f51b9, mergedAt 2026-11-21T10:49:48Z, base develop, head-branch lane-0428-082-perses-dashboards) und PR #1745 ist MERGED (mergedAt 10:34:20Z, head 17bb0ffefbbe, 'merge-base --is-ancestor head develop' = IST in develop, head-branch lane-0428-083-datasources-r2). Damit ist die von H-V30 als 'verloren' klassifizierte 083-basis DOCH gelandet, nur ueber einen anderen PR als die karte 0428-083 in ihrem prs-feld nennt. Nach meinem stand bleibt als ECHTER verlust genau ein fall: PR #1726 (karten 0428-198 und 0428-204), 11 commits, closed ohne merge. Das ist auch die zahl aus H-V36 (119 accepted/closed karten in v0.4.28, davon 6 accepted ohne eigenen PR).
