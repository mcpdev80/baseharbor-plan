---
id: t-20261108-bughunt-appnew-eof-cancel-prompts
card_number: "0427-138"
card_short_title: "Wizard cancel uneven"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-eof"
kanban_status: active
kanban_lane: active
kanban_summary: "A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group."
kanban_title: 0427-138 · Wizard cancel uneven
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1471]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md"]
---
- [ ] t-20261108-bughunt-appnew-eof-cancel-prompts · Bug Hunt v0.4.27: Wizard cancel is uneven #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-eof · **Priority:** normal  
    **PR:** [baseharbor#1471](https://github.com/mcpdev80/baseharbor/pull/1471)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-eof  
**Priority:** normal  
**PRs:** [baseharbor#1471](https://github.com/mcpdev80/baseharbor/pull/1471)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group.

## Problem (source evidence in the dossier)
EOF/empty input on app-new prompts returns a usageError instead of a clean wizard cancel; Ctrl-D is interpreted differently per prompt. Source: hunt H-D3 BF-01/BF-02.

## Acceptance
A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group.

## Dependencies and file ownership
None. Write-set: cmd/baha app new wizard prompts.


## Code/PR owner — 2026-11-08

- Claimed for [PR #1471](https://github.com/mcpdev80/baseharbor/pull/1471): top-level `baha new` EOF cancellation now has a single clean return, and early app-new name/location/stack EOF regressions verify no project creation. Existing pre-consent cancellation test retained.
- Exact PR CI is pending; card remains `active` until full prompt matrix and acceptance. No conflicting worker claim.
