---
id: t-20261114-r28-cli2-app-interact
card_number: "0428-063"
card_short_title: "Guide app logs exec and urls"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex
kanban_status: wait
kanban_lane: wait
kanban_summary: "Guide app logs exec and urls. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-063 · Guide app logs exec and urls
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1623]
sources: []
blocker: ""
wait_reason: "arbeit gestartet und pausiert: stack-base ist der branch von 0428-057, der run am exakten head ca930ce6 ist rot (17 failure bei 60 checks). gewartet wird auf inhalt von #1615, nicht auf einen merge."
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-app-interact · CLI redesign: Guide app logs exec and urls #task #release/v0-4-28 #status/wait #view/wait #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Codex · **Priority:** high  
    **PR:** [baseharbor#1623](https://github.com/mcpdev80/baseharbor/pull/1623)  
    **Waiting:** arbeit gestartet und pausiert: stack-base ist der branch von 0428-057, der run am exakten head ca930ce6 ist rot (17 failure bei 60 checks). gewartet wird auf inhalt von \#1615, nicht auf einen merge.  
    **Needs:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** Codex  
**Priority:** high  
**PRs:** [baseharbor#1623](https://github.com/mcpdev80/baseharbor/pull/1623)  
**Source:** 
<!-- /generated:links -->

## Goal

Guide app logs exec and urls. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Make app logs/exec/urls guide missing choices, support -c; exec defaults shell and --cmd one command, preserve exit status. Include app-bound service GUI URLs only.

## Entry points and ownership

- Starting points: `cmd/baha/app_logs.go; app_access.go; app_access_urls.go; human_open.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Component filtering, ambiguous/non-interactive behavior, safe quoting, no unrelated URL, verified/unknown accessibility and current remote support.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only findings: [PR evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1623-0428-063-independent-review.md). Draft #1623 `8014d71e` has no exact-head checks and three behavior gaps: `app logs -c` does not filter, `app exec --cmd` does not shell-parse, and child exit status collapses to 1.

## Handoff

Round-1 delivered by w063 (flash): candidate lane-0428-063-cli2-app-interact @ beb2ee5859a8a2ffa07fd5725370275411e27011, draft PR baseharbor#1623 (base cli2-identity-secrets-head). Guided logs/exec/urls over the delivered read view, fail-closed app.logs/app.exec/app.urls authorization; no merge, no ready_for_review. Evidence: evidence/r28-welle1-2026-11-15/cli2-app-interact/round-1.md. CI dispatch belongs to the coordinator.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befunde (independent review 1623): (1) 'app logs -c NAME' parst den component-selector, der ausfuehrungspfad nutzt aber nur options.service — die auswahl filtert NICHT; (2) 'app exec --cmd "echo hi > /tmp/x"' geht als EIN argument an Compose, kein shell-parse, die beworbene syntax funktioniert nicht; (3) preserveWorkloadExitStatus wickelt den kind-exit als presented error ein, cli.ExitCode mappt das falsch — der bewahrte exit-code ist nicht belegt.
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).

PR #1623 draft = kein kandidat (§5.2). rebasen auf die basis, sobald #1615 gruen ist.
