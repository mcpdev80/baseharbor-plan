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
kanban_summary: "Add seven missing trusted catalog mappings on product develop for the workload recovery-manifest, runtimeexecutor compose,…"
kanban_title: "0428-359 · trusted runtime catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1860", "https://github.com/mcpdev80/baseharbor/actions/runs/45839413560", "https://github.com/mcpdev80/baseharbor/actions/runs/45839805123", "https://github.com/mcpdev80/baseharbor/pull/1862", "https://github.com/mcpdev80/baseharbor/actions/runs/45842143780", "https://github.com/mcpdev80/baseharbor/pull/1861", "https://github.com/mcpdev80/baseharbor/actions/runs/45842320834", "https://github.com/mcpdev80/baseharbor/pull/1863", "https://github.com/mcpdev80/baseharbor/actions/runs/45844485360"]
---

- [ ] t-20261126-trusted-catalog-baseline-recovery-manifest · Add seven runtime source rows to the develop trusted catalog #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1860), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1862), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45842143780), [proof 6](https://github.com/mcpdev80/baseharbor/pull/1861), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/45842320834), [proof 8](https://github.com/mcpdev80/baseharbor/pull/1863), [proof 9](https://github.com/mcpdev80/baseharbor/actions/runs/45844485360)  
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

Add seven missing trusted catalog mappings on product `develop` for the workload recovery-manifest, runtimeexecutor compose, runtime repository-volume-inventory, and stableid lock-probe sources in BaseHarbor PRs [#1860](https://github.com/mcpdev80/baseharbor/pull/1860), [#1862](https://github.com/mcpdev80/baseharbor/pull/1862), [#1861](https://github.com/mcpdev80/baseharbor/pull/1861), and [#1863](https://github.com/mcpdev80/baseharbor/pull/1863). The trusted planner reads its catalog from the base ref (`scripts/pr-gate-plan.py:259` and `:1869`), so candidate-side rows cannot authorize themselves.

## Scope

- In scope: exactly seven new source rows in `scripts/pr-gate-coverage.json`, published together by a separate catalog-only product PR to `develop` after the freeze lifts or under an explicit owner exception. All seven map to the same existing atomic Docker and Podman data-capabilities surfaces.
- Out of scope: changes to PR #1860's test or product files; planner semantics; `.github/**`; gate definitions; #1812, #1819 or #1820; any claim that the catalog row executes or qualifies runtime gates by itself.

## Required catalog rows

Add exactly these seven rows to the develop-side catalog. The #1860 row matches the row already present in that candidate; the other source IDs and paths are copied from the respective Trusted Plan failure logs:

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
  "id": "source.internal_stableid_lock_probe_go",
  "path": "internal/stableid/lock_probe.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

```json
{
  "id": "source.internal_stableid_lock_probe_platform_test_go",
  "path": "internal/stableid/lock_probe_platform_test.go",
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

- All seven source IDs and paths above appear exactly once in `scripts/pr-gate-coverage.json` on `develop`, each with both Docker and Podman data-capabilities surfaces and `runtime_specific: true`. This flag is required so the resolver does not collapse the Podman sibling when a Docker sibling exists.
- The product baseline PR changes only these seven catalog rows; it does not modify candidate files in #1860, #1861, #1862, or #1863, planner logic, workflow files, tests or runtime behavior.
- The one catalog-only PR receives its required hosted validation and is merged to `develop` before any of the four candidates are re-qualified. Record the baseline PR, merged develop SHA and its validation evidence here.
- After the baseline lands, each owning product lane absorbs the resulting develop tip forward-only into its own candidate and obtains exact-final-head hosted checks. This card does not claim those checks are green or that any runtime gate executed.
- Preserve the failed Trusted Plan records as historical failures: #1860 run [45839413560](https://github.com/mcpdev80/baseharbor/actions/runs/45839413560), attempt 1, on intermediate head `f877febbb176ea84911bb1b2fd9363491b4744cc`; #1860 run [45839805123](https://github.com/mcpdev80/baseharbor/actions/runs/45839805123), attempt 1, on current head `6deab9ff68d15060525cc3078e828027e65e9955`; #1862 run [45842143780](https://github.com/mcpdev80/baseharbor/actions/runs/45842143780), attempt 1, on head `c04d92df18345c1c9ffec0150df49f8851a2cea1`; #1861 run [45842320834](https://github.com/mcpdev80/baseharbor/actions/runs/45842320834), attempt 2, on head `6edbcb23c5112b27c7e8899e03ad9e06441390b3`; and #1863 run [45844485360](https://github.com/mcpdev80/baseharbor/actions/runs/45844485360), attempt 1, on head `34c9d7bdb995ee7cbefb70e4171eb247ad37f8f4`. Their Trusted Plan logs report the uncataloged source IDs and paths listed above. Do not represent any as qualifying evidence.

## Required checks

- Validate the seven-row catalog change with the existing hosted checks on its exact product PR head. Do not add a new test or CI route in this card.
- Re-qualification of #1860/#1861/#1862/#1863 is owned by their product cards/lanes after the baseline reaches develop; require applicable exact-head checks and report executed versus skipped jobs truthfully.

## Test binding

- **Test binding:** existing catalog validation; this baseline introduces no test.
- Source paths: `internal/applicationbackup/recovery_manifest_workload_test.go`; `internal/runtimeexecutor/compose.go`; `internal/runtimeexecutor/compose_test.go`; `internal/runtime/repository_volume_inventory.go`; `internal/runtime/repository_volume_inventory_test.go`; `internal/stableid/lock_probe.go`; `internal/stableid/lock_probe_platform_test.go`.
- Declared surfaces: `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.

## Dependencies and file ownership

- Owned product path: `scripts/pr-gate-coverage.json` only.
- Related product cards: 0428-312 (`t-20261125-hunt39-volume-recovery-manifest`) / PR #1860; 0428-318 (`t-20261125-hunt43-low-severity-pair`) / PR #1862; 0428-329 / PR #1861; and 0428-299 (`t-20261125-hunt33-go-runtime-prereq`) / PR #1863. The shared baseline is a prerequisite for Trusted Plan admission, not a replacement for any card's product work; their source files and product changes remain separate.
- One baseline card/PR for all four sets is appropriate because the remediation is identical and additive: seven exact source rows in the same trusted catalog file, with the same two data-capabilities gate surfaces. Card 0428-299 remains the product contract for the Go lock-probe prerequisite; it does not own this separate trusted-base catalog mapping. No planner semantics or workflow change is needed. The existing gate-catalog baseline cards name different source sets and their contracts remain unchanged.

## Handoff

- Product-side baseline implementation remains deferred until the freeze lifts or an owner exception authorizes transport. The worker must publish one separate catalog-only PR containing exactly these seven rows, record its exact head and Hosted validation result, then provide the merged develop SHA for each of the #1860/#1861/#1862/#1863 lanes to absorb.

## Routing disposition — 2026-11-26

The seven-row 0428-359 baseline remains limited to source admission in `scripts/pr-gate-coverage.json`; it does not absorb runtime gate definitions in `scripts/release-requirements.json`. The current develop catalog already has source rows for `internal/operatorauth/authorization.go` and `internal/operatorauth/config.go` (`scripts/pr-gate-coverage.json:1653-1668`). The newly reported `UNRESOLVED` result is a different layer: runtime gate IDs lack the corresponding `gates[]` declarations needed by the single-path planner. That is a routing/registration gap, not a missing trusted source row.

Do not repoint 0428-275: its original `pr-gate-coverage.json` source-row request is already represented on develop, and changing it to own release gate definitions would change its contract. Do not expand 0428-359 beyond its seven named paths. Track the `release-requirements.json`/planner routing correction under existing card 0428-272, which owns the operatorauth runtime-gate routing decision and its self-consistency registration. The planner change remains owner-scope; w327 records the exact failing plan and proposed row mapping there, and does not implement or merge it.

Ordering: the 0428-359 catalog-only baseline must land on develop before #1860 can be requalified. Keep #1860 held while its candidate-side duplicate source row remains; after the baseline lands, its owning lane absorbs the current develop tip, removes only the now-duplicate candidate-side catalog row, preserves the product/test payload, and obtains a new exact-head Trusted Plan result. The separate 0428-272 routing work must not be mixed into #1860's candidate diff or #136's seven-row baseline. Neither baseline alone is evidence that a runtime gate executed or qualifies a candidate.
