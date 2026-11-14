---
id: t-20261114-r28-cli2-audit-platform
card_number: "0428-045"
card_short_title: "Audit platform and target"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: lane-0428-045-r28
kanban_status: active
kanban_lane: active
kanban_summary: "Audit platform and target semantics. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-045 · Audit platform and target
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

- [ ] t-20261114-r28-cli2-audit-platform · CLI redesign: Audit platform and target semantics #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** lane-0428-045-r28 · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md)  
**Owner:** lane-0428-045-r28  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Audit platform and target semantics. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Trace platform/local/remote/target/node/provider/stack, root install destroy, trust/OpenBao and their actual effects. Mark remote unsupported behavior and distinguish Core, target and connector.

## Entry points and ownership

- Starting points: `cmd/baha/target*.go; node*.go; provider*.go; stack*.go; runtime*.go; openbao.go; internal/deployment/`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Produce a per-path impact and recovery map; identify actual target detach versus full-install destruction and exact version-sensitive gaps.

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
