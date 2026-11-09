---
id: t-20261018-r27-app-binding
card_number: "0427-014"
card_short_title: "attach fresh checkouts to a"
areas: [identity]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: coord-welle4 (Lane w179, freigegeben)
kanban_lane: closed
kanban_summary: Server allocates IDs; explicitly create a new app or attach to a permitted existing app. Two distinct checkout paths can resolve…
kanban_status: closed
kanban_title: "0427-014 · attach fresh checkouts to a"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract, t-20261018-r27-state-owner, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1388]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1388"]
---

- [x] t-20261018-r27-app-binding · Identity: attach fresh checkouts to a registered application #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/identity #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w179, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1388](https://github.com/mcpdev80/baseharbor/pull/1388)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1388)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** coord-welle4 (Lane w179, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1388](https://github.com/mcpdev80/baseharbor/pull/1388)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Server allocates IDs; explicitly create a new app or attach to a permitted existing app. Two distinct checkout paths can resolve one deployment by installation + application ID + Target + environment. Name/Git URL is only discovery evidence, never authorization. Cover monorepo apps, forks, rename, copy, denied lookup, ambiguous matches and concurrent first registration. No IDs authored by developers or hidden repository-path identity.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/app_repository_identity.go; internal/application/identity_resolution.go; bounded registration binding owner/tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused registration/identity tests with two fresh homes/checkouts and simultaneous registration; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Runde 1 pruefbar 2026-11-05 (kopf 4e4a23e89bd)
Nachgemessen: ls-remote echt==head, develop Vorfahr (frischer schnitt 42bfcb1cb4), genau ein eigener
commit, write-set in den karten-grenzaten (binding+identity+store-naht); zwei frische homes parallel
konvergieren (race-20), server-seitige id-vergabe belegt, beide verweigerungs-mutanten rot, red-first
dokumentiert; lauf 42020006887 terminal + akte round-1.md auf main.

## ACCEPT 2026-11-05 (r1388a): merge-reif fuer die Owner-Runde
Kopf 4e4a23e89bd unveraendert; zwei-homes-zelle selbstonde (IDs verschieden, race-20 konvergiert), beide
mutanten rot, echter CLI-pfad, uebrige store-pfade unveraendert. Akte review-1388a.md.


## Owner-Abschluss 2026-11-05

- PR [#1388](https://github.com/mcpdev80/baseharbor/pull/1388) nach `develop` gemerged, Squash-Commit `a34903a230bab7ad75270cf9dec9ac5683af6ac2`.
- Pflicht-CI [Run 42020006887](https://github.com/mcpdev80/baseharbor/actions/runs/42020006887) auf dem vor Merge verifizierten PR-Head abgeschlossen: `success`, einschließlich `PR Selected Checks`.
- Historische Review-Rückrufe und Korrekturen bleiben als Nachweis erhalten. Fachliche Abnahme gemäß letzter ACCEPT-Bewertung; separate Release-/Cross-Repo-Qualifizierung dadurch nicht vorweggenommen.
