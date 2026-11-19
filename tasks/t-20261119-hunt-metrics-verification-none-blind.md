---
id: t-20261119-hunt-metrics-verification-none-blind
card_number: "0428-124"
card_short_title: "none Metriken erzeugen weder"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-124 r2 (codeman 7110b25d, entlassen) — r3 wartet auf freien sitz
kanban_status: review
kanban_lane: review
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-124 · none Metriken erzeugen weder
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1695]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verification-none/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1695.md"]
- https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verification-none/fix-1.md
---

- [ ] t-20261119-hunt-metrics-verification-none-blind · verification:none Metriken erzeugen weder scrape-target noch assertion — composition ohne gegenprobe #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** 0428-124 r2 (codeman 7110b25d, entlassen) — r3 wartet auf freien sitz  
    **PR:** [baseharbor#1695](https://github.com/mcpdev80/baseharbor/pull/1695)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verification-none/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1695.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verification-none/fix-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-124 r2 (codeman 7110b25d, entlassen) — r3 wartet auf freien sitz  
**Priority:** not set  
**PRs:** [baseharbor#1695](https://github.com/mcpdev80/baseharbor/pull/1695)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
## Befund (intake aus hunt-918)
Befund 6 (MEDIUM): Ein Metrik-source mit verification:none ernt weder scrape-target noch assertion; jede uberspringung fuer sich korrekt, die composition hat keine gegenprobe. Akzeptanz: counter/assertion auf 'null effektive targets nach composition' mit klarem grund-EOF.
Erlaubtes write-set (vorschlag, lane prueft): target composition. Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).

124 abgabefertig: PR #1695 head cc25c17e1 (rebased auf develop deeeb6477), CI run 44462738608 TERMINAL SUCCESS, akte fix-1.md publiziert (plan origin/main 206d0bf4). red->green verifiziert: composition-counter meldet verification:none explizit statt still null targets

CODEX-REVIEW REQUEST CHANGES at exact head cc25c17e17d989710923b93d7e629b14a3c0a3e0: CompositionState is computed but has no production consumer; cmd/baha output remains generic. TestRedAllVerificationNoneHasNoCompositionCounter only asserts the existing skips and does not fail on the base. Recipe: wire the state to the operator-facing composition path and add a real-seam output regression plus a true base-red witness. Run 44462738608 is SUCCESS but cannot replace the missing behavior. Return to review after correction and fresh exact-head checks.

REQUEST_CHANGES auf cc25c17e1: ProviderFiles.CompositionState/ProviderSourcesCompositionState werden produktiv nirgends verbraucht, cmd/baha/app_metrics.go druckt weiter den alten zustand. rezept: verdrahten in den operator-facing pfad, regression mit null-target-grund + positiver fall + unveraenderter fall

korrektur abgegeben: CompositionState/CompositionStateError in den echten operator-facing pfad verdrahtet, real-seam regression (null-target-grund + positiver fall + unveraenderter fall). head 4f0d5e9f70 base-exakt develop da76c5cf9 (ancestor bestaetigt), PR clean, run 44478473607 terminal SUCCESS — 'PR · Go unit · cli-1' now green (ORAS is present on the GitHub runner; the earlier local/develop abort was the DISPATCH job's missing install step, see 0428-114). akte verification-none/fix-2.md auf origin/main

abnahme REQUEST_CHANGES auf exaktem head 4f0d5e9f70 (PR-kommentar 7002942896; formelles review lehnt GitHub ab, weil das PR-autor-konto identisch ist — verdict darum als kommentar, nicht als review-objekt): base clean gegen da76c5cf9, run 44478473607 SUCCESS, produkt-verdrahtung im kern okay. zwei operator-ausgabe-faelle: (1) ProviderCompositionState behauptet bei LEERER source-slice 'all provider sources are Verification=none' und der operator-pfad ruft den renderer ohne quellen auf — eigener zustand fuer 'keine quellen' + regression am echten cli-seam; (2) im all-none-fall druckt der CLI die state-zeile, loescht den CompositionStateError und die zweite bedingungslose nachschau druckt sie NOCH EINMAL — genau eine zeile, regression mit count==1. r3 ist vorbereitet (/var/tmp/missions/mission-124-composition-round3.md) und wird auf dem naechsten freien sitz angesetzt; ACHTUNG SCHREIBSET: die dateien cmd/baha/app_logs.go + internal/metrics/{prometheus_files.go,prometheus_verify.go} sind dieselben wie bei 0428-121 — r3 laeuft erst NACH dem 121-merge (koerper der kette)
