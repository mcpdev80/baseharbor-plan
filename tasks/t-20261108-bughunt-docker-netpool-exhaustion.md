---
id: t-20261108-bughunt-docker-netpool-exhaustion
card_number: "0427-146"
card_short_title: "No advice on pool error"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network…
kanban_title: 0427-146 · No advice on pool error
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1477]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42484014091", "https://github.com/mcpdev80/baseharbor/commit/25baf858c59c8352ee733acf01da8853e778e807"]
---
- [x] t-20261108-bughunt-docker-netpool-exhaustion · Bug Hunt v0.4.27: No advice on pool error #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1477](https://github.com/mcpdev80/baseharbor/pull/1477)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42484014091), [proof 3](https://github.com/mcpdev80/baseharbor/commit/25baf858c59c8352ee733acf01da8853e778e807)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1477](https://github.com/mcpdev80/baseharbor/pull/1477)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network prune hint with target context); regression with a producible error path (mock/invalid network name) in the lifecycle group; host-side exhaustion itself is owner-scope, not a product fix.

## Problem (source evidence in the dossier)
On a saturated docker host, baha up (core and workload) dies on all predefined address pools have been fully subnetted without any recovery hint; the user only sees the daemon line. Source: hunt H-D4 BF-hd4-1 (HIGH).

## Acceptance
The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network prune hint with target context); regression with a producible error path (mock/invalid network name) in the lifecycle group; host-side exhaustion itself is owner-scope, not a product fix.

## Dependencies and file ownership
None. Write-set: compose network creation error paths in core/workload up.


## Übernahme und CI — 2026-11-08

- Owner `chatgpt-r27-network-hint`; [PR #1477](https://github.com/mcpdev80/baseharbor/pull/1477) fügt dem echten Network-Create-Pfad einen sicheren Hinweis für Docker-Adressenpool-Erschöpfung hinzu.
- Synthetic native-command regression prüft zwei Pool-Fehler und einen nicht verwandten Fehler. Keine automatische Bereinigung fremder Netzwerke.
- CI exact-head ausstehend; Karte bleibt `active`, keine Acceptance oder Mergefreigabe vor PASS.


## Acceptance 2026-11-08 — PR #1477

- Native pool-exhaustion error detection and safe operator guidance merged in [PR #1477](https://github.com/mcpdev80/baseharbor/pull/1477), merge `25baf858c59c8352ee733acf01da8853e778e807`.
- Exact-head [CI #42484014091](https://github.com/mcpdev80/baseharbor/actions/runs/42484014091) terminal SUCCESS including focused runtime-provider-package tests, CLI guided checks and Docker/Podman destroy retry.
- Fake-runtime regression verifies pool exhaustion, overlap error and unrelated permission denial; no automated destructive network pruning. Host-wide exhaustion is an operational issue, not a promised test result. Product acceptance criteria met; owner released.
