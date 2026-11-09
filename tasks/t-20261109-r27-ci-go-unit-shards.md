---
id: t-20261109-r27-ci-go-unit-shards
card_number: "0427-184"
card_short_title: "Parallel impacted Go tests"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-ci-owner"
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: "0427-184 · Parallel impacted Go tests"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1519]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-r27-ci-go-unit-shards · CI: split slow Go tests and wire impact selection #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** chatgpt-ci-owner · **Priority:** normal  
    **PR:** [baseharbor#1519](https://github.com/mcpdev80/baseharbor/pull/1519)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-ci-owner  
**Priority:** normal  
**PRs:** [baseharbor#1519](https://github.com/mcpdev80/baseharbor/pull/1519)  
**Source:** 
<!-- /generated:links -->

## Problem

PR `go-unit-tests` runs `go test ./...` serially: `cmd/baha` alone took about 494 seconds in run 42674227560, and mandatory owner/node tests run afterwards. This takes longer than the already parallel hosted native Docker/Podman jobs.

## Acceptance

- The trusted impact planner remains authoritative. Narrow changes execute only selected package/CLI checks; ambiguous changes retain fail-closed or full conservative test selection. Do not run every Go test for every PR.
- For selected `cli-package-tests`, run three deterministic isolated CLI shards. For selected `go-unit-tests`, run those plus all other Go packages and all nine named mandatory owner/node regressions.
- Every discovered CLI Test/Example/Fuzz is mapped to exactly one CLI shard for the same SHA; no missing named tests, no zero-test green and no required SKIP treated as PASS.
- Each shard runs on GitHub-hosted `ubuntu-latest` with its own ephemeral PostgreSQL and cleanup; no self-hosted runner and no changes to the existing native Docker/Podman release qualification.
- `PR Selected Checks` accepts only success of the selected shard matrix; skipped or failed required jobs cannot become green. Existing check executor regressions and workflow policy pass.
- Capture exact-head PR CI on [#1519](https://github.com/mcpdev80/baseharbor/pull/1519), actual full-shard execution and before/after wall-clock durations; close only after observed PASS and safe integration.

## Implementation status 2026-11-09

- [PR #1519](https://github.com/mcpdev80/baseharbor/pull/1519) proposes deterministic Go test sharding, per-shard DB fixtures, trusted PR selection and fail-closed final aggregation.
- CI evaluation on current head is still pending; no release, tag or acceptance claimed.
- Only this CI optimization is owned here; remote/enrollment #1473, policies #1514 and Greenfield #1503 remain independently owned.
