---
id: t-20261119-coord-r28-drift-sweep
card_number: "0428-137"
card_short_title: "ahead/behind,"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: drift-sweep (codeman 6d23313f)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: "0428-137 · ahead/behind,"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/e6d31f12/evidence/r28-welle4-2026-11-19/drift-sweep/befund-1.md"]
---

- [x] t-20261119-coord-r28-drift-sweep · Drift-fahrt ueber die 25 lebend-kandidaten: ahead/behind, merge-tree-konflikte, schreibset-kollisionen, hopf-reihenfolge #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** drift-sweep (codeman 6d23313f)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/e6d31f12/evidence/r28-welle4-2026-11-19/drift-sweep/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** drift-sweep (codeman 6d23313f)  
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
Grundlage fuer meine hopf-reihenfolge im merge-window: welche lebend-kandidaten sind base-exakt, welche brauchen einen hopf, welche konfligieren im schreibset miteinander, und welche muessen seriell hinter einem bestimmten merge warten. nachweis je zeile mit dem befehl, der ihn erzeugt.

## Acceptance
akte evidence/r28-welle4-2026-11-19/drift-sweep/befund-1.md (tabelle + sortierung + nachweis-spalte). read-only, KEIN push/comment/close/merge/dispatch, keine karten-statuswechsel, isolierte clones unter /var/tmp, kein subagent (§4.8), host besenrein.

read-only fahrt ueber die 25 lebend-kandidaten: ahead/behind, merge-tree-konflikt-prognose, schreibset-kollisionen, hopf-reihenfolge (akte drift-sweep/befund-1.md). kein push/comment/close durch die lane

sweep abgegeben und mit zwei STICHPROBEN von mir bestaetigt: (a) #1615 ist der wichtigste fund — GitHub sagt 'clean', mein eigener 'git merge-tree --write-tree origin/develop <head>' zeigt aber 'CONFLICT (content) in internal/deployment/target.go': mergeable_state ist fuer gestapelte PRs (base ist ein lane-ast, nicht develop) UNZUEREICHEND, in zukunft zaehlt die merge-tree-prognose; (b) #1695 teilt internal/metrics/prometheus_verify.go mit #1691 (treffer 1) und ist merge-tree-konfliktfrei (1493f2cbb) — die einordnung SERIAL-BEHIND-1691 stimt damit in beiden richtungen. gesamt: 25 lebend-kandidaten, 20 konfliktfrei (4 base-exakt #1691/#1697/#1692/#1695), 5 konfliktbehaftet (#1645/#1613/#1598/#1597 je 4-8 dateien, #1615 add/add), hartester schreibset-cluster perses {1645,1613,1598,1597} je 20 dateien, rebase-chain 1578->1615. gruendung fuer meine weitere sequenzierung: 122r3/123/124r3 bleiben hinter dem 121-merge
