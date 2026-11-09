---
id: t-20261109-r27-ci-go-shard-reuse
card_number: "0427-185"
card_short_title: "Reuse unchanged green Go shards"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Extend authenticated incremental CI reuse to previously green Go shards only if exact inputs and impact are proven unchanged."
kanban_title: "0427-185 · Reuse unchanged green Go shards"
priority: normal
depends_on: [t-20261109-r27-ci-go-unit-shards]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#1519"]
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-r27-ci-go-shard-reuse · CI: reuse green Go shards when their verified inputs are unchanged #task #release/v0-4-27 #status/planned #view/planned #area/ci #kind/task

## Outcome

Avoid rerunning already-green shard results on successive commits in the same PR when the exact unchanged test coverage is cryptographically/auditably proven. This follows accepted sharding PR [#1519](https://github.com/mcpdev80/baseharbor/pull/1519), not part of its merged proof.

## Boundaries

- Extend existing trusted `scripts/pr-incremental-reuse.py` selection to the new `PR · Go unit · cli-{0,1,2}`, `packages` and `owner` matrix without creating a separate or weaker authority.
- Bind reuse to authenticated previous PR run, immutable previous/current HEAD/integration/base, 24h window, complete prior successful results, unchanged Go test inventory/shard assignment and dependency closure, toolchain, CI controller, fixture inputs and environment.
- Changes to the sharder, command discovery, required-test roster, test harness, dependencies, security policy or CI workflow must invalidate affected reuse; unknown impact or missing proof must execute fresh tests.
- Do not count `skipped` as `success`; keep selected-check aggregation fail closed and preserve native Docker/Podman acceptance and source-impact policy.
- Regression tests for negative paths: changed tests, added test name changing shard, new dependency, untrusted prior run, missing prior artifact, changed plan, stale SHA/branch, changed Go/runner/toolchain, previous red/skipped shard.
- Measure before/after total CI wall-clock duration on representative changes and document exact runs. No self-hosted infrastructure and no release/tag.

## Status

Planned, unassigned. Implement only after PR #1519 is fully integrated into `develop` (merge commit `4d827a55cb115f316c074b2e1d72d077fc577637`).
