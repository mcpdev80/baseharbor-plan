---
id: t-20261017-release-0-4-27-prepare
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: prepare
parent: v0.4.27
owner: o66 (coordinator, r27 board-up)
kanban_status: planned
kanban_title: "v0.4.27 · Pre-release: complete ecosystem readiness and candidate preparation"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: ["mcpdev80/baseharbor#1151"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-4-27-prepare · v0.4.27 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-4-27 #status/planned #view/ready #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** o66 (coordinator, r27 board-up) · **Priority:** normal  
    **PR:** [baseharbor#1151](https://github.com/mcpdev80/baseharbor/pull/1151)  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
**Owner:** o66 (coordinator, r27 board-up)  
**Priority:** normal  
**PRs:** [baseharbor#1151](https://github.com/mcpdev80/baseharbor/pull/1151)  
**Source:** 
<!-- /generated:links -->

## Goal

Prepare the v0.4.27 ecosystem release-readiness dossier while implementation progress is tracked by its own CardBoard tasks and epics. This stage does not accept or qualify unfinished features.

## Scope and acceptance

- Apply canonical audit sections 1–8 and section 9 atomic-first prerequisites, plus RELEASE_WORKFLOW.md#prepare. Re-read current sources and workflows instead of copying obsolete v0.4.25 exceptions.
- Inventory outstanding implementation/CI/docs/consumer tasks from the release scope, existing CardBoard views and epics. Document release-note/epic criteria and deferred or waived test debts; all required work must be accepted before release qualification.
- Complete implementation/security/ownership/standards and CLI/JSON/MCP parity; current Core/BaseHarbor, Demo, Console and Node Connector compatibility; real supported developer journeys, auth/mTLS and cleanup tests.
- Complete concise EN/DE docs/reference/specs, navigation/links, changelog and actual human release message, compatibility/security/upgrade/deferred notes, strict Pages candidate builds/workflow without deployment. Keep process rules out of the product README.
- Freeze actual immutable ecosystem SHAs, candidate tree, gate requirements and required test inputs. Verify all required targeted checks, runtime/platform gates and consumer test execution; missing/failed/skipped/unverified requirements block readiness.
- Deliver a reviewable readiness dossier and exact authorized-run plan. Preparation does not authorize full pre-release, promotion, tag, publication or public Pages deployment.

## Required checks

Existing canonical documentation audit, strict EN/DE MkDocs, source/contracts/build/security and affected native/consumer gates. Run the actual affected checks directly; no CI evidence verifier or manifest reuse.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#prepare). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; complete release-scope acceptance is required by Qualify, not duplicated as direct Prepare dependencies.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
