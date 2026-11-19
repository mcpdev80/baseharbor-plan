---
id: t-20261119-coord-r28-docker-checks-jsonl
card_number: "0428-136"
card_short_title: "Docker-runtime-job schreibt"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: docker-checks-jsonl (codeman 272065d5-ee21-491f-ad70-e4e1c0a1cdac)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-136 · Docker-runtime-job schreibt
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/60a73a18/evidence/r28-welle4-2026-11-19/docker-checks-jsonl/probe-1.md"]
---

- [x] t-20261119-coord-r28-docker-checks-jsonl · Docker-runtime-job schreibt keine tests/*.jsonl — verify-step faehrt mit FileNotFoundError (root-cause + owner-rezept) #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** docker-checks-jsonl (codeman 272065d5-ee21-491f-ad70-e4e1c0a1cdac)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/60a73a18/evidence/r28-welle4-2026-11-19/docker-checks-jsonl/probe-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** docker-checks-jsonl (codeman 272065d5-ee21-491f-ad70-e4e1c0a1cdac)  
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
Fund F-7 aus dem closeout-heft: der dispatch-lauf 44466684726 ('Runtime · Docker Core', head deeeb6477) endet FAILURE im step 'Verify all eight executed runtime tests' mit 'FileNotFoundError: /home/runner/work/_temp/docker-runtime-checks/tests/main.jsonl'. Der job 'docker-runtime' (.github/workflows/docker-runtime-acceptance.yml, job ab zeile 174) hat — anders als 'single_default_native' (zeile 127-128) — auch KEINEN 'Install verified ORAS' schritt. Die karte klaert BEIDES: warum die JSONL-aevidenz nicht geschrieben wird (welcher step sie schreiben soll, welche umgebungsvariable den pfad setzt, wo er verloren geht) und welche minimale owner-aenderung den pfad UND das ORAS-install in denselben job bringt.

## Acceptance
akte evidence/r28-welle4-2026-11-19/docker-checks-jsonl/probe-1.md: (1) root-cause mit datei:zeile, (2) der exakte mechanismus, warum 'tests/main.jsonl' fehlt (name der variablen, wo sie gesetzt wird, welche jobs sie setzen und welcher nicht), (3) ein minimales owner-rezept als patch-skizze (kein neuer gate, keine neue zelle), (4) gegenprobe: ein job, bei dem die JSONL-erzeugung FUNKTIONIERT, mit seinem laufenden zeug, (5) auswirkung auf 0428-119/#1690 (exaktkopfiger docker-zeuge) mit klarer aussage. KEIN .github-eingriff durch die lane, kein merge, kein subagent (§4.8), host besenrein.

probe laeuft read-only (akte docker-checks-jsonl/probe-1.md): warum der 'docker-runtime'-job keine tests/main.jsonl schreibt (FileNotFoundError im verify-step, job-log 135366064519) + fehlender ORAS-schritt im selben job (zeilen 174-330) — owner-rezept als patch-skizze, auswirkung auf 0428-119/#1690

probe abgegeben und VON MIR nachgeprueft (akte 60a73a18, ancestor origin/main): root-cause ist ein dead default-ref. meine eigene kontrolle: develop .github/workflows/docker-runtime-acceptance.yml zeile 16 = 'default: release/v0.4.21'; 'git ls-remote origin refs/heads/release/v0.4.21' leer; gh api repos/.../branches/release/v0.4.21 -> 404 'Branch not found'. damit scheitert ein nackter workflow_dispatch an 'Checkout requested ref', alle steps 3-17 werden skipped und der always()-verify-step laeuft auf die fehlende tests/main.jsonl — das ist der FileNotFoundError aus 44466684726, kein test-inhalt. GEGENPROBE der lane: dispatch mit gueltigem SHA-ref -> checkout okay, der fehler wandert nach 'Run runtime integration'. GRENZZEHNUNG: das ORAS-loch ist EIN ANDERER fall (lauf 44464060182, app_repository_integration_test.go:27) und bleibt 0428-114(a). FOLGE: 119/#1690 bleibt blocked (wartet auf 114a), 0428-114 bekommt einen FUENFTEN punkt 'default-ref auf develop setzen' (eine zeile, kein neuer gate, kein mkdir/path-umbau)
