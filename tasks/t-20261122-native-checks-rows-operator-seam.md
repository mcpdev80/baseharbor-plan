---
id: t-20261122-native-checks-rows-operator-seam
card_number: "0428-234"
card_short_title: "native_checks rows for PR 1750 sources"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-234 · native_checks rows for PR 1750 sources
priority: ""
depends_on: [t-20261122-native-gate-admission-rows]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md"]
superseded_by: t-20261122-native-gate-admission-rows
---

- [x] t-20261122-native-checks-rows-operator-seam · CI: give the operator seam and PR 1750 sources native_checks rows #task #release/v0.4.28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Needs:** [t-20261122-native-gate-admission-rows](t-20261122-native-gate-admission-rows.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-native-gate-admission-rows](t-20261122-native-gate-admission-rows.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this card exists and why it is closed as superseded

Measured at develop `1ff16925c4e141d732459a34ddf0b7f49128a214`: `PR · Selected Runtime` still skips at the hopped
heads of PR #1750 (`5d47569f3372`) and PR #1753 (`ce5cf8f30373`), because the trusted selector
`scripts/pr-native-gate-plan.py` resolves gates only from `scripts/pr-gate-coverage.json` - a `components` row whose
`path` matches a changed file plus a `native_checks` row naming that component. Neither the eight PR #1750 test
sources nor the three `cmd/baha/ci_integration_operator_*` sources have such rows; `native_checks` holds six rows in
total. PR #1755 landed the other two tables, which are necessary but not sufficient.

Full measurement, field shapes and the four-step recipe:
`evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md`.

The work belongs to card 0428-230, which already carries the native gate row gap, so this card is closed as
superseded by it rather than run as a second lane on the same write set.
