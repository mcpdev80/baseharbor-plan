---
id: t-20261113-r28-grafana-runtime
card_number: "0428-010"
card_short_title: "Launch optional Grafana"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Implement the minimum optional Grafana OSS service declaration and native runtime start/readiness using existing container-asset…
kanban_title: "0428-010 · Launch optional Grafana"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-contract-seam]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261113-r28-grafana-runtime · Launch optional Grafana OSS #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md)  
**Required by:** [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md), [t-20261113-r28-grafana-lifecycle](t-20261113-r28-grafana-lifecycle.md), [t-20261113-r28-grafana-loki-source](t-20261113-r28-grafana-loki-source.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md), [t-20261113-r28-grafana-tempo-source](t-20261113-r28-grafana-tempo-source.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement the minimum optional Grafana OSS service declaration and native runtime start/readiness using existing container-asset conventions. No Grafana is started by an ordinary application. Pin verified version/image digest at implementation. Do not implement datasource, alert, auth or uninstall in this card.

## Acceptance

An explicitly enabled isolated Grafana starts, health is truthful, no default footprint, exact image/version recorded, all owned temporary resources cleaned in tests.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates.
- **Exclusive write ownership:** New isolated internal/grafana/runtime*.go and internal/grafana/assets/** only; do not touch shared CLI registry, serviceaccess, metrics, logs, traces or CI.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

Go renderer/validation and opt-in default-negative tests; selected native Docker/Podman start/readiness smoke.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Binding current-source implementation note (2026-11-13)

Entry points: `internal/provider/builtin/catalog.go` (existing catalog), `internal/capability/integration_contract.go` (validated descriptor), `internal/providerui/application.go` (optional UI lifecycle example), `internal/metrics/prometheus_files.go` + `internal/metrics/prometheus.go` (native service template), `internal/runtime/` (existing runtime provider execution). Implement ONLY contract-compatible optional Grafana bootstrap and readiness. Do not bypass descriptor/registry, invent portable `metrics` capability or touch general provider resolver. If contract seam is not accepted, stop.

Worker must quote current exact Core/Console commit, confirm entry points still exist, and stop with explicit blocker if changed. Codex checks exact source and CI selected gate before merge.
