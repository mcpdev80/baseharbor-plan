---
id: t-20261018-r27-execution-journal
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (lane w107)
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1373"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/execution-journal/slice-1.md"
  - "https://github.com/mcpdev80/baseharbor/pull/1373"
  - "https://github.com/mcpdev80/baseharbor/commit/0ce814d0"
---

- [ ] t-20261018-r27-execution-journal · Operations: persist execution identity and terminal outcomes #task #release/v0-4-27 #status/active #view/active #area/state #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (lane w107) · **Priority:** normal  
    **PR:** [baseharbor#1373](https://github.com/mcpdev80/baseharbor/pull/1373)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/execution-journal/slice-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1373), [proof 3](https://github.com/mcpdev80/baseharbor/commit/0ce814d0)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md)  
**Owner:** coord-welle4 (lane w107)  
**Priority:** normal  
**PRs:** [baseharbor#1373](https://github.com/mcpdev80/baseharbor/pull/1373)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Persist accepted/running/terminal or uncertain status, correlation and authorized request commitment before effects. Duplicate request with changed content is rejected; reconnect retrieves the same operation. Bound retention, no secrets/artifact payloads in ordinary journal. No claim of exactly-once effects across crashes. Handler/lifecycle wiring is a later task.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/machinehttp/store.go; bounded durable execution-journal files and tests in internal/machinehttp/. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused disk/reopen/corruption/concurrent admission/retention tests, secret scanning; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Stand-Vermerk 2026-11-04 (coord f49a3303)
- Claim publiziert (owner w107). Lane WARTET auf Kapazitaet im Worker-Pool (4 aktive Lanes, Spawn-Hold);
  kartenzustand deshalb Zwischenstand: noch keine code-aenderung, keine branch work/r27-execution-journal.

## Coordination note 2026-11-04 (coordinator f49a3303)
- Lane w112 reported the card as already delivered by the merged journal state and closed without code. That
  claim was checked against develop bb9bc0ef and rejected for two criteria:
  duplicate request with changed content is not refused (internal/machinehttp/store.go:102-130 keys records by
  execution id only, no comparison, no typed error), and reconnect retrieving the same operation has no path.
  Criteria on persistence before effects, bounded retention without payloads, and the no-exactly-once wording
  are satisfied by the merged state.
- Correction round: branch work/r27-execution-journal, red-first tests for both gaps against the real path,
  implementation inside internal/machinehttp, draft PR, terminal gates. Evidence must live in
  evidence/r27-welle4-2026-11-04/execution-journal/ (an off-board proof file does not count).

- Correction round (lane w112) delivered head 0ce814d0, PR #1373 draft on develop 2a43984a: duplicate request
  with changed content is refused and reconnect returns the same operation, both added to store.create through an
  operations index with red-first tests; criteria 1, 4, 5 were already covered by the merged journal state.

## Review-Rueckruf 2026-11-04 (Codex review-1373a, verdict REJECT)
- Die semantische Operationsauswahl wurde als Anfragen-Wiedererkennungsschlüssel benutzt; eine
  anfragen-eigene Identität mit Nicht-Geheimnis-Verpflichtung über die ganze Anfrage fehlt.
- Die Eingabe fehlt in der Verpflichtung; der Wiedererkennungsindex geht beim erneuten Öffnen verloren, weil
  load() ihn nicht aus dem erhaltenen Protokoll aufbaut.
- Doppel- und Wiedererkennungswege sind im Anfragepfad vom neu akzeptierten Lauf nicht unterscheidbar
  (runExecution läuft erneut, typisierter Fehler als internal verpackt).
- Es fehlt die Reihenfolge-Regression: Eintrag lesbar, bevor die erste Wirkung beginnt.
- Formulierung "replayed once, never a second time" muss auf die gebundene Garantie verschlankt werden.
- Korrekturrunde = Lane w119 auf demselben Zweig und PR #1373 (Kopf vorher 0ce814d0).
