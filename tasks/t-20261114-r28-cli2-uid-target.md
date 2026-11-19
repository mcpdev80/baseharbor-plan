---
id: t-20261114-r28-cli2-uid-target
card_number: "0428-052"
card_short_title: "Add stable target identity"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: review
kanban_lane: review
kanban_summary: "Add stable target identity. Follow the owner working brief, command mapping and code entry index; revalidate current develop and…"
kanban_title: 0428-052 · Add stable target identity
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-uid-environment]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1580]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-uid-target · CLI redesign: Add stable target identity #task #release/v0-4-28 #status/review #view/review #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** coord · **Priority:** high  
    **PR:** [baseharbor#1580](https://github.com/mcpdev80/baseharbor/pull/1580)  
    **Needs:** [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md)  
    <!-- /generated:card -->

STACK (owner-anweisung 2026-11-15): basis-karte = cli2-uid-environment (kette app->env->target, max 3 ebenen); branch am head der basis-lane, gewartet wird nur auf inhalte, nie auf merges; nach basis-anderung: rebasen + hier vermerken — PR #1580 base = lane-0428-uid-environment (retarget 15.11)+


<!-- generated:links -->
**State:** review  
**Release:** v0.4.28  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md)  
**Required by:** [t-20261114-r28-cli2-context-shell](t-20261114-r28-cli2-context-shell.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Owner:** coord  
**Priority:** high  
**PRs:** [baseharbor#1580](https://github.com/mcpdev80/baseharbor/pull/1580)  
**Source:** 
<!-- /generated:links -->

## Goal

Add stable target identity. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Add stable target UID without changing runtime ownership or detaching old data; resolve names to UID via safe migration preserving target and deployment records.

## Entry points and ownership

- Starting points: `internal/deployment/target.go; target identity storage and dedicated tests`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Existing target migration is idempotent; rename preserves UID; collisions fail closed; recovery/legacy references remain functional.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.
