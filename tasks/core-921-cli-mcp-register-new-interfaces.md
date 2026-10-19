---
id: core-921
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation)"
depends_on: [core-917, core-918, core-919, core-920, t-20261016-registration-ci-readiness, t-20261019-core921-coverage-binding]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#998]
sources: ["mcpdev80/baseharbor#921"]
source_updated: "2026-10-15T16:45:53Z"
labels: [area/dx, area/compatibility]
blocker: "Protected paused o1 binding remains unpublished/uncommitted; regular claim release or separately authorized owner resumption, publication and independent policy review are required before #998 current Required CI."
resolution: ""
evidence: []
---

- [ ] core-921 · CLI and MCP: register new interfaces consistently #task #release/v0-4-26 #status/blocked #view/blocked #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation)  
    **PR:** [baseharbor#998](https://github.com/mcpdev80/baseharbor/pull/998)  
    **Blocker:** Protected paused o1 binding remains unpublished/uncommitted; regular claim release or separately authorized owner resumption, publication and independent policy review are required before \#998 current Required CI.  
    **Needs:** [t-20261019-core921-coverage-binding](t-20261019-core921-coverage-binding.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md), [t-20261016-registration-ci-readiness](t-20261016-registration-ci-readiness.md), [t-20261019-core921-coverage-binding](t-20261019-core921-coverage-binding.md)  
**Required by:** [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation)  
**Priority:** not set  
**PRs:** [baseharbor#998](https://github.com/mcpdev80/baseharbor/pull/998)  
**Source:** [baseharbor#921](https://github.com/mcpdev80/baseharbor/issues/921)
<!-- /generated:links -->

## Goal

The finished separate handlers are reachable consistently through the real CLI/JSON/MCP entry points. Lane: single shared integration.

## Scope

- In scope: **sole owner** of the `cmd/baha` command tree/registration, `human_new` routing, `machine_coverage`, the MCP tool registry, help/discovery/coverage goldens and generated CLI/MCP references.
- Out of scope: reinventing legacy aliases.

## Acceptance

- `app new`, `app edit` and `app footprint show` are discovered and routed correctly; existing verbs/approval/machine classification stay consistent.
- Discovery/help show only actually available operations; generated references come from real registrations.
- Shared files change in this one small integration PR; predecessor tasks deliver compiling constructors/adapters, no parallel registry patches.

## Required checks

- Command tree/help/discovery/generated drift checks and a generic in-process MCP client; small CLI smokes, no full journey.

## Dependencies and file ownership

- Depends on core-917, core-918, core-919 and core-920. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Sole writer of existing command/root/human_new routing, MCP registration, machine coverage/discovery/help goldens and generated CLI/MCP references; identify actual paths from current develop before editing.
- **Delivered interface/result:** Register already accepted callable handlers and generate references from the live tree; all predecessor handoffs include their final API and test evidence.
- **Task-specific proof:** Real command tree/help/discovery and generated-reference drift checks; in-process MCP client and small CLI smokes. Require actual handler reachability, not just constructor compilation.
- **Boundary:** No speculative registration of unfinished handlers, lifecycle redesign or new interaction framework. Other tasks may not edit these shared files concurrently.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Controlled development pause ordered by Marcel; infrastructure prerequisite (GC evidence preservation) fixed via merged #999/#1000, but trusted gates still block: `integration_sha_mismatch` (#995/#985 lane) and `coverage-unresolved` needing exact reviewed-bundle qualification (#998/#993/#990/#989). No CI reruns, no correction loops, no merges during the pause.
- Independent local Ornith review COMPLETED at `756b22dc8967d0daa7393065cd5bc15f262c7050`: verdict APPROVE, read-only proven by before/after sha256 equality (evidence/board-2026-10-19/o1-core921-review.md). Coverage gate root cause diagnosed and CI predecessor t-20261019-core921-coverage-binding created; its implementation is paused UNCOMMITTED. #998 stays draft; no CI rerun during pause.

### 2026-10-19 — Independent local review complete; CI predecessor added

- Ornith review worker o1 (session b70198fc) reviewed exact candidate `756b22dc8967d0daa7393065cd5bc15f262c7050` read-only with before/after sha256 equality; verdict **APPROVE**, no candidate-blocking findings (report: ecosystem `evidence/board-2026-10-19/o1-core921-review.md`).
- Root cause of the persistent `coverage-unresolved` finalcheck is a missing develop-side reviewed-bundle binding for the 13-file registration set; created predecessor [t-20261019-core921-coverage-binding](t-20261019-core921-coverage-binding.md). After that lands on develop, rerun #998 selected checks, then submit for Codex 6.1 final acceptance.

### 2026-10-19 — Resumed reconciliation; ownership transferred to Codeman lane

- Prior claim: ChatGPT (core-921 registration implementation); implementation was handed off 2026-10-18 and the claim sat dormant through the ended pause. Operation transfers to Flash (codeman w1-baseharbor) under the 2026-10-19 board mandate; prior records preserved.
- Verified on resume: Draft #998 open at `756b22dc8967d0daa7393065cd5bc15f262c7050`, MERGEABLE against develop `f2bad5ef`; GitHub review list shows no formal review records — earlier positive notes exist only as planning handoffs. The sole non-green check in run 39130075369 is the fail-closed `Enforce every required check` step; functional/docs/wizard-registration lanes green; runtime jobs skipped on `coverage-unresolved` for the new registration/machine-operation paths.
- Next boundary: independent Ornith local source review plus immutable coverage binding following the merged #991 pattern, then Codex 6.1 final acceptance; #998 stays draft until then.

### 2026-10-18 — Published candidate; paused for Horde/Codex handover

- Actual open Draft #998: `756b22dc8967d0daa7393065cd5bc15f262c7050`, branch `work/core-921-central-cli-mcp-registration`; trusted develop `f2bad5efa27fa2a791e5b357509af92d8861a3f1`.
- Implementation handed off; canonical status corrected from active to review. Reported CI 39130075369 passes selected functional/docs checks; finalcheck unresolved. Independent full source review and formal coverage have not been performed by Manager and must not be inferred from this handover.
- Existing implementation claim retained but writes paused by Maintainer. No new source edits, tests, policy qualification or merge until explicit resumption/test assignment. See [2026-10-18-horde-codex-handover-pause](../decisions/2026-10-18-horde-codex-handover-pause.md).


- **2026-10-18 — Exact PR CI outcome:** [Actions 39130075369](https://github.com/mcpdev80/baseharbor/actions/runs/39130075369) on `756b22dc8967d0daa7393065cd5bc15f262c7050`: `wizard-registration-tests`, `source-contracts`, `documentation-audit`, EN/DE MkDocs, guided tests, CLI build/vet/gofmt and Public Contracts **SUCCESS**. Mandatory `PR Selected Checks` **FAILS CLOSED** with `coverage-unresolved` for new registration/machine-operation source paths (including independently reviewable mixed registration paths); no own qualification or bypass. Remains **active / awaiting independent source review and immutable coverage binding**. Isolated Planning `render/check` 0 errors/0 warnings and 47 tests PASS; generated views may change concurrently and must be committed from the latest main without overwriting others.

- **2026-10-18 — Registration implementation candidate.** Product [PR #998](https://github.com/mcpdev80/baseharbor/pull/998) opened as a draft against `develop` `f2bad5efa27fa2a791e5b357509af92d8861a3f1` (contains accepted core-918). Current candidate `756b22dc8967d0daa7393065cd5bc15f262c7050`. Existing `app new` CLI/MCP registration retained without duplication; `app edit` interactive CLI and two-phase typed MCP Edit registered through accepted proposal/consent/lifecycle owners; `app footprint show` CLI and read-only MCP registered through GuidedReadContext and canonical Footprint projection. Real CLI help/coverage and in-process MCP registration/negative-consent tests, generated EN/DE CLI/MCP references, Machine Discovery fixture and Go vet checked in isolated targeted tests. No new lifecycle.
- **Hosted CI:** [run 39130075369](https://github.com/mcpdev80/baseharbor/actions/runs/39130075369) for current SHA; explicit final selected-check status must be evaluated before independent qualification. Prior run [39129814400](https://github.com/mcpdev80/baseharbor/actions/runs/39129814400) caught German technical-literal drift and discovery fixture drift; both were corrected. The new file set requires independent review and normal mandatory gates; no self-acceptance, native live test or merge.

- **2026-10-18 — Implementation claim.** Planning-main baseline `b7a4e8cdc6393da30907e74124025d2e1be41fd5` rendered/checked with 47 tests PASS, 0 errors; core-918 confirmed accepted/closed (review 5563005368, CI 39124293692, merge f2bad5efa27fa2a791e5b357509af92d8861a3f1). Claim core-921 as sole writer for registration and generated references; preserve concurrent unrelated claims. No lifecycle changes, bypass, author merge or live tests.

- 2026-10-16: Explicit registration-CI prerequisite [t-20261016-registration-ci-readiness](t-20261016-registration-ci-readiness.md) added as an assignment gate; no prose-only waiting assumption.

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.

### 2026-10-19 — Verified external ownership boundary during CI stabilization

- Remote #998 remains756b22dc8967d0daa7393065cd5bc15f262c7050 unchanged. No competing CORE_921 binding was created in #1001/#1002/#1003.
- Existing binding task documents o1's exactly two unpublished/uncommitted files at paused basef2bad5ef, no PR. The local APPROVE report and ecosystem coordinator status are not in reachable published trees; their contents have not been independently read here. Published task confirms pause and ownership, not source publication.
- Owner/claim preserved. Maintainer coordination marks this prerequisite genuinely blocked while Codeman remains paused; this does not release or transfer the claim. Required continuation: explicit resumption/release, preserve and integrate o1's original work on current trusted develop, finish negative tests, publish, independent policy review, then normal current #998 integration and real Required CI. No automatic worker restart after infrastructure success.
