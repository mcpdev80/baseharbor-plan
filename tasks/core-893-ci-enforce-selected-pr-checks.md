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
blocker: "No approved immutable v0.4.26 Connector/Console/Demo candidate set matching the integration exists; the pin resolver returns 404 for the Connector ref, so no qualified Backup/Restore gate evidence can be produced (also waits for core-896)."
resolution: ""
evidence: []
---

- [ ] core-893 · CI: enforce selected PR checks #task #release/v0-4-26 #status/blocked #view/blocked #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 1) · **Priority:** not set  
    **PR:** [baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930), [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936)  
    **Blocker:** No approved immutable v0.4.26 Connector/Console/Demo candidate set matching the integration exists; the pin resolver returns 404 for the Connector ref, so no qualified Backup/Restore gate evidence can be produced (also waits for core-896).  
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
