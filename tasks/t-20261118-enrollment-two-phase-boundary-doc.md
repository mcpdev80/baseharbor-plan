---
id: t-20261118-enrollment-two-phase-boundary-doc
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w115 (opencode ses_e0f576c30ffe)
kanban_status: blocked
card_number: 0428-115
card_short_title: document the enrollment
kanban_title: 0428-115 · document the enrollment
prs: [mcpdev80/baseharbor#1685]
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1685", "https://github.com/mcpdev80/baseharbor/actions/runs/44408281995"]
blocker: "Requested DE authorization terminology correction is not present in candidate 2039628ba8d981488d93e90f59dff5023fb9a477, and candidate is 20 commits behind current develop 40b9901398a6bae5b92ee45494ef3b70f192a2a7. Correct the narrow DE paragraph, normal base refresh, then run exact-head checks and request re-review."

---
# t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary

- [ ] t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** w115 (opencode ses\_e0f576c30ffe)  
    **PR:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
    **Blocker:** Requested DE authorization terminology correction is not present in candidate 2039628ba8d981488d93e90f59dff5023fb9a477, and candidate is 20 commits behind current develop 40b9901398a6bae5b92ee45494ef3b70f192a2a7. Correct the narrow DE para…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1685), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44408281995)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w115 (opencode ses_e0f576c30ffe)  
**Priority:** not set  
**PRs:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
**Source:** 
<!-- /generated:links -->

## Goal
Per hunt 914 Befund 2 (medium): `Consume` and `RecordIssued` are two transactions; if the issuer fails in between, the grant sits consumed-but-unissued (recovery relies on the `previous_certificate_serial` clause in connector_enrollment.go:87-90). The finding is a documentation/mental-model gap: make the two-phase boundary, its failure window, and the recovery path explicit in the enrollment docs and a targeted code comment at authority.go.

## Scope
- docs (enrollment/trust-plane section) + one code comment block. NO behavior change, no migration.

## Required checks
- docs build/link checks; no runtime gates.

## Dependencies and file ownership
- Source: hunt 914 Befund 2, evidence/r28-welle4-2026-11-18/hunt-authsurf/befund-1.md.

Codex review comment 6993699816 remains open: German wording translates one-use authorization Grant as Zuschuss/Leugnung/toter Zuschuss. English and Store comment reviewed as accurate; merge blocked on corrected DE text and current-base CI.
