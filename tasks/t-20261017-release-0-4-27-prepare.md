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
owner: owner-chatgpt-r27
kanban_lane: active
kanban_summary: Prepare the v0.4.27 ecosystem release-readiness dossier while implementation progress is tracked by its own CardBoard tasks and…
kanban_status: active
kanban_title: "0427-006 · complete ecosystem readiness"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-console#17, mcpdev80/baseharbor-node-connector#23]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-07.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-12.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-13.md"]
wait_reason: ""

---

- [ ] t-20261017-release-0-4-27-prepare · v0.4.27 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-4-27 #status/active #view/active #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** owner-chatgpt-r27 · **Priority:** normal  
    **PR:** [baseharbor-console#17](https://github.com/mcpdev80/baseharbor-console/pull/17), [baseharbor-node-connector#23](https://github.com/mcpdev80/baseharbor-node-connector/pull/23)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-07.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-12.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-prepare-2026-11-13.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
**Owner:** owner-chatgpt-r27  
**Priority:** normal  
**PRs:** [baseharbor-console#17](https://github.com/mcpdev80/baseharbor-console/pull/17), [baseharbor-node-connector#23](https://github.com/mcpdev80/baseharbor-node-connector/pull/23)  
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

2026-11-07: Preparation started with a read-only audit. Verified missing `docs/releases/v0.4.27.md` and `docs/releases/v0.4.27.demo-ref` on product develop, plus incomplete release scope and missing final four-repository candidate qualification. See `evidence/v0.4.27-prepare-2026-11-07.md`.

2026-11-12: Confirmed v0.4.27 is still **unreleased** (GitHub latest is v0.4.26) and inventoried the four fetched source tips. The exact-source preflight fails because Demo's `baseharbor-core.ref` is not the current Core candidate; Console and Connector manifests remain on the 0.4.26 matrix. Release documentation PRs remain open Draft; BaseHarbor #1522 is conflicting. Strict EN/DE MkDocs builds passed on its draft head, but the full documentation audit found a fenced-command parity mismatch in the workstation guide; no candidate Pages run/deployment exists. Candidate refs must be updated only after implementation/consumer acceptance settles. See `evidence/v0.4.27-prepare-2026-11-12.md` for exact SHAs and the next sequence. No full pre-release, release jobs, tags, promotion, Pages publication, or product source changes were made. Preparation remains active and incomplete.

owner-direktive 2026-11-07: release-vorbereitung FORTSETZEN aber NICHT veroeffentlichen (kein pre-release/tag/promotion bis separate freigabe). umbrella; wartet auf rest der welle (117+ci-seam+118+003).

PR#1151 (prepare-branch) MERGED. Karte BLEIBT active gemaess owner-direktive 2026-11-07: release PREPARE ja, PUBLISH/TAG nein bis freigabe. Kein board-lie — GATE=owner publish.

PR#1151 prepare-branch MERGED. Karte NICHT in arbeit (kein worker) — wartet auf OWNER publish-freigabe (direktive prepare-ja/publish-nein) => wait, nicht active. trigger: owner publish-anweisung.


2026-11-13: Reconciled the current release cards and merged documentation. Core #1522 merged as `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52`; Demo #129 merged as `530c64af8e8943db19d17a2552ef0fd6e7be3e84`. The selected implementation cards for workstation/user lifecycle, stage versions and Demo consent are accepted. Target policy presets remain active; the broader docs card and user/team, local/remote runtime, and stage/promotion proofs remain waiting. Exact four-repository pins still do not form a v0.4.27 candidate: Demo points to an older Core SHA, while Console and Connector still declare v0.4.26. Keep Prepare active and Qualify waiting. See `evidence/v0.4.27-prepare-2026-11-13.md`; no release, tag or publication occurred.


## Kanban reconciliation — 2026-11-13

GitHub reports zero open pull requests in `mcpdev80/baseharbor` and `mcpdev80/baseharbor-demo`. The four implementation cards previously shown as active had only merged PRs or no PR; they were moved to Wait pending a real worker assignment. Seven started v0.4.27 cards are in Wait with Maintainer reassignment ownership; two unstarted follow-ups remain Planned behind their prerequisites. Their PR links were removed from current-card metadata where they are merged or closed; task history retains the historical links. This Prepare card remains the only active v0.4.27 card because this session is actively updating its release dossier. See `evidence/v0.4.27-prepare-2026-11-13.md`.
