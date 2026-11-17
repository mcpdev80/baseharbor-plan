---
id: t-20261117-docker-loki-ingestion-timeout
card_number: "0428-113"
card_short_title: "Docker Loki Prov ingestion"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Determine whether the Docker observability gate timeout is caused by product behavior, the combined 0428-108/0428-102 candidate,…"
kanban_title: 0428-113 · Docker Loki Prov ingestion
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1677", "https://github.com/mcpdev80/baseharbor/actions/runs/44049176474", "https://github.com/mcpdev80/baseharbor/commit/d144945af13641e5bdb1564f77b807b2d52b81cb"]
---

- [ ] t-20261117-docker-loki-ingestion-timeout · Observability: Docker Loki provider ingestion gate times out #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1677), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44049176474), [proof 3](https://github.com/mcpdev80/baseharbor/commit/d144945af13641e5bdb1564f77b807b2d52b81cb)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-102](t-20261117-hunt-signals-102.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Determine whether the Docker observability gate timeout is caused by product behavior, the combined 0428-108/0428-102 candidate, or the runtime fixture/gate; deliver a minimal fix if source behavior is defective, otherwise record a bounded evidence-backed gate/fixture finding and its owner.

## Scope

- In scope: reproduce and isolate the exact Docker Loki prometheus/workload series-query timeout from run 44049176474 attempt 2; compare exact current source and gate setup; fix the smallest owned product issue if found.
- Out of scope: weakening or skipping the Loki ingestion assertion, broad CI redesign, unrelated security changes, or changing security.go.

## Acceptance

- Explain the repeated failure using source and runtime evidence, distinguishing product behavior from runner/gate setup.
- If product behavior is defective, add a regression that fails before and passes after the fix, preserving the consent negative assertion.
- Record exact SHA -> test/gate -> trigger -> run URL/outcome. Docker must pass; if shared product behavior changes, run the corresponding rootless Podman gate too.
- Keep PR #1677 open until the required runtime gate is green; link its exact closeout evidence.

## Required checks

- Existing Docker observability native gate selected for PR #1677. It passed metrics scraping but failed Loki series query for provider prometheus/workload with context deadline exceeded after 47.2s on retry attempt 2 at exact SHA d144945af13641e5bdb1564f77b807b2d52b81cb.
- Same PR run also passed workflow policy, formatting, Go unit shards, Go build/vet, identity-provider package tests and Docker identity. Local go vet ./..., go test ./internal/application -count=1, and go build ./... passed at that SHA.
- Rerun only the failed native gate after identifying whether the failure was environmental or code-related; use the existing CI selection and do not weaken its assertion.

## Dependencies and file ownership

- Owned files or areas: diagnostic and minimal fix for the Docker Loki provider log-ingestion failure.
- Shared files: coordinate CI workflow/catalog files with their existing owner.

## Handoff

**ZWEIFEL — queued for an independent lane.** Two exact-head executions of PR #1677 at d144945af13641e5bdb1564f77b807b2d52b81cb failed the same Docker Loki series query for prometheus/workload after the metrics scrape passed. The consent refusal in each run was the expected negative-consent assertion. Cause is not established; do not attribute this to #102 without evidence. The exact run has attempt 1 and attempt 2: https://github.com/mcpdev80/baseharbor/actions/runs/44049176474. This lane hands off its next implementation slot to independent ready card 0428-105.
