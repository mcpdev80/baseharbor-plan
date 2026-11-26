---
id: t-20261124-gate-catalog-baseline-1819
card_number: "0428-273"
card_short_title: "add #1819 catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w328-0428-273-pr1819pre
kanban_status: wait
kanban_lane: wait
kanban_summary: "Unblock #1819 / card 0428-181 (identity dashboard catalog consumer). Exact head 69f76b94 fails Trusted Plan because three…"
kanban_title: "0428-273 · add #1819 catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "disjoint prework complete (w328 akte PR #129, CI 45827274740 GREEN, census=0 rows owed after #1859); w328 released - no live worker, claim reconciled to wait; rebase/qualification deferred until #1812 merges (chain #1812 -> #1819 -> #1820)"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45320885286"]
---

- [ ] t-20261124-gate-catalog-baseline-1819 · CI/catalog: add #1819 source rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** w328-0428-273-pr1819pre  
    **Waiting:** disjoint prework complete (w328 akte PR \#129, CI 45827274740 GREEN, census=0 rows owed after \#1859); w328 released - no live worker, claim reconciled to wait; rebase/qualification deferred until \#1812 merges (chain \#1812 -\> \#1819 -\> \#1820)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45320885286)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w328-0428-273-pr1819pre  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Unblock #1819 / card 0428-181 (identity dashboard catalog consumer). Exact head 69f76b94 fails Trusted Plan because three introduced source paths have no declared gate owner in `scripts/pr-gate-coverage.json`, so the planner rejects and every downstream Go/runtime job skips.

## Required catalog rows (from run 45320885286 Trusted Plan log)

Add to `scripts/pr-gate-coverage.json` on develop, each with surfaces docker + podman data.capabilities:
- `internal/application/runtime_postgres.go` (id source.internal_application_runtime_postgres_go)
- `internal/metrics/perses_dashboard_provision.go` (id source.internal_metrics_perses_dashboard_provision_go)
- `internal/metrics/perses_dashboard_provision_test.go` (id source.internal_metrics_perses_dashboard_provision_test_go)

## Ownership / scope

- OWNER/CI scope (scripts/** + gate catalog). Implement as a separate baseline PR landing on develop (precedent #1817; cf. 0428-261 #1816, 0428-262 #1650), NOT inside #1819.
- After the rows land on develop: 0428-181/w54 rebases #1819 onto the new develop head and reruns exact-head; then #1819 → Owner accept+merge → #1818 dependency satisfied → #1818 → Owner accept.

## Dependencies and file ownership

- Owned files: scripts/pr-gate-coverage.json (owner/CI).
- Product files (runtime_postgres.go, perses_dashboard_provision*.go) are owned by #1819 (0428-181), not this card.

Realized by owner-authorized batch baseline PR (w65): 6 catalog rows + pre-release.yml baha-ci-operator-testonly production. Lands on develop -> unblocks #1819/#1820/#1821/#1812 rebase+rerun.

## Handoff

- AUTGELÖST 2026-11-25 (Owner-Lesart zur Mehrdeutigkeit #1819): disjunkte Vorarbeit darf parallel laufen; Rebase/Qualifikation/Merge bleiben strikt NACH #1812 (Serie #1812->#1819->#1820). Kein Freeze, keine Umordnung.


## Coordinator provenance disposition (2026-11-26)

- Catalog-row result: the requested #1819 catalog rows are already present exactly once through BaseHarbor PR [#1822](https://github.com/mcpdev80/baseharbor/pull/1822), merged at `90086a1f938e106171b08c76e9bcbc98d89d1de4`. No further catalog edit or dispatch is needed for those rows.
- #1812 14-gate pre-flight: NOT qualified by the #1650 run. Live #1650 is open at head `37c4d847ca377d1555163ac4791c8ba08b85de77` on develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`; run [45663047993](https://github.com/mcpdev80/baseharbor/actions/runs/45663047993) is green for old head `1c33e910070a07a6d4105f0d38e3c89988a788a3`. That run's four selected runtime jobs were Docker data-capabilities, Docker observability, Podman data-capabilities, and Podman observability; it is not the exact current PR head and does not establish the separate #1812 14-Light-gate qualification. Keep the #1812 pre-flight unqualified pending exact-head evidence.
- w258's #1819 pre-flight content is sound for its stated point-in-time refs, including the catalog and ancestry findings, but its akte was published by direct-main commit `053b2b6d1` with no associated PR. It is not qualified acceptance evidence. The compliant recovery akte records the finding and channel disposition; the original commit and akte remain unchanged.
