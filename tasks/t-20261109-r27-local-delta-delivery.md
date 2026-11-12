---
id: t-20261109-r27-local-delta-delivery
card_number: "0427-187"
card_short_title: "Dirty + OCI delta delivery"
type: feature
areas: [remote, delivery]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Implement the approved local delta delivery, as scoped by issue #1513. Existing snapshot/candidate-ingress and OCI-native…"
kanban_title: 0427-187 · Dirty + OCI delta delivery
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-connection-client, t-20261109-r27-target-policy-presets]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-r27-local-delta-delivery · Remote: dirty source snapshot and OCI delta delivery #task #release/v0-4-27 #status/planned #view/ready #area/delivery #area/remote #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261109-r27-target-policy-presets](t-20261109-r27-target-policy-presets.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement the approved [local delta delivery](../decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md), as scoped by [issue #1513](https://github.com/mcpdev80/baseharbor/issues/1513). Existing snapshot/candidate-ingress and OCI-native transfer primitives must be reused rather than recreated.

## Acceptance

- Developer workstation with dirty and suitable untracked changes can perform `baha app apply` without mandatory commit, push or remote Git credentials.
- Bounded, immutable source snapshot with safe exclusions, integrity hashes, deletions and mode changes. First transfer full; next apply transfers only relevant changes using a chosen established standard rather than inventing an unauthenticated protocol.
- Existing OCI images reused; digest/platform checked; avoid unnecessary layer transfer, rebuilding and restarts.
- Independent workstation -> authenticated Core -> Connector -> Docker/Podman READY, second changed-only apply, update and destroy, preserving Target/App/environment identity, consent and last good deployment.
- Negative trust/tenant, symlink/secret, tamper, source-concurrency, dirty/policy cases; real hosted/native proof and CI mapping.
- Planned and unassigned as of 2026-11-09; no PR, no completion claim. No release/tag.
