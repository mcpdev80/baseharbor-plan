---
id: t-20261120-r28-podman-consent-gate-stall
card_number: "0428-187"
card_short_title: "consent gate stalls cell"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-187 · consent gate stalls cell
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-podman-consent-gate-stall · The podman data-capabilities cell stalls the guided wizard at the candidate-consent step #task #release/v0-4-28 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found in the PR #1715 run (2026-11-20, run 44743111417, job 136312259900)

The card under review (#1715, destroy-side registry cleanup) changed neither the wizard nor the consent path, but its
`PR · Selected Runtime (atomic/podman/data-capabilities)` cell is red. Log witnesses, verbatim from the job log:

```
13:25:24  Existing consent authority requires 2 confirmation(s)
13:27:13  Error: wizard cancelled without changes
13:36:01  Error: record deployment before mutation: candidate submission requires an explicit operator
13:36:01  RuntimeError: new-edit-new-sql-remove exceeded no-output timeout: elapsed=241s no-output=180
13:32:30  demo-data-capabilities       FAIL
```

The scenario reaches the candidate step, is told two confirmations are required, cancels, and the harness keeps waiting
until the 180-second no-output limit kills the cell. `PR Selected Checks` therefore aggregates red while every Go unit
shard is green. Whether the same stall reproduces on a clean develop head is NOT yet proven: the job only materialises in
PR-selected runs, so no develop push carries a comparable cell (measured: develop runs 44728573148 / 44726527868 list no
data-capabilities job).

## Acceptance

1. Reproduce the guided scenario `new-edit-new-sql-remove` on the current develop head, in the same cell
   (podman, data-capabilities). State in the evidence whether the stall predates this release.
2. Fix the fixture/flow so the consent path is satisfiable in CI: either the fixture supplies the second confirmation the
   product asks for, or the product stops asking twice where the flow can only answer once - one of the two, with the
   chosen side named at file:line.
3. Keep the fail-closed behaviour: never make the cell green by removing the consent requirement or by auto-approving a
   candidate submission in the runner (AGENTS 3.8: the check input must not be set by the party being checked).
4. Bound the wait: the scenario must finish inside the 180-second no-output window; a silent wizard must surface its
   prompt instead of hanging. Record the new duration in the evidence.

## Boundaries

scripts/ci-greenfield-apply.py, the guided-wizard command path in cmd/baha and the data-capabilities fixture. The
destroy-side files of 0428-184 (internal/application/shared_backends_resources_runtime.go, internal/observability/registry.go)
and the identity witness of 0428-078 are NOT part of this card. No .github/** (owner scope): if the workflow needs a
consent env, report the needed change as a finding with file:line instead of editing it (AGENTS 5.3).
