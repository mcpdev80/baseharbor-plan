---
id: t-20261120-other-domain-test-split
card_number: "0428-206"
card_short_title: "Other-domain test split"
type: bug
areas: [cli, ci]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-206 · Other-domain test split
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-other-domain-test-split · Cause split for the 89 other-domain cmd/baha failures #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why

`evidence/r28-welle4-2026-11-20/cli-test-inventory-develop/round-1.md` (sitz w217, read-only, plan-main 0dec6779) measured
`go test ./cmd/baha/ -count=1` at develop `40cb28c758b0`: **206 failing tests** (181 first-level), grouped by entry class
`runWithIO=82`, **other-domain=89**, `MCP=10`, `rootCommand-direct=0`. 0428-204 carries the operator-seam classes. If the 89
stay unsplit, 0428-204 grows past one card (AGENTS 4.2 forbids that) or real defects stay invisible.

## What

1. Take the 89 from the 217 dossier (do not re-invent the list; report any line you cannot place).
2. Group by the FIRST FAILING PRODUCTION FILE, one line per group: `file:line`, count, verbatim first error.
3. Assign each group exactly one rubric:
   - (a) already covered by an open card - name the card (`git grep` over baseharbor-plan tasks),
   - (b) new defect - draft the card text here (title, acceptance, write-set, dependencies),
   - (c) fallout of commit `3653369a4` (#1717: `internal/operatorauth/authorization.go`, `cmd/baha/local_workload_authority.go`, `cmd/baha/mcp.go`) - prove it with `git log -S` and the green/red pair `f5ce95af` -> `3653369a`.

## Acceptance

- Evidence-only: no product file changes, no PR required.
- All 89 appear in exactly one group; every group carries a rubric and a witness.
- Groups judged (b) are turned into cards by the coordinator in the same turn (fund-to-card duty, AGENTS 3.3.5).
