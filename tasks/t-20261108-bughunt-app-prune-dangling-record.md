---
id: t-20261108-bughunt-app-prune-dangling-record
card_number: "0427-173"
card_short_title: "No command prunes a dangling m"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w173b-prune-r2
kanban_status: active
kanban_lane: active
kanban_summary: "A safe 'baha app prune <name>' under the app tree deletes ONLY the dangling record whose source is missing (refuses when source…"
kanban_title: 0427-173 · No command prunes a dangling m
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261108-bughunt-list-stale-after-kill]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1505]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-list-stale-after-kill/round-3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-app-prune-dangling-record · Bug Hunt v0.4.27: Prune dangling record #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w173b-prune-r2 · **Priority:** normal  
    **PR:** [baseharbor#1505](https://github.com/mcpdev80/baseharbor/pull/1505)  
    **Needs:** [t-20261108-bughunt-list-stale-after-kill](t-20261108-bughunt-list-stale-after-kill.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-list-stale-after-kill/round-3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261108-bughunt-list-stale-after-kill](t-20261108-bughunt-list-stale-after-kill.md)  
**Owner:** lane-w173b-prune-r2  
**Priority:** normal  
**PRs:** [baseharbor#1505](https://github.com/mcpdev80/baseharbor/pull/1505)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
A safe 'baha app prune <name>' under the app tree deletes ONLY the dangling record whose source is missing (refuses when source exists or multiple records match, naming each), with command-entry regressions (registered, refuses-live, prunes-dangling) in the cli-surface group (CI captured). Acceptance cross-check: 0427-160's MISSING next-action line then points at this real command - update its hint in the same PR.

## Problem (source evidence in the dossier)
STATE per 0427-160 r3 (evidence bughunt-list-stale-after-kill/round-3.md, plan 1a6f4b2e): an app whose source repo is gone, destroy/down/doctor answer 'no applied intent snapshot' and apply answers 'source unavailable' - NO registered command removes the dangling deployment record (app tree at cmd/baha/commands.go:256-280 has no prune). The record is permanently uncollectable and list keeps showing MISSING.

## Acceptance
A safe 'baha app prune <name>' under the app tree deletes ONLY the dangling record whose source is missing (refuses when source exists or multiple records match, naming each), with command-entry regressions (registered, refuses-live, prunes-dangling) in the cli-surface group (CI captured). Acceptance cross-check: 0427-160's MISSING next-action line then points at this real command - update its hint in the same PR.

## Dependencies and file ownership
Follow-up of 0427-160 (quarantined finding per its r3). Write-set: cmd/baha app command tree + record removal paths (new prune subcommand).
