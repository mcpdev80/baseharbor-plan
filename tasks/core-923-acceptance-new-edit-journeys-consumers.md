---
id: core-923
areas: [acceptance]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: Codex session 2 native acceptance (d48643e22049)
depends_on: [core-921, core-922, core-900]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: ["mcpdev80/baseharbor#1073", "mcpdev80/baseharbor#1072", "mcpdev80/baseharbor#1071", "mcpdev80/baseharbor-console#13", "mcpdev80/baseharbor-console#12", "mcpdev80/baseharbor-node-connector#13", "mcpdev80/baseharbor-console#11", "mcpdev80/baseharbor-node-connector#12", "mcpdev80/baseharbor-demo#121", "mcpdev80/baseharbor-demo#122", "mcpdev80/baseharbor-console#9", "mcpdev80/baseharbor-console#10", "mcpdev80/baseharbor-node-connector#10", "mcpdev80/baseharbor-node-connector#11"]
sources: ["mcpdev80/baseharbor#923"]
source_updated: "2026-10-15T16:45:40Z"
labels: [area/evidence]
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/40128173805", "https://github.com/mcpdev80/baseharbor-demo/actions/runs/40128218519", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/final-release-audit-2026-10-24/v0.4.26.consumer-pins.json"]
---

- [ ] core-923 · Acceptance: verify New/Edit journeys and ecosystem consumers #task #release/v0-4-26 #status/active #view/active #area/acceptance #kind/task
    <!-- generated:card -->
    **Owner:** Codex session 2 native acceptance (d48643e22049)  
    **PR:** [baseharbor#1073](https://github.com/mcpdev80/baseharbor/pull/1073), [baseharbor#1072](https://github.com/mcpdev80/baseharbor/pull/1072), [baseharbor#1071](https://github.com/mcpdev80/baseharbor/pull/1071), [baseharbor-console#13](https://github.com/mcpdev80/baseharbor-console/pull/13), [baseharbor-console#12](https://github.com/mcpdev80/baseharbor-console/pull/12), [baseharbor-node-connector#13](https://github.com/mcpdev80/baseharbor-node-connector/pull/13), [baseharbor-console#11](https://github.com/mcpdev80/baseharbor-console/pull/11), [baseharbor-node-connector#12](https://github.com/mcpdev80/baseharbor-node-connector/pull/12), [baseharbor-demo#121](https://github.com/mcpdev80/baseharbor-demo/pull/121), [baseharbor-demo#122](https://github.com/mcpdev80/baseharbor-demo/pull/122), [baseharbor-console#9](https://github.com/mcpdev80/baseharbor-console/pull/9), [baseharbor-console#10](https://github.com/mcpdev80/baseharbor-console/pull/10), [baseharbor-node-connector#10](https://github.com/mcpdev80/baseharbor-node-connector/pull/10), [baseharbor-node-connector#11](https://github.com/mcpdev80/baseharbor-node-connector/pull/11)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/40128173805), [proof 2](https://github.com/mcpdev80/baseharbor-demo/actions/runs/40128218519), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/final-release-audit-2026-10-24/v0.4.26.consumer-pins.json)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-922](core-922-docs-new-edit-provider-selection.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex session 2 native acceptance (d48643e22049)  
**Priority:** not set  
**PRs:** [baseharbor#1073](https://github.com/mcpdev80/baseharbor/pull/1073), [baseharbor#1072](https://github.com/mcpdev80/baseharbor/pull/1072), [baseharbor#1071](https://github.com/mcpdev80/baseharbor/pull/1071), [baseharbor-console#13](https://github.com/mcpdev80/baseharbor-console/pull/13), [baseharbor-console#12](https://github.com/mcpdev80/baseharbor-console/pull/12), [baseharbor-node-connector#13](https://github.com/mcpdev80/baseharbor-node-connector/pull/13), [baseharbor-console#11](https://github.com/mcpdev80/baseharbor-console/pull/11), [baseharbor-node-connector#12](https://github.com/mcpdev80/baseharbor-node-connector/pull/12), [baseharbor-demo#121](https://github.com/mcpdev80/baseharbor-demo/pull/121), [baseharbor-demo#122](https://github.com/mcpdev80/baseharbor-demo/pull/122), [baseharbor-console#9](https://github.com/mcpdev80/baseharbor-console/pull/9), [baseharbor-console#10](https://github.com/mcpdev80/baseharbor-console/pull/10), [baseharbor-node-connector#10](https://github.com/mcpdev80/baseharbor-node-connector/pull/10), [baseharbor-node-connector#11](https://github.com/mcpdev80/baseharbor-node-connector/pull/11)  
**Source:** [baseharbor#923](https://github.com/mcpdev80/baseharbor/issues/923)
<!-- /generated:links -->

## Goal

The integrated v0.4.26 product surface works for developers and existing consumers on the real candidate. Lane: targeted product acceptance.

## Scope

- In scope: existing Demo/consumer fixtures and release-specific gate/evidence inventories.
- Out of scope: product source changes, except a concrete found bug through its own fix PR. Preparation is not approval for a complete pre-release or promotion.

## Acceptance

- Native Docker and rootless Podman: fresh app without managed capabilities, create with real dependencies, edit/add/remove/provider switch, No/Cancel safety and data/shared preservation covered in a targeted way.
- Qualifies the actual current immutable BaseHarbor/Demo/Console/Connector revisions; CLI/JSON/MCP semantics through the real entry point; no old consumer PASS as a substitute.
- Uses existing gates and the core-888 plan/verifier; reuses green gates, also from failed overall runs, only with proven unchanged inputs.
- Isolates found bugs small; no full journey per fix. Final complete necessary coverage and an independent documented developer path.

## Required checks

- First the predecessors' component/contract evidence, then the necessary real consumer/runtime gates. Source/docs are not run serially before every diagnostic run. Coordinate with #897–#901 for candidate/evidence/pilot.

## Dependencies and file ownership

- Depends on core-921 and core-922; candidate/evidence/GC (#897–#900, already accepted) must be complete before.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Existing release-specific consumer fixtures and evidence inventories in the affected product/consumer repositories; record exact paths and immutable candidate refs before executing.
- **Delivered interface/result:** Own candidate-pin resolution, gate execution, evidence validation and independent developer-path report as one acceptance task; no separate operator session is needed to run its checks.
- **Task-specific proof:** Predecessor component/contract evidence, then only required real New/Edit/runtime/consumer gates. Preserve original evidence and input equality rules; no automatic full release matrix.
- **Boundary:** Source bugs get their own explicit fix assignment. Do not start against missing consumer candidates or unsupported executors: detect those at assignment readiness, before long runs. Pre-release/promotion still requires separate authorization.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

## SQL retirement correction and mandatory source CI — 2026-10-25

Diagnostic run [40141900700](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40141900700) is terminal Docker FAILURE / Podman SUCCESS, with both owned cleanups successful. It proves the primary generated HTTP-only app destroy itself rejects an already-unbound logical SQL scope; the cleanup error was secondary. The unchanged actual resolver reproduces the complete Target plan with no new SQL binding release, logical stop selections and physical Core reuse. Product source938adee7 corrects that read-only verification while preserving canonical ownership, measured absence, empty remaining SQL references, protected active physical Core and foreign/invalid-release checks. The real regression fails before and passes after; the existing safety negatives, vet, build, source readability and application/capability tests pass. The broad local CLI suite is not claimed green because its native Edit case requires unavailable Docker.

CI prerequisite [PR1071](https://github.com/mcpdev80/baseharbor/pull/1071) is accepted at c21c69b3 after run40143895573/final121021399329 SUCCESS. Exact trusted executor/planner [PR1072](https://github.com/mcpdev80/baseharbor/pull/1072) is accepted at6bc4124a after run40144095707/final121021985125 SUCCESS. All144 local planner/runner checks and the actual six Go regression/safety families pass; no independent review is claimed. Product [PR1073](https://github.com/mcpdev80/baseharbor/pull/1073), exact head6ba9ea66 and treec58fcb32, remains pending actual CI40144286041, including its mandatory wizard-runtime-retirement-tests job121022243323. No product merge, new native PASS or release readiness is inferred. Existing failed R/D/U/K graphs and artifacts remain preserved; new final Core/consumer freeze follows actual accepted product integration. Selected63/full65, promotion and tag remain pending.


## Current native failure narrowed to ordinary-retirement consent presentation

Joint [40137607614](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40137607614) finished FAILURE on exact Kacc6 / U529. Both Docker121002381187 and Podman121002381169 pass actual Core Setup READY (SQL/Secrets/Identity ready), consented application apply, plan/status/doctor/repair, real CA rotation and postrotation checks. Both then correctly refuse unconsented ordinary destroy with approval_required/impact-confirmation-required and no writes, but the Console fails to display its valid consequence review; both final owned cleanups succeed. These successful subpaths do not qualify the complete consumer journey.

Independent exact-R source review establishes the mismatch: ordinary local destroy without full_reset calls retireRuntimePreservingData and returns a leaf ProviderImpactPlan; remote/full-reset destruction returns an outer application scope. Console incorrectly requires outer scope for every destroy. A bounded six-file consumer correction supports the actual ordinary leaf under current execution/context/session/selection binding, makes false full-reset intent explicit, retains strict outer subject checks, rejects malformed present scopes without fallback and strengthens actual remote outer-plan assertions. No locality is guessed from absent fields and no Core protection changes. Exact reviewed treec6b00e116b6a00688dd39bf1779ec03e6a72ac42 passes the regression before/after proof, ten independent focused tests and all68 owner-run contracts (zero skips), compiler/lint/architecture/33-route build. Published successor source CI, actual U/K integration and new native acceptance remain pending.

Core R3e27497b and Demo D09595781 remain unchanged. Preserve this failed acc6 graph, both diagnostic ZIP origins and cleanup outcomes. Selected63, full65, promotion and tag remain pending; no release acceptance is granted.


## Protected fixture corrected; exact final native qualification running

Console [PR12](https://github.com/mcpdev80/baseharbor-console/pull/12) is integrated as actual U `52993ac5623cdfa2a3b91001ed078dfd27f31b5e`, tree `b7e4821ce87b6483f3cebfc935ee8e4419d06691`, identical to reviewed sourcefe3fab5c. The two-file correction explicitly protects only the isolated fixture config owner directory and tests the actual preparation block under umask022 for fresh/existing0755 directories. The test fails before and passes after the correction; all67 contracts (zero skips), compiler/lint/architecture/33-route production build and independent source review pass. Hosted sourceCI40136867115/job121000115187 passes. Core ownership checks, accepted consent/callback changes and R/D pins remain unchanged.

Connector [PR13](https://github.com/mcpdev80/baseharbor-node-connector/pull/13), sourcef1cc3ae3/tree510b7934, solely repins actual U529; sourceCI40137062718/job121000708063 passes and merge6bd86048 preserves exact reviewed bytes. Root omitted the workflow marker from the merge message and caught this before moving the native trigger. The correction is one same-tree operational successor, actual K `acc6fba541a47e73781d8ebb7b7f910e2e2e5d42`, with sole parent6bd and existing [ecosystem-runtime] marker. Its full source tree is unchanged; the existing source-only route independently qualifies exact K in40137388108/job121001700088 SUCCESS. Root then performs an expected-head non-force main6bd-to-K fast-forward; no product/workflow change, history rewrite or skipped native run is concealed.

Fresh actual K/U/D manifests and unchanged R resolver/source-origin validation independently generate canonical matrix SHA256 `33cd462d0f159821a6f16c1d2c1e85d311fd92724b3bf61f63806d42f52011bb`. Previous failed Kc436 graph/terminal freeze and diagnostic ZIP origins remain preserved separately. Core R3e27497b and Demo D09595781 are unchanged.

Exactly one expected-head non-force fast-forward moves the existing native trigger from Kc436 to actual Kacc6. New joint [40137607614](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40137607614), push/attempt1, resolves successfully and runs Docker121002381187 and Podman121002381169. Actual complete Core persistence/PKI/Identity, browser/application/remote lifecycle and owned cleanup remain PENDING. No source-only success or previous partial successful subpath substitutes for this required native result. Selected63, full65, promotion and tag remain pending; no release acceptance is claimed.

See CONSOLE-PERMISSIONS-REVIEW.md, JOINT-NATIVE-THIRD-FAILURE.md and the current canonical JSON. Historical checkpoints below retain their original outcomes.


## Actual native failure diagnosed: fixture configuration protection

Joint run [40135623881](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40135623881) failed on actual Kc4363a28 / U51181967. Both Docker120996434480 and Podman120996434447 now complete editor login (callback/token/discovery HTTP200 and verified token lifetime), then actual Settings Core Setup fails with `persist OpenBao recovery-file reference: Target configuration mutation requires its protected owner directory`. Both owned cleanup steps pass. OpenBao initialized/unsealed/manager_ready are true, which does not turn the failed persistence or incomplete Core setup into success.

Independent exact-R source review confirms the fixture precreates `$XDG_CONFIG_HOME/baseharbor` with `mkdir -p` under normal umask, leaving0755, while Core correctly requires an owner-only directory. The fixture protects only config.yaml0600. A minimal fixture-owned0700 correction and focused regression are in preparation; no Core security weakening, timeout increase or Core R change is justified. Subsequent persistence/TLS/Identity/lifecycle still require real native qualification on the reviewed successor graph. Selected63, full65, promotion and tag remain pending; release_eligible stays false.


## Auth correction integrated; bounded actual-R diagnosis running

Console [PR11](https://github.com/mcpdev80/baseharbor-console/pull/11) is integrated as actual U `51181967abfd3170b81857d51e9a4572c84b318b`, exact reviewed tree `79d861526dd21606db182df6216d6eec594ad896`, parent prior U7aed plus reviewed source4238e2e. All66 contract tests (zero skips), compiler/lint/architecture/production build and independent final source review pass; hosted source CI40135195710/job120995134808 succeeds. The seven-file correction preserves the accepted consent UI and exact auth checks, removes the concrete callback self-close race, and adds strictly bounded public error/status observations before teardown. It does not claim to fix the unexposed prior Secrets cause.

Connector [PR12](https://github.com/mcpdev80/baseharbor-node-connector/pull/12) is actual K `c4363a28f5fd3d929a430bc6da630ee036bba104`, tree `740a82389c59c3fed8597590515f07be40ee14d4`, parent prior Ka956 plus reviewed source19615e4f. Sole manifest Consolepin changes to actual U5118; R3e27497b/D09595781, producer, sentinel, Go source and workflows stay exact. Source CI40135417539/job120995796421 and independent complete-tree review pass.

Fresh actual K/U/D manifests generate the canonical complete matrix with unchanged R resolver and source-origin checks. Root and independent reviewer obtain identical SHA256 `dfd87ceb0191702e7b37a287b45ee8f792d00b926cc189a5ec9927f20d5570df`. The full JSON/current freeze are published externally; both earlier failed graph snapshots and original artifacts remain preserved.

Exactly one expected-head non-force FF moved the existing trigger branch from Ka956 to actual Kc436. Joint [40135623881](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40135623881), push/attempt1, has real Docker120996434480 and Podman120996434447 jobs; actual callback/Secrets/lifecycle/cleanup results remain PENDING. This is the existing actual-R route: standalone Console browser workflow hardcodes older Core2ada and cannot diagnose R without an unnecessary workflow change. Actual provider bootstrap cannot be diagnosed by source tests alone. No duplicate dispatch, speculative deadline/Core edit or acceptance waiver is introduced.

See independent `CONSOLE-AUTH-DIAGNOSTICS-REVIEW.md`, `READINESS-DOSSIER.md` and the explicitly pending `INDEPENDENT-DEVELOPER-PATH.md`. The latter distinguishes scripted real W1 execution from independent assessment; no manual session or unexecuted result is invented. Selected63/full65 and main/tag handoff remain held until actual required native evidence succeeds.


## Corrected candidate native failure; targeted investigation active

Joint run40133582447 completed FAILURE on actual Ka95639b3. Docker120990316354 timed out after editor login before the application journey. Podman120990316278 passed the actual unconsented apply negative, then real Settings control-plane.up failed with internal_error; installation phase secrets_failed, SQL true, Secrets/Identity false. Both production enrollment scopes, exact fixture cleanup and final owned-services/private-key cleanup passed. The two authenticated diagnostic ZIPs explicitly report result failure, cleanup success and release_eligible false; no qualified private manifest exists. See the independent `JOINT-NATIVE-SECOND-FAILURE.md` evidence for exact artifacts/digests and diagnostic limits.

A concrete independent Console callback race is being corrected: callback postMessage is asynchronous, but its redundant self-close can make the opener's close observer reject before the validated queued message arrives. Exact origin/source/state/PKCE checks remain mandatory; this source race is not asserted as the experimentally proven cause of Docker's particular timeout. The bounded correction also adds allowlisted, secret-safe editor and public Core error/status observations. Podman's actual underlying Secrets failure is not exposed in old artifacts; no speculative Core fix, deadline increase, waiver or blind retry is authorized by that missing detail.

Core R and Demo D095 are unchanged. A reviewed successor Console/Connector graph and genuine affected native evidence are required. core-923 and the defect audit remain ACTIVE; selected63/full65, promotion and tag handoff stay pending. The historical active-run checkpoint below is superseded by this actual failure.


## Corrected actual immutable ecosystem; native acceptance pending

The integrated graph is Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd`, Demo D `09595781b68e1f41caaba9aec1402eb8009d700f`, Console U `7aed4d58f7ac89d019b1d31fa2d5bc6e557aa2b5`, Connector K `a95639b3448fe869fca439d2db071fe75b82d7d2`. Exact source/merge trees and CI are independently approved; Connector source run40133358644/job120989617504 passed before PR11 merge. Core source remains unchanged.

The complete canonical matrix was regenerated from fresh actual K/U/D manifests using unchanged R resolver/source-origin validation. Root and independent reviewer obtained identical SHA256 `5f01828a247fce1a6fc552bb5b65504cf3c7ec7aa35c83c3bccf5626a4648615`; full JSON is `evidence/final-release-audit-2026-10-24/v0.4.26.consumer-pins.json`. Old failed K543 graph/observation are preserved separately as `v0.4.26.consumer-pins.failed-543e155d.json` and `freeze-sources.failed-543e155d.json`, with the genuine failed run40130842592 retained.

Exactly one expected-head non-force fast-forward moved the existing Connector trigger branch from old K543 to actual Ka956. New joint run [40133582447](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40133582447), push/attempt1, resolves exact actual K and runs Docker job120990316354 / Podman job120990316278 in parallel. The production browser, actual remote lifecycle and owned cleanup remain PENDING. No source CI or skipped opt-in job is native acceptance. core-923 stays ACTIVE; exact63 preproof and complete65 approval remain unstarted until authentic joint native success.


## Reviewed Console consent correction integrated

Console [PR10](https://github.com/mcpdev80/baseharbor-console/pull/10) is integrated as actual U `7aed4d58f7ac89d019b1d31fa2d5bc6e557aa2b5`, tree `7ca78c77680cb5714787259c8da85b002d0f3888`, identical to independently reviewed source `c89d2aaa007d7c5ed5f0f49fd3f8a177280a9026`. Exact-final 61 contract tests (zero skips), compiler, lint, architecture, syntax/diff checks and production build pass. Hosted source run40133151937/job120989000002 succeeds; its browser job120989001216 was intentionally skipped and is not native proof.

The Console preserves typed Core error details, displays the actual current provider consequences, collects separate ordered plan acknowledgements and independent data-deletion consent, and requires an explicit resubmit. Acknowledgements bind the current machine, deployment, context and operation; stale/new plans reset them. Browser fixtures verify actual unconsented apply/destroy leave runtime, deployment and provider registry unchanged, retain real explicit Settings Core setup, production remote lifecycle/repair/rotation and owned cleanup. Strict receipt producers reject the obsolete mandatory-Core marker. These are consumer corrections against unchanged Core R, not permission to fabricate a native PASS.

Connector [PR11](https://github.com/mcpdev80/baseharbor-node-connector/pull/11), source `8daaf545f2b60bfb4af8d492ebcdd43bd51cda2c`, reviewed tree `3a37523db3cb3e93602612f7999fea34390dbcd9`, updates only the actual R/D095/U7aed pins and stricter receipt mapping. Existing sentinel, source and runner/workflow bytes remain unchanged; source CI40133358644 and actual integration/native follow as separate boundaries. See the [independent consent review](../evidence/final-release-audit-2026-10-24/CONSOLE-CONSENT-REVIEW.md).

Canonical Core `release/v0.4.26` is fixed at exact R `3e27497b4ef7b567858ba646bc3071bee37d19bd`; this branch is a source guard, not an approval, run or tag. No complete pre-release is started before the corrected joint native acceptance passes.


## Reviewed Demo reconciliation correction integrated

Static preflight found one additional executable consent mismatch: after stopping shared PostgreSQL, the reconciliation fixture invoked bare apply even though Core R requires the current concrete resume-impact acknowledgement. Demo [PR122](https://github.com/mcpdev80/baseharbor-demo/pull/122) changes only that call to the existing strict `run_consented` helper. Independent review approved exact blob `2c128dbc455647088d2259d08d2fc9208617dadf`; four helper tests, shell syntax and diff checks pass. No hosted PR check is configured for this ordinary branch.

Actual successor Demo D is `09595781b68e1f41caaba9aec1402eb8009d700f`, tree `9219f48d5abd04b8a062edf2d22b265e025ed82a`, matching reviewed source `9611629bf053b4ff08f29a8459b4e69f4248ed12`. Core R remains `3e27497b4ef7b567858ba646bc3071bee37d19bd`. The previous graph below is historical; Console and Connector successors must bind this actual D. Console implementation, disjoint browser/receipt fixtures and independent review continue in parallel.

The earlier standalone Demo backup execution retains its original source/run attribution. Its install, backup, consent-helper, cleanup and workflow bytes are unchanged; it is not relabelled as a new D execution. Canonical v0.4.26 gate fingerprints conservatively change with this Demo fixture, so the actual final63/full65 runs must use new D. Static review found no further concrete consent mismatch in remaining W1/gate callers; that inspection is not native PASS. See [independent Demo review](../evidence/final-release-audit-2026-10-24/DEMO-RECONCILIATION-REVIEW.md) and [joint failure diagnosis](../evidence/final-release-audit-2026-10-24/JOINT-NATIVE-BLOCKER.md).


## Native consumer failure and bounded correction

Joint run [40130842592](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40130842592), attempt 1 on actual K543e155d, failed both Docker and Podman Console Chromium journeys. Production managed enrollment/outbound Connector and owned fixture/key cleanup passed in both jobs. No integration acceptance manifest was produced; no consumer native PASS or release readiness is claimed.

The real first apply returned `approval_required`, cause `impact-confirmation-required`, while the legacy journey expected `capability_missing/core_required`. Independent Core R inspection confirms capability-first SQL provisioning deliberately no longer requires management Core bootstrap; concrete provider impact consent is mandatory. Console currently sends empty apply input and cannot present/acknowledge that plan. This is a real consumer UI gap, not authority to change an assertion or inject consent through a browser route.

Marcel's full-release completion assignment delegates a bounded Console consent UI correction and the necessary genuine browser/remote fixtures plus Connector receipt mapping to consumer_final. final_audit independently reviews the actual contract, stale-plan safety, no-write refusal, explicit Core setup coverage and unchanged native acceptance strength. Root alone integrates reviewed green source. Core R and Demo D stay frozen; U/K and the external graph must be regenerated after actual successor merges. The graph below is the failed prior candidate, preserved as history.

The exact63 preproof and complete65 approval remain unstarted until the corrected actual U/K joint native proof passes. Tagging remains Marcel's final action after genuine approval and main promotion.


### Actual final graph integrated; joint native active

R3e27497b / D03396c805 / U645dda54 / K543e155d are the actual immutable merged sources. Demo native receipt is independently qualified on exact final R and reviewed head a1051ec5 with identical resulting D tree; source integrations and canonical full graph/origins are independently qualified. The full exact JSON is saved externally in final-release-audit evidence; no Core mutation after freeze. Joint actual-K native run40130842592 runs Docker/Podman in parallel and supplies the real Console browser proof. It remains pending, followed by the four W1 cases within the mandatory63 preproof. This card remains ACTIVE; source CI and skipped PR browser jobs do not accept native scope.


### Final Core and exact Demo candidate

Final R=`3e27497b4ef7b567858ba646bc3071bee37d19bd`. Demo121 candidatea1051ec5f5c366cdfafe527298ac60e5db4f951c changes only baseharbor-core.ref and is independently reviewed. Existing Podman native run40128218519 is active; no PASS claimed. Freeze D/U/K in actual predecessor order, then run final W1 and joint consumer gates on the actual immutable graph. Source integration and native acceptance remain separate.


### Current native route and final source boundary

The dispatch-route blocker is resolved through the existing reviewed Demo release-branch workflow. Run40117924670 genuinely passed backup/restore and acceptance cleanup for Core64dbf1df / Demo f90d0623; artifact12569249775 SHA2562d47ee6961d7c55df19630fbce837ecee2a4190cd4e4f6dc3d5328ff496892cc is authenticated. This is intermediate evidence only: final publication prose and user-requested concise release notes must land before final R. Consumer freeze and final W1 remain active, not accepted. New consumer-final lane coordinates successor pins without overriding previous session-2 evidence.


### 2026-10-24 — Current accepted CI integration and remaining final freeze

#1052 is now accepted and merged as 2ee295c3 after complete green actual CI 40116648056; earlier GitHub HTTP502 attempts are historical, and Owner cancellation is no longer needed. #1067 final qualifier is merged as ccb78a65 after fresh green CI 40116917521. Separate canonical 63-ID data PR #1068 is independently approved and in required CI 40117165154. Then #1046 receives its final trusted-target merge and checks, before final Core R is fixed.

Demo history/receipt preparation is independently approved at 5c814cd4, preserving the reviewed helper and tests and adding its cleanup scope upload. Final R pin/native proof remains pending. The existing native Go Docker workflow must also execute the exact eight families on R; five of those are absent from the 65-gate graph. This can run in parallel with final Demo proof. See [coordinator evidence](../evidence/ci-integration-2026-10-24/HANDOFF.md). No release readiness, promotion, tag or v0.4.27 change is claimed.

### 2026-10-24 — Owner-authorized parallel closeout, current checkpoint

Marcel explicitly requested parallel completion; earlier session stop/handoff notes are historical for this authorized scope. #1064, separate #1065 record, #1060, separate #1066 record and corrected #1056 have now been integrated with genuine green mandatory CI. develop is 51a38e2b25eb43e2a657f87d0886bd19fe44bfdc. #1052 selected source/OpenBao test jobs are genuinely completed/success, but its final PR Selected Checks failed on GitHub HTTP502. Only that failed final job was rerun; required final success remains missing and no acceptance is inferred. #1046 final policy/qualification follows this chain. Demo cleanup fix 52dde419 has independent source review and 21 helper tests PASS, with native acceptance still pending.

The historical #1050 persisted C-graph snapshot is explicitly superseded by complete canonical final R/D/U/K JSON plus immutable external Planning evidence; this does not waive that dossier. Core must be finalized before the final consumer freezes. The complete 65-ID release inventory and genuine authenticated approval remain mandatory. See [current coordinator evidence](../evidence/ci-integration-2026-10-24/HANDOFF.md) and [canonical final-candidate audit](../evidence/ci-integration-2026-10-24/FINAL-CANDIDATE-AUDIT.md). No v0.4.27 change, tag, release, deployment or full pre-release has occurred.

### 2026-10-24 — Session 3 corrected-head review (round 2)

[Independent round2 evidence](../evidence/review-v0426-2026-10-24-session3/ROUND2.md): #1064 e7fe45ccb3c2103bb3b57ad3300892b932818934 APPROVE at base65aa063e; actual full planner115 PASS and mandatory CI 40110621660 green. #1060 db79f24a39ccc1a6f8f38a13d20dd18ab151abc2 corrected source delta APPROVE; six focused regressions and actual 21 unit tests on #1052 source 9f715184 PASS, but final CI 40110759871 still correctly blocks qualification. #1052 source/unit contract is now independently APPROVE, with current-base CI/native/integration prerequisites preserved.

Actual merge-tree confirms the #1064/#1060 test-file conflict. Session1 must preserve both matrices, obtain fresh exact-anchor review after manual resolution, then separately accepted target record, clean record-forward merge and mandatory CI. No later head or inherited bootstrap fallback is waived. #1056 remote b0abe105 remains rejected; local correction preparation is not accepted. All verdicts are technical PR issue comments, not formal GitHub reviews. No card acceptance, product/CI edit, merge, native run or release-readiness claim from session3; other session owners/states and v0.4.27 remain unchanged.


### 2026-10-24 — Session 3 independent review and evidence reconciliation

Marcel assigned this session to independent review/evidence and coordinated planning only. Session 1 retains implementation/integration/all merges; session 2 owns native acceptance/freeze. Original owners and task states remain. The [exact-candidate dossier and executed probes](../evidence/review-v0426-2026-10-24-session3/HANDOFF.md) supersede reported ACCEPTs only for the explicitly reviewed heads.

Technical REQUEST_CHANGES: #1064 H54dfa458 (false-negative rejection fixtures, binding to rejected R); #1060 H0f3bd169 (missing actual OpenBao qualification, unreachable strict executor, removed exact SQL-safety test anchors); #1056 Hb0abe105 (bootstrap fallback and DAG/origin validator defects independently reproduced). #1046 H1ec67f8d source-only APPROVE, with current-base CI/native prerequisites still open; #1052 H9f715184 awaits complete qualification after corrected #1060. Findings are published as linked PR issue comments; no formal GitHub review or merge was submitted.

Demo#121 Hf57c8b6e evidence acceptance REQUEST_CHANGES: genuine successful Docker/Podman run39990941852 tests Demo25c31969/Core1861ed07, but cleanup/evidence inputs differ. Identical core.ref alone does not prove reusable receipt compatibility. Final D→U→K pins, #1050 reconciliation, native/ownership/cleanup origins and independent developer path remain open. W1 Core anchor stays1861ed07888a1ec22c218ca491d23ee54f48e261; v0.4.27 is fenced.

Clean product65aa063e docs audit PASS (158 EN/DE pairs). Strict MkDocs unavailable locally. Final pins/gate inventory/origin bundle remain missing. Unavailable Ops originals are explicitly inventoried in the dossier. #1047/#1063 and older stop/failed-head notes are historical; no new global hold, worker start, task acceptance or release readiness is asserted.

### 2026-10-24 — Session 2 checked handoff; native execution blocked

- Separate dossier: [native acceptance / freeze handoff](../evidence/native-acceptance-2026-10-24/HANDOFF.md), [immutable input comparison](../evidence/native-acceptance-2026-10-24/input-comparison.json), [exact single-gate dispatch payload](../evidence/native-acceptance-2026-10-24/demo121-podman-dispatch.json).
- Actual checks: 31 existing Demo helper/cleanup regressions PASS at `f57c8b6e`; 47 existing planning tests PASS. No native PASS is claimed for the current candidate. Historical Podman artifact 12518384969 was downloaded and its SHA256 matches GitHub; it binds Demo `25c31969`, whose longer cleanup budget is incompatible with current #121. Exactly two differing blobs proven by direct 87-vs-87 blob inventory.
- Existing hosted rootless route is available in source and byte-identical at Core C / current develop, but current GitHub MCP lacks workflow dispatch. No configured host/runtime access is available. Marcel requested GitHub MCP; no browser continuation. Concrete authenticated-dispatch request published in [core-923](https://github.com/mcpdev80/baseharbor/issues/923#issuecomment-6386350458) and [Demo #121](https://github.com/mcpdev80/baseharbor-demo/pull/121#issuecomment-6386427876).
- Freeze remains Demo D → Console U → Connector K → Core #1050. Fresh Console #9 / Connector #10 are each ahead 1 / behind 0 main and change only their pin manifest. No current reason requires replacement of Console #9. Repin only after actual predecessor merges. [Coordinator/session 3 handoff](https://github.com/mcpdev80/baseharbor/pull/1050#issuecomment-6386436562) distinguishes source-success jobs from skipped native/browser jobs and requests independent receipt review.
- W1 waits for actual final graph and CI integration, then existing `guided` + `data-capabilities` gates on Docker/rootless Podman cover the required New/Edit/SQL/provider/No/Cancel/data/shared/cleanup journeys. Core C remains `1861ed07888a1ec22c218ca491d23ee54f48e261`. Session 1 retains every merge. No speculative pins, product changes, v0.4.27 changes, worker starts or complete pre-release.
- Shared projections: session 2 renders only the consequences of its own task status/owner, preserves concurrent main, and leaves the preparation card/release/epics to session 3. This is a blocked handoff, not release or native acceptance.


### 2026-10-24 — Owner-assigned native acceptance and consumer freeze (session 2)

- Marcel explicitly lifted the previous stop for this bounded assignment. Owner: Codex session 2 (`d48643e22049`); dedicated local worktree `native-plan`, branch `work/native-acceptance-d48643e`. No old worker/daemon resumed.
- Session 1 owns all product merges, develop integration and shared CI implementation. Session 3 owns independent review and evidence checks. Session 2 publishes only its task and separate `evidence/native-acceptance-2026-10-24/` dossier. Generated-view changes are limited to this claim; subsequent shared projections must be coordinated with session 3, preserving current main.
- Native proof remains pending. W1 Core anchor stays `1861ed07888a1ec22c218ca491d23ee54f48e261`. Final consumer pins follow actual Demo, Console, Connector merges in that order. No acceptance, merge, release, tag, deploy or complete pre-release is authorized here.
- Fresh remote snapshot: Core develop `65aa063e90767c85af976081c100be1817370e67`; Demo #121 `f57c8b6e5ff39d0873df62b26272962765e88d6e`; Console #9 `6017de2845fa3e4e408c69038a0a5bdd7e82cad9`; Connector #10 `e832d5651752121dea9484e18422d3e6459f9a72`.


### 2026-10-24 — W1/journeys prerequisite sync, round 5 (live gh, mission f60; develop `65aa063e`)

- W1 (H-Kette) is provisionally BLOCKED until the ecosystem pins stand on develop (dispatch sheet `evidence/board-2026-10-24/q116-w1dispatchsheet.md`, f54 Tafel). Chain heads re-read live: #1060 `0f3bd169` source independently ACCEPT (o139), prerequisite Policy-PR in work (o140, branch `work/v0.4.26-ci-qualifier-1060`); #1052 `9f715184` r6 correction pushed, independent review running (q123); #1056 `b0abe105` CI green but Codex cmf12 REQUEST_CHANGES (F1/F2), correction chain R'/Q'/H' serialized behind #1060; #1046 `1ec67f8d` source tests pass (q118/cmf10), qualifier serialized after C/D.
- Consumer freeze chain (Demo → Console → Connector → #1050 reconcile) still mid-lane: Demo #121 held at the OWNER/HOST Podman receipt (CX-DEMO121R4); Console #9 and Connector #10 ACCEPT_WITH_NONBLOCKING awaiting the Demo merge and their repins/final pins. The immutable four-consumer pin matrix is therefore not cut and no green v0.4.26 journey run exists (q116 negative evidence).
- No new journey execution is implied or started by this sync; card stays ACTIVE (status unchanged; the W1 wait is documented here, consistent with prior rounds).

### 2026-10-24 — W1/journeys prerequisite sync, round 3 (live gh, mission o127; develop still f3929568)

- W1 journey execution still cannot start, for current chain reasons rather than missing preparation. Appid test-source chain: #1047's gate-plan qualification is MERGED on develop `f3929568`, while #1046 (now head `1ec67f8d`, BEHIND, PR Selected Checks FAIL in [40086275780](https://github.com/mcpdev80/baseharbor/actions/runs/40086275780) on workflow policy/focused-python/source-contracts SUCCESS, PR Selected Checks FAILURE) still needs its develop-fresh rebase/requalification. Pins-data documentation chain: #1056 (now head `32b85d95`) structurally blocked — run [40088680501](https://github.com/mcpdev80/baseharbor/actions/runs/40088680501) shows pr-planner-tests PASS but PR Selected Checks FAIL `coverage-unresolved: scripts/pr-check-runner.py` (PR · Selected Runtime job FAILURE, o118: linear branch vs core752_reviewed_merge_chain; owner decision pending), and #1050 is ordered behind it. OpenBao gate chain: #1060 (now head `6a0d36da`) green [40086442202](https://github.com/mcpdev80/baseharbor/actions/runs/40086442202) (all mkdocs/documentation-audit/pr-planner-tests PASS) but PR Selected Checks FAILURE in the same run, plus Codex-REVIEW REQUEST_CHANGES (4 findings) with its repair running; #1052 (now head `789299a9`, failing [40084607362](https://github.com/mcpdev80/baseharbor/actions/runs/40084607362)) waits for that corrected landing.
- Consumer freeze chain still mid-lane in dependency order Demo → Console → Connector → #1050 reconcile: demo#121 (head `f57c8b6e`, mergeState CLEAN) in review, console#9 (head `6017de28`, CLEAN) and connector#10 (head `e832d565`, CLEAN) follow; the immutable four-consumer pin matrix (C/D/U/K) is therefore not cut. #1050 (head `38896762`, BEHIND) PR Selected Checks FAIL in [40073196114](https://github.com/mcpdev80/baseharbor/actions/runs/40073196114) (coverage-unresolved consumer-pins.json). Final candidate/native receipts for this card remain gated by these merges. No new journey execution is implied or started by this sync; card stays ACTIVE.

### 2026-10-24 — W1 prerequisite sync from live gh (mission o116)

- The W1/journeys CI path still waits on the open PR chain: #1046 (BEHIND, failing [39995102290](https://github.com/mcpdev80/baseharbor/actions/runs/39995102290)) and #1047 (green [40076426268](https://github.com/mcpdev80/baseharbor/actions/runs/40076426268), awaiting Maintainer-lane approval/merge) gate the appid test sources; #1056/#1050 gate the pins-data documentation path consumed by journey validation. No new native journey execution is implied or started by this sync; card stays ACTIVE.

### 2026-10-21 — Public MCP proof and concrete New/Edit fixture preparation

- Fresh public client bootstrap defect is corrected in candidate `f762f4480a2eb6b29ceebb35ae4032cb2ce7288c`, not yet accepted. Actual [39626844187](https://github.com/mcpdev80/baseharbor/actions/runs/39626844187), job119314164799, PASS71.07s proves omitted revision through public propose, exact returned desired intent through Apply, real SQL add, coreless execution, wrong/stale consent refusal and zero owned residuals. Test/package PASS with zero skip/fail; downloaded artifact12357012289 SHA256 `a1c4270ffa109484a94064614cf4f62cffe493497c33db261fd7082f58c9ed12` independently verified.
- Two further bounded corrections remain unaccepted: terminal reader Name delegation restores single No/Cancel/EOF without source/state changes (reviewed source99901ff2); Edit pre-execution refusals retain truthful unchanged state and original error (sourcec6dfb988, including its directly executed existing Guided regression wrapper). No runtime guard or lifecycle engine is relaxed.
- Demo preparation checkpoint `56661ac9372ce0c5aa296f247e5ebb2f48ce54e2` is local-only and reuses existing guided/data-capabilities/MCP gates, adding actual New/Edit SQL/provider/data/shared journeys and a foreign paused sentinel. Nine helper cases and real daemon-free New/Edit No/Cancel/EOF + MCP/CLI Footprint parity PASS; Docker/Podman executions remain unproven. Cleanup source checkpoints bb9eb892/e6ba5b45 are local-only preparation; fourteen ownership/privacy regressions plus actual trap/error-path checks pass, but final native cleanup acceptance is still open. Sentinel verification must run after actual acceptance teardown and before its separate exact-owner removal.
- No claimed max11 resource limit is established by current catalogs; do not carry that unverified figure as a blocker. Additional workload/SQL/sentinel resources must fit the real selected runner. Immutable four-consumer pins, actual Docker/rootless Podman journeys and final candidate evidence remain outstanding.


### 2026-10-21 — Concrete acceptance gaps under the authorized complete-release audit

- core-921 is accepted, while core-922 final documentation integration remains open; this card stays PLANNED/WAITING until that real prerequisite is accepted. Bounded fixture preparation is proceeding under the existing complete-release audit, not an accepted native journey.
- Existing 65 gates do not yet prove real CLI New/Edit/remove/provider-switch/No/Cancel across Docker and rootless Podman. The successful Core MCP native proof covers a real coreless SQL add and conflict safety, not all these journeys.
- Assigned disjoint preparation: Demo guided PTY/no-capability safety plus heavy data-capabilities real SQL/provider-edit journey; strict MCP tool-list/Edit/Footprint parity; ownership-bounded cleanup and redacted diagnostics with independently owned foreign-resource sentinel. Reuse existing gates and production authorities; no fake registry, relaxed guards, or historical consumer PASS.
- Current consumer SHA freeze, actual targeted native executions and complete candidate evidence are still outstanding. No release acceptance is implied.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.\n\n> 2026-10-23 progress (coordinator): develop now 49d396c4 (Q+stepcap merged, C2-final pending #1042); consumer PRs #7/#8 validated against C2 line (q41); W1 matrix sheet ready with live consumer_ref tips (o49).\n

### 2026-10-23 — Owner-assigned preparatory consumer merges (ROLLE: MERGE)

Console [#7](https://github.com/mcpdev80/baseharbor-console/pull/7) and Connector [#8](https://github.com/mcpdev80/baseharbor-node-connector/pull/8) were independently reviewed as preparatory source diffs and merged under the bounded cmx2 Owner assignment. Exact source/merge SHAs, live gates, reused source CI and post-merge verification are recorded in the [merge receipt](../evidence/board-2026-10-23/codex-merge-c7n8-post-review.md). Console main is `e7d1e4a1d603158dece19bbc25a8e267d07cde5e`; Connector main is `7c7093d9671dfaa1aafeb92d62bbe9d074f9f47e`. Connector post-merge Test/Vet/Build run 39996344778 passed.

This is source preparation only. The immutable final four-consumer matrix, pending Console pin in Connector, actual native/browser receipts and independent developer path remain unaccepted. core-923 stays ACTIVE under its existing Flash-Coordinator owner; no claim, dependency acceptance, card completion, release qualification or production activation changes.
