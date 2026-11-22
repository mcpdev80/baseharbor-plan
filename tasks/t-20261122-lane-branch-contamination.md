---
id: t-20261122-lane-branch-contamination
card_number: "0428-239"
card_short_title: "sibling PR content merged into"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
tags: [#task, #release/v0-4-28]
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-239 · sibling PR content merged into
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1723]
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/commit/acc34323968"]
---

- [x] t-20261122-lane-branch-contamination · re-cut PR 1723 and PR 1725 without sibling PR content #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1723](https://github.com/mcpdev80/baseharbor/pull/1723)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/acc34323968)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1723](https://github.com/mcpdev80/baseharbor/pull/1723)  
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


- **Test binding (select exactly one):**  normal (auto-discovered) ·  contract  add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR ·  new check  update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

## Finding (2026-11-22, measured with ls-remote + ancestry tests)

Branch `lane-0428-199-workloadport` (PR #1723, head `12a62523fc5`) and branch `w201-0428-201-statever` (PR #1725, head
`485103523b9`) each carry an extra merge author `0428-222-childenv` with merges of ARBITRARY sibling heads:

```
12a62523f Merge commit 'b2d9aeb446f...' into HEAD     # own previous hop
bfd01276f Merge commit '0768274c6f6...' into HEAD     # <-- #1627's head, foreign content
485103523 Merge commit 'dd4e826f6c8...' into HEAD     # own previous hop
```

Ancestry proof: `0768274c6f6` (old #1627 head) IS an ancestor of #1723 (`JA`), of #1725 (`JA`), and of #1627 itself -
but NOT of #1645. Consequence: #1723's diff against develop `52a3c5446f4` shows 16 files including
`cmd/baha/env_destroy.go`, `cmd/baha/env_destroy_integration_test.go`, `cmd/baha/app_apply.go` - all #1627/#0428-055
work, not #1723's. The reviewer's REQUEST CHANGES for #1723 ('6 failed jobs, none match the 0428-237 broker', 'the
develop-only additivity fails') is therefore a CONTAMINATION artefact, not a workload-port defect.

## Fix recipe

Re-cut both PRs from the develop tip: new branch from `52a3c5446f4`, cherry-pick only the PR's own content commits
(#1723: the workload-port commit; #1725: the state-version commit), verify `git diff --name-only develop...head` lists
only that card's files, force nothing (close the polluted PR and open the clean one, one PR per card). Rule check:
lanes merge only their OWN base chain (AGENTS 3.3.8); a hop must never merge a sibling PR head - `git merge --no-ff
<develop-sha>` only, and the develop SHA must be resolved from `refs/heads/develop` immediately before the merge.
Witness: run `44995050874` (#1723, 6 failed jobs), run `44995066580` (#1725), review
`evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1723-head12a62523fc5.md`.

kein re-cut noetig - die messung hat die ursache aufloest, indem der fremde inhalt in develop einzog: nach dem 1627-merge (develop acc34323968) schrumpft der diff von PR 1723 gegen develop von 16 auf 4 dateien (app_apply.go, app_workload_ports.go, runtime.go, workload_port_local_regression_test.go) und der von PR 1725 von 19 auf 7. Die ahnen-kette bleibt, aber sie ist jetzt develop-inhalt. Was bleibt, ist die REGEL: ein hop loest refs/heads/develop direkt vor dem merge auf und merged NUR diesen stand, nie einen parallelen PR-head - die beiden zusatz-merges mit verfaesser 0428-222-childenv (0768274c6f6 und b2d9aeb446f) waren der verlauf, der die 1723-review verfaelschte. Naechster schritt fuer 1723/1725 ist ein normaler hop auf acc34323968 (back=2).

kein re-cut noetig - die ursache loeste sich auf, indem der fremde inhalt in develop einzog: nach dem 1627-merge (develop acc34323968) schrumpft der diff von PR 1723 gegen develop von 16 auf 4 dateien (app_apply.go, app_workload_ports.go, runtime.go, workload_port_local_regression_test.go) und der von PR 1725 von 19 auf 7. Die ahnen-kette bleibt, aber sie ist jetzt develop-inhalt. Was bleibt, ist die REGEL: ein hop loest refs/heads/develop direkt vor dem merge auf und merged NUR diesen stand, nie einen parallelen PR-head - die beiden zusatz-merges mit verfaesser 0428-222-childenv (0768274c6f6 und b2d9aeb446f) waren der hergang, der die 1723-review verfaelschte. Naechster schritt fuer 1723/1725 ist ein normaler hop auf acc34323968 (back=2).

kein re-cut noetig - die ursache loeste sich auf, indem der fremde inhalt in develop einzog: nach dem 1627-merge (develop acc34323968) schrumpft der diff von PR 1723 gegen develop von 16 auf 4 dateien (app_apply.go, app_workload_ports.go, runtime.go, workload_port_local_regression_test.go) und der von PR 1725 von 19 auf 7. Die ahnen-kette bleibt, aber sie ist jetzt develop-inhalt. Was bleibt, ist die REGEL: ein hop loest refs/heads/develop direkt vor dem merge auf und merged NUR diesen stand, nie einen parallelen PR-head - die beiden zusatz-merges mit verfaesser 0428-222-childenv (0768274c6f6 und b2d9aeb446f) waren der hergang, der die 1723-review verfaelschte. Naechster schritt fuer 1723/1725 ist ein normaler hop auf acc34323968 (back=2).
