---
id: t-20261113-r28-current-contract-inventory
card_number: "0428-008"
card_short_title: "Audit Core Console gaps"
type: task
areas: [architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Audit only the existing Console live/preview route inventory against the accepted Core 0.4.27 machine contract. Inspect console…
kanban_title: "0428-008 · Audit Core Console gaps"
priority: high
depends_on: [t-20261017-release-0-4-28-updates]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md"]
early: true
---

- [x] t-20261113-r28-current-contract-inventory · Audit Core Console gaps #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
**Required by:** [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Audit only the existing Console live/preview route inventory against the accepted Core 0.4.27 machine contract. Inspect console PR #8; identify exactly which semantic operations and tests exist versus missing. No product edits.

## Acceptance

One table route | current implementation | Core operation | proof | missing integration. No invented functionality; coordinator can assign subsequent cards based on this report.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates.
- **Exclusive write ownership:** Planning audit note in this card only; Core and Console read-only.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

List source commit SHAs, endpoints, file paths, tests, CI triggers, results; no new test or native run.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.
