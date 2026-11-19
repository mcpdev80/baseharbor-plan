---
id: t-20261119-r28-registry-orphan-shared-instance
kanban_title: 0428-151 · shared provider retention
card_number: "0428-151"
card_short_title: "shared provider retention"
type: task
areas: [capability, lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: codex-open-pr-sweep-0428-151
kanban_status: closed
kanban_lane: closed
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "False-positive disposition for hunt 0428-146 after auditing BaseHarbor develop d5c11753ea437495eb2469a02f80b91d788fef4f."
evidence:
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L49-L51"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L270-L289"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_core_requirement_test.go#L192-L212"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry_test.go#L347-L375"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/runtime_openbao_registry_test.go#L39-L52"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/capability/registry.go#L366-L389"
  - "https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_metrics.go#L149-L156"
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md"
resolution: accepted
created: 2026-11-19
---

- [x] t-20261119-r28-registry-orphan-shared-instance · shared-provider retention is by contract #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/lifecycle #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-0428-151  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L49-L51), [proof 2](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L270-L289), [proof 3](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_core_requirement_test.go#L192-L212), [proof 4](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry_test.go#L347-L375), [proof 5](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/runtime_openbao_registry_test.go#L39-L52), [proof 6](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/capability/registry.go#L366-L389), [proof 7](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_metrics.go#L149-L156), [proof 8](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** codex-open-pr-sweep-0428-151  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Determine whether retaining a shared provider registry record after its last application binding is removed violates provider ownership. The hunt observed the state correctly but misclassified retained target-owned inventory as an orphan.

## Disposition

Accepted as a false positive. `ScopeShared` plus `OwnershipBaseHarbor` represents target/platform-owned provider inventory. Application bindings are consumer references; removing the last binding does not transfer or erase that provider ownership. `ReleaseApplicationProviderRegistryAt` intentionally snapshots shared instances, releases the selected application's bindings, then restores the shared instances. Unused inventory remains visible, and reclamation requires explicit ownership-verified cleanup.

The initial hunt also misread `removeUnboundOwnedInstances`: it builds a new instance slice, so `case ScopeShared: continue` omits an unreferenced shared instance from that slice. The observed retention comes from the application-level preservation contract and is independently asserted by existing tests. No product code or tests were changed. Existing tests are cited below; they were inspected, not rerun for this planning-only disposition.

## Evidence

- The provider-registry contract says removed capability instances retain ownership and releasing a binding does not reclaim a provider: [provider_registry.go:49-51](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L49-L51).
- The destroy path snapshots all shared instances, releases the selected app/environment bindings, then re-registers those instances: [provider_registry.go:270-289](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L270-L289).
- The direct lifecycle regression removes SQL from the manifest, destroys the app, and asserts one shared provider remains with zero bindings and is reported in `Footprint.Unused`: [app_core_requirement_test.go:192-212](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_core_requirement_test.go#L192-L212).
- A separate multi-environment regression asserts destroying one environment preserves the shared inventory and the other environment's binding: [provider_registry_test.go:347-375](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry_test.go#L347-L375).
- A zero-binding shared OpenBao control-plane root must survive application release: [runtime_openbao_registry_test.go:39-52](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/runtime_openbao_registry_test.go#L39-L52).
- The lower-level `continue` branch omits the shared instance from the newly built slice; it does not append/preserve it: [registry.go:366-389](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/capability/registry.go#L366-L389).
- The user-facing metrics lifecycle labels unused provider resources `[RETAINED]` and requires explicit ownership-verified cleanup for reclamation: [app_metrics.go:149-156](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_metrics.go#L149-L156).
- The original hunt record is corrected at [baha-podman-146.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md).

## Handoff

2026-11-20: Owner-delegated Maintainer disposition completed. The only change is this planning card and its linked hunt evidence. No product branch, PR, provider-registry mutation, VM mutation, or test execution was performed. Planning validation: `python3 scripts/plan.py render` and `python3 scripts/plan.py check`.
