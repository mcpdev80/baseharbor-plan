---
id: t-20261123-promql-ci-capture-followup
card_number: "0428-255"
card_short_title: "promql ci-capture followup"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Coordinator (review-merge fecbada9) / 9b7683b5
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-255 · promql ci-capture followup
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1789]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1789"]
tags: [status/promql, wave/r28-welle5]
---

- [x] t-20261123-promql-ci-capture-followup · Promql CI-capture followup: remove dead parser test + rows, heal comments #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Coordinator (review-merge fecbada9) / 9b7683b5  
    **PR:** [baseharbor#1789](https://github.com/mcpdev80/baseharbor/pull/1789)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1789)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Coordinator (review-merge fecbada9) / 9b7683b5  
**Priority:** not set  
**PRs:** [baseharbor#1789](https://github.com/mcpdev80/baseharbor/pull/1789)  
**Source:** 
<!-- /generated:links -->

## Contract
Merge proof for PR #1789: exact-current-base hosted run green + independent exact-head review record; delete-only catalog delta (6 promql minus, 0 plus vs develop), no `.github/**`, no product logic.

Origin: review findings on the #1765/#1786 qualification chain (dead promqlparser test kept six catalog rows selectable; stale comments in the dashboard test family). Created by the Coordinator 2026-11-23 under the finding-to-card rule; the work predates the card.

END akzeptiert: head 2be113660, run 45094339280 exact SUCCESS (advisory=0428-253), akte fdc3a183; fresh review->merge laeuft.

test

END akzeptiert: head 2be113660, run 45094339280 exact SUCCESS (advisory=0428-253), akte fdc3a183; fresh review->merge laeuft.

CLOSED: #1789 gemergt 01:41:46Z; exact run 45094339280 SUCCESS am final head 2be113660 (akte review-merge-1789-2be1136.md, APPROVE + randbefund advisory 0428-253 mit follow-up-rezept); develop danach e8acf74055.
