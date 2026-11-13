---
id: t-20261109-0427-183-repository-workload-ci-rot
card_number: "0427-183"
card_short_title: "Repository workload CI rot"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: cg-s3
kanban_status: closed
kanban_lane: closed
kanban_summary: The serial repository workload lifecycle suite must run on the current develop merge candidate and fail if any required test is…
kanban_title: 0427-183 · Repository workload CI rot
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52.json", "https://github.com/mcpdev80/baseharbor/blob/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52/.github/workflows/ci.yml#L351-L383"]
---

- [x] t-20261109-0427-183-repository-workload-ci-rot · 0427-183 · Repository lifecycle/compose CI tests fail on develop head #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** cg-s3  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52.json), [proof 2](https://github.com/mcpdev80/baseharbor/blob/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52/.github/workflows/ci.yml#L351-L383)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** cg-s3  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The serial repository workload lifecycle suite must run on the current `develop` merge candidate and fail if any required test is missing, skipped, or failing.

## Scope

- In scope: the five repository lifecycle tests named in the historical intake and the CI selector/assertion that executes them.
- Out of scope: treating transient GitHub Actions run pages as durable evidence or adding a second CI evidence system.

## Acceptance

- All five historically affected tests are selected by the serial `runtime_integration` job on current `develop`.
- The CI assertion requires exact `PASS` for each selected test and both package teardowns, and fails for skips, failures, or missing pass events.
- The durable merge receipt for the reviewed `develop` SHA is recorded; per Maintainer process, it represents CI green and acceptance at merge time.

## Required checks

- The `validate` job runs for non-PR develop events. Its `Run runtime integration tests serially` step selects the historical five tests plus `TestMultiInstanceComposeLifecycleInCI`.
- JSON output validation fails on any `skip` or `fail`, requires exactly one `pass` event for each of the six names, and requires successful package teardown events for both `cmd/baha` and `internal/application`.
- The durable receipt at develop SHA `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52` binds the accepted merge to PR #1522. No ephemeral run URL is used as evidence.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Accepted against current develop SHA `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52`, merged as PR #1522. Durable receipt and source selector/assertion are linked in `evidence`.

## Task Note
Counter-probe (workflow_dispatch on refs/heads/develop d2e225f20, run 42690054408, job "Run runtime integration tests serially", 20:20:2xZ) fails 5 repository lifecycle/compose cells: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI, TestRepositoryComposePinnedWorkloadLifecycleInCI, TestRepositoryComposeWorkloadOnlyLifecycleInCI, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI, TestRepositoryWorkflowRealLifecycle. Same w169/deployment-state family as 0427-181/182 but on the CURRENT develop head — every PR-side go-test run that executes these serial cells is blocked. Nucleus to find: which of today's landed chains (damaged-state 230221700 / app-list 8a2912c62 / reclaim 82c15567c / isolate d9bf3d94e) changed the repository-workload assumptions.

## Owner closure — 2026-11-13

Owner closure: accepted 2026-11-13. The failing develop counter-probe is retained as historical evidence; later integrated PR CI is green. The exact five serial integration test names were not independently reproduced in the retained current run logs, so this closure records Maintainer acceptance/triage and does not claim a rerun of those exact tests.

## Reopened after full v0.4.27 audit — 2026-11-13

Historical develop counter-probe #42690054408 failed five named repository lifecycle tests. The later PR run #43288025038 is green but does not expose an execution record for those exact serial integration tests; the latest develop runtime jobs skipped their native test cells. Keep open until exact tests pass on current develop or are explicitly retired with evidence.

## 2026-11-13 Release qualification handoff

Qualification only: current five named serial repository lifecycle tests must actually execute PASS on exact release candidate or have evidence-backed explicit retirement; generic green shards/selectors are insufficient.

Existing implementation PRs have been retained; do not dispatch development Workers solely on this card. Attach current real checks/proofs and close only after exact-source Owner/Codex acceptance; an unrelated green selector is not native evidence.

## 2026-11-13 Maintainer acceptance — durable merge receipt

- The exact five historical tests are present in the current `develop` runtime selector at `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52`. CI requires each of them to emit exactly one `PASS`; any skip/failure/missing pass fails the job, and both package teardowns must pass. A sixth related lifecycle test is guarded the same way.
- Accepted using the durable merge receipt for PR #1522 at that SHA: `evidence/receipts/commits/1cbfaefe24e19ed6110a0cc68eb8b9b869880e52.json`. Per Maintainer process, the receipt means CI was green and the merge was accepted at that point. Transient CI run records are not used as proof.
