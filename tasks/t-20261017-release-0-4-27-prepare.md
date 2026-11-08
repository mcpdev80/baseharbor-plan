---
id: t-20261017-release-0-4-27-prepare
card_number: "0427-006"
card_short_title: "complete ecosystem readiness"
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: prepare
parent: v0.4.27
owner: mcpdev80
kanban_lane: wait
kanban_summary: Prepare the v0.4.27 ecosystem release-readiness dossier while implementation progress is tracked by its own CardBoard tasks and…
kanban_status: wait
kanban_title: "0427-006 · complete ecosystem readiness"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor#1151]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-07.md"]
wait_reason: "prepare-branch (PR#1151) gemergt; wartet auf OWNER publish-freigabe (direktive prepare-ja/publish-nein), keine aktive bahn"

---

- [ ] t-20261017-release-0-4-27-prepare · v0.4.27 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-4-27 #status/wait #view/wait #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** normal  
    **PR:** [baseharbor#1151](https://github.com/mcpdev80/baseharbor/pull/1151)  
    **Waiting:** prepare-branch (PR\#1151) gemergt; wartet auf OWNER publish-freigabe (direktive prepare-ja/publish-nein), keine aktive bahn  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-07.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
**Owner:** mcpdev80  
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

## Mandatory CI test-routing audit (Owner decision 2026-11-07)

Before declaring preparation complete, require a test-to-check-to-trigger matrix for every new or modified v0.4.27 regression, including already accepted Core, Demo, Console and Node Connector cards. The matrix must establish actual package discovery, native Docker and rootless Podman/Quadlet execution where supported, real external prerequisites, and explicit develop-acceptance or release gate registration. A new test with no executable CI route or a silent skip blocks qualification. Use [the current audit](../evidence/v0.4.27-ci-test-routing-audit-2026-11-07.md); coordinate implementation with the assigned [CI-lanes owner](t-20261018-r27-ci-lanes.md). Do not modify that worker's files from this release-preparation task.

The candidate release catalog presently lacks v0.4.27 registration; prepare the mapping without assuming publication. This card authorizes no release workflow execution, tag, promotion or publication.

## Required checks

Existing canonical documentation audit, strict EN/DE MkDocs, source/contracts/build/security and affected native/consumer gates. Run the actual affected checks directly; no CI evidence verifier or manifest reuse.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#prepare). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; complete release-scope acceptance is required by Qualify, not duplicated as direct Prepare dependencies.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

2026-11-07: Preparation started with a read-only audit. Verified missing `docs/releases/v0.4.27.md` and `docs/releases/v0.4.27.demo-ref` on product develop, plus incomplete release scope and missing final four-repository candidate qualification. See `evidence/v0.4.27-prepare-2026-11-07.md`. No release jobs, tags, promotion, Pages publication or product branch changes authorized/performed. Continue preparation only; do not mark accepted until all criteria are met.

owner-direktive 2026-11-07: release-vorbereitung FORTSETZEN aber NICHT veroeffentlichen (kein pre-release/tag/promotion bis separate freigabe). umbrella; wartet auf rest der welle (117+ci-seam+118+003).

PR#1151 (prepare-branch) MERGED. Karte BLEIBT active gemaess owner-direktive 2026-11-07: release PREPARE ja, PUBLISH/TAG nein bis freigabe. Kein board-lie — GATE=owner publish.

PR#1151 prepare-branch MERGED. Karte NICHT in arbeit (kein worker) — wartet auf OWNER publish-freigabe (direktive prepare-ja/publish-nein) => wait, nicht active. trigger: owner publish-anweisung.
