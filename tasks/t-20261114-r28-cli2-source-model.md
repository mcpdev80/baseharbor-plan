---
id: t-20261114-r28-cli2-source-model
card_number: "0428-059"
card_short_title: "Extend app sources and"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Extend app sources and components. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-059 · Extend app sources and
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-uid-app]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1595]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-source-model/round-1.md"]
---

- [ ] t-20261114-r28-cli2-source-model · CLI redesign: Extend app sources and components #task #release/v0-4-28 #status/planned #view/ready #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **PR:** [baseharbor#1595](https://github.com/mcpdev80/baseharbor/pull/1595)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-source-model/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-uid-app](t-20261114-r28-cli2-uid-app.md)  
**Required by:** [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-app-status](t-20261114-r28-cli2-app-status.md), [t-20261114-r28-cli2-source-pull](t-20261114-r28-cli2-source-pull.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** [baseharbor#1595](https://github.com/mcpdev80/baseharbor/pull/1595)  
**Source:** 
<!-- /generated:links -->

## Goal

Extend app sources and components. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Build source/component domain changes for optional unique components, multiple per source, local directory and existing Git/OCI, incremental add/path/remove with ownership-safe detach.

## Entry points and ownership

- Starting points: `internal/development/ source models; cmd/baha/app_workspace.go; app_workspace_wizard.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

No neighboring scans or artificial components; unique names and multi-component maps, non-Git source, no local files deleted, deterministic machine parity.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

draft PR #1595 @ eda0cd61c, base lane-0428-uid-target; local package+audit runs green on candidate SHA; CI trigger finding (no PR CI for lane bases) in akte

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

INHASBERSCHAFT FREIGEGEBEN (transfer-ersuchen, queue662): der eigentümer-text nannte 'lane-0428-059-cli2-source-model (flash)' — GEMESSEN KEINE solche sitzung (codeman agent list: nur codex-rev-cli2b als reviewer, idle; der flash-sitz traegt 0428-083). zweig refs/heads/lane-0428-059-cli2-source-model = 818d572b982a, PR #1595 draft=true base.ref=lane-0428-uid-target, 19 dateien, unveraendert seit 11-16. write-set cmd/baha/app_workspace* + human_workspace.go ist DISJUNKT zu meinen laeufernden PRs (#1690 application_provider_authorization.go, #1702 app_status_*/app_perses_*, #1684 app_apply_lifecycle.go — keine gemeinsame datei gemessen). ACHTUNG: ein base.ref der cli2-kette eroeffnet KEINEN pull_request-lauf (ci.yml :14-18 nur develop/main/lane-*)

INHASBERSCHAFT FREIGEGEBEN, karte zurueck auf planned/ready damit scripts/plan.py claim sie annehmen kann (active ohne owner war ein regelverstoss, den mein eigenes skript nicht schreiben kann: 'if a.owner:' ist fuer einen leeren string falsy — queue662, werkzeug-befund). Gemessen: keine sitzung namens lane-0428-059-cli2-source-model mehr (flash traegt 0428-083); zweig 818d572b982a; PR #1595 draft=true base.ref=lane-0428-uid-target; write-set cmd/baha/app_workspace* disjunkt zu meinen laeufernden PRs. WARNUNG an den nehmer: ein base.ref der cli2-kette eroeffnet KEINEN pull_request-lauf (ci.yml :14-18 oeffnet nur develop/main/lane-*) — basis auf develop umbiegen oder den Zweig in lane-* umbenennen, sonst gibt es nie einen exact-head-beleg
