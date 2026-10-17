---
id: t-20261017-release-0-8-4-prepare
type: acceptance
areas: [release]
release: v0.8.x
version: v0.8.4
release_stage: prepare
parent: v0.8.x
owner: ""
priority: normal
depends_on: [core-317, t-20261017-release-0-8-4-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-8-4-prepare · v0.8.4 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-8-x #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [core-317](core-317-kubernetes-updates-migration-recovery.md), [t-20261017-release-0-8-4-updates](t-20261017-release-0-8-4-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.4)  
**Depends on:** [core-317](core-317-kubernetes-updates-migration-recovery.md), [t-20261017-release-0-8-4-updates](t-20261017-release-0-8-4-updates.md)  
**Required by:** [t-20261017-release-0-8-4-qualify](t-20261017-release-0-8-4-qualify.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Finish every prerequisite for complete-ecosystem pre-release readiness.

## Scope and acceptance

- Apply canonical audit sections 1–8 and section 9 atomic-first prerequisites, plus RELEASE_WORKFLOW.md#prepare. Re-read current sources and workflows instead of copying obsolete v0.4.25 exceptions.
- Accept all assigned implementation/CI/docs/consumer tasks and verify release-note/epic criteria, even when no executable children have been cut. Accepted cards alone do not prove release readiness; inspect deferred or waived test debts explicitly.
- Complete implementation/security/ownership/standards and CLI/JSON/MCP parity; current Core/BaseHarbor, Demo, Console and Node Connector compatibility; real supported developer journeys, auth/mTLS and cleanup evidence.
- Complete concise EN/DE docs/reference/specs, navigation/links, changelog and actual human release message, compatibility/security/upgrade/deferred notes, strict Pages candidate builds/workflow without deployment. Keep process rules out of the product README.
- Freeze actual immutable ecosystem SHAs, candidate tree, gate requirements and verifier-compatible evidence origins. Verify all required targeted checks, runtime/platform gates and consumer receipts; missing/failed/skipped/unverified requirements block readiness.
- Deliver a reviewable readiness dossier and exact authorized-run plan. Preparation does not authorize full pre-release, promotion, tag, publication or public Pages deployment.

## Required checks

Existing canonical documentation audit, strict EN/DE MkDocs, source/contracts/build/security and affected native/consumer gates. Reuse only verifier-proven compatible evidence; do not rerun unaffected green gates.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#prepare). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
