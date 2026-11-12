---
id: t-20261113-r28-grafana-secure-access
card_number: "0428-013"
card_short_title: "Secure Grafana login"
type: task
areas: [security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Integrate the optional Grafana UI with existing operator identity/trust gateway using its supported auth integration. Keep…
kanban_title: "0428-013 · Secure Grafana login"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-contract-seam, t-20261113-r28-grafana-runtime]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261113-r28-grafana-secure-access · Protect Grafana operator login #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/security #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md)  
**Required by:** [t-20261113-r28-console-monitoring-entry](t-20261113-r28-console-monitoring-entry.md), [t-20261113-r28-grafana-contact-routing](t-20261113-r28-grafana-contact-routing.md), [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Integrate the optional Grafana UI with existing operator identity/trust gateway using its supported auth integration. Keep private listener and forbid anonymous/public admin. Do NOT build a new Core login, roles or identity store. Obtain signed Core/OIDC trust contract before editing.

## Acceptance

One authenticated private Grafana URL, operator-only access enforced by the existing authority, denied paths fail closed, and no unverified public listener.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime.
- **Exclusive write ownership:** Existing serviceaccess/management gateway + narrowly scoped Grafana auth config files exclusively owned by this worker. No UI pages, datasource/alerts, or runtime module writes.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

Positive authorized / negative unauthenticated, forbidden actor, expired token, cross-origin redirect, secret/header log tests with real HTTPS/OIDC selected gate.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Binding current-source implementation note (2026-11-13)

Exact source: `docs/spec/management-access-v1.md`, `docs/spec/provider-management-acceptance-v1.md`, `internal/metrics/management_ui.go`, `internal/providerui/application.go`, `cmd/baha/app_dev_routing.go`. Reuse existing management authentication class/role mapping and Core authority. Grafana auth is not automatically equal to Core OIDC: prove supported Grafana OSS flow and fail closed if role parity cannot be enforced.

Worker must quote current exact Core/Console commit, confirm entry points still exist, and stop with explicit blocker if changed. Codex checks exact source and CI selected gate before merge.
