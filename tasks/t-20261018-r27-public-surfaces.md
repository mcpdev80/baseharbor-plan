---
id: t-20261018-r27-public-surfaces
areas: [cli]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-access-wizard, t-20261018-r27-delegated-handoff, t-20261018-r27-maintenance-client, t-20261018-r27-management-host, t-20261018-r27-node-cli, t-20261018-r27-onboarding-wizard, t-20261018-r27-promote, t-20261018-r27-remote-podman-web, t-20261018-r27-remote-rollout, t-20261018-r27-version-view, t-20261022-r27-ci-access, t-20261022-r27-ci-authority, t-20261022-r27-ci-delivery, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-public-surfaces · Integration: register the accepted CLI JSON MCP HTTP operations #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [console-2](console-2-live-core-adapter-workflow-proofs.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Single owner wires accepted callable adapters into public commands and machine discovery without duplicates. Same auth/identity/state/consent/remediation on CLI/JSON/MCP/HTTP. Keep Application Runtime API out of management; preserve existing local commands and v0.4.26 wizard behavior. No new domain implementation inside registration.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/commands.go; MCP registrations and internal/machine/ contract/coverage owners; shared help/schema/golden indexes. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused actual command discovery/help/schema/golden/MCP execution and authorization matrix; trust selection requirements remain independently reviewed. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
