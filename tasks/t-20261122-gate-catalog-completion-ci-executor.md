---
id: t-20261122-gate-catalog-completion-ci-executor
card_number: "0428-248"
card_short_title: "catalog completion #1774"
type: task
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: b90e4ba1 (#1778 sammelt ALLE katalog-luecken) / 0847d100 (read-only zensus)
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-248 · catalog completion #1774
priority: high
depends_on: [t-20261122-gate-catalog-missing-app-broker-component]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1774, mcpdev80/baseharbor#1776, mcpdev80/baseharbor#1777, mcpdev80/baseharbor#1778]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-gate-catalog-completion-ci-executor · Complete the gate catalog by registering the three remaining changed paths in pr-gate-coverage.json so dependent gates execute #task #release/v0-4-28 #status/active #view/active #area/ci #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (\#1778 sammelt ALLE katalog-luecken) / 0847d100 (read-only zensus) · **Priority:** high  
    **PR:** [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774), [baseharbor#1776](https://github.com/mcpdev80/baseharbor/pull/1776), [baseharbor#1777](https://github.com/mcpdev80/baseharbor/pull/1777), [baseharbor#1778](https://github.com/mcpdev80/baseharbor/pull/1778)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-gate-catalog-missing-app-broker-component](t-20261122-gate-catalog-missing-app-broker-component.md)  
**Owner:** b90e4ba1 (#1778 sammelt ALLE katalog-luecken) / 0847d100 (read-only zensus)  
**Priority:** high  
**PRs:** [baseharbor#1774](https://github.com/mcpdev80/baseharbor/pull/1774), [baseharbor#1776](https://github.com/mcpdev80/baseharbor/pull/1776), [baseharbor#1777](https://github.com/mcpdev80/baseharbor/pull/1777), [baseharbor#1778](https://github.com/mcpdev80/baseharbor/pull/1778)  
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

#1774 head acd57828 = NUR eintrag B, normal PR run 45030308249 TERMINAL SUCCESS, native skipped (katalog-only, korrekt). review+merge an 1450c201 geroutet (unlockt #1770 native bei merge). A (ci-fast-check.sh) + C (app_footprint_presenter.go) NICHT in diesem head -> FOLGE-katalog-PR (b90e4ba1, 248 bleibt offen bis A+C+ #1746-static + #1773 entblockt). Kein merged PR ueberschreibt den anderen: folge PR rebased nach #1774-merge.

B (ci-native-pr-gate.sh) GEMERGED ueber #1774 @ 3cbb2bac (exact run 45030308249 SUCCESS). Das entblockt #1770 native docker+podman (owner hoppte #1770->2a4adca0, run 45030747445 queued). 0428-248 BLEIBT OFFEN fuer A+C (folgen in eigenem katalog-pr auf 3cbb2bac): A ci-fast-check.sh (unlockt #1746 static planner), C app_footprint_presenter.go (unlockt #1773/246).

#1775 geschlossen (war dirty dup-B). #1776 = test-only planner-test auf develop 7391946f (hosted CI laeuft). Die ECHTEN fehlenden mappings A(ci-fast-check.sh)+C(app_footprint_presenter.go)+243(local_workload_authority.go/_test/main.go) sind NICHT in develop (nur shell-ux vorhanden) und bleiben #1746-static/#1773/#1771 blockierer -> eigener sauberer 0428-248 mappings-pr (b90e4ba1).

#1776 (test-only planner-test) gemergt als 713aadd4. Die ECHTEN fehlenden mappings sind VIER saetze und laufen in EINEM sauberen 0428-248 mappings-pr auf develop 713aadd4: app_broker_diagnostics_test.go(#1763) + app_footprint_presenter.go(#1773) + local_workload_authority.go/_test.go/main.go(#1771) + scripts/ci-fast-check.sh(#1746-static). Ziel-surfaces atomic.* existieren. #1775 (dup+conflict) wird als superseded geschlossen (kein owner-replacement). b90e4ba1 dispatched fuer alle vier.

#1777 (branch lane-0428-248-catalog-mappings d9c1b895) deckt A(ci-fast-check)+C(footprint_presenter)+243(local_workload_authority/test/main) ab. EIN gap: app_broker_diagnostics_test.go (#1763) fehlt -> b90e amended #1777 additiv (kein neuer PR, kein dup-B, surfaces schema ok). Nach merge entblockt dieser eine PR #1763 #1771 #1773 #1746-static. develop 713aadd4.

#1777 GEMERGT als 68b26bd (exact run 45035683974). Katalog enthaelt A(ci-fast-check via static-surface)+C(app_footprint_presenter)+243(local_workload_authority/_test/main). EINZIGER rest: app_broker_diagnostics_test.go (#1763) -> b90e oeffnet MINI follow PR auf develop 68b26bd. #1773 owner re-hoppt additiv auf 68b26bd (presenter-docs, keine aktive lane). develop JETZT 68b26bd7.

#1777 merged 68b26bd. #1778 (draft head 5d9bd262, additive auf 68b26bd7) mappt app_broker_diagnostics_test.go -> #1763 trusted-planner cataloged:ja (draft run 45036510669 routing+go-shards success, planner bei ready). b90e ergaenzt #1778 um app_workload_ports.go + workload_port_local_regression_test.go (#1723). Nach merge: #1763 + #1723 entblockt. File existiert auf #1763 head 9bd97ca3 (mapping korrekt in beiden merge-reihenfolgen).

Whack-a-Mole beendet: 0847d100 faehrt katalog-luecken-zensus ueber alle offenen PRs -> komplette fehlende-paths liste. b90e deckt in #1778: broker-diag(#1763) + app_workload_ports/_regression(#1723) + perses-cluster(#1597: app_perses_cli_test.go/app_status_result.go/internal/metrics/perses_dashboards*.go) + rest laut zensus. develop 68b26bd7.
