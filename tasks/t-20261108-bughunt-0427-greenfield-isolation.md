---
id: t-20261108-bughunt-0427-greenfield-isolation
card_number: "0427-133"
card_short_title: "Greenfield-Isolation offen"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w133-greenfield-r3
kanban_status: active
kanban_lane: active
kanban_summary: "An isolated greenfield run (BASEHARBORTARGET-selected second target, docker-2 style) completes bootstrap + core self-install +…"
kanban_title: "0427-133 · Greenfield-Isolation offen"
priority: normal
depends_on: [t-20261018-r27-access-wizard, t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1460]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/act-1451-review.md"]
---

- [ ] t-20261108-bughunt-0427-greenfield-isolation · Bug Hunt v0.4.27: Greenfield-Isolation offen #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w133-greenfield-r3 · **Priority:** normal  
    **PR:** [baseharbor#1460](https://github.com/mcpdev80/baseharbor/pull/1460)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/act-1451-review.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w133-greenfield-r3  
**Priority:** normal  
**PRs:** [baseharbor#1460](https://github.com/mcpdev80/baseharbor/pull/1460)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

An isolated greenfield run (BASEHARBOR_TARGET-selected second target, docker-2 style) completes bootstrap + core self-install + status without creating or mutating shared-plane objects; proven by a native docker AND podman cell in CI.

## Problem (split decision 2026-11-08)

act-1451-review.md: the 0427-124 production reader merged, but use/activate resolves through the management-connection binding whose authority belongs to access-wizard (#1430) and onboarding (#1435); the review requires this clause as a separate task.

## Acceptance

- Documented deterministic flow for isolated targets (use/activate honours the selected target's own core bootstrap); regression in CI; no shared-plane writes when operating an isolated target.

## Dependencies and file ownership

Depends on access-wizard acceptance (#1430). Write-set: cmd/baha target/use/activate paths + internal/deployment target-state reader.
