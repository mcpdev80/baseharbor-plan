---
id: t-20261122-gate-catalog-completion-ci-executor
card_number: "0428-248"
card_short_title: "catalog completion #1774"
type: task
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (#1774) / owner (promote+merge) / coord
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
wait_reason: "#1774 promoted ready (draft run 45029281024 SUCCESS) aber diff=head acd57828 = NUR eintrag B. b90e4ba1 ergaenzt A (scripts/ci-fast-check.sh->atomic/static/ci-fast-check) + C (app_footprint_presenter.go) als zweiten additiven commit VOR merge, damit der eine merge #1770-native UND #1746-static(A) UND #1773(C) entblockt. Owner fuehrt native docker+podman evidence + review, merged selbst. Akzeptanz: alle drei planner-selektionen + validate-catalog + unittests gruen, native nicht skipped gebucht."
resolution: ""
evidence: []
---

- [ ] t-20261122-gate-catalog-completion-ci-executor · Complete the gate catalog by registering the three remaining changed paths in pr-gate-coverage.json so dependent gates execute #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1774) / owner (promote+merge) / coord · **Priority:** high  
    **PR:** [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774)  
    **Waiting:** \#1774 promoted ready (draft run 45029281024 SUCCESS) aber diff=head acd57828 = NUR eintrag B. b90e4ba1 ergaenzt A (scripts/ci-fast-check.sh-\>atomic/static/ci-fast-check) + C (app\_footprint\_presenter.go) als zweiten additiven commit VOR mer…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-gate-catalog-missing-app-broker-component](t-20261122-gate-catalog-missing-app-broker-component.md)  
**Owner:** b90e4ba1 (#1774) / owner (promote+merge) / coord  
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
