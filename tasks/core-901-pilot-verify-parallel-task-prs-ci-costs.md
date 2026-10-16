---
id: core-901
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: "mcpdev80 (core-901)"
depends_on: [core-893, core-895, core-896, core-900]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#958"]
sources: ["mcpdev80/baseharbor#901"]
source_updated: "2026-10-15T16:47:38Z"
labels: [area/evidence]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/958", "https://github.com/mcpdev80/baseharbor/commit/394e0398fc56137f6009477cd0f878fb2851ce6b", "https://github.com/mcpdev80/baseharbor/actions/runs/38887508335", "https://github.com/mcpdev80/baseharbor/actions/runs/38869216983", "https://github.com/mcpdev80/baseharbor/actions/runs/38882179679"]
---

- [x] core-901 · Pilot: verify parallel task PRs and CI costs #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-901) · **Priority:** not set  
    **PR:** [baseharbor#958](https://github.com/mcpdev80/baseharbor/pull/958)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/958), [proof 2](https://github.com/mcpdev80/baseharbor/commit/394e0398fc56137f6009477cd0f878fb2851ce6b), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38887508335), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/38869216983), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/38882179679)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Owner:** mcpdev80 (core-901)  
**Priority:** not set  
**PRs:** [baseharbor#958](https://github.com/mcpdev80/baseharbor/pull/958)  
**Source:** [baseharbor#901](https://github.com/mcpdev80/baseharbor/issues/901)
<!-- /generated:links -->

## Goal

Qualify the new workflow with necessary regular work and own the before/after documentation.

## Scope

- In scope: two independent small PRs in parallel, one shared-interface or conflict case, cost record.
- Out of scope: extra full matrix for benchmarking; final release evidence (a separately authorized step). This task does not block early independent product work after a qualified PR/review/runner foundation.
- The accepted core-752/#935 and core-910/#934 histories are existing pilot evidence. Analyze them rather than implementing/reproducing an already fixed defect. Establish actual overlap and the shared-interface case from timestamps and supporting PRs; do not assume that two completed PRs prove parallel execution. This gives #750/#751/#754/#766 no new release target.

## Acceptance

- Two independent small PRs in parallel; one case with a shared interface/pre-contract or conflict resolution without overwriting.
- Selection, fail-closed, review, runners and candidate handoff of the predecessor packages are traced together; an independent final review is documented.
- Run/attempt, SHAs, runner, scope, newly run/reused gates, wall time and runner minutes before/after.
- Real savings demonstrated or remaining costs documented honestly; no invented targets.

## Required checks

- Existing green runs and necessary small regular pilot PRs.

## Dependencies and file ownership

- Satisfied: #890, #891, #892, #897, #898, #899 (closed). Open: as listed.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Only new `docs/internal/v0.4.26-parallel-pr-pilot.md`; embed the measurement tables and link original evidence in that Markdown file. No extra unclassified fixture files, CI changes or product implementation edits.
- **Delivered interface/result:** One evidence-backed comparison and explicit limitations, accepted independently of the remaining feature implementations.
- **Task-specific proof:** Use existing runs for #934/#935 and their supporting CI PRs first; collect run/job/attempt, duration and concurrency facts. No extra benchmark run.
- **Boundary:** Do not wait for sessions to send measurements. Fetch logs directly. If history does not establish a criterion, state the gap and use only the next already-required regular run; no synthetic savings.
- **Assignment gate:** the accepted core-893/895/896/900 baseline and existing GitHub API evidence suffice. The trusted documentation-only path already selects the four existing documentation validations and zero release gates for the sole Markdown output. This task does NOT depend on the wizard CI-readiness task or core-894 display cosmetics. It reads existing evidence directly and does not own shared execution files.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer-delegated review ACCEPTED/CLOSED **core-901 — parallel task PR/CI-cost pilot**, product PR #958, squash-merged into develop as `394e0398fc56137f6009477cd0f878fb2851ce6b`. Independently recalculated all executed-job first/last log timestamps in original runs #934 `38869216983` and #935 `38882179679`: approximately 323.838 s (5.40 runner-min) and 186.839 s (3.11 runner-min), peak concurrency 7 and 6 within each run, no overlap between final PR runs. Verified exact tested source SHAs and both `run_attempt=1` through GitHub's run API. Confirmed original docs-CI success at `d2cdd80360ce8176884bbadea851e7d576067de2`; made one coherent documentation correction to state actual attempts, remove a literal colspan artifact and identify zero standard-hosted public-repository compute cost as a tariff inference rather than a measured bill. Corrected head `0139f11992dd1afb525520ba9d910929838de245` passed regular [Actions 38887508335](https://github.com/mcpdev80/baseharbor/actions/runs/38887508335), including all four documentation validations, workflow policy, focused Python and actual `PR Selected Checks` SUCCESS. Runtime/release/legacy broad jobs were skipped. Accept the evidence-backed independent product progress and separately serialized shared CI integration; no unobserved cross-PR CI speedup or counterfactual savings is claimed. Historical negative evidence and deferred core-895 verification remain honest; no new runtime campaign, protection changes, product-main update or release occurred. Earlier review handoff below is historical and superseded by this acceptance.

- 2026-10-16 core-901 review handoff: report PR [baseharbor#958](https://github.com/mcpdev80/baseharbor/pull/958), branch `task/core-901-parallel-pr-pilot`, exact report commit `d2cdd80360ce8176884bbadea851e7d576067de2`; the product diff is only `docs/internal/v0.4.26-parallel-pr-pilot.md`. Regular documentation CI [Actions 38886711992](https://github.com/mcpdev80/baseharbor/actions/runs/38886711992) is SUCCESS: Trusted Plan, Workflow policy, Focused Python, documentation audit, strict MkDocs EN/DE, Pages candidate and actual `PR Selected Checks` passed; runtime/HA/release/candidate/public-contracts and legacy validate paths were not required and were skipped. Existing evidence shows #934 and #935 were file-disjoint product changes and their PR lifetimes overlapped 12 h 52 min 33 s, but neither the early focused jobs nor the final regular CI jobs executed concurrently across the two PRs. Final regular evidence: #934 [Actions 38869216983](https://github.com/mcpdev80/baseharbor/actions/runs/38869216983) used a 2.03 min observed run envelope, 5.40 observed runner-min and at most 7 simultaneous jobs inside that run; #935 [Actions 38882179679](https://github.com/mcpdev80/baseharbor/actions/runs/38882179679) used 1.22 min, 3.11 runner-min and at most 6 simultaneous jobs. Combined observed runner time is 8.51 min. The repository is public and these are standard GitHub-hosted runners, so current standard Actions compute charge is $0 under GitHub's public-repository billing policy; artifact/cache storage, external transfer and developer time were not measured. Historical native timings are context only, not a same-input savings baseline. The shared #935 CI interface was independently integrated through #955 [Actions 38881495869](https://github.com/mcpdev80/baseharbor/actions/runs/38881495869) and then #953 [Actions 38881765634](https://github.com/mcpdev80/baseharbor/actions/runs/38881765634) before the final #935 run, without overwriting either product change. Earlier #934 [Actions 38813614933](https://github.com/mcpdev80/baseharbor/actions/runs/38813614933) retained an unrelated legacy validate failure, and earlier #935 [Actions 38872599405](https://github.com/mcpdev80/baseharbor/actions/runs/38872599405) correctly failed closed on unresolved coverage; neither is presented as a pass. Await independent review/acceptance; do not merge or self-accept.

- 2026-10-16 parallel-readiness correction: removed the non-functional dependency on core-894 (display/summary polish). Pilot evidence can be analyzed on the already accepted execution baseline. Direct GitHub reads confirm #934 opened `2026-10-15T20:31:23Z` and merged `2026-10-16T09:32:18Z`, while #935 opened `2026-10-15T20:39:45Z` and merged `2026-10-16T09:43:11Z`; their PR lifetimes overlap. This is NOT yet proof of simultaneous job execution or a savings claim: the task must inspect job timestamps, changed files and interface/integration histories. Preserve all original acceptance criteria and report gaps honestly. Read existing historical cost references from core-888; no new measurement campaign. The sole Markdown output uses the already integrated documentation CI profile, so it can be completed independently of new wizard checks.

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
