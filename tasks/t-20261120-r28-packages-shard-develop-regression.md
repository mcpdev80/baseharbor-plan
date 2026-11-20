---
id: t-20261120-r28-packages-shard-develop-regression
card_number: "0428-202"
card_short_title: "packages shard red on develop"
type: bug
areas: [ci, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-202 · packages shard red on develop
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-r28-packages-shard-develop-regression · packages shard red on develop #task #release/v0-4-28 #status/planned #view/ready #area/ci #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Finding (measured 2026-11-20, from a lane handoff, re-verified by the coordinator)

The `PR · Go unit · packages` shard is red for every PR that hops onto develop `40cb28c758b0`, and the failing
package is **not** the PR's own code:

- PR #1714 at head `5159192dadeec8335eb401c90fca6614e29048b0`, job `136433151042` (run `44778040176`):
  `--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (`loki_test.go:522` "health must pass
  for a healthy multi-source Loki: perses Loki datasource health client: …"),
  `--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability` (`loki_test.go:586`),
  `--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (`loki_test.go:633` "expected 2 per-source
  queries even on full miss, got 0") and `FAIL github.com/mcpdev80/baseharbor/internal/logs 0.124s`. The PR
  touches only `internal/metrics/**`, which is `ok` in the same log.
- The same PR at the previous base `f5ce95afce1c` had `PR · Go unit · packages` **success** (run `44755545566`),
  so the breakage entered between `f5ce95af` and `40cb28c`.
- Merged in exactly that window: `#1715` (0428-184), `#1716` (0428-182), `#1717` (0428-188), `#1594` (0428-053)
  plus the CI changes `#1721`/`#1722`. `internal/logs` itself last changed on Nov 19 in `c296086ca` (0428-086).
- Cross-check on an unrelated PR: #1645 at head `4abc25ab6772`, job of run `44731562217`, fails the same shard on
  a different package: `FAIL github.com/mcpdev80/baseharbor/internal/identityprovider` (owner field, #1650 - see
  stop rule below), with `internal/metrics` `ok` there.
- Why nobody saw it: develop push runs contain only `Runtime · Docker Core` / `Runtime · Podman Core` (runs
  `44769994971`, `44769994909` = success). The unit shards are PR-only, so a develop-side breakage is invisible
  until a PR hops onto it and pays for it.

## Acceptance

1. `PR · Go unit · packages` runs green at the exact head of any PR whose own diff is inside `internal/metrics` -
   i.e. the `internal/logs` multi-source Loki expectations are satisfied again on develop, with the behaviour, not
   the assertion, fixed.
2. The root cause is named by merge and file: which of `#1715`/`#1716`/`#1717`/`#1594` (or a CI routing change)
   made the per-source selector count become 0, proven by a bisect on develop with the test command and its
   output in the evidence file.
3. The blind spot itself gets a witness line in the evidence file (develop push workflow names vs the PR shard
   names). If closing it needs a `.github/**` change, that need is reported with file:line as a finding for the
   owner - not implemented here.
4. No test is deleted, skipped, or widened to make the shard pass. A green run without the assertion is a second
   defect.

## Boundaries and stops

- Start read-only: build the two revisions and run
  `go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource'` at `f5ce95afce1c` and at `40cb28c758b0`,
  then bisect the merge range.
- Allowed to write: `internal/logs/**` and the producer/selector code those tests exercise
  (`internal/observability/**` read-only first, see below).
- Locked: `internal/metrics/perses_dashboards_valkey.go` and its test (#1714, handoff candidate),
  `internal/observability/registry.go` (0428-078 owner takeover plus 0428-189..194),
  `internal/application/perses_runtime.go` and `internal/metrics/perses_prometheus_datasource.go` (#1684, live
  lane), `internal/identityprovider/**` + `internal/operatorauth/**` + `internal/machine/**` (#1650/#1594/#1615,
  owner is working there). If the root cause sits in a locked file: STOP and report the one line - the owner or
  the owning lane fixes it there.
- `internal/identityprovider` failures inside this shard are NOT this card's work: name them, prove they are a
  different package, and leave them to #1650.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.
