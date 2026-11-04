---
id: t-20261018-r27-connection-client
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w145, freigegeben)
kanban_lane: review
kanban_summary: Keep management connection separate from placement Target. Explicit selection wins deterministically; bind server installation…
kanban_status: review
kanban_title: "Client: resolve trusted local or remote management connections"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261018-r27-profile-codec, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1380]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-connection-client · Client: resolve trusted local or remote management connections #task #release/v0-4-27 #status/review #view/review #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w145, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor#1380](https://github.com/mcpdev80/baseharbor/pull/1380)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md)  
**Owner:** coord-welle4 (Lane w145, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor#1380](https://github.com/mcpdev80/baseharbor/pull/1380)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Keep management connection separate from placement Target. Explicit selection wins deterministically; bind server installation identity, pinned trust and discovery/version negotiation. User-scoped local cache stores no remote authority; unavailable or changed server fails closed without local execution.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded management connection/client package; cmd/baha/use_target.go connection-selection helper (no root registry edits). These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

TLS httptest, wrong peer/equal alias/two-installation/stale-cache/precedence tests; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Anspruch 2026-11-04
- Auftrag: Verwaltungsverbindung und Platzierungsziel getrennt halten, ausdrueckliche Auswahl gewinnt
  deterministisch, Bindungen (Installation, Vertrauen, Entdeckung) weisen bei Abweichung vor jeder Wirkung ab.

## Kandidat pruefbar 2026-11-04
- Kopf f1f3551291c, develop ist Vorfahr, log-Zeile traegt nur den eigenen Commit (von mir gemessen).
- Die Wiederverwendung laeuft ueber die bereits abgenommene Kern-Installations-Autoritaet; Verbindung und
  Ziel sind getrennt, ausdrueckliche Auswahl gewinnt, Bindungen schliert fehlgeschluessen.
- Die Lane meldet einen PRE-EXISTING Ausfall der Compose-Lebenszyklus-Pruefung und nennt das keine
  Regression. Der Review muss das auf Deiner Hauptlinie selbst nachmessen (rote Grundlinie, nicht
  behauptet); die PR-eroeffnung uebernahm ich, weil die Lane den Schritt vergessen hatte.
