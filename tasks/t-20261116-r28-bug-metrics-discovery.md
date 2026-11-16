---
id: t-20261116-r28-bug-metrics-discovery
card_number: "0428-104"
card_short_title: "Validate metrics source mappin"
type: bug
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Wizard found /metrics from a Bruno file and defaulted to caddy; generated source caddy:8080/metrics is not supported by Comp"
kanban_title: "0428-104 · Validate metrics source mappin"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-metrics-discovery · Validate metrics source mapping #task #release/v0-4-28 #status/planned #area/observability #kind/bug

## Goal

Wizard found `/metrics` from a Bruno file and defaulted to `caddy`; generated source `caddy:8080/metrics` is not supported by Compose evidence (`caddy` ports 80/443). J-Commerce contains Quarkus Micrometer and Spring Boot Micrometer services.

## Reproduction (2026-11-16 J-Commerce live test)

Init original J-Commerce, accept default metrics service and port 8080; inspect generated metrics source `service: caddy`, `path: /metrics`. Compare Quarkus `/q/metrics` and Spring `/actuator/prometheus` configured routes.

## Acceptance

- Metrics discovery binds proven service, internal port and path together; reject or clearly mark unverified endpoints before apply. Support Quarkus/Spring Actuator paths and conventional `/metrics` based on evidence; do not confuse Prometheus backend with application exporter.
- Preserve existing BaseHarbor safety, immutable candidate consent, source ownership and shared-provider isolation. Never bypass preflight or delete foreign resources.
- Include positive/negative regressions and classify baseline-red vs candidate-green.

## Required checks and CI mapping

- Discover all affected existing tests; implement smallest causal regression and register it in existing package tests / PR-gate selection. Prove touched paths select the test and unrelated paths do not trigger unnecessary full native gates.
- Capture exact SHA, test ID, actual CI check/trigger and passing run URL. Where behavior is common to Docker and rootless Podman, produce independent native evidence in existing appropriate integration/release qualification gates. No separate CI framework.
- Reproduction is local user evidence; its observations must be verified in code before declaring a product fix.

## Dependencies and file ownership

- Coordinate shared CLI, wizard, lifecycle and provider files with existing v0.4.28 CLI redesign owners; no competing writes or blanket permissions.

## Handoff

- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
