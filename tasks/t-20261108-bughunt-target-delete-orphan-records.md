---
id: t-20261108-bughunt-target-delete-orphan-records
card_number: "0427-165"
card_short_title: "target delete leaves uncollect"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-165-r7
kanban_status: active
kanban_lane: active
kanban_summary: Deleting a target either refuses while apps/records exist (naming them) or prunes its records under the existing destroy…
kanban_title: 0427-165 · target delete leaves uncollect
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1500]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-delete-orphan-records/round-2.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-target-delete-orphan-records · Bug Hunt v0.4.27: Delete leaves orphans #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-165-r7 · **Priority:** normal  
    **PR:** [baseharbor#1500](https://github.com/mcpdev80/baseharbor/pull/1500)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-delete-orphan-records/round-2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-165-r7  
**Priority:** normal  
**PRs:** [baseharbor#1500](https://github.com/mcpdev80/baseharbor/pull/1500)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Deleting a target either refuses while apps/records exist (naming them) or prunes its records under the existing destroy contract; no uncollectable residue. Regression with a damaged/orphan fixture in the lifecycle group.

## Problem (source evidence in the dossier)
target delete is config-only: deployment records and runtime state of the removed target stay behind; records whose source repo was deleted show MISSING and are unreachable for app-delete afterwards (BF-04).

## Acceptance
Deleting a target either refuses while apps/records exist (naming them) or prunes its records under the existing destroy contract; no uncollectable residue. Regression with a damaged/orphan fixture in the lifecycle group.

## Dependencies and file ownership
None. Write-set: target delete / record retention paths.
