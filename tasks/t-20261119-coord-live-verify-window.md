---
id: t-20261119-coord-live-verify-window
card_number: "0428-138"
card_short_title: "Accept-/smoke-pfade der"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: live-verify-window (codeman b9a62e5c-6102-4887-839a-f2d06a8ba31c)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-138 · Accept-/smoke-pfade der
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/78f02964/evidence/r28-welle4-2026-11-19/verify-window/befund-1.md"]
---

- [x] t-20261119-coord-live-verify-window · Live-verifikation des gemergten fensters auf develop: acceptance-/smoke-pfade der heutigen merges, ergebnis je karte #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** live-verify-window (codeman b9a62e5c-6102-4887-839a-f2d06a8ba31c)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/78f02964/evidence/r28-welle4-2026-11-19/verify-window/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** live-verify-window (codeman b9a62e5c-6102-4887-839a-f2d06a8ba31c)  
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

## Purpose (coordination)
Die heutigen merges (093, 102, 115, 116, 117, 118, 120, 125, 126 + demo 099) sind je karte einzeln abgenommen. Diese karte prueft das GEMEINSAME ergebnis auf develop: laufen die acceptance-/smoke-pfade der betroffenen gruppen auf dem aktuellen develop-kopf wirklich durch, oder hat eine kombinierung etwas verstummt lassen? grundlage fuer die release-freigabe statt einzelner grüner zeilen.

## Acceptance
akte evidence/r28-welle4-2026-11-19/verify-window/befund-1.md: tabelle je pruefung (name | befehl | lauf-id oder host-zeug | PASS/FAIL/SKIP + grund | betroffene karte), gegenprobe an einem bekannten gruenen pfad, und eine klare aussage, ob develop da76c5cf9 (oder der dann aktuelle kopf) fuer ein release-qualifikationsoffset taugt. KEINE produkt-aenderung, KEIN .github/scripts-eingriff (befund mit datei:zeile), KEIN merge, KEIN PR, isolierte worktrees nur unter /var/tmp, host besenrein (vorher/nachher docker ps -a + podman ps -a, 'cleanliness:'-zeile; ambient bh-local-shared-* und core-*/bilder fremder karren unangetastet), kein subagent (§4.8).

fahrt ueber die heutigen merges auf develop (akte verify-window/befund-1.md): acceptance-/smoke-pfade der betroffenen gruppen, je zeile PASS/FAIL/SKIP + grund, gegenprobe an sicher gruenem pfad. read-only, kein dispatch/rerun/push

read-only fahrt ueber die heutigen merges auf develop (akte verify-window/befund-1.md): acceptance-/smoke-pfade der betroffenen gruppen, je zeile PASS/FAIL/SKIP + grund, gegenprobe an sicher gruenem pfad. kein dispatch/rerun/push

fahrt abgegeben und von mir nachgeprueft (akte 78f02964, ancestor origin/main): basis develop da76c5cf9c963207038d5599bd130b89ecb1e8a4; lokal go test/vet PASS je gruppe (internal/metrics, internal/observability, internal/identityprovider, internal/application, cmd/baha fuer 0428-118-stdout-leak) und hosted 'Runtime · Docker Core' + 'Runtime · Podman Core' auf da76c5cf9 SUCCESS (von mir per gh api bestaetigt, dazu derselbe stand auf 21161b101); merge-kette first-parent #1696 <- #1694 <- ... <- #1688 <- #1689 <- #1685. ERGEBNIS: die heutigen merges (093/102/115/116/117/118/120/125/126 + demo 099) sind gemeinsam auf develop gruen — ein release-qualifikations-offset ist damit belegt, solange develop sich nicht bewegt
