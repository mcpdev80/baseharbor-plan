---
id: t-20261122-gate-catalog-missing-app-broker-component
card_number: "0428-242"
card_short_title: "app_broker not in gate catalog"
type: bug
areas: [testing, ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Make broker diagnostics provable in hosted CI: scripts/pr-gate-coverage.json carries 65 cmd/baha path entries but no entry…"
kanban_title: 0428-242 · app_broker not in gate catalog
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-gate-catalog-missing-app-broker-component · Gate catalog: no coverage component for cmd/baha/app_broker.go #task #release/v0-4-28 #status/planned #view/ready #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make broker diagnostics provable in hosted CI: `scripts/pr-gate-coverage.json` carries 65 `cmd/baha` path entries but no
entry matching `app_broker`, so a PR that only changes `cmd/baha/app_broker.go` plans an EMPTY native matrix and its runtime
diagnostic path is never exercised by a hosted job.

## Measured evidence

- `git show develop:scripts/pr-gate-coverage.json` → `cmd/baha` appears 65 times, `app_broker` 0 times (2026-11-22).
- PR #1763 run `45009251403` at exact head `b38838e1c30` is SUCCESS, trusted plan job `137167667713` reports the native gate
  plan selected an empty matrix, and `PR · Native matrix` is SKIPPED. A skipped gate is not evidence.

## Acceptance

1. One catalog component maps `cmd/baha/app_broker.go` to the gates that must run when broker diagnostics change.
2. A follow-up PR that only edits that file triggers at least one executed native or selected runtime row (witnessed by job
   id), or the plan explicitly documents why unit sentinels are sufficient.
3. No lane edits `scripts/**`: this is an Owner-scope catalog change, tracked here so the finding is not lost.

## Boundaries

`scripts/pr-gate-coverage.json` (Owner scope) plus its validation script. No product files in this card.
