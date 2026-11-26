---
id: t-20261124-gate-catalog-baseline-0428-270
card_number: "0428-275"
card_short_title: "add #1820-sib catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w65-0428-269-batchbaseline
kanban_status: wait
kanban_lane: wait
kanban_summary: "Unblock 0428-270 (PR head 88f5c7f05, w61). Exact-head CI run 45326369749 aborts in 'PR Trusted Plan' with fail-loud 'uncataloged…"
kanban_title: "0428-275 · add #1820-sib catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "stale claim reconciled at owner harvest 2026-11-26 (14:22Z roster: only w322+w327 live): no worker behind the active state; baseline rows re-evaluated together with #1859-era catalog work"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45326369749"]
---

- [ ] t-20261124-gate-catalog-baseline-0428-270 · CI/catalog: add operatorauth rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** w65-0428-269-batchbaseline  
    **Waiting:** stale claim reconciled at owner harvest 2026-11-26 (14:22Z roster: only w322+w327 live): no worker behind the active state; baseline rows re-evaluated together with \#1859-era catalog work  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45326369749)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w65-0428-269-batchbaseline  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal
Unblock 0428-270 (PR head 88f5c7f05, w61). Exact-head CI run 45326369749 aborts in 'PR Trusted Plan' with fail-loud 'uncataloged source change' because scripts/pr-gate-plan.py has no gate owner for two files changed here for the first time on develop.

## Required catalog rows (from run 45326369749 Trusted Plan log)
Add to scripts/pr-gate-coverage.json on develop, surfaces docker + podman data.capabilities:
- internal/operatorauth/authorization.go (id source.internal_operatorauth_authorization_go)
- internal/operatorauth/config.go (id source.internal_operatorauth_config_go)

## Ownership / scope
OWNER/CI scope (scripts/** + gate catalog), separate baseline on develop (#1817; cf. 0428-261/262/273/274). After it lands, w61 rebases 0428-270 + reruns exact-head, then Owner accept+merge.

Realized by owner-authorized batch baseline PR (w65): 6 catalog rows + pre-release.yml baha-ci-operator-testonly production. Lands on develop -> unblocks #1819/#1820/#1821/#1812 rebase+rerun.
