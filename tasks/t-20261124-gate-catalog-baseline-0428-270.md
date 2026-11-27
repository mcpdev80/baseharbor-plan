---
id: t-20261124-gate-catalog-baseline-0428-270
card_number: "0428-275"
card_short_title: "add #1820-sib catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "w388-0428-329-1861recipe"
kanban_status: active
kanban_lane: active
kanban_summary: "Unblock 0428-270 (PR head 88f5c7f05, w61). Exact-head CI run 45326369749 aborts in 'PR Trusted Plan' with fail-loud 'uncataloged…"
kanban_title: "0428-275 · add #1820-sib catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45326369749", "https://github.com/mcpdev80/baseharbor-plan/pull/196"]
---

- [ ] t-20261124-gate-catalog-baseline-0428-270 · CI/catalog: add operatorauth rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w388-0428-329-1861recipe  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45326369749), [proof 2](https://github.com/mcpdev80/baseharbor-plan/pull/196)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w388-0428-329-1861recipe  
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

## Status reconciliation history (2026-11-27)

Prior wait reason retained verbatim: `Codex disposition is published in Plan PR #196; hold until the existing 0428-359 card in Plan PR #136 carries the corrected family scope and the develop-side catalog baseline can proceed.`
