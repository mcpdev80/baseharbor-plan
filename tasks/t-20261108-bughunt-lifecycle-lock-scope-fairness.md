---
id: t-20261108-bughunt-lifecycle-lock-scope-fairness
card_number: "0427-176"
card_short_title: "Target lock serializes and sta"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w176-lockfairness
kanban_status: active
kanban_lane: active
kanban_summary: lock granularity or ordering documented and improved so independent apps do not serialize; starvation-free acquisition (fairness…
kanban_title: 0427-176 · Target lock serializes and sta
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1507]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-lifecycle-lock-scope-fairness · Bug Hunt v0.4.27: Target lock serializes and starves #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w176-lockfairness · **Priority:** normal  
    **PR:** [baseharbor#1507](https://github.com/mcpdev80/baseharbor/pull/1507)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w176-lockfairness  
**Priority:** normal  
**PRs:** [baseharbor#1507](https://github.com/mcpdev80/baseharbor/pull/1507)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
 lock granularity or ordering documented and improved so independent apps do not serialize; starvation-free acquisition (fairness or bounded retry) for up vs destroy; regressions in the CI-covered concurrency group.

## Problem (source evidence in the dossier)
BF-02 + BF-03 (damms): the lifecycle lock is per TARGET not per APP, so parallel ups of completely service-less different apps serialize fully; and destroy can starve up on the same target indefinitely (no fairness/bias control in internal/stableid/lock_unix.go FASS lock order). Acceptance: lock granularity or ordering documented and improved so independent apps do not serialize; starvation-free acquisition (fairness or bounded retry) for up vs destroy; regressions in the CI-covered concurrency group.

## Dependencies and file ownership
None blocking. Write-set: internal/stableid lock + lifecycle call sites.
