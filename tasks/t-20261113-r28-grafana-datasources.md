---
id: t-20261113-r28-grafana-datasources
card_number: "0428-011"
card_short_title: "Provision existing telemetry s"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Provision only genuinely existing authorized Prometheus/Loki/Tempo instances into the optional Grafana service using configur"
kanban_title: "0428-011 · Provision existing telemetry sources"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-datasources · Provision existing telemetry sources #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Outcome and scope

Provision only genuinely existing authorized Prometheus/Loki/Tempo instances into the optional Grafana service using configuration as code. Preserve endpoint/CA/mTLS/credential boundaries, provider placement and per-installation ownership. Do not invent collectors, exporters, scrape targets or full access credentials.

## Acceptance

Reconcile/update and deletion of source bindings are idempotent; unavailable or unauthorized source displays no fabricated data; credentials never enter logs or client-side JSON.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime.
- Grafana provisioning assets and narrow adapter only. No changes to general metrics/logs/traces backends or shared CLI wiring.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Declarative source/CA/credentials negative tests and a live Grafana datasource query against the existing provider instances in isolated Docker/Podman.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
