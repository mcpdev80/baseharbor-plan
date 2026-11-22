---
id: t-20261122-gate-catalog-completion-ci-executor
card_number: "0428-248"
card_short_title: "catalog completion #1774"
type: task
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (#1774) / owner (akzeptanz) / coord
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-248 · catalog completion #1774
priority: high
depends_on: [t-20261122-gate-catalog-missing-app-broker-component]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1774]
sources: []
blocker: ""
wait_reason: "STAND diff acd57828 = NUR eintrag B (ci-native-pr-gate.sh). A (scripts/ci-fast-check.sh->atomic/static/ci-fast-check) und C (app_footprint_presenter.go product-gate) FEHLEN noch -> #1746-static + #1773/246 bleiben blockiert. b90e4ba1 ergaenzt A+C als zweiten additiven commit + planner-3x-ja beweis. Draft-CI 45029281024 (nur B) war SUCCESS; nach A+C exact-hosted neu + owner-akzeptanz + normale PR-CI + native/data-caps exact (nicht skipped) vor merge."
resolution: ""
evidence: []
---

- [ ] t-20261122-gate-catalog-completion-ci-executor · Complete the gate catalog by registering the three remaining changed paths in pr-gate-coverage.json so dependent gates execute #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1774) / owner (akzeptanz) / coord · **Priority:** high  
    **PR:** [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774)  
    **Waiting:** STAND diff acd57828 = NUR eintrag B (ci-native-pr-gate.sh). A (scripts/ci-fast-check.sh-\>atomic/static/ci-fast-check) und C (app\_footprint\_presenter.go product-gate) FEHLEN noch -\> \#1746-static + \#1773/246 bleiben blockiert. b90e4ba1 ergae…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-gate-catalog-missing-app-broker-component](t-20261122-gate-catalog-missing-app-broker-component.md)  
**Owner:** b90e4ba1 (#1774) / owner (akzeptanz) / coord  
**Priority:** high  
**PRs:** [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774)  
**Source:** 
<!-- /generated:links -->

## Scope (follow-up to 0428-242 / PR #1768)

PR #1768 merged the catalog with only `cmd/baha/app_broker.go`. Three changed paths remain uncataloged and each blocks a dependent gate:

- `scripts/ci-fast-check.sh` -> `atomic/static/ci-fast-check` (test_repo_core_paths_preserve_legacy_release_gate_coverage expects it; blocks #1746 static cells).
- `scripts/ci-native-pr-gate.sh` -> ci-executor (blocks #1770 native Docker/Podman data-capabilities selection).
- `cmd/baha/app_footprint_presenter.go` -> declared product gate (fail-loud guardian aborts #1773 / 0428-246 without it).

## Acceptance

1. Add all three entries to scripts/pr-gate-coverage.json (Codeman/242 scope, no product code change), guardian semantics unchanged.
2. Exact Draft CI run 45029281024 (head acd57828) SUCCESS already (routing + all cli/package shards); before merge: owner acceptance -> promote draft->ready -> re-run NORMAL PR CI -> verify native/docker+podman/data-capabilities EXACT selected jobs run (not skipped).
3. Do not treat skipped native cells as evidence.

## Boundaries

scripts/pr-gate-coverage.json + planner/guardian metadata only. Not the presenter/product code, not operatorauth, not .github workflows (pre-release.yml is owner scope).
