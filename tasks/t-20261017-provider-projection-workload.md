---
id: t-20261017-provider-projection-workload
type: task
areas: [cli]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (Maintainer dependency repair)"
priority: high
depends_on: [core-913]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#979"]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/979", "https://github.com/mcpdev80/baseharbor/actions/runs/38987081285", "https://github.com/mcpdev80/baseharbor/commit/beca492d36c0c625e1a68a7ca055f6685fc10fba"]
---

- [x] t-20261017-provider-projection-workload · Provider choice: preserve workload identity in requirement projections #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (Maintainer dependency repair) · **Priority:** high  
    **PR:** [baseharbor#979](https://github.com/mcpdev80/baseharbor/pull/979)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/979), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/38987081285), [proof 3](https://github.com/mcpdev80/baseharbor/commit/beca492d36c0c625e1a68a7ca055f6685fc10fba)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-913](core-913-wizard-compatible-providers-same-view.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (Maintainer dependency repair)  
**Priority:** high  
**PRs:** [baseharbor#979](https://github.com/mcpdev80/baseharbor/pull/979)  
**Source:** 
<!-- /generated:links -->

## Goal

Unblock the real core-917 New controller path by retaining existing workload-component identity in its read-only provider-choice projection.

## Scope

- Only cmd/baha/app_provider_choice.go and app_provider_choice_test.go.
- Use the existing manifest constructor and ResolveFootprint authority; no second resolver, New/Edit changes, domain or workflow edits.

## Acceptance

- A declared HTTP exposure retains its original workload components and resolves through the existing authority.
- Related workload-dependent requirement projections preserve the same existing context.
- Invalid missing or mismatched workload declarations remain rejected; original inputs are unchanged and copied components are not aliased.

## Required checks

- Existing wizard-provider-choice-tests, source/contracts, CLI format/vet/build and authenticated PR Selected Checks. No native runtime change or matrix.

## Dependencies and file ownership

- core-913 is accepted. Maintainer owns only the two provider-choice files for this bounded regression repair; core-917 retains its New files.

## Handoff

- 2026-10-17 Maintainer acceptance: [PR #979](https://github.com/mcpdev80/baseharbor/pull/979), source `7745223fce3965c10f4068d142f1acff4e0ec2f4`, exact integration `820ffcd` over trusted develop `b73e27603ee082f2fabb81df1b2789fba3367d23`, merged as `beca492d36c0c625e1a68a7ca055f6685fc10fba`. The only production change copies existing Workload.Components through application.WithWorkloadComponents before projecting the selected requirement; no synthesized component, resolver bypass, domain change or runtime mutation. [Hosted run 38987081285](https://github.com/mcpdev80/baseharbor/actions/runs/38987081285) independently confirms all 12 provider-choice test families ran and passed, including actual ResolveFootprint parity for HTTP, metrics and OTLP, detached component storage, unchanged manifest/snapshot/selection and rejection of missing or mismatched workload/HTTP declaration. CLI gofmt, vet, build, source/contracts, focused Python, trusted plan, workflow policy and authenticated PR Selected Checks all PASS. Only the two owned provider-choice files changed; no native/runtime matrix. Local Go was unavailable and never claimed executed. Task accepted, Obsidian closed, core-917 dependency defect repaired; its New implementation and formatting remain Session 1 scope. Planning release cycles, render/check and all 47 tests validated before publishing; other sessions preserved.

- 2026-10-17 Maintainer claim on current planning main: independently confirmed appProviderChoiceProjection creates an empty-workload manifest, although existing HTTP, metrics and OTLP validators require original portable workload identity. Investigating and repairing outside core-917's owned files. No changes to the New branch and no code acceptance claimed.
