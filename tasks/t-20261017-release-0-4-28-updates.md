---
id: t-20261017-release-0-4-28-updates
card_number: "0428-006"
card_short_title: "integrate Renovate updates"
type: maintenance
areas: [release]
release: v0.4.28
version: v0.4.28
release_stage: updates
parent: v0.4.28
owner: ""
kanban_lane: ready
kanban_summary: Complete dependency intake before feature development.
kanban_status: planned
kanban_title: "0428-006 · integrate Renovate updates"
priority: high
depends_on: [t-20261017-release-0-4-28-cleanup]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261017-release-0-4-28-updates · v0.4.28 · Release start: integrate Renovate updates before feature work #task #release/v0-4-28 #status/planned #view/ready #area/release #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md) (v0.4.28)  
**Depends on:** [t-20261017-release-0-4-28-cleanup](t-20261017-release-0-4-28-cleanup.md)  
**Required by:** [console-2](console-2-live-core-adapter-workflow-proofs.md), [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-28-prepare](t-20261017-release-0-4-28-prepare.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md), [t-20261105-r27-test-wire-helper](t-20261105-r27-test-wire-helper.md), [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md), [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md), [t-20261109-r27-ci-go-shard-reuse](t-20261109-r27-ci-go-shard-reuse.md), [t-20261109-r27-local-delta-delivery](t-20261109-r27-local-delta-delivery.md), [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md), [t-20261113-r28-console-docs-closeout](t-20261113-r28-console-docs-closeout.md), [t-20261113-r28-console-live-evidence](t-20261113-r28-console-live-evidence.md), [t-20261113-r28-console-live-inventory](t-20261113-r28-console-live-inventory.md), [t-20261113-r28-console-live-observability](t-20261113-r28-console-live-observability.md), [t-20261113-r28-console-live-recovery](t-20261113-r28-console-live-recovery.md), [t-20261113-r28-console-live-security](t-20261113-r28-console-live-security.md), [t-20261113-r28-console-live-target-wizard](t-20261113-r28-console-live-target-wizard.md), [t-20261113-r28-console-live-wizards](t-20261113-r28-console-live-wizards.md), [t-20261113-r28-console-live-workspace-wizard](t-20261113-r28-console-live-workspace-wizard.md), [t-20261113-r28-console-monitoring-entry](t-20261113-r28-console-monitoring-entry.md), [t-20261113-r28-console-native-journey](t-20261113-r28-console-native-journey.md), [t-20261113-r28-current-contract-inventory](t-20261113-r28-current-contract-inventory.md), [t-20261113-r28-grafana-alerts](t-20261113-r28-grafana-alerts.md), [t-20261113-r28-grafana-contact-routing](t-20261113-r28-grafana-contact-routing.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-dashboard-databases](t-20261113-r28-grafana-dashboard-databases.md), [t-20261113-r28-grafana-dashboard-hosts](t-20261113-r28-grafana-dashboard-hosts.md), [t-20261113-r28-grafana-dashboard-identity](t-20261113-r28-grafana-dashboard-identity.md), [t-20261113-r28-grafana-dashboard-messaging](t-20261113-r28-grafana-dashboard-messaging.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md), [t-20261113-r28-grafana-dashboard-valkey](t-20261113-r28-grafana-dashboard-valkey.md), [t-20261113-r28-grafana-dashboards](t-20261113-r28-grafana-dashboards.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md), [t-20261113-r28-grafana-lifecycle](t-20261113-r28-grafana-lifecycle.md), [t-20261113-r28-grafana-log-trace-dash](t-20261113-r28-grafana-log-trace-dash.md), [t-20261113-r28-grafana-loki-source](t-20261113-r28-grafana-loki-source.md), [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md), [t-20261113-r28-grafana-tempo-source](t-20261113-r28-grafana-tempo-source.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Complete dependency intake before feature development.

## Scope and acceptance

- Immediately inventory all open Renovate PRs, dependency-dashboard entries, grouped updates and lockfile/container/action/toolchain pins in the active BaseHarbor and Demo product repositories; include this plan repository when applicable.
- Process and integrate all applicable pending updates first through product PR review and sufficient targeted checks. Resolve stale bases, conflicts, grouped/superseded PRs and actual failures; then freeze the post-update baseline.
- Never merge unverified or incompatible updates blindly. An update that cannot safely land is an explicit blocker until fixed or the Maintainer explicitly decides its documented exclusion; remaining unresolved updates do not silently count as done.
- Record PRs, merged SHAs, exact checks and any explicit exclusion. Keep subsequent Renovate arrivals in the normal intake; candidate-time changes go back through affected qualification.

## Required checks

Existing trusted dependency/lockfile/build/security/compatibility checks by impact; native tests only for uniquely uncovered risks. No automatic full matrix.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#updates). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
