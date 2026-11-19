---
id: t-20261119-coord-r28-ci-intake-audit
card_number: "0428-133"
card_short_title: "tests ohne gemappten trigger —"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ci-intake-audit (codeman 7add5c03-efa6-49d9-a355-bfc5f246eca1)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-133 · tests ohne gemappten trigger —
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/74fa2814evidence"]
---

- [x] t-20261119-coord-r28-ci-intake-audit · CI-aufnahme-audit: tests ohne gemappten trigger (perses-smoke, demo-pr-gate, weitere) — liste mit datei:zeile fuer die gate-map #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** ci-intake-audit (codeman 7add5c03-efa6-49d9-a355-bfc5f246eca1)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/74fa2814evidence)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** ci-intake-audit (codeman 7add5c03-efa6-49d9-a355-bfc5f246eca1)  
**Priority:** not set  
**PRs:** none  
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
Ein audit ueber die tests des fensters, die auf dem papier existieren, aber von keinem CI-job erreicht werden (§5.3 CI-aufnahmepflicht). bereits bekannte faelle: TestPersesRuntimeSmokeDockerIsolated (kein trigger, BASEHARBOR_PERSES_RUNTIME_SMOKE ungesetzt — blockiert 0428-088/#1592), demo .github/workflows/pr-guided-consent.yml:5 (triggert nur auf main — develop-kandidaten im demo-repo laufen nie), scripts/pr-gate-coverage.json ohne perses-eintrag. gesuchte klasse: alle tests, die in karten-akten als pflichtbeleg dienen, aber keiner testgruppe zugeordnet sind.

## Acceptance
liste je fund: testname, datei:zeile des tests, workflow-/gate-datei mit zeile die ihn NICHT erwaehnt, betroffene karte/PR, vorschlag des passendes gates (existierend, kein neuer gate). akte evidence/r28-welle4-2026-11-19/ci-intake-audit/befund-1.md. KEINE aenderung an .github oder scripts (owner-scope), KEINE neuen gates.

audit laeuft read-only (akte ci-intake-audit/befund-1.md): alle tests des fensters ohne gemappten CI-trigger, inklusive der drei bekannten faelle (perses-smoke, demo pr-gate main-only, pr-gate-coverage ohne perses). kein .github/scripts-eingriff durch die lane — nur die liste fuer deine gate-map

audit abgegeben und verifiziert:akte befund-1.md commit 74fa2814, ancestor von origin/main 36cf77e2. VIER löcher derselben klasse mit datei:zeile: (1) das VOLLE go-unit-suite-lauf 'go test ./...' sitzt in ci.yml:342 hinter einer if-bedingung zeile 259, die pull_request ausschliesst — auf PRs haengt jede Go-unit-abdeckung an der pr_plan-routinen-auswahl (zeile 709, pr_unit_shards/pr_validations/pr_focused), pr_focused (1091) ist eine fixe Python-suite; (2) TestPersesRuntimeSmokeDockerIsolated existiert nur auf dem kandidaten-zweig (internal/application/perses_runtime_test.go auf lane-0428-088, 0 treffer auf develop) und hat KEINEN trigger — genau die §5.3-verletzung, die 088/#1592 blockiert; (3) baseharbor-demo .github/workflows/pr-guided-consent.yml:4-5 triggert nur auf branches:[main]; (4) documentation-audit (ci.yml:1186) wird durch scripts/pr-gate-plan.py:1189-119x fuer docs/internal/*.json nicht ausgewaehlt — blockiert 131/#1697. gegenprobe der methode: TestObservabilityFullStackAcceptanceInCI ist positiv gemappt (observability-acceptance.yml:78 und :186) — die masse ist also nicht pauschal blind. KEIN .github/scripts-eingriff durch die lane, host besenrein
