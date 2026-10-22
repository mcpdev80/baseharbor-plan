---
id: core-922
areas: [docs]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Codex (Owner-authorized readiness documentation preparation)"
depends_on: [core-921, core-900]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1031]
sources: ["mcpdev80/baseharbor#922"]
source_updated: "2026-10-15T16:45:47Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-922 · Docs: explain New/Edit and provider selection concisely #task #release/v0-4-26 #status/review #view/review #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized readiness documentation preparation)  
    **PR:** [baseharbor#1031](https://github.com/mcpdev80/baseharbor/pull/1031)  
    **Blocker:** Owner explicitly requested stop; Codeman handoff prepared; await Owner-directed resumption or reassignment.  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Required by:** [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Owner-authorized readiness documentation preparation)  
**Priority:** not set  
**PRs:** [baseharbor#1031](https://github.com/mcpdev80/baseharbor/pull/1031)  
**Source:** [baseharbor#922](https://github.com/mcpdev80/baseharbor/issues/922)
<!-- /generated:links -->

## Goal

Developers find a short, accurate New/Edit guide that needs no prior infrastructure product knowledge. Lane: EN/DE guide.

## Scope

- In scope: EN/DE public guides, navigation, examples, changelog and v0.4.26 release notes.
- Out of scope: generated CLI/MCP references (core-921); process docs (#890, closed).

## Acceptance

- Explains needs-first selection, optional provider, preview, No/Cancel, zero capabilities, footprint and effects with real supported examples.
- Only essential delivered developer changes; Console/Connector consumption described by its actual reach; no anticipation of v0.4.28/platform features.
- EN/DE identical; Pages candidate build/navigation checked; no process rules added to the README and no public Pages deployment before promotion.

## Required checks

- Existing targeted docs/link/EN-DE/candidate build checks; no runtime matrix for text alone.

## Dependencies and file ownership

- Depends on core-921. Final candidate/evidence qualification additionally needs #897–#900 (already accepted); coordinate with pilot core-901.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Public EN/DE New/Edit/provider/footprint guides, navigation and v0.4.26 changelog/release prose; list matching locale paths from the delivered command tree.
- **Delivered interface/result:** Document only the accepted registered surface. Existing merged pin/evidence/GC prerequisites are satisfied; query their current records rather than copying old open-status prose.
- **Task-specific proof:** Existing docs audit, locale integrity/parity, strict EN/DE MkDocs and Pages candidate checks. No deployment or native runtime for text alone.
- **Boundary:** No generated CLI/MCP references, product code, shared CI or process-rule edits. Do not wait for a session summary: inspect accepted handlers/help and planning directly.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

### 2026-10-21 — OWNER STOP; Codeman handoff, not acceptance

- Owner explicitly requested stopping work and preparing a Codeman handoff. No new product changes, merges or CI starts after that instruction. This card is BLOCKED by that explicit Owner stop; unfinished release scope is not accepted. No implementation PR is invented for the documentation checkpoint. Preserve existing claims/history and coordinate resumption with the Owner.
- Canonical [Codeman handoff and portable patch inventory](../evidence/codeman-2026-10-21/HANDOFF.md) records accepted develop30e11243, green but unmerged #1030/head446e, real native scopes, unpublished docs/Demo/consumer work, dirty SQL classification and missing final candidate evidence. No release or Pages publication occurred.


### 2026-10-21 — Current 16-file EN/DE draft validated; final Core dependency retained

- Preserved exactly sixteen owned documentation paths; portable patch `docs-v0426-owned.patch` is ready to apply onto accepted final Core without importing the old unaccepted registration ancestry. Published draft e1206a6a remains an older snapshot; current corrections are locally reviewed and not yet published.
- Fresh EN/DE strict builds, complete documentation audit, 158 locale pairs and 17,749 rendered references PASS. Notes/changelog now cover actual workload-only backup stop, bounded recovery after partial stop, canonical SQL identity/TLS, detached retirement preferences and typed MCP partial/refusal outcomes. Automatic reset implementation is accepted through #1018; it is no longer an implementation blocker.
- Consumer draft checks PASS: Console 64 contracts plus architecture, Demo six consent/diagnostic tests, Connector four HTTP-evidence tests and actionlint on affected workflows. No native consumer acceptance or immutable final matrix is claimed. Final accepted Core, docs PR qualification, changelog date, Core → Demo → Console → Connector pins and actual joint runtime gates remain prerequisites. No Pages deployment or release publication.


### 2026-10-21 — Complete draft and local documentation validation

- Thirteen files are prepared on isolated `docs/v0426-new-edit`: paired New/Edit/provider/footprint guides, paired unpublished v0.4.26 notes, changelog and navigation/entry-point links. Generated CLI/MCP references and consumer pins are untouched.
- Actual documentation audit, strict EN/DE MkDocs, 158 locale-pair technical-integrity checks and 17,748 rendered links/assets PASS. No Pages deployment, release publication, native success or consumer qualification is claimed.
- Registration remains unaccepted; preserve this draft and integrate the accepted source before PR qualification/acceptance. The discovered Edit Automatic-reset defect is being corrected separately rather than documented as supported before its implementation passes.


- Draft implementation prepared under the explicit complete-readiness mandate; final integration still requires accepted core-921.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
