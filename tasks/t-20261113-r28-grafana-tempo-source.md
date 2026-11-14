---
id: t-20261113-r28-grafana-tempo-source
card_number: "0428-023"
card_short_title: "Connect Grafana Tempo"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Provision only existing owned/authorized Tempo query endpoint into Grafana with current CA and access policy; no new tracing…
kanban_title: "0428-023 · Connect Grafana Tempo"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-contract-seam, t-20261113-r28-grafana-runtime, t-20261113-r28-grafana-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261114-r28-perses-tempo-source
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md"]
early: true
---

- [x] t-20261113-r28-grafana-tempo-source · Connect Grafana Tempo #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md)  
**Required by:** [t-20261113-r28-grafana-log-trace-dash](t-20261113-r28-grafana-log-trace-dash.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Provision only existing owned/authorized Tempo query endpoint into Grafana with current CA and access policy; no new tracing backend.

## Acceptance

One actual Tempo trace lookup and absent endpoint handling, TLS errors fail closed.

## Dependencies and exclusive file ownership

- Only start implementation once dependencies in frontmatter are accepted and an actual interface is available. Do not wait on independent cards.
- **Owned files:** New Grafana provisioning Tempo files and tests only; no Loki/Prometheus modules.
- No other worker may change these files concurrently. File overlap requires explicit Coordinator serialization before coding.

## Worker instructions (local 256k LLM)

1. Fetch the current exact product head and this task's accepted predecessors. Read only named source paths and their direct tests, not the entire repository or all backlog.
2. Check current behavior before editing. If already delivered, present exact code/test SHA and ask Coordinator to mark the card superseded; do not duplicate.
3. Implement ONLY the Goal in owned files, using the existing Core authority/transport and native provider patterns; do not add a new API, database, custom monitoring engine or provider capability.
4. Add one executable positive and one negative test for the Acceptance, identify exact test -> existing CI check -> path/trigger -> real result. If missing CI routing, hand off to assigned shared CI owner rather than silently skipping.
5. Run the smallest relevant checks and selected native proof where required. Open one limited PR to the product's normal integration branch; hand off head SHA, files, observed test output, exact gate run and unresolved issues.
6. **Worker never reviews/merges. Codex is reviewer and merger** after required green exact-HEAD checks and real negative tests. Coordinator updates task state and schedules up to 5 ready non-overlapping workers; no release/tag authorization.

## Handoff

Unassigned. No code or acceptance evidence yet.

## Binding current-source implementation note (2026-11-13)

Existing Tempo: `internal/traces/tempo.go`, `internal/traces/runtime_retirement.go`, `internal/capability/reference.go`. Verify actual Tempo query endpoint and source-scoped trace access. No new trace source, no fake correlation, no direct Console credentials.

Worker must quote current exact Core/Console commit, confirm entry points still exist, and stop with explicit blocker if changed. Codex checks exact source and CI selected gate before merge.

## Superseded by Owner decision (2026-11-14)

Closed as superseded by [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md). The Owner chose Perses in place of Grafana visualization; historical planning is retained. Alert rule evaluation and contact routing are re-specified rather than presumed to be Perses features. No implementation is asserted.
