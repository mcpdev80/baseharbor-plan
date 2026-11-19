---
id: t-20261119-r28-demo-drive-matcher-warning-marker
card_number: "0428-129"
card_short_title: "drive.py matcher auf das"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-129 (codeman 60be3d2d)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-129 · drive.py matcher auf das
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor-demo#165]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md", "https://github.com/mcpdev80/baseharbor-demo/pull/165", "https://github.com/mcpdev80/baseharbor-demo/actions/runs/44477622615", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/129-demo-165.md"]
---

- [x] t-20261119-r28-demo-drive-matcher-warning-marker · Demo: drive.py matcher auf das Warning-marker-verhalten der annerkennenden stadien ziehen #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** 0428-129 (codeman 60be3d2d)  
    **PR:** [baseharbor-demo#165](https://github.com/mcpdev80/baseharbor-demo/pull/165)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-demo/pull/165), [proof 3](https://github.com/mcpdev80/baseharbor-demo/actions/runs/44477622615), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/129-demo-165.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-129 (codeman 60be3d2d)  
**Priority:** not set  
**PRs:** [baseharbor-demo#165](https://github.com/mcpdev80/baseharbor-demo/pull/165)  
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
- 2026-11-19: candidate `bc4c6113be92599c962b2377b038173593483a18` on `lane-0428-demo-drive-matcher` (cut from demo `origin/develop@5d1cf312e18d06915db35c340bebe4e3d4f39d45`), PR https://github.com/mcpdev80/baseharbor-demo/pull/165, required run https://github.com/mcpdev80/baseharbor-demo/actions/runs/44477622615 `completed success` observed by the lane at the exact head. Evidence: `evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md`. Card at review; merge/acceptance is not the lane's step.

## Purpose
Folgekarte zu 0428-126 (core, PR #1696, gemeldet in evidence/r28-welle4-2026-11-19/dualmatch-docs/fix-1.md): das Warning-marker wird jetzt in JEDEM annerkennenden CLI-stadium gedruckt (gate-semantik unveraendert). Die Demo-lane `drive.py` erkennt stadien ueber ein eigenes matcher-pattern; bleibt das Muster unveraendert, sieht die demo einen zustand als nicht-annerkannt, waehrend der core das marker setzt — also eine demo-seitige Scheibenfalse-negativ-erkennungs-luecke.

## Acceptance
- `drive.py`-matcher akzeptiert die annerkennenden stadien MIT Warning-marker konsistent (identische regel wie core, keine doppelte auslegung).
- eine demo-seitige pruefung/regression deckt den fall "stadium annerkannt + marker gesetzt" ab, damit die kopplung nicht erneut driftet.
- exakte-head CI des demo-repos auf dem kandidaten terminal gruen; akte unter baseharbor-plan evidence/r28-welle4-2026-11-19/demo-drive-matcher/.

## Abhaengigkeiten
Content-abhaengig von 0428-126 (merged oder abgenommen); basis ist develop des demo-repos.

demo-seitig abgegeben: drive.py/new_edit.py nutzen jetzt EINE generierte regel auf der core-Warning-marker-basis aus #1696 ('Achtung:' nur als negativer guard), rote->gruene regression test_21..test_25, kandidat bc4c6113b auf lane-0428-demo-drive-matcher (basis demo origin/develop 5d1cf312e), run 44477622615 SUCCESS am exakten head, akte a372fe8c. OWNER-BEFUND: .github/workflows/pr-guided-consent.yml:5 triggert nur auf main — develop-kandidaten im demo-repo starten damit keine CI (aufgenommen in 0428-114)

CODEX-REVIEW: ACCEPT at exact head bc4c6113be92599c962b2377b038173593483a18. The shared generated matcher covers marked/plain acknowledge and apply labels; production-path regression suite passes in exact-head PR run 44477622615 (41 seconds). CODEX-MERGE: squash merge adda7599cb5b79689702f6a63a5ca802179df967 verified as demo main. The current PR-gate workflow selects PRs to main only; develop-targeted candidates need the owner-scoped trigger fix tracked by 0428-114.

GEMERGT: CODEX-REVIEW ACCEPT auf exaktem head bc4c6113be92599c962b2377b038173593483a18, merge 07:34:17Z in baseharbor-demo main (der merge ist ein squash, deshalb ist bc4c6113b selbst nicht ancestor von main — inhalts-zeug: drive.py traegt die gemeinsame generierte marker-regel auf main). exact-head run 44477622615 SUCCESS, akte a372fe8c. F-4 aus dem closeout-heft (base=main statt develop) erweist sich damit als hinfaelig: das demo-repo integriert auf main, sein pr-guided-consent-gate haengt genau dort an (zeile 4-5 branches:[main]) — die branch-base ist also konsistent, nicht falsch
