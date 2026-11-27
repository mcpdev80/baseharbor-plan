---
id: t-20261124-gate-catalog-baseline-0428-270
card_number: "0428-275"
card_short_title: "add #1820-sib catalog rows"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Unblock 0428-270 (PR head 88f5c7f05, w61). Exact-head CI run 45326369749 aborts in 'PR Trusted Plan' with fail-loud 'uncataloged…"
kanban_title: "0428-275 · add #1820-sib catalog rows"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1817"]
sources: []
blocker: ""
wait_reason: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1817", "https://github.com/mcpdev80/baseharbor/commit/6df6807e7651b38fc142559ea9780238264b6d8f", "https://github.com/mcpdev80/baseharbor/blob/ea5218d72e263f21e79853b679af50074dab8c25/scripts/pr-gate-coverage.json#L1663", "https://github.com/mcpdev80/baseharbor/blob/ea5218d72e263f21e79853b679af50074dab8c25/scripts/pr-gate-coverage.json#L1671", "https://github.com/mcpdev80/baseharbor-plan/blob/1990688d09dc552ea45614ff7d66a46c390fccd9/evidence/2026-11-27/0428-275/codex-disposition-136.md", "https://github.com/mcpdev80/baseharbor-plan/blob/1990688d09dc552ea45614ff7d66a46c390fccd9/evidence/w388-0428-275-rowdiff/akte.md", "https://github.com/mcpdev80/baseharbor/actions/runs/45326369749", "https://github.com/mcpdev80/baseharbor-plan/pull/196"]
---

- [x] t-20261124-gate-catalog-baseline-0428-270 · CI/catalog: add operatorauth rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1817](https://github.com/mcpdev80/baseharbor/pull/1817)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1817), [proof 2](https://github.com/mcpdev80/baseharbor/commit/6df6807e7651b38fc142559ea9780238264b6d8f), [proof 3](https://github.com/mcpdev80/baseharbor/blob/ea5218d72e263f21e79853b679af50074dab8c25/scripts/pr-gate-coverage.json#L1663), [proof 4](https://github.com/mcpdev80/baseharbor/blob/ea5218d72e263f21e79853b679af50074dab8c25/scripts/pr-gate-coverage.json#L1671), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/1990688d09dc552ea45614ff7d66a46c390fccd9/evidence/2026-11-27/0428-275/codex-disposition-136.md), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/1990688d09dc552ea45614ff7d66a46c390fccd9/evidence/w388-0428-275-rowdiff/akte.md), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/45326369749), [proof 8](https://github.com/mcpdev80/baseharbor-plan/pull/196)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1817](https://github.com/mcpdev80/baseharbor/pull/1817)  
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

## Status reconciliation (2026-11-27)

The required catalog baseline landed in product PR #1817, merged at `6df6807e7651b38fc142559ea9780238264b6d8f`. The PR diff is limited to `scripts/pr-gate-coverage.json`. On `develop` `ea5218d72e263f21e79853b679af50074dab8c25`, `source.internal_operatorauth_authorization_go` is present at line 1663 and `source.internal_operatorauth_config_go` at line 1671. The required rows are therefore delivered; this card is closed as accepted and its prior owner assignment is cleared.

Session witness: `codeman agent list --json` showed session `8873ac0c-5570-4fdf-8c15-fdb85569f8df`, named `w388-0428-329-1861recipe`, status `busy`, `isWorking: true`, working directory `/home/marcel/dev/baseharbor-ecosystem/workers/.models/ornith`. Its registered card is 0428-329, so it is not evidence of active work on this completed 0428-275 card.

Evidence-scope note: the linked `evidence/w388-0428-275-rowdiff/akte.md` ends as `w388-0428-216-blobcensus` and covers other catalog rows; it is retained only as contextual material and is not relied on to prove the two operatorauth rows. The completion proof is PR #1817, its merge commit, and the pinned `develop` catalog entries above.
