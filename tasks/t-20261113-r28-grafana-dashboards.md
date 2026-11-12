---
id: t-20261113-r28-grafana-dashboards
card_number: "0428-012"
card_short_title: "Ship useful Grafana dashboards"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Provision compact default dashboards for installation/Target/application/provider status, resource history, log exploration a"
kanban_title: "0428-012 · Ship useful Grafana dashboards"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-datasources]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboards · Ship useful Grafana dashboards #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Outcome and scope

Provision compact default dashboards for installation/Target/application/provider status, resource history, log exploration and traces where actual labels/data are present. Reuse proven labels; never claim metrics or dimensions not collected. Keep dashboard definitions independently maintained and optional.

## Acceptance

Dashboards render populated panels from actual test series/log/trace signals; absent capabilities show clear no-data rather than fake health; no export of secrets.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-datasources.
- Grafana dashboard JSON and focused fixtures only; no Console UI, collection or runtime authority changes.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Dashboard schema/provisioning validation and one isolated smoke with actual selected datasources.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
