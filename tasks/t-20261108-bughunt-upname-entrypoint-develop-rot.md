---
id: t-20261108-bughunt-upname-entrypoint-develop-rot
card_number: "0427-172"
card_short_title: "TestUpNameResumesThroughComman"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w172b-inventoryfix
kanban_status: closed
kanban_lane: closed
kanban_summary: TestUpNameResumesThroughCommandEntrypoint passes again in hosted go test ./... on a develop HEAD with no PR-side changes…
kanban_title: 0427-172 · TestUpNameResumesThroughComman
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1502]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-use-activate-issuer-failclosed/round-3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [x] t-20261108-bughunt-upname-entrypoint-develop-rot · Bug Hunt v0.4.27: Entrypoint test rots #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w172b-inventoryfix · **Priority:** normal  
    **PR:** [baseharbor#1502](https://github.com/mcpdev80/baseharbor/pull/1502)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-use-activate-issuer-failclosed/round-3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261109-0427-181-upname-entrypoint-hosted-rot](t-20261109-0427-181-upname-entrypoint-hosted-rot.md)  
**Owner:** lane-w172b-inventoryfix  
**Priority:** normal  
**PRs:** [baseharbor#1502](https://github.com/mcpdev80/baseharbor/pull/1502)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
TestUpNameResumesThroughCommandEntrypoint passes again in hosted go test ./... on a develop HEAD with no PR-side changes pending: either the marker/teardown sequencing in the fixture is repaired (dead-pid adoption must find a persisted bootstrap target) or the test is made hermetic against adoption races; one hosted full-matrix green run on develop named in the card as the healing proof.

## Landing check — 2026-11-09

PR #1502 was squash-merged as `1912734ff864bdfefd7ab8ae71a25e856859d5d8`, then the `develop` head. The merge-triggered native Docker and Podman develop runs are `42582097892` and `42582097798`; both were still in progress when checked. At that time the healing proof remained pending until a develop run actually executed and passed both `TestUpNameResumesThroughCommandEntrypoint` and `TestControlPlaneSingleDefaultNativeRuntimeInCI`. A skipped or absent test is not evidence. No follow-up cases were closed by this merge.

Follow-up observation: runs `42582097892` and `42582097798` later ended `cancelled` after the next develop pushes. The subsequent Docker/Podman develop runs on `2abfeee70419140c8115d864572152071406dce9` and `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` completed successfully, but their native single-default selectors skipped the execution jobs (for example, run `42582356511`, job `129043924832`, `Native single-default · Docker`, conclusion `skipped`). These runs do not prove that both named tests executed. Planning status was concurrently changed to `closed/accepted` in commit `c31d02e5b05bc89fb882bdec599b50716f8d865f`; this merge review did not change that status. Reconcile the acceptance status with the execution evidence before relying on the card as proof of healing.

## Problem (witness runs)
After the bootstrap-marker adoption work (0427-156 era + owner acceptance #1495 on develop), the hosted go test ./... matrix fails on TestUpNameResumesThroughCommandEntrypoint (~80s, "adopting orphaned marker from dead pid", "adoption found no persisted bootstrap target") across UNRELATED branches and pure-wording PRs (runs 42516911484 on 03fa07f8, 42516978054 on the 0427-159 branch) - a global develop rot that reds the unit gate of every PR; successor of the 156 marker gap.

## Acceptance
TestUpNameResumesThroughCommandEntrypoint passes again in hosted go test ./... on a develop HEAD with no PR-side changes pending: either the marker/teardown sequencing in the fixture is repaired (dead-pid adoption must find a persisted bootstrap target) or the test is made hermetic against adoption races; one hosted full-matrix green run on develop named in the card as the healing proof.

## Dependencies and file ownership
Blocks the unit gate for ALL open PRs (#1489 wording candidate parked on this card; the 0427-160 r3 rerun will hit it too). Write-set: cmd/baha entrypoint test fixture / bootstrap marker teardown paths (shared with the #1495 acceptance work).
