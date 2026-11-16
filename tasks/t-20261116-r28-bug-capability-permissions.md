---
id: t-20261116-r28-bug-capability-permissions
card_number: "0428-105"
card_short_title: "Scope inferred provider grants"
type: bug
areas: [security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "RabbitMQ is listed as replaceable Compose infrastructure yet Messaging Queue was not preselected; baha app init proposed obj"
kanban_title: "0428-105 · Scope inferred provider grants"
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

- [ ] t-20261116-r28-bug-capability-permissions · Scope inferred provider grants #task #release/v0-4-28 #status/planned #area/security #kind/bug

## Goal

RabbitMQ is listed as replaceable Compose infrastructure yet Messaging Queue was not preselected; `baha app init` proposed `object-storage.s3/v1 runtime.create` for all 12 workload services despite no identified S3 capability. Distinguish a conservative optional toggle from a false detection; avoid universal runtime grants.

## Reproduction (2026-11-16 J-Commerce live test)

Init J-Commerce and inspect queue default, Runtime API operation discovery and list of services allowed to use `runtime.create` including caddy/cadvisor/prometheus.

## Acceptance

- Ensure provider suggestions and default selections are consistent with confidence and show why. Runtime operation grants are least privilege, tied to observed consumers or affirmative explicit selection. No automatic broad permission to unrelated services; negative security tests.
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
