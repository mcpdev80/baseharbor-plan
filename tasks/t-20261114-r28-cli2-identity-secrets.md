---
id: t-20261114-r28-cli2-identity-secrets
card_number: "0428-057"
card_short_title: "Separate human/runtime secret"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w2c3555a6-0428-057
kanban_status: review
kanban_lane: review
kanban_summary: "Separate human/runtime secret authority. Follow the owner working brief, command mapping and code entry index; revalidate…"
kanban_title: 0428-057 · Separate human/runtime secret
priority: high
depends_on: [t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1615]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md"]
---

- [ ] t-20261114-r28-cli2-identity-secrets · CLI redesign: Separate human/runtime secret authority #task #release/v0-4-28 #status/review #view/review #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w2c3555a6-0428-057 · **Priority:** high  
    **PR:** [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
    **Needs:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** v0.4.28  
**Depends on:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Required by:** [t-20261114-r28-cli2-app-data](t-20261114-r28-cli2-app-data.md), [t-20261114-r28-cli2-app-export](t-20261114-r28-cli2-app-export.md), [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-audit-events](t-20261114-r28-cli2-audit-events.md)  
**Owner:** w2c3555a6-0428-057  
**Priority:** high  
**PRs:** [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
**Source:** 
<!-- /generated:links -->

## Goal

Separate human/runtime secret authority. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement configured human authorization for service credential reveal via OpenBao while keeping workload access independent. Prevent unauthorized alternate path via env files, machine output, export and API.

## Entry points and ownership

- Starting points: `internal/openbao/; internal/application/access.go; cmd/baha/app_env.go; app_access.go; secret_operations.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Explicit auth for selected/all reveal, denial, sealed/unavailable behavior, app/env/target isolation, all alternate interfaces and runtime startup; no secret in logs or normal machine output.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)

secret.reveal op + fail-closed human-authorization seam; draft PR #1615 base=cli2-env-policy-head head=cli2-identity-secrets-head 6f0555c44; tests a/b/c/d green; one base-parity failure (git archive OOM, unrelated)
