---
id: t-20261102-broker-ready3-widen-readiness-grace
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "worker-ornith"
kanban_lane: review
kanban_summary: "The runtime-broker Compose container reaches readiness in time: app apply's /readyz wait no longer times out because the broker…"
kanban_status: review
kanban_title: Widen broker readiness grace to the established healthcheck pattern
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1287"]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1287/merge@6ddef0ff"]
---

- [ ] t-20261102-broker-ready3-widen-readiness-grace · Widen broker readiness grace to the established healthcheck pattern #task #release/v0-4-x #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith  
    **PR:** [baseharbor#1287](https://github.com/mcpdev80/baseharbor/pull/1287)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1287/merge@6ddef0ff)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** worker-ornith  
**Priority:** not set  
**PRs:** [baseharbor#1287](https://github.com/mcpdev80/baseharbor/pull/1287)  
**Source:** 
<!-- /generated:links -->

## Goal

The runtime-broker Compose container reaches readiness in time: app apply's `/readyz` wait no longer times out because the broker container is marked unhealthy before OpenBao (~30s to come up) has initialized.

## Scope

- In scope: `internal/runtimebroker/compose_render.go` `writeHealthcheck` timing (timeout 10s, retries 24, start_period 15s) + matching `internal/runtimebroker/broker_test.go` assertions + this planning card.
- Out of scope: `.github/workflows/*`, other provider files, any product logic outside the four healthcheck timing values. CI coverage binding of the `internal/runtimebroker/` path is already landed (#1264).

## Acceptance

- The four healthcheck values equal interval:5s timeout:10s retries:24 start_period:15s in the rendered broker Compose; no other line of `writeHealthcheck` changed.
- `go test ./internal/runtimebroker/... ./cmd/baha -run Broker|Healthcheck` pass.
- `scripts/pr-gate-plan.py` suite passes.
- PR #1287 `PR Selected Checks` + atomic/docker + atomic/podman lifecycle gates pass; branch mergeStateStatus CLEAN.
- Merge by CODEX-MERGE after CODEX-REVIEW acceptance at the SHA (worker does not self-approve).

## Required checks

- Local: broker + cmd/baha broker/healthcheck tests, pr-gate-plan suite.
- Hosted: PR Selected Checks + atomic docker + podman lifecycle (CI #41447175508, all pass).

## Dependencies and file ownership

- Owned: `internal/runtimebroker/*`.
- Depends on #1264 (runtimebroker CI coverage binding, merged).

## Handoff

- 2026-11-02: Worker completed the product fix on branch `work/broker-ready3-startperiod-grace` (commit 6ddef0ff), opened PR #1287, watched CI to terminal (all gates pass, mergeStateStatus CLEAN). Local tests + pr-gate-plan suite pass. Ready for CODEX-REVIEW/CODEX-MERGE.
- Candidate SHA: 6ddef0ff2b575e9a9a3c4ee1a7bb988a5d1acd86
