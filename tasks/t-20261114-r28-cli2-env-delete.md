---
id: t-20261114-r28-cli2-env-delete
card_number: "0428-055"
card_short_title: "Env deletion lifecycle"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Environment deletion lifecycle. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-055 · Env deletion lifecycle
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-env-delete · CLI redesign: Environment deletion lifecycle #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Required by:** [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md), [t-20261114-r28-cli2-wizard-env](t-20261114-r28-cli2-wizard-env.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Environment deletion lifecycle. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement environment-scoped destruction with impact preview, one Keep data default/Delete data choice, explicit confirmation, auth/audit, preserve global apps, other environments, shared services and node hosts.

## Entry points and ownership

- Starting points: `new environment deletion domain files; cmd/baha/runtime_destroy_impact.go interfaces via coordinator`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Test shared app cross-env protection, ownership unknown fail-closed, recoverability if retain claimed, data delete consent, partial failure and retry; real isolated runtime where required.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.
