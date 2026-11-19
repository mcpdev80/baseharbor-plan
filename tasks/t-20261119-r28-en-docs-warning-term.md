---
id: t-20261119-r28-en-docs-warning-term
card_number: "0428-131"
card_short_title: "EN-Dokumentation nennt das"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-131 (codeman bbd9132d)
kanban_status: review
kanban_lane: review
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-131 · EN-Dokumentation nennt das
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1697]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44478483899", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1697.md"]
---

- [ ] t-20261119-r28-en-docs-warning-term · EN-Dokumentation nennt das Marker-Wort 'Achtung' statt 'Warning' (i18n-drift nach 0428-126) #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** 0428-131 (codeman bbd9132d)  
    **PR:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44478483899), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1697.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-131 (codeman bbd9132d)  
**Priority:** not set  
**PRs:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
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

## Purpose
Nebefund aus der live-verify-kette 0428-130 (akte evidence/r28-welle4-2026-11-19/verify-env-chain/befund-1.md): nach 0428-126 heisst das annerkennende marker im ausgelieferten EN-katalog 'Warning', die englische dokumentation (EN-zweig der doku, inkl. decisions-/cli-texte) verwendet an mindestens einer stelle weiterhin 'Achtung'. severity niedrig, aber kartenwuerdig, weil die EN-doku damit ein wort zeigt, das der EN-CLI nie druckt — dieselbe klasse wie der von 0428-126 behobene rename-drift.

## Acceptance
- alle EN-doku-stellen fuer das marker sagen 'Warning' (grep-beleg: kein 'Achtung' in EN-dateien), deutsche texte bleiben bei 'Achtung'
- ein docs-check laeuft in der betroffenen CI-gruppe mit (bestehender docs-audit genuegt, keine neue workflow-datei)
- akte evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md mit datei:zeile je fundstelle + gruenlauf

abgegeben: EN-doku an drei stelle auf 'Warning' gezogen (docs/de bewusst unveraendert), grep-kontrolle leer, head 3448f73e base-exakt develop da76c5cf9, PR #1697 clean, run 44478483899 TERMINAL SUCCESS (14 jobs gruen, rest durch if-bedingungen skipped), akte origin/main 084c3f93, host besenrein (docker 7 ambient vorher==nachher, podman 0)

CODEX-REVIEW: REQUEST CHANGES at exact head 3448f73e697cd7fdb1a338ef8422b5d484bbe814. Content scope passes; required documentation-audit check is absent from exact-head CI because docs/internal/*.json did not select it. Recipe: select the existing docs-audit gate for those paths (or use the approved exact-head hosted CI route that executes it), then record terminal SUCCESS. Run 44478483899 PR Selected Checks SUCCESS does not prove the skipped/unselected docs check. No merge.
