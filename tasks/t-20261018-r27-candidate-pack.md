---
id: t-20261018-r27-candidate-pack
card_number: "0427-019"
card_short_title: "package an exact bounded"
areas: [sources]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w151, freigegeben)
kanban_lane: closed
kanban_summary: "Adapt existing native build-context/source-acquisition mechanisms for one selected local checkout, including honest dirty-source…"
kanban_status: closed
kanban_title: "0427-019 · package an exact bounded"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1381]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/c762022e7596f90c529593538717d7413867a93b", "https://github.com/mcpdev80/baseharbor/actions/runs/41928560959"]
---

- [x] t-20261018-r27-candidate-pack · Sources: package an exact bounded deployment snapshot #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/sources #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w151, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor#1381](https://github.com/mcpdev80/baseharbor/pull/1381)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/c762022e7596f90c529593538717d7413867a93b), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/41928560959)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261105-r27-snapshot-change-guard-deterministic](t-20261105-r27-snapshot-change-guard-deterministic.md)  
**Owner:** coord-welle4 (Lane w151, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor#1381](https://github.com/mcpdev80/baseharbor/pull/1381)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Adapt existing native build-context/source-acquisition mechanisms for one selected local checkout, including honest dirty-source identity and exact inputs. Reuse workspace/Git ownership and native ignore/context rules; do not write a custom release/archive format or clone engine. Source transfer is required only for an explicitly selected source-build path; a CI-produced OCI/release input skips it. Constrain paths, symlinks, bytes and secret/build credentials; detect changes during capture, keep .git/local state/credential material out by default, and reject unsupported live bind mounts with useful guidance.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded source snapshot packer/tests using existing repository/workspace inspection APIs; no app_workload_build.go edits. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Temporary repository tests for ignore negation, malicious paths/symlinks, monorepo components, dirty/change-during-read, limits and secret exclusions. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Kandidat pruefbar 2026-11-05 (kopf f6a6ca44059)
- Begrenzter Quellen-Schnappschuss-Packer fuer genau ein lokales Checkout, Wiederverwendung der nativen
  Build-Kontext-Mechanismen; von mir gemessen: Vorfahr ja, nur eigener Commit, Querschnitt ohne Pflege-dateien,
  gehosteter Lauf 41928560959 terminal erfolgreich.

## Merge-Abschluss 2026-11-05

- [PR #1381](https://github.com/mcpdev80/baseharbor/pull/1381) nach develop per Squash gemergt: [c762022e7596f90c529593538717d7413867a93b](https://github.com/mcpdev80/baseharbor/commit/c762022e7596f90c529593538717d7413867a93b).
- Zugehörige selektierte Tests/Builds im GitHub-Run [41928560959](https://github.com/mcpdev80/baseharbor/actions/runs/41928560959) erfolgreich. Nicht gewählte Gates nicht als ausgeführt bewertet.
