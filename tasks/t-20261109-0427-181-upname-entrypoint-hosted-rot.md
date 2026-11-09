---
id: t-20261109-0427-181-upname-entrypoint-hosted-rot
card_number: "0427-181"
card_short_title: "TestUpNameResumes hosted rot"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-181-impl
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0427-181 · TestUpNameResumes hosted rot
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1516]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/42627177914", "https://github.com/mcpdev80/baseharbor/commit/d9bf3d94e"]
superseded_by: ""
---

- [x] t-20261109-0427-181-upname-entrypoint-hosted-rot · 0427-181 · TestUpNameResumes fails in hosted #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-181-impl · **Priority:** normal  
    **PR:** [baseharbor#1516](https://github.com/mcpdev80/baseharbor/pull/1516)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/42627177914), [proof 2](https://github.com/mcpdev80/baseharbor/commit/d9bf3d94e)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-181-impl  
**Priority:** normal  
**PRs:** [baseharbor#1516](https://github.com/mcpdev80/baseharbor/pull/1516)  
**Source:** 
<!-- /generated:links -->

## Task Note

Card 0427-172 was closed with an isolation-only PASS; the defect is NOT fixed. Counter-probe: workflow_dispatch of "CI · Source & Quality" on refs/heads/develop at fea92f379 (run 42627177914, job log 2026-11-09T13:48:44Z) fails `--- FAIL: TestUpNameResumesThroughCommandEntrypoint (81.09s)` in cmd/baha deterministically (same line on PR #1500 head runs 42613341749 @12:10:07Z and its rerun attempt @13:26:09Z — 3/3). Failure nucleus: "up NAME with a registered NAME must fail before runtime realization (no Core hered...)" preceded by "bootstrap trust-plane teardown: orphan adoption FAILED (marker kept)" lines from another test in the same package — cross-test state leakage (serving holder on a shared port + retained bootstrap marker) makes the entrypoint guard pass isolated but fail in the full matrix. Required: make the test hermetic (own data root + own ports + no retained trust-plane marker from other tests) OR fix the production ordering the test asserts, so `go test ./cmd/baha/` is green in the full hosted matrix on a develop-head run.
