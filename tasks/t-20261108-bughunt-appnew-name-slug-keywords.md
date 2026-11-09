---
id: t-20261108-bughunt-appnew-name-slug-keywords
card_number: "0427-139"
card_short_title: "Name reshaped silently"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing…"
kanban_title: 0427-139 · Name reshaped silently
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1465]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42478010118", "https://github.com/mcpdev80/baseharbor/commit/618d23bde0870391541a8bbdf3ee103f22d70560"]
---
- [x] t-20261108-bughunt-appnew-name-slug-keywords · Bug Hunt v0.4.27: Name silently reshaped #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42478010118), [proof 3](https://github.com/mcpdev80/baseharbor/commit/618d23bde0870391541a8bbdf3ee103f22d70560)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1465](https://github.com/mcpdev80/baseharbor/pull/1465)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing field.

## Problem (source evidence in the dossier)
app new silently slugifies input (My App!! -> my-app) and accepts reserved words like cancel as a name. Source: hunt H-D3 BF-03/BF-04.

## Acceptance
Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing field.

## Dependencies and file ownership
None. Write-set: cmd/baha app new name validation.


## PR #1465 — CI and acceptance (closed)

- PR [#1465](https://github.com/mcpdev80/baseharbor/pull/1465) merged into develop as `618d23bde0870391541a8bbdf3ee103f22d70560`, exact PR head `933b3380ca107b7bfcb81100aa77b6f7fc0e3446`. [CI run 42478010118](https://github.com/mcpdev80/baseharbor/actions/runs/42478010118) completed SUCCESS, including selected checks, build/vet, Go-unit and native Docker/Podman destroy retry.
- Visible slug normalization and rejection of reserved navigation names are exercised by the production wizard path and targeted regression; the card is accepted and the worker claim released.
