---
id: t-20261018-r27-mutation-lock
card_number: "0427-037"
card_short_title: "reject concurrent or stale"
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lane w184c, freigegeben)
kanban_lane: closed
kanban_summary: All clients use the existing owner lock. Bind application and provider changes to current revision and exact consent;…
kanban_status: closed
kanban_title: "0427-037 · reject concurrent or stale"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-state-owner, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1390]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: 
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1390"]
---

- [x] t-20261018-r27-mutation-lock · Lifecycle: reject concurrent or stale shared changes #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/state #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w184c, freigegeben) · **Priority:** normal  
    **PR:** [baseharbor#1390](https://github.com/mcpdev80/baseharbor/pull/1390)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1390)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md)  
**Owner:** coord-welle4 (Lane w184c, freigegeben)  
**Priority:** normal  
**PRs:** [baseharbor#1390](https://github.com/mcpdev80/baseharbor/pull/1390)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

All clients use the existing owner lock. Bind application and provider changes to current revision and exact consent; conflicting plans require re-preview. Serialize operations touching shared providers across the necessary scope; preserve independent safe reads. One active writer only; no distributed lock framework or second process bypass.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/application_lifecycle_lock.go; internal/coreinstallation/lifecycle_lock.go and lock implementations; bounded server revision/consent adapter tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Real two-process filesystem lock tests; stale revision/consent and shared-consumer conflicts; no native journey. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Angehalten an bindingem Dokument, nicht an Technik
Der Kandidat ist ungeroestet: kein commit, kein test, kein zweig — die lane hat den COST_CONTROL-stop korrekt
als handlungsblockierend erkannt und gemeldet. Mutation-lock selbst ist voll abhaengig frei (state-owner +
ci-authority + updates geschlossen).

## Konflikt Aufloesung (flash-sitz):
COST_CONTROL.md (2026-10-18) verbietet CODEX-implementierungs-Sessions und weist schwere Arbeit den
LOKALEN modellen zu. Owner-Anweisung 2026-11-05: 'nutze einmalig ein worker flash' — w184 laeuft auf dem
worker-flash-kanal (AgentGateway, kein codex). Kein verstoss gegen den stop; AGENTS 2026-11-04 pool
bleibt fuers protokoll notiert, flash-sitz gilt als einmalige ausnahme dieser schicht.

## Runde 2 pruefbar 2026-11-05 (kopf c8c8810f017)
Nachgemessen: ls-remote echt==head, gehosteter lauf terminal SUCCESS am kopf; zweiprozess-locktest echt
+ wörtlich, klienten-inventar 21 vor/nach identisch, beide mutanten rot; develop-stand bei schnitt a53c10a7
(weiterer drift 10e8d646 = merge-zweig-notiz). round-1.md auf main, übergabe der flash-rest-kette
dokumentiert (05bb5a25 → w184c).

## ACCEPT 2026-11-05 (1390a): merge-MISION UNTERWEGS (Luna, SHA c8c8810f017); karte bleibt review bis gemergter develop-beleg vorliegt.

## Gemerged 2026-11-05 (CODEX-MERGE nach 1390a ACCEPT): develop 2301ad0f10, merge-zweig ab382be70d,\ngehosteter lauf 42070352204 terminal success am kopf, gh pr merge --merge ohne bypass. Abhängige\ndamit entriegelt (journal-wiring, management-host — nur NOTIZ).
