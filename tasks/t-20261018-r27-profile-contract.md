---
id: t-20261018-r27-profile-contract
areas: [access]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-profile-contract · Access: define portable connection and device profile records #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/access #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Define non-secret profile versus sensitive one-use device enrollment versus explicitly encrypted local-credential export. Pin installation identity/trust/recipient/scope/expiry; import grants no rights, cannot run plugins or redirect credentials. Document native Git/SSH/kube/cloud reuse; session-only versus protected durable storage and DR separation. Publish minimal profile/credential-source interfaces and golden fixtures; no provider implementations.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

docs/spec/credential-access-v1.md and DE counterpart; bounded versioned connection/profile records and fixtures under contracts/managementaccess/v1/. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Schema/golden/negative fixture tests and focused docs/EN-DE checks. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
