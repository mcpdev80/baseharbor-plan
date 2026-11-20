---
id: t-20261114-r28-cli2-app-export
card_number: "0428-065"
card_short_title: "App export and recovery UX"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex-open-pr-sweep-065
kanban_status: active
kanban_lane: active
kanban_summary: "App export and recovery UX. Follow the owner working brief, command mapping and code entry index; revalidate current develop and…"
kanban_title: 0428-065 · App export and recovery UX
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1625]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-app-export · CLI redesign: App export and recovery UX #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-065 · **Priority:** high  
    **PR:** [baseharbor#1625](https://github.com/mcpdev80/baseharbor/pull/1625)  
    **Needs:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** codex-open-pr-sweep-065  
**Priority:** high  
**PRs:** [baseharbor#1625](https://github.com/mcpdev80/baseharbor/pull/1625)  
**Source:** 
<!-- /generated:links -->

## Goal

App export and recovery UX. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Provide guided encrypted app data export choosing eligible code/backups/secret/env/evidence, preserve backup/restore distinction and existing secure-profile export features.

## Entry points and ownership

- Starting points: `cmd/baha/app_backup_restore*.go; app_evidence.go; secure profile export implementation`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Selected scope only, encrypted archive, secrets consent, non-Git/OCI metadata, unavailable sources clearly reported; restore claims tested, no silent unsupported import.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Independent review

Read-only findings: [PR #1625 / 0428-065](../evidence/r28-welle4-2026-11-19/codex-review-wave/1625-0428-065-independent-review.md). Draft head `da7a4e62` has no exact-head checks; managed-secret export is unreachable/unimplemented, no positive authorized-path test exists, and authorization precedes interactive source selection.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

## Independent review 2026-11-19

- Befund (independent review 1625): cmd/baha/app_export.go:273-275 'managedSecretScopePresent' ist HARDCODED (false, nil), collectExportEntries (:279-298) behandelt den fall als leer — der ANGEKUENDIGTE managed-secret export ist nie verfuegbar. Entweder implementieren (mit positivem authorized-path-test) oder aus dem vertrag entfernen.
- Nachweis-Voraussetzung: ein exaktkopf-lauf mit dem geforderten gate; ueber den gestapelten base-ref ist der derzeit nicht ausloesbar (owner-draht ci.yml:14-18, derselbe grund wie #1615).
