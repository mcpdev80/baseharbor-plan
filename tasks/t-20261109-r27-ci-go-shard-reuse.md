---
id: t-20261109-r27-ci-go-shard-reuse
card_number: "0427-185"
card_short_title: "Reuse green Go shards"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0427-185 · Reuse green Go shards
priority: critical
depends_on: [t-20261017-release-0-4-28-updates, t-20261109-r27-ci-go-unit-shards]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261109-r27-ci-go-shard-reuse · CI: reuse green Go shards when their verified inputs are unchanged #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261109-r27-ci-go-unit-shards](t-20261109-r27-ci-go-unit-shards.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Outcome

Avoid rerunning already-green shard results on successive commits in the same PR when the exact unchanged test coverage is cryptographically/auditably proven. This follows accepted sharding PR [#1519](https://github.com/mcpdev80/baseharbor/pull/1519), not part of its merged proof.

## Boundaries

- Extend existing trusted `scripts/pr-incremental-reuse.py` selection to the new `PR · Go unit · cli-{0,1,2}`, `packages` and `owner` matrix without creating a separate or weaker authority.
- Bind reuse to authenticated previous PR run, immutable previous/current HEAD/integration/base, 24h window, complete prior successful results, unchanged Go test inventory/shard assignment and dependency closure, toolchain, CI controller, fixture inputs and environment.
- Changes to the sharder, command discovery, required-test roster, test harness, dependencies, security policy or CI workflow must invalidate affected reuse; unknown impact or missing proof must execute fresh tests.
- Do not count `skipped` as `success`; keep selected-check aggregation fail closed and preserve native Docker/Podman acceptance and source-impact policy.
- Regression tests for negative paths: changed tests, added test name changing shard, new dependency, untrusted prior run, missing prior artifact, changed plan, stale SHA/branch, changed Go/runner/toolchain, previous red/skipped shard.
- Measure before/after total CI wall-clock duration on representative changes and document exact runs. No self-hosted infrastructure and no release/tag.

## Release placement and execution order

**v0.4.28: critical, FIRST engineering task after mandatory release-start cleanup and Renovate intake; before Console/backend feature development.** No duplicate 0.4.27 implementation card. The original stable card identifier `0427-185` is retained as required by the board's no-renumber-on-release-move policy. The existing Go shard architecture is already integrated via PR #1519, merge `4d827a55cb115f316c074b2e1d72d077fc577637`.

## Acceptance details

- Extend the **existing** trusted incremental planner and final status gate rather than adding another workflow or test authority.
- Authenticate prior successful individual `cli-0`, `cli-1`, `cli-2`, `packages`, and `owner` shards against exact test inventory, sharding assignment, compiled code, import dependency closure, fixtures, Go toolchain, runner/OS and verified prior PR/base/integration SHAs.
- A change restricted to `internal/stableid/lock_reclaim_unix_test.go` must rerun the affected authority/StableID tests while reusing completed green, unaffected CLI shards. Failed, skipped, pending, cancelled, stale or missing checks must never be reused.
- A modified CLI production dependency, test discovery rule, selected-test list, CI controller or source policy invalidates relevant reuse. Unknown impact fails closed to fresh testing.
- `PR Selected Checks` must accept an authenticated reusable proof for a required shard, not a synthetic green result or a merely skipped job; ensure a missing proof blocks merge.
- Demonstrate positive and negative cases with planner regressions and at least one real PR run comparing CI wall-clock and executed work, preserving Docker/Podman native acceptance selection.

## Status

Planned, unassigned; **highest priority for v0.4.28 immediately after release-start prerequisites**. Planning change only; implementation deferred from 0.4.27 to avoid destabilizing ongoing #1521 validation.
