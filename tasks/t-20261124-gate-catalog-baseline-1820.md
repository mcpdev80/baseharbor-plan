---
id: t-20261124-gate-catalog-baseline-1820
card_number: "0428-274"
card_short_title: "add #1820 catalog row"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)
kanban_status: wait
kanban_lane: wait
kanban_summary: "Unblock #1820 / card 0428-271 (verifyRuntimeBrokerBuildIdentity commit check). Exact head f5e50f5a fails Trusted Plan because…"
kanban_title: "0428-274 · add #1820 catalog row"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/45322832347"]
---

- [ ] t-20261124-gate-catalog-baseline-1820 · CI/catalog: add #1820 source row to develop pr-gate-coverage.json #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45322832347)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261124-r28-broker-build-identity-commit](t-20261124-r28-broker-build-identity-commit.md)  
**Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Unblock #1820 / card 0428-271 (verifyRuntimeBrokerBuildIdentity commit check). Exact head f5e50f5a fails Trusted Plan because the introduced test source has no declared gate owner in scripts/pr-gate-coverage.json; PR Selected Checks then fails and all required runtime jobs skip.

## Required catalog row (from run 45322832347 Trusted Plan log)

Add to scripts/pr-gate-coverage.json on develop, surfaces docker + podman data.capabilities:
- cmd/baha/app_broker_compat_test.go (id source.cmd_baha_app_broker_compat_test_go)

## Ownership / scope

- OWNER/CI scope (scripts/** + gate catalog). Land as a separate baseline on develop, NOT inside #1820 (#1817 precedent; cf. 0428-261/262/273).
- After it lands: w60 rebases #1820 onto the new develop head + reruns exact-head; then #1820 -> Owner accept+merge.

Realized by owner-authorized batch baseline PR (w65): 6 catalog rows + pre-release.yml baha-ci-operator-testonly production. Lands on develop -> unblocks #1819/#1820/#1821/#1812 rebase+rerun.
