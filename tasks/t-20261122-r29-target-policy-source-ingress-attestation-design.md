---
id: t-20261122-r29-target-policy-source-ingress-attestation-design
card_number: "0429-016"
card_short_title: "Policy source/artifact design"
type: architecture
areas: [remote, deployment]
release: v0.4.29
version: ""
parent: v0.4.29
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Define the source-ingress and artifact-confirmation contracts needed before editable Target policy presets can be safely…
kanban_title: "0429-016 · Policy source/artifact design"
priority: normal
depends_on: [t-20261017-release-0-4-29-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261122-r29-target-policy-source-ingress-attestation-design · 0429-016 · Policy source/artifact design #task #release/v0-4-29 #status/planned #view/waiting #board/planned #area/deployment #area/remote #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Depends on:** [t-20261017-release-0-4-29-updates](t-20261017-release-0-4-29-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

# 0427-186-Nachfolge · Design: Richtlinien-Voreinstellungs-Quellzufluss & Artefakt-Bestätigung

## Goal

Define the source-ingress and artifact-confirmation contracts needed before editable Target policy presets can be safely implemented. This is a design-only task for v0.4.29.

## Requirements

1. Define how the apply path obtains and passes verifiable facts for the current candidate's target branch, remote and image digest. The application path must pass proven facts to policy evaluation; `EvaluateDeploymentAdmission(policy, nil)` is not an acceptable contract.
2. Define the evidence and confirmation boundary in the source model, including the encryption and access scope through which policy presets may read and write.
3. Use the preserved implementation branch head `28842990d8fe86cc9090b1867c6b503b57adccdc` on `lane/0427-186-target-policy-presets` as a design influence; do not rewrite or delete that branch.

## Out of scope

- Implementation or product code.
- CI workflow wiring.
- UI.

## Acceptance

- The design specifies authoritative sources, freshness/current-candidate binding, and verification behavior for target branch, remote and image digest facts.
- The design states the source model's evidence/confirmation boundary and read/write encryption and access scope for presets.
- The preserved branch head is linked as design input; the task does not claim the deferred feature is implemented.
- The card remains planned and waits for the v0.4.29 release-start intake prerequisite; early=true records Owner intent to pull this design forward after that prerequisite. It has no code, CI or UI acceptance criteria.

## Required checks

- Planning validation only: `python3 scripts/plan.py render` and `python3 scripts/plan.py check`.

## Handoff

- Created as the design-only v0.4.29 successor to the deferred 0427-186 scope.
- Source branch retained: [28842990d8fe86cc9090b1867c6b503b57adccdc](https://github.com/mcpdev80/baseharbor/commit/28842990d8fe86cc9090b1867c6b503b57adccdc).
