---
id: t-20261018-r27-onboarding-wizard
areas: [wizard]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-ci-access, t-20261018-r27-client-commands, t-20261018-r27-device-lifecycle, t-20261018-r27-profile-codec, t-20261018-r27-secure-export]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-onboarding-wizard · Onboarding: attach a workstation with minimal questions #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Native success continues silently; import one trusted device bundle or non-secret team profile and authenticate only as policy requires. Distinguish bootstrap from attach; never install duplicate services when joining. Provide explicit existing-app attach versus new app, path remap and session-only/secure choice. Back/cancel/EOF never mutate.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded connection import/export/onboarding wizard files/tests; existing presentation/controller APIs; no central registry edits. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Actual wizard entry tests for both connection modes, repeated operations/no re-prompt, invalid imports/conflicts/cancel; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
