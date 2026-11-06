---
id: t-20261018-r27-management-host
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle5 (w278, entlassen)
kanban_lane: review
kanban_summary: Expose the same existing lifecycle executor on a protected management host with one durable state root and active-writer…
kanban_status: review
kanban_title: "Management: run one durable minimal authority on the selected host"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-lifecycle, t-20261018-r27-journal-wiring, t-20261018-r27-state-owner, t-20261018-r27-team-auth, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1405]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-management-host · Management: run one durable minimal authority on the selected host #task #release/v0-4-27 #status/review #view/review #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w278, entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1405](https://github.com/mcpdev80/baseharbor/pull/1405)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** coord-welle5 (w278, entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1405](https://github.com/mcpdev80/baseharbor/pull/1405)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Expose the same existing lifecycle executor on a protected management host with one durable state root and active-writer ownership. Reconcile the present operator API PostgreSQL/OIDC requirements explicitly: ordinary local use remains no-login and service-free; remote management provisions only its genuine authentication/state dependencies, not an unconditional SQL/Secrets/Identity bundle. Configure least-privilege host/runtime access, persistent service/storage and explicit bootstrap versus attach. Verify installed lifecycle state survives service restart. No HA replica/federation or container socket exposure to clients.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/serve.go; internal/controlplaneruntime/server.go and server_run.go; bounded management-host/service bootstrap files and tests. No other task owns these files concurrently; shared command/contract registrations remain with public-surfaces.

## Required checks

Focused server-config/auth/startup/ownership/restart tests; one isolated service persistence smoke if required. CLI clients use discovery and the accepted host API; no new product-specific transport. No automatic full matrix or self-approved trust exemption.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Entriegelt 2026-11-06: alle vorlaeufer (geraete-lebenszyklus, tagebuch-kette ausnahme: laeuft noch runde-3-basisRefresh) gemergt. Claimbereit.
