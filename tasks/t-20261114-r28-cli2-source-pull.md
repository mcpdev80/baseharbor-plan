---
id: t-20261114-r28-cli2-source-pull
card_number: "0428-061"
card_short_title: "Implement guided source pull"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w27-pr1627-0428-061-pull
kanban_status: active
kanban_lane: active
kanban_summary: "Implement guided source pull. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-061 · Implement guided source pull
priority: high
depends_on: [t-20261114-r28-cli2-app-lifecycle, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1752]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-source-pull · CLI redesign: Implement guided source pull #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w27-pr1627-0428-061-pull · **Priority:** high  
    **PR:** [baseharbor#1752](https://github.com/mcpdev80/baseharbor/pull/1752)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-app-lifecycle](t-20261114-r28-cli2-app-lifecycle.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** w27-pr1627-0428-061-pull  
**Priority:** high  
**PRs:** [baseharbor#1752](https://github.com/mcpdev80/baseharbor/pull/1752)  
**Source:** 
<!-- /generated:links -->

## Goal

Implement guided source pull. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Implement app pull with -c selecting sources, actual entire-repository pull and optional --up same domain operation; preview target/env and shared impacts.

## Entry points and ownership

- Starting points: `cmd/baha/app_update.go; app_workspace_git.go; new dedicated pull coordinator`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Dirty/diverged refs, same repo across components/apps, no-git, partial failures and noninteractive safe consent, --up only after successful pull; preview/metadata side effects truthful.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

beide basis-karten geschlossen (0428-059 gemergt, 0428-060 als PR #1747 mergeCommit e6c199e7b7dd). Lane arbeitet auf develop-exakter base, ein PR 'lane-0428-061-sourcepull'; akzeptanz-kriterien einzeln belegt (dirty/diverged/no-git/partial/consent/--up erst nach erfolg/unverified explizit).

active again: previous lane (0428-216-sourcepull) was a documented lane loss; fresh laptop lane dispatched with the card mission (base corrected to develop d1acf3f31a36). Dependencies 0428-059 and 0428-060 are closed/merged, so the card is dep-free.

RUECKGANG MEINER STAND-DOWN: der owner hat ausdrtuecklich klargestellt, dass er #1752 NICHT uebernimmt ('I have made no edits', 'I will not write reserved files without your assignment') und dass die karte w27-pr1627-0428-061-pull als inhaber traegt, waehrend commands.go, die machine registry, .github und die generierten indexes bei den jeweiligen integration-/CI-inhabern bleiben - gemeinsame writes laufen ueber mich. ALSO: w27 arbeitet weiter, in zwei schritten. (1) AGENTS.md wiederherstellen: der +0 -125-fall ist real gegen merge-base d1acf3f31a36 (von mir gemessen, 'git diff --numstat develop..refs/pull/1752/head -- AGENTS.md'), die datein gehoert der lane. (2) die BEIDEN restlichen punkte sind reservierte dateien und werden von mir separat vergeben: die machine_coverage-klassifikation fuer 'baha app pull' (exakter hosted run 44955232402 = completed/failure, required 'PR Draft Go · cli-0', cmd/baha TestMachineCoverageCIRealTreeAndJSONClassification, registration_ci_readiness_test.go:82, 'unclassified command: baha app pull') und die generierten EN/DE-indexzeilen. PR bleibt draft, back=4 gegen develop 513488eeb6d, hop folgt.
