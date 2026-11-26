---
id: t-20261126-trusted-catalog-baseline-recovery-manifest
card_number: "0428-359"
card_short_title: "recovery manifest catalog row"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Add the missing trusted catalog mapping on product develop for the workload recovery-manifest test source in BaseHarbor PR…
kanban_title: "0428-359 · recovery manifest catalog row"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1860", "https://github.com/mcpdev80/baseharbor/actions/runs/45839413560", "https://github.com/mcpdev80/baseharbor/actions/runs/45839805123"]
---

- [ ] t-20261126-trusted-catalog-baseline-recovery-manifest · Add the recovery-manifest workload test source to the develop trusted catalog #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1860), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123)  
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

## Goal

Add the missing trusted catalog mapping on product `develop` for the workload recovery-manifest test source in BaseHarbor PR [#1860](https://github.com/mcpdev80/baseharbor/pull/1860). The trusted planner reads its catalog from the base ref (`scripts/pr-gate-plan.py:259` and `:1869`), so a candidate-side row cannot authorize itself.

## Scope

- In scope: one new source row in `scripts/pr-gate-coverage.json`, published by a separate catalog-only product PR to `develop` after the freeze lifts or under an explicit owner exception.
- Out of scope: changes to PR #1860's test or product files; planner semantics; `.github/**`; gate definitions; #1812, #1819 or #1820; any claim that the catalog row executes or qualifies runtime gates by itself.

## Required catalog row

Add exactly this row to the develop-side catalog, matching the row already present in #1860's candidate:

```json
{
  "id": "source.internal_applicationbackup_recovery_manifest_workload_test_go",
  "path": "internal/applicationbackup/recovery_manifest_workload_test.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

## Acceptance

- The exact source ID and path above appear exactly once in `scripts/pr-gate-coverage.json` on `develop`, with both Docker and Podman data-capabilities surfaces and `runtime_specific: true`.
- The product baseline PR changes only that catalog row; it does not modify `#1860`, planner logic, workflow files, tests or runtime behavior.
- The catalog-only PR receives its required hosted validation and is merged to `develop` before the `#1860` candidate is re-qualified. Record the baseline PR, merged develop SHA and its validation evidence here.
- After the baseline lands, the owning product lane absorbs the resulting develop tip forward-only into the candidate and obtains exact-final-head hosted checks. This card does not claim those checks are green or that any runtime gate executed.
- Preserve the two failed Trusted Plan records as historical failures: run [45839413560](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), attempt 1, on intermediate head `f877febbb176ea84911bb1b2fd9363491b4744cc`; and run [45839805123](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123), attempt 1, on current head `6deab9ff68d15060525cc3078e828027e65e9955`. Both fail because the trusted base catalog lacks this source row; the latter log says `uncataloged source change, no declared runtime gate owner` for the exact path and ID above. Do not represent either run as qualifying evidence.

## Required checks

- Validate the one-row catalog change with the existing hosted checks on its exact product PR head. Do not add a new test or CI route in this card.
- Re-qualification of #1860 is owned by its product card/lane after the baseline reaches develop; require the applicable exact-head checks and report executed versus skipped jobs truthfully.

## Test binding

- **Test binding:** existing catalog validation; this baseline introduces no test.
- Source path: `internal/applicationbackup/recovery_manifest_workload_test.go`.
- Declared surfaces: `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.

## Dependencies and file ownership

- Owned product path: `scripts/pr-gate-coverage.json` only.
- Related product card: 0428-312 (`t-20261125-hunt39-volume-recovery-manifest`) and its PR #1860. The baseline is a prerequisite for Trusted Plan admission, not a replacement for that card's test work.
- The existing gate-catalog baseline cards name different source sets; this card adds only the recovery-manifest source and does not extend or alter their contracts.

## Handoff

- Product-side baseline implementation remains deferred until the freeze lifts or an owner exception authorizes transport. The worker must publish a separate catalog-only PR, record its exact head and Hosted validation result, then provide the merged develop SHA for the #1860 lane to absorb.
