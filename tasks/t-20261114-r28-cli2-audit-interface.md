---
id: t-20261114-r28-cli2-audit-interface
card_number: "0428-047"
card_short_title: "Audit help and machine Compat"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Audit help and machine compatibility. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-047 · Audit help and machine Compat
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-audit-interface · CLI redesign: Audit help and machine compatibility #task #release/v0-4-28 #status/planned #view/ready #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Audit help and machine compatibility. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Inventory every visible and hidden CLI path, handler-dispatched mode, global/command flags, JSON/MCP/HTTP, completion, shell setup and exit codes against current code, not help alone.

## Entry points and ownership

- Starting points: `cmd/baha/commands.go; completion.go; shell_init.go; machine_coverage.go; mcp*.go; internal/cli/; internal/machine/`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Provide exhaustive old-option-to-target contract evidence including --agents, --no-input, --yes, source/dest and safety-specific non-equivalence, plus machine-interface compatibility.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

## Parallel planning boundary — 2026-11-14

This bounded audit/coordination may proceed while v0.4.27 remains unreleased. Preserve active work and file ownership. Implementation tasks may proceed when their actual technical prerequisites are accepted; coordinate shared files and preserve active work. Release stages retain their own prerequisites.
