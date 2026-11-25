---
id: t-20261125-hunt40-realversion-migration-quali
card_number: "0428-311"
card_short_title: "Core update runtime qualification"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Qualify the documented Core provider-update path against real pinned provider versions and native runtime checks."
kanban_title: 0428-311 · Core update runtime qualification
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt40-realversion-migration-quali · 0428 hunt H-V40: qualify the supported Core provider-update runtime path #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver the missing real-version runtime qualification for BaseHarbor's supported Core provider-update path. The test must use a release-pinned, owned Core installation and exercise preflight, verified recovery, provider mutation, and post-update semantics through the existing runtime checks.

## Scope

- In scope: one cohesive qualification slice for the documented supported Keycloak and PostgreSQL update path, exact candidate provider versions/digests, and the existing runtime test/gate route.
- Derive the installed and target versions from the candidate's immutable provider catalog. Do not assume that every 0.4.27-to-0.4.28 release changes provider versions or manufacture an unsupported PostgreSQL major-upgrade scenario.
- Use the existing Docker and rootless Podman/native release checks where the candidate path requires them; do not add a parallel workflow or a second evidence system.
- Out of scope: changing API compatibility policy, generic database migrations, and unrelated fixes to downgrade classification or SQL migration files.

## Acceptance

- For each candidate-supported version delta, the native test drives the owned Core provider through preflight, verified recovery-point creation, apply, and semantic verification; it does not treat container health alone as success.
- Verify the documented provider-specific outcome: Keycloak authentication/issuer behavior remains usable and PostgreSQL data remains readable and consistent after the admitted update.
- Prove an unsupported/downgrade path is rejected before any provider mutation using the existing focused preflight/contract coverage; do not duplicate a guard already enforced in Core planning and adapter preflight.
- Execute the applicable existing Docker and rootless Podman qualification paths on the exact candidate source and immutable provider digests. Record skipped or unavailable native execution as a blocker, not as a pass.
- Bind every changed test to the existing package discovery or native gate and record exact source SHA, test ID, check/gate, trigger, run URL, and actual result.
- If the frozen candidate has no supported provider-version delta, document that result with the candidate catalog and retain the native migration qualification as explicit release debt; do not claim the path was tested.

## Dependencies and file ownership

- Owned areas: Core provider-update native qualification and its existing test/gate routing.
- Coordinate shared CI catalog/workflow changes with their owner; add no new parallel pipeline.
- The release Prepare/Qualify cards consume the accepted evidence; this task does not authorize a complete pre-release or release.

## Audit disposition — REWRITE

Rechecked current BaseHarbor `develop` at `3a2ae6b1139570c98b8924e3b19975c56a289400`. `docs/spec/core-provider-update-v1.md` still states that real-version runtime qualification is pending, so the release-relevant gap remains. Two other H-V40 sub-findings are stale and are deliberately excluded: Core planning and execution validation reject provider downgrades for all provider kinds, including Identity; the current SQL migration directory contains migrations 0001–0011 with matching down files, not the reported 0012-without-down case. The card is therefore narrowed to the unproven real-version native path; no product behavior or compatibility policy is being changed by this planning rewrite.

Evidence: [current provider-update contract](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/docs/spec/core-provider-update-v1.md), [current Core planner and downgrade guard](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/coreupdate/plan.go), [current SQL migration inventory](https://github.com/mcpdev80/baseharbor/tree/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/database/migrations), [H-V40 source dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/w173/hunt-v40-upgrade-migration.md).
