---
id: t-20261108-bughunt-openbao-stale-manager-cred
card_number: "0427-154"
card_short_title: "Stale OpenBao manager credenti"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w154-baocred-b
kanban_status: active
kanban_lane: active
kanban_summary: "Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server =…"
kanban_title: 0427-154 · Stale OpenBao manager credenti
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-openbao-stale-manager-cred · Bug Hunt v0.4.27: Stale cred blocks rebirth #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w154-baocred-b · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w154-baocred-b  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server = re-bootstrap path (with clear notice), not permanent denial; regression with stale-file fixture in the bao field.

## Problem (source evidence in the dossier)
When OpenBao reports uninitialized but the old openbao-admin.env still exists, bootstrap refuses forever (internal/openbao/bootstrap.go:234-243). Source: hunt H-D5 BF-1 (HIGH).

## Acceptance
Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server = re-bootstrap path (with clear notice), not permanent denial; regression with stale-file fixture in the bao field.

## Dependencies and file ownership
None. Write-set: internal/openbao/bootstrap.go.
