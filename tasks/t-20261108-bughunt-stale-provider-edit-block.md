---
id: t-20261108-bughunt-stale-provider-edit-block
card_number: "0427-150"
card_short_title: "Stale instance blocks edit"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same…
kanban_title: 0427-150 · Stale instance blocks edit
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1490]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-stale-provider-edit-block/round-1.md"]
---
- [x] t-20261108-bughunt-stale-provider-edit-block · Bug Hunt v0.4.27: Stale instance blocks edit #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1490](https://github.com/mcpdev80/baseharbor/pull/1490)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-stale-provider-edit-block/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1490](https://github.com/mcpdev80/baseharbor/pull/1490)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same target in the lifecycle group.

## Problem (source evidence in the dossier)
app edit cannot change a need when an unapplied state-only app exists: a stale provider instance in the target registry leads to broken references. Source: hunt H-P3 BF-03 (blocker candidate).

## Acceptance
Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same target in the lifecycle group.

## Dependencies and file ownership
None. Write-set: target registry provider-instance refresh on the edit path.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): same registry surface as #149 - sequence after the name gate lands. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)

## Final review acceptance and merge — 2026-11-08

- [PR #1490](https://github.com/mcpdev80/baseharbor/pull/1490) squash-merged into `develop` at `20902f0a6ab016fd8fe6a501751e1becc5f334dd` from exact reviewed head `35e5496203dc75fe6ad3bd4d1b97a44e98308792`.
- [CI #42511516539](https://github.com/mcpdev80/baseharbor/actions/runs/42511516539) terminal SUCCESS: Go full unit tests; targeted wizard-app-edit, wizard-controller and wizard-provider-choice tests; go-build, go-vet, gofmt, focused Python, native Docker and Podman destroy-retry, and the final `PR Selected Checks` gate all PASS. The required checks were executed rather than interpreted from skipped jobs.
- Scope accepted: stale live provider instance re-resolution from the Target registry, genuinely missing instances described actionably, preserved explicit preferences on unrelated edits, and cancel/no-write regressions as documented in [round 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-stale-provider-edit-block/round-1.md). No separate full native two-app wizard lifecycle was claimed from this unit-surface acceptance.
- Card closed/accepted; prior worker released. No additional PR or release/tag.
