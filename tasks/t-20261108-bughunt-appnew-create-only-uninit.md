---
id: t-20261108-bughunt-appnew-create-only-uninit
card_number: "0427-140"
card_short_title: "app new left uninit"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-appnew"
kanban_status: review
kanban_lane: review
kanban_summary: "Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale;…"
kanban_title: 0427-140 · app new left uninit
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1465]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42478010118", "https://github.com/mcpdev80/baseharbor/commit/618d23bde0870391541a8bbdf3ee103f22d70560"]
---
- [ ] t-20261108-bughunt-appnew-create-only-uninit · Bug Hunt v0.4.27: app new left uninit #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-appnew · **Priority:** normal  
    **PR:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42478010118), [proof 3](https://github.com/mcpdev80/baseharbor/commit/618d23bde0870391541a8bbdf3ee103f22d70560)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-appnew  
**Priority:** normal  
**PRs:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale; regression in the lifecycle path.

## Problem (source evidence in the dossier)
The create-only path of app new leaves a repository without init state; up/plan/show then demand init - a flow gap (medium, investigate). Source: hunt H-D3 BF-09; reinforced by hunt H-P1 BF-04 (create-only on an ownerless target reports project created but ... with no recovery path).

## Acceptance
Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale; regression in the lifecycle path.

## Dependencies and file ownership
None. Write-set: cmd/baha app new + init seam.


## PR #1465 — CI and acceptance (review)

- PR [#1465](https://github.com/mcpdev80/baseharbor/pull/1465) merged into develop as `618d23bde0870391541a8bbdf3ee103f22d70560`, exact PR head `933b3380ca107b7bfcb81100aa77b6f7fc0e3446`. [CI run 42478010118](https://github.com/mcpdev80/baseharbor/actions/runs/42478010118) completed SUCCESS, including selected checks, build/vet, Go-unit and native Docker/Podman destroy retry.
- The create-only UX now prints a documented init/up sequence in wizard and headless paths; unit regression verifies the sequence. The card remains review because an actual generated project -> app init -> up lifecycle success is not established by this output test. No false runtime PASS.
