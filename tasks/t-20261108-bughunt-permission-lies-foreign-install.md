---
id: t-20261108-bughunt-permission-lies-foreign-install
card_number: "0427-174"
card_short_title: "Permission and invalid-name er"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w174-permissiontruth
kanban_status: active
kanban_lane: active
kanban_summary: "Identity resolution distinguishes three outcomes explicitly: unreadable/denied = named access error with the path and a fix hint…"
kanban_title: 0427-174 · Permission and invalid-name er
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd6.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-permission-lies-foreign-install · Bug Hunt v0.4.27: Denied lies foreign #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w174-permissiontruth · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd6.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w174-permissiontruth  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Identity resolution distinguishes three outcomes explicitly: unreadable/denied = named access error with the path and a fix hint (chown/permissions); invalid name/argument = usage error naming the offending input; only a genuine foreign owner hash = 'foreign installation'. Regressions per branch in the cli-surface/lifecycle group (fake permission-denied fixture + empty-target case).

## Problem (source evidence in the dossier)
A root-owned installation.json (permission denied on read) is reported as 'foreign installation' at the repository identity seam (BF-HD6-1, blocker: the idle-time interface on that host becomes unusable for the operator), and an empty target name making ListDeployments fail with an invalid-name error takes the SAME misleading 'foreign installation' label (BF-HD6-2). Access errors and contract violations must never masquerade as ownership verdicts.

## Acceptance
Identity resolution distinguishes three outcomes explicitly: unreadable/denied = named access error with the path and a fix hint (chown/permissions); invalid name/argument = usage error naming the offending input; only a genuine foreign owner hash = 'foreign installation'. Regressions per branch in the cli-surface/lifecycle group (fake permission-denied fixture + empty-target case).

## Dependencies and file ownership
None. Write-set: repository identity resolution paths (cmd/baha + internal/deployment seams per dossier).
