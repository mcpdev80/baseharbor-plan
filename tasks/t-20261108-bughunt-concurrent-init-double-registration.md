---
id: t-20261108-bughunt-concurrent-init-double-registration
card_number: "0427-175"
card_short_title: "Double init poisons target"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-175-r2
kanban_status: active
kanban_lane: active
kanban_summary: "concurrent init is serialized or CAS-rejected so duplicates cannot exist; if a target is already poisoned, a named CLI recovery…"
kanban_title: "0427-175 · Double init poisons target"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1512]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/bughunt-concurrent-init-double-registration/round-1.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-concurrent-init-double-registration · Bug Hunt v0.4.27: Double init poisons target #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-175-r2 · **Priority:** normal  
    **PR:** [baseharbor#1512](https://github.com/mcpdev80/baseharbor/pull/1512)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/bughunt-concurrent-init-double-registration/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-175-r2  
**Priority:** normal  
**PRs:** [baseharbor#1512](https://github.com/mcpdev80/baseharbor/pull/1512)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
 concurrent init is serialized or CAS-rejected so duplicates cannot exist; if a target is already poisoned, a named CLI recovery exists (or a refusal text that names the exact working recovery, verified against built binaries per lesson 162); regression in CI-covered lifecycle/concurrency group.

## Problem (source evidence in the dossier)
BF-01 + BF-10 (blocker): two concurrent app init runs on the same repo path/manifest both succeed and create DUPLICATE application_id records; the target then permanently fails with provider consumer inventory damaged for list/plan/destroy of ALL apps, and NO CLI path (app destroy NAME, --uuid selector) can recover it — only full-consensus magic works, without any hint pointing there. Acceptance: concurrent init is serialized or CAS-rejected so duplicates cannot exist; if a target is already poisoned, a named CLI recovery exists (or a refusal text that names the exact working recovery, verified against built binaries per lesson 162); regression in CI-covered lifecycle/concurrency group.

## Dependencies and file ownership
None blocking. Write-set: cmd/baha app init path, internal registration + recovery guidance.

candidate f442b7e99 on PR #1512, hosted CI observed
