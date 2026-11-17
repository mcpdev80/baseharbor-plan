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
kanban_lane: planned
kanban_summary: Remove the invalid Prometheus-attributed application workload log source that caused the Docker Loki ingestion gate to query a…
kanban_title: 0428-113 · Docker Loki Prov ingestion
priority: ""
depends_on: [t-20261117-observability-native-gate-bootstrap]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1680]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1680", "https://github.com/mcpdev80/baseharbor/commit/504a8678c2391cb379622fa02c2c8d9769fa192b", "https://github.com/mcpdev80/baseharbor/actions/runs/44057402207", "https://github.com/mcpdev80/baseharbor/actions/runs/44057603711", "https://github.com/mcpdev80/baseharbor/actions/runs/44057705927", "https://github.com/mcpdev80/baseharbor/actions/runs/44049176474"]
---

- [ ] t-20261117-docker-loki-ingestion-timeout · Observability: Docker Loki provider ingestion gate times out #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1680](https://github.com/mcpdev80/baseharbor/pull/1680)  
    **Waiting for prerequisites**  
    **Needs:** [t-20261117-observability-native-gate-bootstrap](t-20261117-observability-native-gate-bootstrap.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1680), [proof 2](https://github.com/mcpdev80/baseharbor/commit/504a8678c2391cb379622fa02c2c8d9769fa192b), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44057402207), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44057603711), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44057705927), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44049176474)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261117-observability-native-gate-bootstrap](t-20261117-observability-native-gate-bootstrap.md)  
**Required by:** [t-20261117-hunt-signals-102](t-20261117-hunt-signals-102.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1680](https://github.com/mcpdev80/baseharbor/pull/1680)  
**Source:** 
<!-- /generated:links -->

## Goal

Remove the invalid Prometheus-attributed application workload log source that caused the Docker Loki ingestion gate to query a stream no runtime emitter can produce, and verify the unchanged application log and consent behavior.

## Scope

- In scope: reproduce and isolate the exact Docker Loki prometheus/workload series-query timeout from run 44049176474 attempt 2; compare exact current source and gate setup; fix the smallest owned product issue if found.
- Out of scope: weakening or skipping the Loki ingestion assertion, broad CI redesign, unrelated security changes, or changing security.go.

## Acceptance

- Explain the repeated failure using source and runtime evidence, distinguishing product behavior from runner/gate setup.
- Add a regression that proves legacy provider logs are pruned and metrics-enabled reconciliation does not recreate them, while preserving metrics and the consent negative assertion.
- Record exact SHA -> test/gate -> trigger -> run URL/outcome. Docker and rootless Podman must pass.
- Keep PR #1677 open until PR #1680 is accepted and its exact runtime evidence is green; link closeout evidence.

## Test binding

- Test binding: normal (auto-discovered).
- Test: internal/application.TestLegacyPrometheusTraceSignalIsReclaimedWithoutMetricsPolicy, automatically discovered by the existing Go package shard. It verifies legacy cleanup, metrics preservation, and no invalid log source recreation with metrics enabled.
- Runtime route: existing observability-acceptance.yml workflow, manually dispatched against the exact PR SHA for Docker; the existing runtime-validation/observability/podman/* push route selects rootless Podman for the same SHA. No new gate or assertion bypass.

## Required checks

- Previous exact PR #1677 run [44049176474](https://github.com/mcpdev80/baseharbor/actions/runs/44049176474) passed metrics scraping but returned zero Loki entries for application-provider/prometheus/workload; source inspection confirmed Prometheus has no runtime log emitter for that symbolic workload target.
- Exact candidate 504a8678c2391cb379622fa02c2c8d9769fa192b: focused regression and full internal/application, internal/observability, internal/metrics tests, go vet ./internal/application, go build ./..., and git diff --check passed locally.
- Ready PR #1680 run [44057402207](https://github.com/mcpdev80/baseharbor/actions/runs/44057402207) completed successfully for workflow policy, source format, selected Go unit shards, build and vet; the native gate matrix was skipped.
- Exact-SHA Docker dispatch [44057603711](https://github.com/mcpdev80/baseharbor/actions/runs/44057603711) and rootless Podman validation push [44057705927](https://github.com/mcpdev80/baseharbor/actions/runs/44057705927) failed before the test at app_observability_acceptance_test.go:34 because ORAS was missing. No Loki assertion ran; preserve both Loki and negative-consent assertions.

## Dependencies and file ownership

- Owned files or areas: diagnostic and minimal fix for the Docker Loki provider log-ingestion failure.
- Shared files: coordinate CI workflow/catalog files with their existing owner.

## Handoff

**ZWEIFEL - returned to the queue; no merge.** Product fix is in PR [#1680](https://github.com/mcpdev80/baseharbor/pull/1680), exact SHA 504a8678c2391cb379622fa02c2c8d9769fa192b. Local targeted/full application, observability, metrics, vet and build checks passed; PR #1680 workflow checks passed. Required runtime evidence is absent: Docker [run 44057603711](https://github.com/mcpdev80/baseharbor/actions/runs/44057603711) and Podman [run 44057705927](https://github.com/mcpdev80/baseharbor/actions/runs/44057705927) failed before test execution because ORAS was not installed (app_observability_acceptance_test.go:34); the ordinary PR native gate matrix was skipped for these internal/application paths. No Loki runtime assertion executed, so the fix is not accepted and PR #1680 remains open. Handoff to 0428-114 for existing CI owner to restore ORAS setup and route this source to both existing observability gates; next free implementation card is 0428-109.
