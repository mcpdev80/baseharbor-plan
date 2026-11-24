---
id: t-20261124-gate-catalog-baseline-1819
card_number: "0428-273"
card_short_title: "add #1819 catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w65-0428-269-batchbaseline
kanban_status: active
kanban_lane: active
kanban_summary: "Unblock #1819 / card 0428-181 (identity dashboard catalog consumer). Exact head 69f76b94 fails Trusted Plan because three…"
kanban_title: "0428-273 · add #1819 catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45320885286"]
---

- [ ] t-20261124-gate-catalog-baseline-1819 · CI/catalog: add #1819 source rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w65-0428-269-batchbaseline  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45320885286)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w65-0428-269-batchbaseline  
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
