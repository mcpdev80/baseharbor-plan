---
id: t-20261128-hunt49-archived-gates-validator-blindspot
card_number: "0428-340"
card_short_title: "detect archived gate names"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-340 · detect archived gate names
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/scripts/pr-gate-coverage.json#L1-L6","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/scripts/test_ci_v0427_gate_catalog.py#L40-L75","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv49-gate-vocabulary/w192-0428-224-hunt-v49.md"]
---

- [x] t-20261128-hunt49-archived-gates-validator-blindspot · 0428 hunt H-V49: archived gate catalog distinction #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/scripts/pr-gate-coverage.json#L1-L6), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/scripts/test_ci_v0427_gate_catalog.py#L40-L75), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv49-gate-vocabulary/w192-0428-224-hunt-v49.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Disposition

DROP after current-source recheck. The coverage catalog is intentionally anchored to `v0.4.27`; the three consumer gates are historical archived entries in `release-requirements.json`, not required gates for that active catalog. Existing `test_ci_v0427_gate_catalog.py` asserts that these gates are excluded from v0.4.27 selection. The proposed set-equality rule would need a permanent archive exception list and protects only a hypothetical future edit; it does not identify a current false-green or release-0.4.28 gap. When the active catalog advances, the validator already requires every gate whose `required_for` contains that active release.
