---
id: core-921
areas: [cli]
type: task
release: v0.4.26
priority: critical
version: ""
parent: v0.4.26
owner: "Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation)"
depends_on: [core-917, core-918, core-919, core-920, t-20261016-registration-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#998]
sources: ["mcpdev80/baseharbor#921"]
source_updated: "2026-10-15T16:45:53Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-921 · CLI and MCP: register new interfaces consistently #task #release/v0-4-26 #status/active #view/active #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation) · **Priority:** critical  
    **PR:** [baseharbor#998](https://github.com/mcpdev80/baseharbor/pull/998)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md), [t-20261016-registration-ci-readiness](t-20261016-registration-ci-readiness.md)  
**Required by:** [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor); prior implementation: ChatGPT (core-921 registration implementation)  
**Priority:** critical  
**PRs:** [baseharbor#998](https://github.com/mcpdev80/baseharbor/pull/998)  
**Source:** [baseharbor#921](https://github.com/mcpdev80/baseharbor/issues/921)
<!-- /generated:links -->

## Goal

The finished separate handlers are reachable consistently through the real CLI/JSON/MCP entry points. Lane: single shared integration.

## Scope

- In scope: **sole owner** of the `cmd/baha` command tree/registration, `human_new` routing, `machine_coverage`, the MCP tool registry, help/discovery/coverage goldens and generated CLI/MCP references.
- Out of scope: reinventing legacy aliases.

## Acceptance

- Before final acceptance/merge, the [existing exact-source coverage task](t-20261019-core921-coverage-binding.md) must be independently accepted for the corrected reviewed source; current mandatory registration/MCP/CLI/docs/Public Contracts checks must actually pass. This is an acceptance prerequisite, not a prohibition on fixing the rejected source first.

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

### 2026-10-20 (post-reboot) — Codex round 3 delivered CHANGES_REQUESTED; app.edit wiring fix in progress

- Codex verdict (round2 + round3): the native proof must run through baseharbor.app.edit (propose -> JSON round-trip -> apply with consent, verified execution; stale/wrong-consent negatives must compare relevant persisted state byte-wise). All four findings reproduced statically against a66e5de6 (tests called plan/apply only).
- Correction lane p20 (Ornith, post-reboot resume of interrupted o20) is reworking cmd/baha/app_mcp_provider_edit_native_test.go in the branch worktree, native re-run on baha-docker, push, evidence o20-appedit-fix.md. CORE_921 pins in the binding must re-pin to the resulting final head.
- Binding #1007: trusted-base clause implementation verified (q15 guard-set review APPROVE, all six guards); pending items are #998 final head, H freeze, separate record PR (draft prepared + under audit r8), then Codex round 4. Reviewer session fe5dff6c was lost in the VM reboot; replacement restart pending Maintainer go.


### 2026-10-20 — TODO queued: PR metadata rewrite after final heads (per q12 audit)

- Coordinator action after o20/o21 final SHAs: rewrite #998 body (current head lineage + native gate evidence), `gh pr ready` #998, rewrite #1007 title/body (three stale SHAs: title 6931ba9c / body 08d8f498 / real head). Labels/milestones deliberately unchanged (repo convention: merged #999/#1005/#1006 also lack them). Evidence: q12-pr-state-audit.md.


### 2026-10-20 — Codex round 3: CHANGES_REQUESTED on candidate a66e5de6 (new cause: app.edit wiring)

- Reviewer findings (verbatim: evidence/board-2026-10-19/codex-verdict-core921-round3.md): the native test drives baseharbor.plan/apply, never baseharbor.app.edit; it pre-writes the manifest instead of obtaining an app.edit propose and round-tripping the proposal JSON into the apply phase; negative assertions check presence instead of before/after persisted-state and the inventory helper returns success on inspection failure. Coordinator reproduced finding 1 statically (CallTool names in a66e5de6 test file).
- Fresh error cause, new correction budget. Smallest sufficient gate per reviewer: one isolated Docker test: app.edit propose -> JSON round-trip -> app.edit apply with matching consent and verified execution; stale proposal + wrong consent -> structured errors with unchanged relevant persisted state.
- Consequence for #1007: CORE_921 constants must re-pin to the final #998 head after this round; binding lane implements Codex design ruling (a) (content-hash anchoring for self-qualifying binding PRs) in parallel (disjoint write set).


### 2026-10-19 — Native MCP gate PROVEN on baha-docker; #998 head now a66e5de6 (delta review running)

- o10 ran the real native lifecycle on baha-docker (202 s, exit 0): valid propose->apply converges a supported SQL add with verified complete receipt (State:running Verified:true); stale proposal -> structured `conflict` with unchanged binding; missing second stage -> `approval-required` with unchanged binding. Closes Codex round-2 native gap. Evidence: ecosystem `evidence/board-2026-10-19/o10-native-mcp-proof.md`; new commit `a66e5de6` (parent 6931ba9c, +1 test file) pushed to `work/core-921-central-cli-mcp-registration`.
- Independent delta review (6931ba9c..a66e5de6): **APPROVE** (r3) - implements exactly Codex's four requirements against the real baseharbor.apply MCP entry, genuine opt-in env skip (CI-safe, matches sibling lifecycle test), gofmt/vet clean. Evidence: ecosystem `evidence/board-2026-10-19/r3-998-native-delta-review.md`. Candidate `a66e5de6` fully reviewed locally; awaiting #1007 binding fix+re-pin (o12) for consolidated Codex handoff.
- Independent re-verification by a qwen3.6 session (fresh isolated dir on baha-docker, same SHA): **REVERIFIED** exit 0, ~235 s, structured conflict/approval-required negatives unchanged-state confirmed. Evidence: ecosystem `evidence/board-2026-10-19/q1-native-reverify.md`. binding re-pin to a66e5de6 delegated to o12 together with the r4 merge-chain reachability fix on #1007.


### 2026-10-19 — Local pre-review of candidate 6931ba9c: F1-F4 PASS, only native proof open

- Independent read-only pre-review (qwen3.6 session r1): snake_case schemas, typed classifyAppMachineError paths, structured handler negatives with zero-write proof, repo conventions - all PASS with file:line evidence; build/vet/tests/gofmt green at 6931ba9c. Single CHANGES_REQUESTED item is the known native propose->apply gate (o10 lane, in progress), no new findings. Evidence: ecosystem `evidence/board-2026-10-19/r1-998-prereview.md`.


### 2026-10-19 — Codex round 2: typed errors accepted, native happy-path open

- Codex 6.1 round-2 verdict (session fe5dff6c, evidence/board-2026-10-19/codex-verdict-core921-round2.md): #998 at `6931ba9c` CHANGES_REQUESTED with exactly one blocking gap - fully successful real MCP propose->apply requires one focused native proof on the docker VM (Codex named the smallest sufficient gate). All round-1 P1/P2 items (schema root assertion, typed adapter classifications, structured negatives, zero-write by snapshot equality) verified closed; guards unchanged.
- Independent delta review of `6931ba9c` by worker o8: APPROVE (evidence/board-2026-10-19/o8-998-delta.md). Worker o10 now implementing the native MCP proof on baha-docker (isolated state, disposable app; podman/#995 untouched). Binding must re-pin to o10's resulting SHA.

### 2026-10-19 — Corrected candidate reviewed; handed to Maintainer with binding PR #1007

- FINAL source `08d8f498fd82992e762d764967ac892721d9adeb` (branch head; merge of develop plus F1 typed-error closure). Independent full-source review at `24119eb9` and delta review to `08d8f498` both **APPROVE** (worker o4, session 19d72a4b): snake_case public/nested schemas with phase-conditional proposal/consent, typed `machine.NewError(machine.ErrorConflict,...)` classifications, structured-code handler negatives with proven zero writes, valid real MCP propose→apply, guards byte-unchanged; `evidence/board-2026-10-19/o4-998-rereview.md`.
- Coverage predecessor PR **#1007** open (non-draft, MERGEABLE): exact binding of reviewed head `08d8f498` plus the complete fifteen path/status pairs, all develop-side clauses preserved, `evidence/board-2026-10-19/o1-binding-final.md`.
- Open infrastructure finding handed to the CI owner: stale webhook `base.sha` vs regenerated merge ref causes `integration_sha_mismatch` on otherwise healthy runs; `evidence/board-2026-10-19/ci-finding-integration-sha-mismatch.md`. #998 selected checks are expected to resolve after #1007 lands and CI re-plans on a current base.
- Maintenance boundary: independent review/acceptance/merge of #1007 and #998 belong to the Maintainer (Codex 6.1 lane). Flash sets this task to review; no self-acceptance.


### 2026-10-19 — Resumed: review 5569055023 defects corrected on the existing branch

- Worker o5 (74144db2) corrected all three confirmed defects on branch `work/core-921-central-cli-mcp-registration`; new head `24119eb936520e56b6f23b16773d30770532a386` = normal merge of develop `19548bf0` plus fixes; pushed, PR #998 stays draft. Snake_case public/nested schemas with phase-conditional proposal/consent, typed machineMCPFailure classifications, real tools/list + valid propose→apply + precise handler-level zero-write negatives. Handoff evidence: ecosystem `evidence/board-2026-10-19/o5-998-correction.md`.
- Fresh independent full-source review running with worker o4 (session 19d72a4b); the final core-921 coverage binding will qualify only this re-reviewed head plus the complete path/status set from that review. The old `756b22dc` candidate stays unqualified.

### 2026-10-19 — Maintainer resumption: source correction active

- Marcel explicitly reconfirmed Codeman's continuation and required current board status. Existing Flash claim/branch and protected o1 work are retained; this update is an assignment, not evidence that an external worker was started.
- This task is ACTIVE for correction of review5569055023: actual MCP schema, phase-specific inputs and typed public errors with real SDK/handler regressions. These are work to perform, not a reason to leave the source task globally blocked.
- Removed only the unfinished exact-source binding from implementation depends_on: no missing callable input or test executor prevents correcting #998. The existing registration/CLI/docs/contract test profile already executes; the binding can only be finalized after corrected source review. Keeping it as a hard implementation predecessor inverted that order. All accepted interface dependencies remain unchanged.
- Final immutable binding remains a mandatory ACCEPTANCE gate: [existing o1 binding task](t-20261019-core921-coverage-binding.md), fresh independent full-source review, complete file/status inventory and current green Required Checks are required before merge/accepted. No coverage, review or test requirement is waived.
- Current product develop19548bf0; current published source756b22dc remains Changes required. Preserve o1's two uncommitted files; no competing implementation, force push or task acceptance.

### 2026-10-19 — Complete-release review: source changes required, existing owner to correct

- Exact current #998 source remains756b22dc8967d0daa7393065cd5bc15f262c7050. Independent full-release review [5569055023](https://github.com/mcpdev80/baseharbor/pull/998#pullrequestreview-5569055023) overrides the earlier positive source assumption: missing JSON tags infer PascalCase and require proposal/consent for propose; the reject-any-error SDK test does not reach the actual consent handler.
- Correct public/nested snake_case schema and optional phase-specific fields through this existing owner/branch. Assert tools/list schema; execute valid real MCP propose and consented apply plus specific missing/stale/wrong-target denial with no writes. Ordinary errors and private appMachineError currently map through machineMCPFailure/main.go to internal_error; reuse existing typed error owners and assert public error codes/remediation.
- Flash retains ownership. No source mutation or claim transfer by this audit. Existing selected registration/adapter/docs/CLI tests must actually execute on the corrected source before a fresh independent full-source review; no old coverage binding may qualify the rejected source in advance.
- Preserve/checkpoint o1's two original uncommitted planner files. Finish the existing binding only after the corrected reviewed source/status set is known, preserving accepted infrastructure and disjoint coordinator SQL-layout qualification. The new source correction precedes final policy acceptance; do not wait idly for an approval of the defective old source.

### 2026-10-19 — Controlled existing-owner resumption

- Infrastructure hold superseded by the [controlled resumption decision](../decisions/2026-10-19-ci-stabilization-controlled-resumption.md). Flash/o1 claim preserved; complete its existing binding predecessor first, with dirty work checkpointed and current accepted infrastructure normally integrated.
- #998 remains at 756b22dc8967d0daa7393065cd5bc15f262c7050; no product source or branch changed here. After independent binding acceptance, integrate current develop normally, confirm reviewed source equivalence, execute actual selected registration/docs/contract gates and obtain final Maintainer acceptance. This task remains blocked on its unfinished predecessor, not on a global Codeman pause or unrelated #995 native recovery.

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
