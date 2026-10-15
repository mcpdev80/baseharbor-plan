---
id: core-893
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
blocker: "Outstanding conservative selected-gate coverage and immutable Console/Connector candidates for genuinely private consumer gates; targeted Docker/Podman Backup/Restore original evidence is qualified and merged core-896 is not a blocker."
resolution: ""
evidence: []
---

- [ ] core-893 · CI: enforce selected PR checks #task #release/v0-4-26 #status/blocked

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893-interface](core-893-interface-agree-planning-execution-interface.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Required by:** [core-390](core-390-architecture-service-contracts-provider-catalog.md), [core-750](core-750-inspect-source-neutral-findings.md), [core-751](core-751-inspect-no-false-positives-comments-text.md), [core-752](core-752-inspect-reconcile-default-instances.md), [core-754](core-754-mcp-classify-expected-preconditions.md), [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [core-894](core-894-actions-concise-names-clear-results.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Owner:** mcpdev80 (session 1)  
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

- 2026-10-16 (verified core-893 review handoff): **Original authenticated Docker and Podman Backup/Restore evidence QUALIFIED** by GitHub-hosted [Actions 38817134426](https://github.com/mcpdev80/baseharbor/actions/runs/38817134426) using exact current #930 verifier source `60d1368ce485205a4f428a05f529156b78bd4105`, no source reconstruction or rerun of native gates. The job loaded the trusted exact PR plan and original artifacts from [38811852362](https://github.com/mcpdev80/baseharbor/actions/runs/38811852362), verified ZIP digests and canonical manifest candidate `4738671718ed85b8dc539de2dcf3b562ecaea40a`, Demo SHA `85c0db5a6f078c0331e802765d018939caaf07f4`, run/attempt, outcome and cleanup, and printed `QUALIFIED original gate evidence ['atomic/docker/backup-restore', 'atomic/podman/backup-restore']`. Workflow policy and focused negative authenticity/final-verifier tests PASS. **Review only, NOT accepted/mergeable:** Current #930 workflow orchestrator remains conservatively broad under #892; outstanding selected non-Backup/Restore gate coverage and the approved private Console/Connector candidate graph remain unavailable; stable `PR Selected Checks` must remain blocked, not forced green. Latest full #930 Actions [38816826930](https://github.com/mcpdev80/baseharbor/actions/runs/38816826930) was still queued at handoff behind older long-running native checks. #895 required-check ruleset activation remains another session's scope. Implementation branch includes current develop and merged core-896. No merge, release or full pre-release matrix.

- 2026-10-16 (Session 1 current integration handoff): #930 HEAD `60d1368ce485205a4f428a05f529156b78bd4105`, latest develop included, exact PR merge/integration SHA `f90d0ad8533a928080f770c9d145c96b9ebde49c`. GitHub Actions [38816826930](https://github.com/mcpdev80/baseharbor/actions/runs/38816826930) is registered but `pending` with no jobs at handoff; previous native [38814539070](https://github.com/mcpdev80/baseharbor/actions/runs/38814539070) still has Docker and Podman Backup/Restore in progress. The latest code now collects authenticated `required_job_conclusions` (including blocked private consumer checks), verifies them in the final checker, and independently verifies original gate ZIP digest/provenance, run/attempt and canonical executed integration manifest. Focused negative fixtures cover missing/failed/duplicate prerequisites; no unverified gate PASS is possible. Current #930 CI orchestration change still conservatively selects broader required checks; the targeted two-gate pilot must not be reported as full selected coverage or green `PR Selected Checks`. Verified planning automation for this note: [38816599506](https://github.com/mcpdev80/baseharbor-plan/actions/runs/38816599506) PASS; run render/check again after this update. **Remaining:** finish latest exact-source Actions checks, authenticate complete selected coverage, and for genuinely private gates resolve their immutable Console/Connector candidates. #895 protection remains outside this task.

- 2026-10-15T22:xxZ (original authenticated artifact provenance): Actual [Actions 38811852362](https://github.com/mcpdev80/baseharbor/actions/runs/38811852362), run attempt 1, PR head `eee7d2697c4f7ae6f987ef93e63617e15755be5b`, exact Core integration `4738671718ed85b8dc539de2dcf3b562ecaea40a`, Demo source `85c0db5a6f078c0331e802765d018939caaf07f4`. Native Docker and Podman Backup/Restore jobs both completed `success`. Original uploaded artifact digest Docker: `sha256:ad522f89bab66d4f173cbfb215cb89fe0a04ab4d081dd9a2a9e28e7a3ec74b7e`, Podman: `sha256:d7e861cf903634273ca7ce17c51db359f262d964ae94548af4507d2f2fd66a89`. The workflow-level run was later cancelled, and its final required check failed (private candidate prerequisite). **These original artifacts are real but do not constitute a complete PR Selected Checks PASS.** #893 now checks PR-head job/artifact provenance separately from the executed Core integration in the unchanged canonical manifest, and records authenticated unsuccessful prerequisites without dropping independently qualified gate evidence. Exact-current GitHub Actions acceptance remains pending.

- 2026-10-15T22:15Z (Session 1 evidence): develop includes qualified/merged core-896 commit `fb229964dd277700e1c7ec815db42fa19c3ba2bd`. PR #930 now accepts an explicit exact Demo PR source SHA (or resolves Demo main once to an immutable SHA), separately retains the original Demo repository's `baseharbor-core.ref`, and verifies exact executed Core integration in the original atomic manifest. GitHub Actions [38811852362](https://github.com/mcpdev80/baseharbor/actions/runs/38811852362) recorded both Docker and Podman Backup/Restore gate jobs as `success` and produced original Docker evidence, but the required final check failed on an unrelated private-consumer prerequisite under the **broad current gate selection**, and subsequent activity cancelled the workflow: this is NOT a qualified overall PASS. The adapter was corrected to bind GitHub job/artifact provenance to PR head and executed candidate_sha separately; latest implementation HEAD `09d7793b4767760d7517c3816af3fc8e54ded709` is pending re-verification. Coverage of all actual selected gates and authenticated artifacts remains mandatory; full matrix was not invoked. The unapproved Connector candidate `work/v0.4.26-integrations-docs` remains a prerequisite ONLY for gates genuinely consuming private Console/Connector, not for targeted Core+Demo Backup/Restore. No merge/release.

- 2026-10-15 (Session 1): core-896 PR #932 merged into develop at `fb229964dd277700e1c7ec815db42fa19c3ba2bd`; isolation dependency is satisfied, not a remaining blocker. Existing #893 PR #930 includes develop. Targeted PR-only Backup/Restore uses a recorded immutable Demo source commit independent of the release-candidate graph, and the original atomic evidence validates the exact executed integration + Demo SHAs. Connector/Console candidates are required only by gates whose authoritative `dependencies` name them. Pilot [38811852362](https://github.com/mcpdev80/baseharbor/actions/runs/38811852362): Docker Backup/Restore completed with success and uploaded original gate evidence; Podman and complete Selected Checks qualification pending final outcome. No full matrix, merge or release.

- 2026-10-15T20:35Z (issue comment): draft PR #930 head `edc524206ebdcafc53b4b2c47bdb5a0f79f16737`, NOT complete. Run [38802476334](https://github.com/mcpdev80/baseharbor/actions/runs/38802476334) passed trusted PR plan, actionlint/workflow policy, focused Python regressions, exact unmerged core-896 runner fixtures, docs/EN-DE/Pages candidate and exact integration binary + Docker image. The authenticated Actions result adapter blocks missing, stale, failed or forged status and synthesizes no PASS. `scripts/ecosystem_release_pins.py --tag v0.4.26 …` from the trusted base fails with HTTP 404 for `baseharbor-node-connector` ref `work/v0.4.26-integrations-docs`; Demo main pins unrelated Core `f325b93c…`. Therefore `PR Selected Checks` is correctly FAILURE and no qualified Backup/Restore evidence exists. **External handoff required:** an approved immutable v0.4.26 Connector/Console/Demo candidate set matching the integration plus authorized cross-repository read access; then run the targeted Backup/Restore gate and recheck acceptance. Preserve develop commit `bf69ad0a…` (#900) when resuming. Draft PR #936 is a temporary CI pilot for PR #934 (must not be merged).
- 2026-10-15: session 1 took ownership ("preserve the integrated #891/#892 contracts, implement trusted PR planning and fail-closed required check enforcement in the existing CI workflow surface"). Draft PR #930 ("begin fail-closed selected-check enforcement"), head `ca2653cbf5` at snapshot time.


- 2026-10-15T21:xxZ (#893/#910 coordination): The isolated targeted pilot PR [baseharbor#936](https://github.com/mcpdev80/baseharbor/pull/936) was updated to checkout and assert immutable #934 source `574488ba3ae9b3c07ac78e057f7abc5168d69e5a`. It prints `gofmt -d` if formatting fails and executes `TestGuided`, application/contracts, `go vet ./cmd/baha`, and `go build ./cmd/baha`. The pilot is an unmerged, read-only qualification lane, not PR Selected Checks or accepted runtime evidence. The normal `push` pilot event was explicitly enabled for only its isolated validation branch. [Actions run 38813614933](https://github.com/mcpdev80/baseharbor/actions/runs/38813614933) verified exact source `574488ba3ae9b3c07ac78e057f7abc5168d69e5a`: **PASS** for complete Go-file gofmt, focused `TestGuided`, application/contracts, `go vet ./cmd/baha`, `go build ./cmd/baha`, and Workflow policy. General `validate` failed separately in the same run; that unrelated failure is not a green overall workflow nor evidence of #893 selected-check qualification. #893 remains blocked on its own authenticated targeted Backup/Restore prerequisite/selected-check qualification; do not treat this Go pilot as closing #893.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
