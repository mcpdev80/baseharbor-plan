---
id: t-20261018-r27-candidate-contract
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-candidate-contract · Deployment: define immutable source and image submission #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Specify one checkout, one portable intent and server-assigned application binding. Source snapshot/OCI digest, provenance including dirty source, size/ignore/symlink rules, permitted build secrets and builder choice are explicit. Untrusted build/source input cannot obtain the management Docker socket, unrelated files or server credentials; define bounded build isolation, resource limits and credential use. Build/runtime/access/delivery remain separate; no mandatory registry, BuildKit or target-side build. Define existing workspace/Git acquisition ownership and how updates submit a next exact candidate without assuming a server-side .git directory. Define safe candidate ingestion, exact revision binding, image availability and cleanup ownership. Native live bind mounts/hot reload are not silently converted into remote snapshots; unsupported cases fail clearly.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

docs/spec/remote-deployment-v1.md and DE counterpart (new bounded spec); contracts/deploymentcandidate/v1/ records and fixtures. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Record/golden validation; malformed/digest/path/secret-reference fixtures; docs/EN-DE only. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
