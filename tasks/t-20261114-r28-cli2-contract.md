---
id: t-20261114-r28-cli2-contract
card_number: "0428-049"
card_short_title: "Specify reviewed CLI contract"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Specify reviewed CLI contract. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-049 · Specify reviewed CLI contract
priority: high
depends_on: [t-20261114-r28-cli2-audit-access, t-20261114-r28-cli2-audit-app, t-20261114-r28-cli2-audit-interface, t-20261114-r28-cli2-audit-platform, t-20261114-r28-cli2-audit-wizards]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-contract · CLI redesign: Specify reviewed CLI contract #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-cli2-audit-platform](t-20261114-r28-cli2-audit-platform.md), [t-20261114-r28-cli2-audit-wizards](t-20261114-r28-cli2-audit-wizards.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-audit-access](t-20261114-r28-cli2-audit-access.md), [t-20261114-r28-cli2-audit-app](t-20261114-r28-cli2-audit-app.md), [t-20261114-r28-cli2-audit-interface](t-20261114-r28-cli2-audit-interface.md), [t-20261114-r28-cli2-audit-platform](t-20261114-r28-cli2-audit-platform.md), [t-20261114-r28-cli2-audit-wizards](t-20261114-r28-cli2-audit-wizards.md)  
**Required by:** [t-20261114-r28-cli2-app-export](t-20261114-r28-cli2-app-export.md), [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-app-lifecycle](t-20261114-r28-cli2-app-lifecycle.md), [t-20261114-r28-cli2-app-status](t-20261114-r28-cli2-app-status.md), [t-20261114-r28-cli2-context-shell](t-20261114-r28-cli2-context-shell.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md), [t-20261114-r28-cli2-uid-app](t-20261114-r28-cli2-uid-app.md), [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md), [t-20261114-r28-cli2-uid-target](t-20261114-r28-cli2-uid-target.md), [t-20261114-r28-cli2-wizard-platform](t-20261114-r28-cli2-wizard-platform.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Specify reviewed CLI contract. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Reconcile five audit outputs with owner decisions in the evidence brief. Define exact command grammar/flags, lifecycle rules, environment and app identity model, secure scope, initialization, compatibility, authoritative registration and unresolved owner choices. Update Core specs/contracts through a product PR; do not implement runtime.

## Entry points and ownership

- Starting points: `docs/spec/; contracts/; docs/decisions/; CLI interface and legacy mapping design`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Owner accepts the exact contract or records blockers; every old leaf/flag and sensitive/remote behavior has an agreed destination, no fixed dev semantics; five independent implementation seams and migration/testing matrix explicit.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.
