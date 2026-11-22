---
id: t-20261122-static-cells-operator-auth-helper
card_number: "0428-231"
card_short_title: "operator auth in static cells"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-231 · operator auth in static cells
priority: ""
depends_on: [t-20261121-develop-full-suite-red]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-static-cells-operator-auth-helper · operator auth in static cells #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->


## Why

Measured by lane `b90e4ba1` (akte
evidence/r28-welle5-2026-11-22/develop-full-suite-red/diagnose-1.md): the helper
`testIsolatedSelectionContext` exists in 7 files at head f16cef27 of PR #1750 and in 0 files at develop 8b9a8f50645 -
so most of these cells clear when #1750 merges. This card stays open only for the parts that survive that merge.


At head `fec44963` of PR #1746 the full Pre-Release run `44980411417` fails in several cells with the same guard:
`Static · init` job 137080600559, `Static · shell-ux` job 137080600541, `Static · config-matrix` job 137080600642,
plus `Integration · integration/docker/core-bootstrap` job 137080600131 and
`Integration · integration/podman/core-bootstrap` job 137080600055 all print
`Managed-environment machine operations require an authenticated BaseHarbor operator.`

That message comes from `cmd/baha/mcp.go:317`. The helper that satisfies it inside a test process already exists
(`runWithIOAsTestOperator`, used by `cmd/baha/env_destroy_integration_test.go:127`), but these cells still drive the
machine paths through the interactive operator path, so they fail regardless of which product PR runs them.

## Acceptance

- The failing init / shell-ux / config-matrix / core-bootstrap paths use the same non-interactive operator helper that
  #1750 delivers for env destroy, so the guard is satisfied without a terminal.
- Hosted CI shows the five jobs above green at one exact head; no local run counts.
