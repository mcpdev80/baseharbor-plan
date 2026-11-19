---
id: t-20261119-hunt-metrics-target-env-key-asymmetry
card_number: "0428-125"
card_short_title: "Runtime-metrics"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w99-0428-125 (hopf-handoff 045d7e8a-bundel)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-125 · Runtime-metrics
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1694]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/target-env-key/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1694.md", "https://github.com/mcpdev80/baseharbor/pull/1694", "https://github.com/mcpdev80/baseharbor/actions/runs/44465054273"]
---

- [x] t-20261119-hunt-metrics-target-env-key-asymmetry · Runtime-metrics target-file-key fuehrt environment nicht, group-label schon — asymmetrische Zuordnung #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w99-0428-125 (hopf-handoff 045d7e8a-bundel)  
    **PR:** [baseharbor#1694](https://github.com/mcpdev80/baseharbor/pull/1694)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/target-env-key/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1694.md), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1694), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44465054273)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w99-0428-125 (hopf-handoff 045d7e8a-bundel)  
**Priority:** not set  
**PRs:** [baseharbor#1694](https://github.com/mcpdev80/baseharbor/pull/1694)  
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

- Owned files or areas: internal/metrics/runtime_source.go (target file key formula and resource id) plus the new regression test file.
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- 2026-11-19: fix-1 candidate published. Branch `lane-0428-125-target-env-key` @ `4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f`, PR https://github.com/mcpdev80/baseharbor/pull/1694 (base develop `ec592fd38`). Red regression green after fix; CI run 44457185039 terminal success on the exact head. Evidence: evidence/r28-welle4-2026-11-19/target-env-key/fix-1.md.
## Befund (intake aus hunt-918)
Befund 7 (MEDIUM): Der runtime-metrics target-file-key spaart den environment, das gespeicherte group-label fuehrt ihn — asymmetrisch, in multi-env collision. Akzeptanz: schluessel-formel ein documentarischer ort, test mit zwei envs.
Erlaubtes write-set (vorschlag, lane prueft): file-key builder. Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).

END akzeptiert: schluessel-formel an einer stelle mit environment, regression red/green (TestRuntimeSourceSeparatesTargetFilesPerEnvironment), head 4fcb2b35d base-exakt ec592fd38, run 44457185039 SUCCESS terminal, akte am band dd89401b. Routing an CODEX. registry.go-ueberschneidungsregel (erst-gruen-zuerst) gilt weiter

CODEX-REVIEW ACCEPT(content) steht auf 4fcb2b35d; der bundel-hopf hat den zweig auf e1742275e gehoben (diff-vs-diff identisch, run 44465054273 SUCCESS). abnahme-instanz gebeten, das urteil auf den base-exakten kopf zu heben — danach merge nach §8

CODEX-MERGE: ACCEPT on hopped exact head e1742275e984aebd4e0cef027a999aed6a6b7f97. Content diff SHA-256 d69d5aae5f0be64f58081723eed50da3b72185f653bb192e3a58a2ddca3766a1 matches accepted 4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f; develop deeeb6477 is an ancestor. Exact-head run 44465054273 SUCCESS (21.17 runner-minutes). Squash merge 21161b101f66a47fb1a253ae17e87fe82567ba4d verified on develop.
