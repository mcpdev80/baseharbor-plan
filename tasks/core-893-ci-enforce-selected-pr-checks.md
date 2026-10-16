---
id: core-893
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: mcpdev80 (session 1)
depends_on: [core-893-interface, core-896]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#930", "mcpdev80/baseharbor#936"]
sources: ["mcpdev80/baseharbor#893"]
source_updated: "2026-10-15T20:35:28Z"
labels: [area/evidence]
blocker: "Unresolved CI/security execution impact in trusted #942 coverage plan remains blocking for PR #930; no self-exemption. Scoped positive and negative final-check pilots are qualified; further review of #930 coverage is required."
resolution: ""
evidence: []
---

- [ ] core-893 · CI: enforce selected PR checks #task #release/v0-4-26 #status/blocked #view/blocked #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 1) · **Priority:** not set  
    **PR:** [baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930), [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936)  
    **Blocker:** Unresolved CI/security execution impact in trusted \#942 coverage plan remains blocking for PR \#930; no self-exemption. Scoped positive and negative final-check pilots are qualified; further review of \#930 coverage is required.  
    **Needs:** [core-893-interface](core-893-interface-agree-planning-execution-interface.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893-interface](core-893-interface-agree-planning-execution-interface.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Required by:** [core-390](core-390-architecture-service-contracts-provider-catalog.md), [core-750](core-750-inspect-source-neutral-findings.md), [core-751](core-751-inspect-no-false-positives-comments-text.md), [core-752](core-752-inspect-reconcile-default-instances.md), [core-754](core-754-mcp-classify-expected-preconditions.md), [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [core-894](core-894-actions-concise-names-clear-results.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Owner:** mcpdev80 (session 1)  
**Priority:** not set  
**PRs:** [baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930), [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936)  
**Source:** [baseharbor#893](https://github.com/mcpdev80/baseharbor/issues/893)
<!-- /generated:links -->

## Goal

Existing workflows execute the PR test plan and always deliver a reliable required final check. This is phase 2 (final runtime/evidence integration and acceptance) of [baseharbor#893](https://github.com/mcpdev80/baseharbor/issues/893); phase 1 is core-893-interface.

## Scope

- In scope: capture PRs against develop; generate the real matrix from the plan; fail-closed final check; consume integrated core-896 isolation.
- Out of scope: release, promotion, evidence-verifier semantics, product code.
- Concrete case "Backup/Restore only": split today's monolithic `Source · Contracts · Docs` job as a blanket prerequisite of targeted runtime checks. Separate planning/input verification and provisioning of the exact needed candidate from full source/docs/snapshot checks. A targeted Backup/Restore gate waits only for its real prerequisites: trusted plan, necessary affected checks, verified pins and binary/image artifacts matching the exact candidate. Reuse these artifacts with proven identity, otherwise build them; never present an old binary as a new candidate. Independent required source/docs checks run in parallel or are reused under the verifier policy. A targeted diagnostic run must not become an overall PASS; final PR/release acceptance waits for all required results. V1 may select extra checks conservatively; the fingerprint policy may prevent reuse, so promise no removed lead time.

## Acceptance

- PRs against develop are captured; the actual matrix comes from the plan, not a static wall of skips.
- Planning rules come from a trusted state; a PR cannot exempt itself via markers, labels or policy changes.
- Failures, missing results, improper skips, timeout/cancel block; not-required stays separate from PASS.
- No duplicate expensive PR/push runs without new inputs; re-plan when the integration state changes.
- A necessary small pilot shows that an exclusively selected Backup/Restore test no longer waits on unrelated docs/snapshot checks only because of the combined job.
- Stays open until authenticated runtime evidence and its Backup/Restore pilot pass.

## Required checks

- Workflow policy/syntax and fixtures for empty plan, success, failure, missing result and manipulation; one small regular PR pilot.

## Dependencies and file ownership

- Owns `.github/workflows/ci.yml`, PR planning/execution orchestration, authenticated gate-evidence consumption and `PR Selected Checks`.
- Consumes integrated and qualified core-896. Order fixed by the [2026-10-15 dependency correction](../epics/core-888-development-and-ci.md#binding-dependency-correction--2026-10-15). core-895 follows a qualified status check from this task.

## Handoff

- 2026-10-15T20:35Z (issue comment): draft PR #930 head `edc524206ebdcafc53b4b2c47bdb5a0f79f16737`, NOT complete. Run [38802476334](https://github.com/mcpdev80/baseharbor/actions/runs/38802476334) passed trusted PR plan, actionlint/workflow policy, focused Python regressions, exact unmerged core-896 runner fixtures, docs/EN-DE/Pages candidate and exact integration binary + Docker image. The authenticated Actions result adapter blocks missing, stale, failed or forged status and synthesizes no PASS. `scripts/ecosystem_release_pins.py --tag v0.4.26 …` from the trusted base fails with HTTP 404 for `baseharbor-node-connector` ref `work/v0.4.26-integrations-docs`; Demo main pins unrelated Core `f325b93c…`. Therefore `PR Selected Checks` is correctly FAILURE and no qualified Backup/Restore evidence exists. **External handoff required:** an approved immutable v0.4.26 Connector/Console/Demo candidate set matching the integration plus authorized cross-repository read access; then run the targeted Backup/Restore gate and recheck acceptance. Preserve develop commit `bf69ad0a…` (#900) when resuming. Draft PR #936 is a temporary CI pilot for PR #934 (must not be merged).
- 2026-10-15: session 1 took ownership ("preserve the integrated #891/#892 contracts, implement trusted PR planning and fail-closed required check enforcement in the existing CI workflow surface"). Draft PR #930 ("begin fail-closed selected-check enforcement"), head `ca2653cbf5` at snapshot time.


- 2026-10-15T21:xxZ (#893/#910 coordination): The isolated targeted pilot PR [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936) was updated to checkout and assert immutable #934 source `574488ba3ae9b3c07ac78e057f7abc5168d69e5a`. It prints `gofmt -d` if formatting fails and executes `TestGuided`, application/contracts, `go vet ./cmd/baha`, and `go build ./cmd/baha`. The pilot is an unmerged, read-only qualification lane, not PR Selected Checks or accepted runtime evidence. The normal `push` pilot event was explicitly enabled for only its isolated validation branch. [Actions run 38813614933](https://github.com/mcpdev80/baseharbor/actions/runs/38813614933) verified exact source `574488ba3ae9b3c07ac78e057f7abc5168d69e5a`: **PASS** for complete Go-file gofmt, focused `TestGuided`, application/contracts, `go vet ./cmd/baha`, `go build ./cmd/baha`, and Workflow policy. General `validate` failed separately in the same run; that unrelated failure is not a green overall workflow nor evidence of #893 selected-check qualification. #893 remains blocked on its own authenticated targeted Backup/Restore prerequisite/selected-check qualification; do not treat this Go pilot as closing #893.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.


## Core-893 trusted #942 coverage integration — 2026-10-16

- **#896 is already qualified and merged:** PR #932 via develop commit `fb229964dd277700e1c7ec815db42fa19c3ba2bd`. No outstanding runner-isolation dependency.
- **Current core-893 source:** PR [#930](https://github.com/mcpdev80/baseharbor/pull/930), exact head `a4d1c2b0a45910c732939ae5389a6df2e4d4ab4c` at positive/negative pilot setup (newer task commits must be tracked separately). Trusted #942 coverage contract merged in develop at `14d864dfd38801a56e54901ea520f3b02db134b2` and incorporated into #930. For its own CI/runtime/verifier diff, the trusted planner reports `coverage_status=unresolved` with per-file reasons and `selected_gates=[]`; the **actual PR Selected Checks correctly FAILS** rather than fabricating a full-release matrix or a PASS: [Actions 38822308902](https://github.com/mcpdev80/baseharbor/actions/runs/38822308902).
- **Positive complete-path independent pilot:** Staged trusted integration branch `pilot/core-893-trusted-base` was derived from #930 and only adjusted the PR base name for the standalone pilot (never merged into develop). Child [PR #943](https://github.com/mcpdev80/baseharbor/pull/943) changes README prose only. The trusted #942 planner produced **resolved** coverage, `selected_gates=[]`, and four named required documentation validations. On exact head `bf887413ab33b8f9df0ed8e6c8fd03878431d4a0`, GitHub-hosted [Actions 38822478991](https://github.com/mcpdev80/baseharbor/actions/runs/38822478991) executed Workflow policy, Trusted Plan, Focused Python, `documentation-audit`, strict MkDocs EN, strict MkDocs DE, and non-deploying Pages candidate; all **PASS**. Its real always-running **`PR Selected Checks` completed SUCCESS**. Candidate/runtime gates were not run because none were selected; no fake native evidence.
- **Negative complete-path independent pilot:** Same trusted staging base, [PR #944](https://github.com/mcpdev80/baseharbor/pull/944), exact head `6eaae0d24d3b6cd18a819b1b6ea0e949c65adb75`, introduces an unclassified CI path. GitHub-hosted [Actions 38822585616](https://github.com/mcpdev80/baseharbor/actions/runs/38822585616) executed Trusted Plan, Workflow policy, Focused Python, and all 3 independently required CI validations successfully, while the real **`PR Selected Checks` completed FAILURE** with `BLOCKED: coverage-unresolved: CI execution/evidence impact requires specific qualification: scripts/ci-unclassified-negative-fixture.txt`. This proves policy cannot be bypassed by passing validations.
- **Already authenticated native gate evidence:** Real original Docker and Podman Backup/Restore receipts from [Actions 38811852362](https://github.com/mcpdev80/baseharbor/actions/runs/38811852362) were independently digest/provenance/candidate/Demo/run/attempt/cleanup verified by [Actions 38817134426](https://github.com/mcpdev80/baseharbor/actions/runs/38817134426). These receipts qualify the specific Core+Demo gates only; the release candidate graph and any required private Console/Connector edges remain unchanged and required only for gates that consume them.
- **Acceptance boundary:** This validates the complete planning → required-validation execution → authenticated actual-job results → required final check for zero-native-gate scoped PRs, including blocking negative cases. It is **not** acceptance of #930's unresolved CI/runtime/evidence impact. Any coverage-policy resolution must be explicit and independently reviewed in the trusted #892/#942 authority; no #930 self-exemption, automatic 65-gate matrix, merge, protection activation or release.


## Core-893 executor gap closure — exact proof (2026-10-16)

- **Task PR #930 exact verified head:** `7a27acdd92c8edca431772414e541f4baa53a15a`, separate from the disposable staging pilot. The previously truncated `scripts/pr-selected-runtime-matrix.py` now returns **every** selected supported native Docker/Podman gate; the workflow's `strategy.max-parallel: 2` limits concurrency only. Exact-source `test_three_native_gates_all_scheduled_with_bounded_parallelism` proves three gates remain in the matrix rather than a two-gate subset. Unsupported required gates are NOT declared successful, remain in the original selected list and block final acceptance.
- **Original existing public-contracts owner, not a synthetic PASS:** `integration/static/public-contracts` is executed by `python3 scripts/pre-release-integration.py --gate integration/static/public-contracts` on the exact synthetic Core candidate via an unprivileged GitHub-hosted `PR · Public Contracts` job. It uploads the owner-produced `baseharbor.pre-release.integration-evidence/v1` archive. The existing `scripts/pre-release-resume.py` archive/digest and canonical manifest validator authenticates the exact gate, PR head, run/attempt, integration SHA, immutable Demo origin, successful outcome and skipped static cleanup. Authentic API job result `PR · Public Contracts` is also a required final prerequisite. Missing, failed, stale, duplicate, tampered or unverified results are rejected by focused tests; the final check never synthesizes success.
- **Executed end-to-end public-contracts positive pilot:** disposable scoped [PR #946](https://github.com/mcpdev80/baseharbor/pull/946), exact head `b8e15cd684694f02ba452f55d481b08edd9f84fa`, trusted staging base `91ac892c909bda8fdd5bb9d1360c852be9f7df27`; only contracts Go test comment is changed by the tested PR. [GitHub Actions run 38824698862](https://github.com/mcpdev80/baseharbor/actions/runs/38824698862) **SUCCESS**: Trusted Plan PASS (selected `integration/static/public-contracts`), Workflow policy PASS, Focused Python PASS, required `source-contracts` validation PASS, `PR · Demo Pin` PASS, `PR · Public Contracts` PASS (real owner), and actual `PR Selected Checks` **SUCCESS** after authenticating the original owner artifact. Original artifact `pre-release-integration-static-public-contracts-evidence-38824698862-1` has GitHub SHA-256 `sha256:ed7ce3de6861feda114295d5a608026303761cd3447473a7ee2ade26afc92b17` and authenticated origin run `38824698862` / PR head `b8e15cd...`. This pilot is **not** a merge candidate and does not qualify #930's own unresolved self-impact.
- **Diagnosed corrective replay, no blind push churn:** The first scoped [run 38824317869](https://github.com/mcpdev80/baseharbor/actions/runs/38824317869) executed the public-contracts owner successfully but correctly failed final acceptance because the workflow's `git show` still loaded the old evidence verifier, despite updating `git fetch`. Only that exact pinned `git show` was corrected, then the successful run above qualified the whole owner/evidence/final path. #930's [run 38824558828](https://github.com/mcpdev80/baseharbor/actions/runs/38824558828) passed trusted plan, workflow policy and exact-source Python regression tests; its final check intentionally remained failed due trusted `integration_sha_mismatch`: the GitHub synthetic merge parent belonged to a newer develop commit than the PR event's claimed target base. Do not reinterpret this as passing self-impact.
- **Remaining independent coverage decision:** The merged #942 trusted policy marks the central `.github/workflows/ci.yml`, selected-runtime orchestration and security/evidence verifier changes of PR #930 as `coverage_status=unresolved`, with explicit file reasons. Independently review whether specific CI changes require targeted additional gates/validations and document the exact independently justified scope in the **trusted policy authority**, not within PR #930. No blanket allowlist for this PR, no invented PASS, no full 65-gate release matrix, no reuse of unrelated original native evidence. For gates genuinely consuming Console/Connector, the approved immutable candidate graph remains a prerequisite; Core+Demo Backup/Restore does not inherit that blanket dependency. The separate intentionally **negative** scoped [PR #944](https://github.com/mcpdev80/baseharbor/pull/944) and [Actions 38822585616](https://github.com/mcpdev80/baseharbor/actions/runs/38822585616) continue to demonstrate actual fail-closed unresolved coverage. Do not accept #930 as mergeable until its own resolved coverage and required evidence qualify.


### Exact production workflow helper-pin correction (2026-10-16)

- **Final core-893 PR #930 head:** `b0acfc32ddf4d940294a43f98db4618d3aba83cd` (Draft; NOT accepted). Independent review showed `ci.yml` still pinned `scripts/pr-selected-runtime-matrix.py` at `b4a6f35ab0fb06208a480a50040947888ba3164d`, which applied `supported[:capacity]` and silently omitted a third supported selected gate. Fixed the **production `git show` pin**, not merely the helper source: new immutable helper revision `45500525aa65957a22e6076ac28fe5cb6c6f9610`. `max-parallel: 2` remains the ONLY concurrency cap; all selected supported native gates are scheduled and missing results block final acceptance.
- **All six pinned helpers audited byte-for-byte:** `pr-check-runner.py`, `pr-gate-dependencies.py`, and `pr-verified-atomic-evidence.py` matched current source. Three mismatches were corrected: `pr-selected-runtime-matrix.py`, `pr-authenticated-results.py`, and `pr-required-final.py`. The latter two corrections preserve authentication of failed, missing and stale required results.
- **Workflow-selected production helper regression:** the new exact-source `test_actual_workflow_pinned_helper_schedules_all_three` reads the SHA directly from production `.github/workflows/ci.yml`, fetches and executes the exact `git show SHA:scripts/pr-selected-runtime-matrix.py` implementation with three selected supported gates, asserts that ALL three appear in the output, and confirms `max-parallel: 2`. The initial [Actions 38825721851](https://github.com/mcpdev80/baseharbor/actions/runs/38825721851) found a test-only regex-escaping error (Focused Python FAIL), diagnosed and corrected without changing scheduling policy. On [Actions 38825819114](https://github.com/mcpdev80/baseharbor/actions/runs/38825819114), Trusted Plan PASS, Workflow policy PASS and **Focused Python PASS**, including the production-pin regression. The overall `PR Selected Checks` remains governed by unresolved CI self-impact and is NOT claimed successful.
- **Prior original evidence preserved:** [Public Contracts Actions 38824698862](https://github.com/mcpdev80/baseharbor/actions/runs/38824698862) SUCCESS with authentic canonical owner artifact and real final PASS on the independent scoped pilot. The intentionally negative [Actions 38822585616](https://github.com/mcpdev80/baseharbor/actions/runs/38822585616) is clearly labelled a fail-closed negative pilot. No unrelated native gate reruns or full release matrix.
- **Required independent coverage decision remains OPEN:** merged trusted #942 planner marks PR #930's central CI/runtime/evidence self-modifications `coverage_status=unresolved`. A separate authorized reviewer must justify a targeted coverage scope under trusted policy; PR #930 cannot self-exempt or claim merge readiness. No merge or protection activation.


### Trusted coverage accepted; exact new PR integration (2026-10-16)

- Independent policy PR [#947](https://github.com/mcpdev80/baseharbor/pull/947) was accepted and integrated on `develop` at `7240c701d09f3658209733433c41c06f941b55c9`. Immutable reviewed #930 source `b0acfc32ddf4d940294a43f98db4618d3aba83cd` and original trusted merge-base `14d864dfd38801a56e54901ea520f3b02db134b2` are unchanged. No merge from develop into #930.
- Temporary pilot [#948](https://github.com/mcpdev80/baseharbor/pull/948) CLOSED without merge, retaining successful policy pilot [Actions 38827731872](https://github.com/mcpdev80/baseharbor/actions/runs/38827731872), including planner/diff, workflow policy, actionlint and isolation.
- First #930 reopened PR event [Actions 38827977345](https://github.com/mcpdev80/baseharbor/actions/runs/38827977345) was rejected: stale `BASE_SHA=14d864df...` and reused `INTEGRATION_SHA=0276b228...`; this is NOT eligible evidence. The PR base was refreshed via a temporary ref exactly at `7240c701...` and restored to develop WITHOUT changing #930 head.
- **Fresh eligible PR event** [Actions 38828055047](https://github.com/mcpdev80/baseharbor/actions/runs/38828055047) now reports `BASE_SHA=7240c701d09f3658209733433c41c06f941b55c9`, `HEAD_SHA=b0acfc32ddf4d940294a43f98db4618d3aba83cd`, and fresh `INTEGRATION_SHA=d9220ea70a2333be2cf1fcfd7898d4ec5c1839a9`. Trusted Plan PASS selected only public-contracts and Docker/Podman backup-restore, all mandatory validations. Original provenance/final-check outcomes must still be inspected; no result is pre-accepted.
