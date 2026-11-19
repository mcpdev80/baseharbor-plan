---
id: t-20261118-enrollment-two-phase-boundary-doc
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w01-0428-115 (r2 reserviert)
kanban_status: active
card_number: 0428-115
card_short_title: document the enrollment
kanban_title: 0428-115 · document the enrollment
prs: [mcpdev80/baseharbor#1685]
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1685", "https://github.com/mcpdev80/baseharbor/actions/runs/44408281995"]
blocker: ""

---
# t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary

- [ ] t-20261118-enrollment-two-phase-boundary-doc · document the enrollment consume/issue two-phase boundary #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w01-0428-115 (r2 reserviert)  
    **PR:** [baseharbor#1685](https://github.com/mcpdev80/baseharbor/pull/1685)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1685), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44408281995)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w01-0428-115 (r2 reserviert)  
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

reviewer haelt #1685 bei 2039628b: comment 6993699816 gueltig (Grant->'Zuschuss', denial->'Leugnung' = sicherheitssemantik verkannt; Grant bleibt englischer Eigenname, denial='Verweigerung') + 20 commits rueckstaendig hinter develop 40b9901398. mission-115r2-wording-hopf.md RESERVIERT fuer ersten END-freiraum; kein merge vom stale head
