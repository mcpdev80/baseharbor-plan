---
id: t-20261113-r28-console-native-journey
card_number: "0428-018"
card_short_title: "Qualify native Console journey"
type: task
areas: [acceptance]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Integrate and update existing browser/native tests, including Console PR #8; do not recreate covered tests. Prove representat"
kanban_title: "0428-018 · Qualify native Console journeys"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-live-inventory, t-20261113-r28-console-live-wizards, t-20261113-r28-console-live-security, t-20261113-r28-console-live-observability, t-20261113-r28-console-live-target-wizard, t-20261113-r28-console-live-workspace-wizard, t-20261113-r28-console-live-recovery, t-20261113-r28-console-live-evidence]
repos: [mcpdev80/baseharbor-console, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-native-journey · Qualify native Console journeys #task #release/v0-4-28 #status/planned #area/acceptance #kind/task

## Outcome and scope

Integrate and update existing browser/native tests, including Console PR #8; do not recreate covered tests. Prove representative real Docker and rootless Podman flow, remote authorized target, OIDC denial, log/terminal, no fixtures and optional Grafana on/off. Use exact immutable source refs and isolated fixtures.

## Acceptance

Both native families execute actual assertions and clean up. Every new test is discoverable and routed to existing CI/develop/release acceptance with exact trigger and result; skipped is not PASS.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-console-live-inventory, t-20261113-r28-console-live-wizards, t-20261113-r28-console-live-security, t-20261113-r28-console-monitoring-entry, t-20261113-r28-grafana-alerts.
- Browser E2E fixtures, CI-selected test wiring and readiness matrix only; no feature implementation. Reviewer Codex checks test evidence before merge.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Source/contract/build + selected native Docker/Podman and browser tests, exact SHA logs. No duplicate workflow or evidence approval chain.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.

## Binding current-code reference

Use existing Console PR #8, `scripts/browser/live-browser.mjs`, `scripts/browser/application-journey.mjs`, and `src/components/live/live-core-view.tsx`. Grafana native proof is separate 0428-030: do not serialize Console on monitoring implementation.

Worker must verify path and source at current exact commit, not assume any pre-existing proof means live readiness. Codex reviews source-specific tests and CI routing.
