---
id: t-20261126-trusted-catalog-baseline-recovery-manifest
card_number: "0428-359"
card_short_title: "trusted runtime catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Add five missing trusted catalog mappings on product develop for the workload recovery-manifest, runtimeexecutor compose, and…"
kanban_title: "0428-359 · trusted runtime catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1860", "https://github.com/mcpdev80/baseharbor/actions/runs/45839413560", "https://github.com/mcpdev80/baseharbor/actions/runs/45839805123", "https://github.com/mcpdev80/baseharbor/pull/1862", "https://github.com/mcpdev80/baseharbor/actions/runs/45842143780", "https://github.com/mcpdev80/baseharbor/pull/1861", "https://github.com/mcpdev80/baseharbor/actions/runs/45842320834"]
---

- [ ] t-20261126-trusted-catalog-baseline-recovery-manifest · Add five runtime source rows to the develop trusted catalog #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1860), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1862), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45842143780), [proof 6](https://github.com/mcpdev80/baseharbor/pull/1861), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/45842320834)  
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

Add five missing trusted catalog mappings on product `develop` for the workload recovery-manifest, runtimeexecutor compose, and runtime repository-volume-inventory sources in BaseHarbor PRs [#1860](https://github.com/mcpdev80/baseharbor/pull/1860), [#1862](https://github.com/mcpdev80/baseharbor/pull/1862), and [#1861](https://github.com/mcpdev80/baseharbor/pull/1861). The trusted planner reads its catalog from the base ref (`scripts/pr-gate-plan.py:259` and `:1869`), so candidate-side rows cannot authorize themselves.

## Scope

- In scope: exactly five new source rows in `scripts/pr-gate-coverage.json`, published together by a separate catalog-only product PR to `develop` after the freeze lifts or under an explicit owner exception. All five map to the same existing atomic Docker and Podman data-capabilities surfaces.
- Out of scope: changes to PR #1860's test or product files; planner semantics; `.github/**`; gate definitions; #1812, #1819 or #1820; any claim that the catalog row executes or qualifies runtime gates by itself.

## Required catalog rows

Add exactly these five rows to the develop-side catalog. The #1860 row matches the row already present in that candidate; the other source IDs and paths are copied from the respective Trusted Plan failure logs:

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

```json
{
  "id": "source.internal_runtimeexecutor_compose_go",
  "path": "internal/runtimeexecutor/compose.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

```json
{
  "id": "source.internal_runtimeexecutor_compose_test_go",
  "path": "internal/runtimeexecutor/compose_test.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

```json
{
  "id": "source.internal_runtime_repository_volume_inventory_go",
  "path": "internal/runtime/repository_volume_inventory.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

```json
{
  "id": "source.internal_runtime_repository_volume_inventory_test_go",
  "path": "internal/runtime/repository_volume_inventory_test.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

## Acceptance

- All five source IDs and paths above appear exactly once in `scripts/pr-gate-coverage.json` on `develop`, each with both Docker and Podman data-capabilities surfaces and `runtime_specific: true`. This flag is required so the resolver does not collapse the Podman sibling when a Docker sibling exists.
- The product baseline PR changes only these five catalog rows; it does not modify candidate files in #1860, #1861, or #1862, planner logic, workflow files, tests or runtime behavior.
- The one catalog-only PR receives its required hosted validation and is merged to `develop` before any of the three candidates are re-qualified. Record the baseline PR, merged develop SHA and its validation evidence here.
- After the baseline lands, each owning product lane absorbs the resulting develop tip forward-only into its own candidate and obtains exact-final-head hosted checks. This card does not claim those checks are green or that any runtime gate executed.
- Preserve the failed Trusted Plan records as historical failures: #1860 run [45839413560](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), attempt 1, on intermediate head `f877febbb176ea84911bb1b2fd9363491b4744cc`; #1860 run [45839805123](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123), attempt 1, on current head `6deab9ff68d15060525cc3078e828027e65e9955`; #1862 run [45842143780](https://github.com/mcpdev80/baseharbor/actions/runs/45842143780), attempt 1, on head `c04d92df18345c1c9ffec0150df49f8851a2cea1`; and #1861 run [45842320834](https://github.com/mcpdev80/baseharbor/actions/runs/45842320834), attempt 2, on head `6edbcb23c5112b27c7e8899e03ad9e06441390b3`. Their Trusted Plan logs report the uncataloged source IDs and paths listed above. Do not represent any as qualifying evidence.

## Required checks

- Validate the five-row catalog change with the existing hosted checks on its exact product PR head. Do not add a new test or CI route in this card.
- Re-qualification of #1860/#1861/#1862 is owned by their product cards/lanes after the baseline reaches develop; require applicable exact-head checks and report executed versus skipped jobs truthfully.

## Test binding

- **Test binding:** existing catalog validation; this baseline introduces no test.
- Source paths: `internal/applicationbackup/recovery_manifest_workload_test.go`; `internal/runtimeexecutor/compose.go`; `internal/runtimeexecutor/compose_test.go`; `internal/runtime/repository_volume_inventory.go`; `internal/runtime/repository_volume_inventory_test.go`.
- Declared surfaces: `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.

## Dependencies and file ownership

- Owned product path: `scripts/pr-gate-coverage.json` only.
- Related product cards: 0428-312 (`t-20261125-hunt39-volume-recovery-manifest`) / PR #1860; 0428-318 (`t-20261125-hunt43-low-severity-pair`) / PR #1862; and 0428-329 / PR #1861. The shared baseline is a prerequisite for Trusted Plan admission, not a replacement for any card's product work; their source files and product changes remain separate.
- One baseline card/PR for all three sets is appropriate because the remediation is identical and additive: five exact source rows in the same trusted catalog file, with the same two data-capabilities gate surfaces. No planner semantics or workflow change is needed. The existing gate-catalog baseline cards name different source sets and their contracts remain unchanged.

## Handoff

- Product-side baseline implementation remains deferred until the freeze lifts or an owner exception authorizes transport. The worker must publish one separate catalog-only PR containing exactly these five rows, record its exact head and Hosted validation result, then provide the merged develop SHA for each of the #1860/#1861/#1862 lanes to absorb.
