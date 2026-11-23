---
id: t-20261114-r28-cli2-app-status
card_number: "0428-062"
card_short_title: "Unify app status and versions"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Coordinator (auto-merge be5c6c890) / f0f6c8b4 hop + 043d rework receipts
kanban_status: closed
kanban_lane: closed
kanban_summary: "Unify app status and versions. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-062 · Unify app status and versions
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1614]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1614"]
---

- [x] t-20261114-r28-cli2-app-status · CLI redesign: Unify app status and versions #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Coordinator (auto-merge be5c6c890) / f0f6c8b4 hop + 043d rework receipts · **Priority:** high  
    **PR:** [baseharbor#1614](https://github.com/mcpdev80/baseharbor/pull/1614)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1614)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Required by:** [t-20261114-r28-cli2-cli-integration](t-20261114-r28-cli2-cli-integration.md)  
**Owner:** Coordinator (auto-merge be5c6c890) / f0f6c8b4 hop + 043d rework receipts  
**Priority:** high  
**PRs:** [baseharbor#1614](https://github.com/mcpdev80/baseharbor/pull/1614)  
**Source:** 
<!-- /generated:links -->

## Goal

Unify app status and versions. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Integrate app show/versions useful output into app status and source list, with app components and health, remote/local/running revisions only when evidence supports it.

## Entry points and ownership

- Starting points: `cmd/baha/app_show.go; app_status_collect.go; app_version_view.go; app_versions_command.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Preserve wanted/applied/observed machine fields, unknown Git/image digest, -c filters and all-targets; CLI/JSON/MCP parity.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

UEBERGABE DURCH OWNER-BEFEHL. WAHRHEIT VORAB, und sie ist mein fehler: der claim dieser karte war zu dem zeitpunkt, als der owner fragte, NICHT auf origin/main (karte zeigte 'owner: coord', 'kanban_status: planned', letzter commit 01a725b6 um 00:07). Ich hatte die bahn dispatched, ohne den fehlgeschlagenen publizierungs-schritt zu bemerken — verstoss gegen AGENTS 4.3 (claim veroeffentlichen, BEVOR aenderungen beginnen). Diese zeile hier ist der berichtigte, gepubliscte zustand.
FAKTEN FUER DEN NEUEN INHABER (gemessen, nicht erzaehlt): PR mcpdev80/baseharbor#1614, zweig lane-0428-062-cli2-app-status, kopf 80d4df52e913 seit 2026-11-16T10:32:06+01:00 (committer w073-perses-alerts), draft=TRUE, checks ALLE SKIPPED (ein draft laeuft nicht), base-sha 15727ca8878938 = ZWEI hops hinter develop d5c11753ea43. write-set 14 dateien, schwerpunkt cmd/baha/app_version_view.go, app_versions_view.go, app_versions_command.go, app_status_result.go plus parity-/regression-tests.
ZWEI WARNUNGEN, die der owner vor dem ersten diff kennen sollte: (1) der diff beruehrt cmd/baha/app_workspace.go UND cmd/baha/app_workspace_source_model.go — beide dateien hat 0428-059 im merge 15727ca88 ANDERS geloest; wenn 062 dort eigene zeilen setzt, pruefe, ob du 059 rueckgaengig machst. (2) KOLLIDIERENDES WRITE-SET: PR #1645 (karte 091, Perses Tempo) beruehrt cmd/baha/app_status_result.go — von mir gemessen (pr diff name-only, treffer 1). Wenn du und 091 gleichzeitig daran arbeiten, braucht es einen integrations-inhaber, sonst zwei konfliktfaelle in derselben datei.
KONTAKT: die alt-lane meldet ihren /var/tmp-worktree-pfad noch (arbeitsbaum bleibt stehen, damit du dort weitermachen kannst, statt bei null).

wer die einheitliche status-zeile zieht, braucht zuerst die basis-karten. draft ist kein kandidat.

CLOSED: merged be5c6c890; exact-base qualifikation 3b40c05da@b411 terminal green; receipts-portale lifecycle-cell-route + resolver-design (1656) traegt.
