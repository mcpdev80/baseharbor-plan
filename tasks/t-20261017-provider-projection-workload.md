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
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-provider-projection-workload · Provider choice: preserve workload identity in requirement projections #task #release/v0-4-26 #status/active #view/active #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (Maintainer dependency repair) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-913](core-913-wizard-compatible-providers-same-view.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (Maintainer dependency repair)  
**Priority:** high  
**PRs:** none  
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

- 2026-10-17 Maintainer claim on current planning main: independently confirmed appProviderChoiceProjection creates an empty-workload manifest, although existing HTTP, metrics and OTLP validators require original portable workload identity. Investigating and repairing outside core-917's owned files. No changes to the New branch and no code acceptance claimed.
