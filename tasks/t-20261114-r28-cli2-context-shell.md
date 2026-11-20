---
id: t-20261114-r28-cli2-context-shell
card_number: "0428-068"
card_short_title: "Terminal-scoped context and"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w068-pr0428-068-context-shell
kanban_status: review
kanban_lane: review
kanban_summary: "Terminal-scoped context and completion. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-068 · Terminal-scoped context and
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-env-registry, t-20261114-r28-cli2-uid-target]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1710]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44695244800"]
---

- [ ] t-20261114-r28-cli2-context-shell · CLI redesign: Terminal-scoped context and completion #task #release/v0-4-28 #status/review #view/review #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w068-pr0428-068-context-shell · **Priority:** high  
    **PR:** [baseharbor#1710](https://github.com/mcpdev80/baseharbor/pull/1710)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44695244800)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md), [t-20261114-r28-cli2-uid-target](t-20261114-r28-cli2-uid-target.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** w068-pr0428-068-context-shell  
**Priority:** high  
**PRs:** [baseharbor#1710](https://github.com/mcpdev80/baseharbor/pull/1710)  
**Source:** 
<!-- /generated:links -->

## Goal

Terminal-scoped context and completion. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement terminal-only app/target/env selection with shell hook and durable one-time completion setup; do not repurpose per-user persisted selection.

## Entry points and ownership

- Starting points: `cmd/baha/target_selection.go; shell_init.go; completion.go; prompt.go; internal/cli/`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Independent simultaneous terminals, explicit flags precedence, shell absent fallback, Bash/Zsh/Fish where supported, installation/update behavior and no-input.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Active owner branch and PR: #1710 at `c379a742e67fc65eb5e3d69670045b32e26e3d46`, based on `develop`. Exact run `44695244800` remains in progress overall at the latest 07:32 UTC poll: 34 jobs, 8 success, 20 skipped, 5 failures and 1 job still running. `PR · Source format`, `cli-gofmt`, Go unit shards `cli-0`, `cli-1` and `cli-3` failed; `cli-2` remained in progress. Workflow policy, Trusted Plan, Native gate plan, focused Python and other completed selected checks passed. Native/runtime, release and contract jobs are skipped. This is not acceptance.

dep-frei nach plan.py show (contract, env-registry, uid-target accepted). Auftragetraegerin muss zuerst das owner-working-brief cli-redesign-20261114/brief.md lesen ( Teil des vertrags ). write-set CLI; app_status_result.go und die perses-pfade sind gesperrt, weil dort 078 und 083/174 schreiben

entscheidung auf ihren befind: KEIN rename von cmd/baha/commands.go (301 zeilen, rootCommand/versionCommand/configuredApplicationCommand + noArgs/noArgsCtx/usageError, zuletzt 1019190d8 durch 0428-084 = zentraler registrierungspunkt mehrerer karten). erlaubt ist nur additive registration in rootCommand(); ihr neuer inhalt kommt in eigene dateien (context_terminal.go, completion_setup.go). verlangt das owner-working-brief den rename, ist das ein contract-befund an mich, kein eigenmachtiger PR

design-entscheidung auf ihre frage: mechanisme = source-barer snippet + einmaliger shell-hook, der das eval selbst aufruft; KEINE marker-datei. grund gemessen: die einzige terminal-identitaet, die ein hook ohne protokoll kennt, ist PID-artig, und PID-reuse laesst ein neues terminal das ziel eines gestorbenen erben = fail-open. zusaetzlich messung ihrer praemisse: cmd/baha/completion.go (250 zeilen, zuletzt 1019190d8/0428-084) hat KEIN export/hook/BASEHARBOR-treffer, BASEHARBOR_TARGET erscheint auf develop fast nur in tests, und in app_context*.go gibt es keine use/clear-subcommands — der kartenteil fehlt also wirklich


## Open-PR sweep reconciliation — 2026-11-20 07:30 UTC

Added live PR #1710 to this active card after direct GitHub REST enumeration identified it as a new open PR. The PR is OPEN and non-draft at exact head `c379a742e67fc65eb5e3d69670045b32e26e3d46` on `develop`, with no formal reviews and no review decision. Exact run [44695244800](https://github.com/mcpdev80/baseharbor/actions/runs/44695244800) is still in progress overall: `PR · Source format` and `PR · Validation · cli-gofmt` failed; `PR · Focused Python`, Workflow policy, Trusted Plan and Native gate plan passed; Go unit shards, go-build and go-vet remained in progress; native/runtime, contract and release gates were skipped. The source-format failure log was not yet available while the run remained active. Keep the task Active under its existing owner; no acceptance or Review transition is established.

## Exact-run terminal result — 2026-11-20 07:34 UTC

Run [44695244800](https://github.com/mcpdev80/baseharbor/actions/runs/44695244800) is now terminal **FAILURE** on head `c379a742e67fc65eb5e3d69670045b32e26e3d46`: 35 jobs, 9 success, 20 skipped, 6 failed. `PR · Source format` and `cli-gofmt` identify `cmd/baha/context_terminal.go` as unformatted. CLI shards also fail: `cli-0` finds `baha context clear` unclassified, `cli-1` reports the unformatted source, and `cli-3` reports command metadata/documentation mismatch; `PR Selected Checks` fails because selected shard coverage is incomplete. PR remains OPEN, non-draft, with no formal review. Task stays Active under its existing owner; fix and rerun required checks before any Review handoff.

ihr PR ist da und war mir noch nicht gemeldet: #1710 'feat(0428-068): additive per-terminal context (use/clear…', head c379a742e67f, base = develop, draft=false, erstellt 07:28:38Z. additiv, wie befohlen: keine umbenennung von cmd/baha/commands.go, eigener inhalt in neuen dateien. karte auf review, abnahme bestelle ich erst, wenn ihre akte den praedenz-nachweis enthaelt (flag > im kommand gesetzte env > terminal-env > default, ein test pro stufe)
