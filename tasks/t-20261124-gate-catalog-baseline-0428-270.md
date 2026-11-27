---
id: t-20261124-gate-catalog-baseline-0428-270
card_number: "0428-275"
card_short_title: "add #1820-sib catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "w383-0428-275-136rows (prework: hop/classification only - qualification stays after plan 136 / 183 merge per card blocker)"
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
wait_reason: "lane released; awaiting Codex/Owner content disposition under the 2026-11-27 sweep resume (per-card holds apply)"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45326369749"]
---

- [ ] t-20261124-gate-catalog-baseline-0428-270 · CI/catalog: add operatorauth rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w383-0428-275-136rows (prework: hop/classification only - qualification stays after plan 136 / 183 merge per card blocker)  
    **Waiting:** lane released; awaiting Codex/Owner content disposition under the 2026-11-27 sweep resume (per-card holds apply)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45326369749)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w383-0428-275-136rows (prework: hop/classification only - qualification stays after plan 136 / 183 merge per card blocker)  
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
