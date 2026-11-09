---
id: t-20261109-0427-181-upname-entrypoint-hosted-rot
card_number: "0427-181"
card_short_title: "TestUpNameResumes fails in hosted"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: queued
kanban_summary: "TestUpNameResumesThroughCommandEntrypoint fails deterministically in the full hosted matrix on develop-head; it only passes in isolation — cross-test state leakage (shared port + retained bootstrap trust-plane marker) is the nucleus."
kanban_title: 0427-181 · TestUpNameResumes fails in hosted
priority: normal
depends_on: [t-20261108-bughunt-upname-entrypoint-develop-rot]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/42627177914"]
superseded_by: ""
---

## Task Note

- [ ] Make TestUpNameResumesThroughCommandEntrypoint green in the full hosted matrix on a develop-head run (hermetic test or production ordering fix).
Card 0427-172 was closed with an isolation-only PASS; the defect is NOT fixed. Counter-probe: workflow_dispatch of "CI · Source & Quality" on refs/heads/develop at fea92f379 (run 42627177914, job log 2026-11-09T13:48:44Z) fails `--- FAIL: TestUpNameResumesThroughCommandEntrypoint (81.09s)` in cmd/baha deterministically (same line on PR #1500 head runs 42613341749 @12:10:07Z and its rerun attempt @13:26:09Z — 3/3). Failure nucleus: "up NAME with a registered NAME must fail before runtime realization (no Core hered...)" preceded by "bootstrap trust-plane teardown: orphan adoption FAILED (marker kept)" lines from another test in the same package — cross-test state leakage (serving holder on a shared port + retained bootstrap marker) makes the entrypoint guard pass isolated but fail in the full matrix. Required: make the test hermetic (own data root + own ports + no retained trust-plane marker from other tests) OR fix the production ordering the test asserts, so `go test ./cmd/baha/` is green in the full hosted matrix on a develop-head run.
