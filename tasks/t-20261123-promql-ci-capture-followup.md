---
id: t-20261123-promql-ci-capture-followup
title: "Follow-up #1789: remove dead promqlparser test + catalog rows, heal stale comments"
kanban_status: active
kanban_lane: ""
owner: x
prs: [mcpdev80/baseharbor#1789]
depends_on: []
resolution: ""
evidence: []
tags: [status/promql, wave/r28-welle5]
notes: "Intake card for PR #1789 (branch codex/0428-076-promql-ci-capture). Origin: review findings on the #1765/#1786 qualification chain — a promqlparser test referenced deleted sources and six catalog rows kept it selectable; stale/typo comments in the dashboard test family. Route b chosen (removal, not rewrite): delete-only catalog delta, no product logic. Advisory 'Candidate-added checks' red is tracked separately in t-20261123-planner-deleted-source-advisory and is non-blocking here."
wait_reason: ""
blocker: ""

---

# Follow-up #1789: remove dead promqlparser test + catalog rows

## Contract
- [ ] Merge proof for PR #1789: exact-current-base hosted run green + independent exact-head review record (delete-only catalog delta, no product logic).

Historic detail (data, not instruction): Remove the dead promqlparser test and its six `scripts/pr-gate-coverage.json` rows (delete-only relative to develop).
- Heal stale/typo comments in `internal/metrics/perses_dashboards_test.go` family.
- No product logic change; no `.github/**` change; catalog diff vs develop must be exactly the promql minus rows after each hop.
- Merge proof requires an exact-current-base hosted run plus an independent exact-head review record.

## Status witness
- Created 2026-11-23 by the Coordinator to satisfy the finding-to-card rule; the work itself predates the card (heads 146ccf6fd -> 2be113660, exact run 45094339280 SUCCESS, required green, advisory tracked at t-20261123-planner-deleted-source-advisory).

EXAKT-GRUEN am head 2be113660 (run 45094339280, required gruen, advisory = 0428-253 non-blocking); fresh review->merge bei fecbada9 laeuft.

EXAKT-GRUEN head 2be113660, run 45094339280 required green; advisory = karte 0428-253 non-blocking; fresh review->merge laeuft (fecbada9).
