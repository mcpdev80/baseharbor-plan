---
id: t-20261114-r28-cli2-final-acceptance
card_number: "0428-071"
card_short_title: "Coordinate final review and"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Coordinate final review and acceptance. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-071 · Coordinate final review and
priority: high
depends_on: [t-20261109-r31-cli-manpage-after-consolidation, t-20261114-r28-cli2-audit-events, t-20261114-r28-cli2-cli-docs, t-20261114-r28-cli2-env-delete]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-final-acceptance · CLI redesign: Coordinate final review and acceptance #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261109-r31-cli-manpage-after-consolidation](t-20261109-r31-cli-manpage-after-consolidation.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-cli-docs](t-20261114-r28-cli2-cli-docs.md), [t-20261114-r28-cli2-env-delete](t-20261114-r28-cli2-env-delete.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261109-r31-cli-manpage-after-consolidation](t-20261109-r31-cli-manpage-after-consolidation.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-cli-docs](t-20261114-r28-cli2-cli-docs.md), [t-20261114-r28-cli2-env-delete](t-20261114-r28-cli2-env-delete.md)  
**Required by:** [t-20261114-r28-cli-command-semantics](t-20261114-r28-cli-command-semantics.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Coordinate final review and acceptance. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Coordinator collects exact-SHA PRs, audit outputs, ownership and CI routing, reviews every slice and merged behavior against owner brief, and submits to Codex/Owner-delegated Maintainer for actual review and merges.

## Entry points and ownership

- Starting points: `planning evidence and coordination only; no shared product files`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

All preceding cards accepted, no silent failure/skips; independently review 154-command migration/flags and safety matrix, real runtime/remote evidence where needed; record merge SHA/checks and remaining blockers. No release/tag authority.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.
