---
id: t-20261113-r28-grafana-runtime
card_number: "0428-010"
card_short_title: "Provide optional Grafana runti"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Add Grafana OSS as an explicitly enabled, optional installation-owned visualization service using existing Compose/Quadlet pr"
kanban_title: "0428-010 · Provide optional Grafana runtime"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-runtime · Provide optional Grafana runtime #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Outcome and scope

Add Grafana OSS as an explicitly enabled, optional installation-owned visualization service using existing Compose/Quadlet provider/Target realization patterns. Only selected installations use it; no new portable app capability and no automatic addition to minimal applications. Record runtime image by verified digest at implementation time; no guessed version. Cover lifecycle and removal without deleting existing Prometheus/Loki/Tempo data.

## Acceptance

On demand enable/status/disable preserves provider ownership and retention; unavailable runtime fails before mutation; no Grafana is started by default.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory.
- New isolated Grafana runtime module/asset files only. Existing shared CLI registration, gateway and authentication files are reserved for later integration slices.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Source tests for enable/reconcile/remove and no-default footprint, plus exact selected Docker and rootless Podman native lifecycle gates.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
