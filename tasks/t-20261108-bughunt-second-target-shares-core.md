---
id: t-20261108-bughunt-second-target-shares-core
card_number: "0427-163"
card_short_title: "Second same-host target silent"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w163-sharedcore
kanban_status: review
kanban_lane: review
kanban_summary: "Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for…"
kanban_title: 0427-163 · Second same-host target silent
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1487]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-second-target-shares-core · Bug Hunt v0.4.27: Second target reuses Core #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w163-sharedcore · **Priority:** normal  
    **PR:** [baseharbor#1487](https://github.com/mcpdev80/baseharbor/pull/1487)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w163-sharedcore  
**Priority:** normal  
**PRs:** [baseharbor#1487](https://github.com/mcpdev80/baseharbor/pull/1487)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for a second same-host target must refuse to silently join another target's Core and must name the owning target plus concrete options. Decision note in the card for owner if by-design; regression in the runtime group.

## Problem (source evidence in the dossier)
Creating a second podman target with the same local access reference and running up --control-plane-only connects to the already-running shared Core: same ports 15433/18201, same bh-<first>-shared-* containers/networks; the second target gets no state dir and status still reports the first target (BF-05, blocker candidate, architecture/hazard). The project name is keyed by target name but running discovery resolves to whichever Core is up. Sources: internal/runtime/project_names.go:7-9, cmd/baha/target.go:603-605.

## Acceptance
Either true per-target isolation (distinct project/ports/state dir, verified), or an explicit fail-closed conflict gate: up for a second same-host target must refuse to silently join another target's Core and must name the owning target plus concrete options. Decision note in the card for owner if by-design; regression in the runtime group.

## Dependencies and file ownership
None. Write-set: control-plane up / runtime project naming.

## Exact-head CI monitoring — 2026-11-08 (0427-163)

- [PR #1487](https://github.com/mcpdev80/baseharbor/pull/1487), head `a158f2b183db3ed2dcfd6dcbead378b626ae9a55`, [CI #42503466672](https://github.com/mcpdev80/baseharbor/actions/runs/42503466672). Source format failed on unformatted shared_core_conflict_test.go; aligned map/fixture formatting, then re-triggered CI. Card remains open until the required CI is terminal green.
