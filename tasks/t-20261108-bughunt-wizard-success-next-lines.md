---
id: t-20261108-bughunt-wizard-success-next-lines
card_number: "0427-142"
card_short_title: "Success omits next step"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-wizard-ux"
kanban_status: review
kanban_lane: review
kanban_summary: "Success/next text consistent across all create paths (wizard, headless, alias, top-level); prompt input errors as usageError…"
kanban_title: 0427-142 · Success omits next step
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1465, mcpdev80/baseharbor#1469]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42480609018", "https://github.com/mcpdev80/baseharbor/commit/f05d6ee2e596da73056dfd1bda64a79ebbfe6b92"]
---
- [ ] t-20261108-bughunt-wizard-success-next-lines · Bug Hunt v0.4.27: Success omits next step #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-wizard-ux · **Priority:** normal  
    **PR:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465), [baseharbor#1469](https://github.com/mcpdev80/baseharbor/pull/1469)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42480609018), [proof 3](https://github.com/mcpdev80/baseharbor/commit/f05d6ee2e596da73056dfd1bda64a79ebbfe6b92)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-wizard-ux  
**Priority:** normal  
**PRs:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465), [baseharbor#1469](https://github.com/mcpdev80/baseharbor/pull/1469)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Success/next text consistent across all create paths (wizard, headless, alias, top-level); prompt input errors as usageError with a Next line; regressions in the cli-surface group.

## Problem (source evidence in the dossier)
Create-only and headless success paths give different or missing success/next-step text; yes/no input errors harden with exit 1 and no Next block (fmt.Errorf instead of usageError). Source: hunt H-P1 BF-01/BF-03/BF-07.

## Acceptance
Success/next text consistent across all create paths (wizard, headless, alias, top-level); prompt input errors as usageError with a Next line; regressions in the cli-surface group.

## Dependencies and file ownership
None. Write-set: cmd/baha app new + wizard message paths.


## Ownership and code link — 2026-11-08

- Claimed by `chatgpt-r27-wizard-ux` for the remaining CLI-surface scope, while merged [#1465](https://github.com/mcpdev80/baseharbor/pull/1465) already unified create-only/headless next instructions.
- [#1469](https://github.com/mcpdev80/baseharbor/pull/1469) adds structured invalid yes/no input errors and a Next action after verified wizard-run success. Exact-head CI pending; no acceptance or closure claimed.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): success-vs-error text overlap with #138 cancel path and #145 raw-mode messaging - keep separate contracts, cross-reference in fixes. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## Merge and review — 2026-11-08

- PR [#1469](https://github.com/mcpdev80/baseharbor/pull/1469) merged to `develop` as `f05d6ee2e596da73056dfd1bda64a79ebbfe6b92` (exact head `7458eca9e4990c8f7af45fecde9079da09856531`). [CI #42480609018](https://github.com/mcpdev80/baseharbor/actions/runs/42480609018) terminal SUCCESS, including Go-unit, build, vet and Docker/Podman native destroy-retry.
- Targeted change: `promptYesNo` errors now carry structured usage guidance; verified `run` wizard emits `Next: baha app status`. Combined with #1465, headless/create-only share the same init/up guidance.
- `review` rather than `closed`: exact end-to-end/alias user-facing output matrix for every entry point was not run in this review; the additional top-level interactive `baha new` choice error path remains a candidate for confirmation. No synthetic PASS.
