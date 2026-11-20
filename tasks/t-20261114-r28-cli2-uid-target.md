---
id: t-20261114-r28-cli2-uid-target
card_number: "0428-052"
card_short_title: "Add stable target identity"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex-open-pr-sweep-1580
kanban_status: closed
kanban_lane: closed
kanban_summary: "Add stable target identity. Follow the owner working brief, command mapping and code entry index; revalidate current develop and…"
kanban_title: 0428-052 · Add stable target identity
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-uid-environment]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1580]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1580", "https://github.com/mcpdev80/baseharbor/actions/runs/44641180590", "https://github.com/mcpdev80/baseharbor/commit/bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978"]
---

- [x] t-20261114-r28-cli2-uid-target · CLI redesign: Add stable target identity #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-1580 · **Priority:** high  
    **PR:** [baseharbor#1580](https://github.com/mcpdev80/baseharbor/pull/1580)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1580), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44641180590), [proof 3](https://github.com/mcpdev80/baseharbor/commit/bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978)  
    <!-- /generated:card -->

STACK (owner-anweisung 2026-11-15): basis-karte = cli2-uid-environment (kette app->env->target, max 3 ebenen); branch am head der basis-lane, gewartet wird nur auf inhalte, nie auf merges; nach basis-anderung: rebasen + hier vermerken — PR #1580 base = lane-0428-uid-environment (retarget 15.11)+


<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md)  
**Required by:** [t-20261114-r28-cli2-context-shell](t-20261114-r28-cli2-context-shell.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md)  
**Owner:** codex-open-pr-sweep-1580  
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

### 2026-11-20 00:48 CET — PR sweep

- PR #1580 branch `lane-0428-uid-target`, exact head `522af6f4aa5ca1ec2119750be06f84d795612b85` (Draft, base `develop`). The UID migration writer now uses `Config.SaveExpected(expected)`, preserving protected-owner validation, state-file locking, and expected-byte comparison instead of a standalone rename path.
- Added `TestLegacyTargetUIDMigrationRespectsConfigurationLock`: migration fails without changing config bytes while the lock is held, then persists the UID after unlock. `go test ./internal/deployment -count=1` and `git diff --check` pass locally.
- Exact-head Draft CI [44640366511](https://github.com/mcpdev80/baseharbor/actions/runs/44640366511) succeeded on `522af6f4`; Source/Routing and all five Draft Go shards passed (non-draft gates skipped under Draft policy).
- After refreshing the PR description and marking it ready, exact-head full CI [44641180590](https://github.com/mcpdev80/baseharbor/actions/runs/44641180590) completed SUCCESS on `522af6f4`: workflow policy, trusted/native gate plans, source format, all Go shards, `deployment-package-tests`, build, vet, focused Python, and PR Selected Checks passed. The selected Docker lifecycle runtime gate passed; Podman, unrelated native/release and full pre-release jobs were skipped by impact selection.
- Independent read-only review of the full PR against the current base and acceptance found no code blocker. PR #1580 merged with an expected-head guard at exact head `522af6f4`; merge commit [bbc937c8](https://github.com/mcpdev80/baseharbor/commit/bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978). The branch is accepted.

Historical intake note above; see the dated handoff for current implementation and verification state.

test

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand
