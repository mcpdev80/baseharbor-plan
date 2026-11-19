---
id: t-20261119-coord-r28-docker-gate-oras-wiring
card_number: "0428-128"
card_short_title: "Docker-lebenszyklus-beleg vor"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-128 · Docker-lebenszyklus-beleg vor
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261119-coord-r28-docker-gate-oras-wiring · Docker-lebenszyklus-beleg vor dem merge nicht fahrbar (ORAS trust-plane + targeted-integration integriert-only) #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
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

## Purpose (befund-aufnahme)
Zwei strukturelle befunde aus der welle 2026-11-19, beide blockieren den pre-merge docker-lifecycle-beleg mehrerer karten (betroffen: 0428-119 #1690, kinftige coreless-/runtime-karten):

1.  — die zelle 'Core-less application' checkt ref: develop aus und prueft danach 'git rev-parse HEAD = CANDIDATE_SHA' (schritt 'Checkout integrated exact SHA' / 'Verify exact SHA input'). Damit ist der lauf ein INTEGRIERTER post-merge-beleg; vor dem merge kann er strukturell nie gruen werden. Belege: push-getriggert #557-#559 und dispatch #560/#561 auf kopf 4e032c858, dispatch #562ff auf 84ee9a93e (run-ids 44462753158/44462927088/44463099667/44463184000/44463342207), alle brachen in demselben schritt.
2.  (name 'Runtime · Docker Core') respektiert inputs.ref (checkout ref: ${{ inputs.ref || github.sha }}, zeile ~188-190) und fuehrt den job 'docker-runtime' tatsaechlich aus — der lauf bricht aber in der vorbereitung: app_repository_integration_test.go:27 'prepare BaseHarbor integration trust plane: ORAS is required'. Zeuge: run 44464060182, job 135357465520, kopf 84ee9a93e; derselbe bruch reproduziert auf sauberem develop (c000c5db25) und host-lokal (baha-docker, ORAS 1.3.6 installiert, docker native plugin 'native' nicht gefunden).

## Akzeptanz
Ein pre-merge-pfad existiert, der die docker-lifecycle-zelle auf dem EXAKTEN kandidaten-kopf ausfuehrt (nicht skipped, nicht integrated-only), oder die karten-vertraege werden auf einen qualifizierten ersatz-beleg umgestellt. Beides ist - bzw. runner-scope = owner-entscheid.

## Blocker
Owner-scope: workflow-Dateien und runner-/host-praesenz von ORAS (trust-plane). Kein lane-zugriff.
