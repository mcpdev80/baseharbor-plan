---
id: t-20261113-r28-grafana-alerts
card_number: "0428-020"
card_short_title: "Provision Grafana OSS alerts"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Provision real, scoped Grafana OSS alert rules and contact routes; prove failures and no implicit notifications."
kanban_title: "0428-020 · Provision Grafana OSS alerts"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-datasources, t-20261113-r28-grafana-secure-access]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-alerts · Grafana: deliver managed OSS alerting and scoped routing #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Outcome

Complete the Grafana OSS monitoring experience with **real** provisioned alert rules, notification policies and optional operator-configured contact points. Prefer existing OSS alerting; do not invent another alert engine or require any external notification service.

## Scope and boundaries

- Provision a small, useful starter alert set for genuinely collected health, availability and resource signals; keep alert expressions disabled/unavailable when required metrics are absent.
- Preserve one installation/Core authority and per-environment/Target scoping. Alert rules, routing and contact-point lifecycle are installation-owned, versioned and idempotent.
- Bind operator edits to existing policy, authorization and secret storage. Never disclose notification credentials in client JSON, repository, tests or logs.
- Support opt-in delivery configuration, validate URLs and origins, prove safe restart and restore behavior, and distinguish firing/no-data/error states.
- No mandatory Slack/email/webhook destination, no anonymous/public Grafana, no blanket production alert noise, no new portable application contract, no real external spam.

## Acceptance

- On a real authorized source, one bounded threshold crossing fires a Grafana rule with correct status and scoped ownership; normal state clears it.
- Missing/failed datasource, denied actor, invalid destination and forbidden credential disclosure fail closed.
- Contact-point provisioning and update/removal are safe and repeatable; no notification is sent without explicit operator configuration.
- Docker and rootless Podman representative qualification, exact source pins, appropriate alert tests, cleanup and documentation of supported delivery types.

## Dependencies and file ownership

- Depends on accepted data-source and secured Grafana integration; never develop against unfinished branches.
- Own only Grafana alert/routing provisioning assets and dedicated adapter/tests. Do not edit the shared Grafana runtime, datasource files, gateway, Console pages or CI registry (owned by separate tasks).
- The Coordinator assigns this to a free worker only when prerequisites are accepted; max five independent workers total.

## Required checks and CI routing

- Alert provisioning schema, no-data/error/routing/secret-negative tests; one real Grafana OSS alert evaluation in an isolated native fixture.
- Explicitly identify test -> existing selected check/native gate -> source-change trigger -> exact SHA result. No fabricated skip-success or redundant CI pipeline.

## Coordinator / Codex handoff

- Worker claims one task, opens one small PR to the normal product development branch and hands off exact verified results.
- Codex independently reviews and merges only after relevant real checks pass. No worker or Coordinator merges or publishes.
- Coordinator updates planning state after acceptance and dispatches newly unblocked tasks.

## Handoff

Not started. Actual branch, PR, exact checks and test evidence will be attached here.
