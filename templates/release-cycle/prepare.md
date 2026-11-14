---
id: {{id}}
type: acceptance
areas: [release]
release: {{release}}
version: {{version}}
release_stage: prepare
parent: {{release}}
owner: ""
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] {{id}} · {{version}} · {{title}} #task #{{release_tag}} #status/planned

## Goal

Prepare the ecosystem release-readiness dossier while feature work is tracked on CardBoard.

## Scope and acceptance

- Apply canonical audit sections 1–8 and section 9 atomic-first prerequisites, plus RELEASE_WORKFLOW.md#prepare. Re-read current sources and workflows instead of copying obsolete v0.4.25 exceptions.
- Track outstanding implementation/CI/docs/consumer scope in the existing feature cards, epics and release view, without copying all task dependencies into this preparation card. Inventory release-note/epic criteria and deferred or waived test debts; qualification remains blocked until all required scope is accepted.
- Complete implementation/security/ownership/standards and CLI/JSON/MCP parity; current Core/BaseHarbor and Demo compatibility; archived Console and Node Connector are excluded; real supported developer journeys, auth/mTLS and cleanup tests.
- Complete concise EN/DE docs/reference/specs, navigation/links, changelog and actual human release message, compatibility/security/upgrade/deferred notes, strict Pages candidate builds/workflow without deployment. Keep process rules out of the product README.
- Freeze actual immutable ecosystem SHAs, candidate tree, gate requirements and required test inputs. Verify all required targeted checks, runtime/platform gates and consumer test execution; missing/failed/skipped/unverified requirements block readiness.
- Deliver a reviewable readiness dossier and exact authorized-run plan. Preparation does not authorize full pre-release, promotion, tag, publication or public Pages deployment.

## Required checks

Existing canonical documentation audit, strict EN/DE MkDocs, source/contracts/build/security and affected native/consumer gates. Run the actual affected checks directly; no CI evidence verifier or manifest reuse.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#prepare). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; all release scope is verified at qualification, not duplicated here.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
