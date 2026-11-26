---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "runtime list pagination"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-344 · runtime list pagination
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1872", "mcpdev80/baseharbor#1871"]
sources: []
blocker: "BASELINE ACT ACCEPTED: #1872 merge-ready-HELD (w255 7203347331, head 3ed6882e/run 45894876938 SUCCESS, 15/15 rows; PR body forbids merge). #1871 (969362e3) stays blocked: continue ONLY after actual #1872 landing on develop + fresh consumer exact-head CI; then lane absorbs develop and close+reopen per W46 recipe"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
    **PR:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
    **Blocker:** BASELINE ACT ACCEPTED: \#1872 merge-ready-HELD (w255 7203347331, head 3ed6882e/run 45894876938 SUCCESS, 15/15 rows; PR body forbids merge). \#1871 (969362e3) stays blocked: continue ONLY after actual \#1872 landing on develop + fresh consumer…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
**Priority:** not set  
**PRs:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.