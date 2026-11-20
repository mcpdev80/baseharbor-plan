---
id: t-20261114-r28-cli2-uid-environment
card_number: "0428-051"
card_short_title: "Introduce logical Env identity"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex-open-pr-sweep-1578
kanban_status: closed
kanban_lane: closed
kanban_summary: "Introduce logical environment identity. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-051 · Introduce logical Env identity
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-uid-app]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1578]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1578", "https://github.com/mcpdev80/baseharbor/actions/runs/44637676104"]
---

- [x] t-20261114-r28-cli2-uid-environment · CLI redesign: Introduce logical environment identity #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-1578 · **Priority:** high  
    **PR:** [baseharbor#1578](https://github.com/mcpdev80/baseharbor/pull/1578)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1578), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44637676104)  
    <!-- /generated:card -->

STACK (owner-anweisung 2026-11-15): basis-karte = cli2-uid-app (kette app->env->target, max 3 ebenen); branch am head der basis-lane, gewartet wird nur auf inhalte, nie auf merges; nach basis-anderung: rebasen + hier vermerken — PR #1578 base = lane-0428-uid-app (retarget 15.11)+


<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-uid-app](t-20261114-r28-cli2-uid-app.md)  
**Required by:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md), [t-20261114-r28-cli2-uid-target](t-20261114-r28-cli2-uid-target.md), [t-20261120-trusted-local-operation-grant](t-20261120-trusted-local-operation-grant.md)  
**Owner:** codex-open-pr-sweep-1578  
**Priority:** high  
**PRs:** [baseharbor#1578](https://github.com/mcpdev80/baseharbor/pull/1578)  
**Source:** 
<!-- /generated:links -->

## Goal

Introduce logical environment identity. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## DESIGN-RULING (coordinator 2026-11-15, owner decision B)

OWNER DECISION 2026-11-15: Option B. Environment identity is a dedicated per-target identity record (`environment.json`), NOT a field inside existing deployment-state records. Storage: under the target's state root, one lean versioned record carrying the environment UID plus renameable metadata (name), generated idempotent under lock, reused on checkout, fail-closed on conflict. Deployment-state records stay unchanged. uid-target (#1580) is confirmed built correctly on this basis.
## Scope

Implement shared environment UID and stable renameable metadata independently of app, node, target and deployment; support multiple apps and multiple execution nodes. Define ownership/locking and versioned storage from accepted contract.

## Entry points and ownership

- Starting points: `new internal environment-domain package; internal/deployment/deployment_store.go interfaces by coordination`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Identity uniqueness, concurrent registration, rename stability, shared multiple apps/nodes, migration and no accidental identity recreation or cross-tenant mixing.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Accepted and merged by the Maintainer under the delegated authorization. PR #1578 head `97689a75d54d2b28a04e002ccc3afd202b9d5210` merged to `develop` as `d5c11753ea437495eb2469a02f80b91d788fef4f` on 2026-11-19 23:32:33 UTC.

- Regression: `TestGetEnvironmentConcurrentRegistrationIsAtomic` (package `internal/deployment`), auto-discovered by PR Go unit and `deployment-package-tests`.
- Local verification on the merged candidate: focused concurrency test `-count=30`, `go test ./internal/environment ./internal/deployment -count=1`, matching `go vet`, `go build ./...`, source readability audit, and `git diff --check` passed.
- Exact-head hosted run `44637676104` passed selected Go shards/packages, deployment-package-tests, build, vet, source format, workflow policy, trusted plan, focused Python, and aggregate. Native/runtime/release checks were skipped by impact selection; this change is a local filesystem identity registration fix.
- No release/tag or cross-repository work was involved.
