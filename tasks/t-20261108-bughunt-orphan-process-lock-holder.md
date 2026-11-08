---
id: t-20261108-bughunt-orphan-process-lock-holder
card_number: "0427-147"
card_short_title: "Orphan holds the target"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-lock-holder"
kanban_status: active
kanban_lane: active
kanban_summary: "Lock holder visible: status/up show pid+state of the holding process and name the next step; optional explicit-release cleanup…"
kanban_title: 0427-147 · Orphan holds the target
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1480]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md"]
---
- [ ] t-20261108-bughunt-orphan-process-lock-holder · Bug Hunt v0.4.27: Orphan holds the target #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-lock-holder · **Priority:** normal  
    **PR:** [baseharbor#1480](https://github.com/mcpdev80/baseharbor/pull/1480)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-lock-holder  
**Priority:** normal  
**PRs:** [baseharbor#1480](https://github.com/mcpdev80/baseharbor/pull/1480)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Lock holder visible: status/up show pid+state of the holding process and name the next step; optional explicit-release cleanup path; regression (fake lock holder) in the lifecycle field.

## Problem (source evidence in the dossier)
SIGKILL case: the kernel lock releases cleanly and resume up repairs DEGRADED (positively proven). BUT an orphaned baha up (ssh closed, process survives) keeps holding the lock - up/status report blocked until an external pkill. Source: hunt H-D4 BF-hd4-2 (medium).

## Acceptance
Lock holder visible: status/up show pid+state of the holding process and name the next step; optional explicit-release cleanup path; regression (fake lock holder) in the lifecycle field.

## Dependencies and file ownership
None. Write-set: lifecycle lock reporting + target status.


## Code-/CI-Übernahme — 2026-11-08

- Owner `chatgpt-r27-lock-holder`, Implementierung in [PR #1480](https://github.com/mcpdev80/baseharbor/pull/1480). Der private Flock schreibt PID beim Erwerb, meldet PID/Status und eine explizite Prüf-/Freigabeanweisung bei Konflikt. Keine automatische Signalisierung oder Löschung fremder Locks.
- Unix-Regression mit echtem Lock-Konflikt und sauberem Reacquire implementiert. Exact-head CI läuft/steht aus. Kein Acceptance ohne bestätigten PASS.
