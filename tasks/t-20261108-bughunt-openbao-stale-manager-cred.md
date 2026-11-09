---
id: t-20261108-bughunt-openbao-stale-manager-cred
card_number: "0427-154"
card_short_title: "Stale OpenBao manager credenti"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server =…"
kanban_title: 0427-154 · Stale OpenBao manager credenti
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1468]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [x] t-20261108-bughunt-openbao-stale-manager-cred · Bug Hunt v0.4.27: Stale cred blocks rebirth #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1468](https://github.com/mcpdev80/baseharbor/pull/1468)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1468](https://github.com/mcpdev80/baseharbor/pull/1468)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server = re-bootstrap path (with clear notice), not permanent denial; regression with stale-file fixture in the bao field.

## Problem (source evidence in the dossier)
When OpenBao reports uninitialized but the old openbao-admin.env still exists, bootstrap refuses forever (internal/openbao/bootstrap.go:234-243). Source: hunt H-D5 BF-1 (HIGH).

## Acceptance
Bootstrap treats manager-credential state as part of the uninitialized check: stale admin env on an uninitialized server = re-bootstrap path (with clear notice), not permanent denial; regression with stale-file fixture in the bao field.

## Dependencies and file ownership
None. Write-set: internal/openbao/bootstrap.go.

## Duplex note
Own candidate PR #1467 closed unmerged per act-1468-fate.md (patch byte-identical); #1468 (owner side) is the leading candidate and still needs the act-1467 review deltas.

## Merge verification — 2026-11-08

- Product PR: https://github.com/mcpdev80/baseharbor/pull/1468
- Squash merge SHA: `224fa801f1ae9fcab166a2407178b380e650f923`
- CI run `42481502910`: Go build, vet, unit tests, OpenBao package tests and native Docker/Podman destroy retry successful. Unrelated skipped jobs were not treated as passing.
- Full end-to-end Greenfield qualification remains separate.
