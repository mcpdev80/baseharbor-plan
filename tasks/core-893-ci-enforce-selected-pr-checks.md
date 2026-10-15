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
    **Blocker:** Unresolved CI/security execution impact in trusted #942 coverage plan remains blocking for PR #930; no self-exemption. Scoped positive and negative final-check pilots are qualified; further review of #930 coverage is required.  
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
