---
id: t-20261117-trace-probe-adapter-gap
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-108"
title: "runtimeComponentTraceProbe lacks trace-consumer adapter for prometheus sources"
kanban_status: active
kanban_lane: active
kanban_title: 0428-108 · runtimeComponentTraceProbe
kanban_summary: ""
sources: []
source_note: "0428-093 lane diagnose-pflicht END_BLOCKED (akte: evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md); PR zu frueh geoeffnet, candidate unvollstaendig bis restauration; run auf af2fb5f6 zaehlt nicht"
depends_on: []
owner: traceprobe (mission-108 lane)
blocker: ""
resolution: ""
superseded_by: ""
prs: [mcpdev80/baseharbor#1679]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md", "https://github.com/mcpdev80/baseharbor/pull/1679", "https://github.com/mcpdev80/baseharbor/actions/runs/44040963470"]
card_short_title: runtimeComponentTraceProbe
---

- [ ] t-20261117-trace-probe-adapter-gap · runtimeComponentTraceProbe lacks trace-consumer adapter #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** traceprobe (mission-108 lane)  
    **PR:** [baseharbor#1679](https://github.com/mcpdev80/baseharbor/pull/1679)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1679), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44040963470)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-102](t-20261117-hunt-signals-102.md)  
**Owner:** traceprobe (mission-108 lane)  
**Priority:** not set  
**PRs:** [baseharbor#1679](https://github.com/mcpdev80/baseharbor/pull/1679)  
**Source:** 
<!-- /generated:links -->


## 2026-11-17 candidate status

- PR #1679 is open at exact head `af2fb5f6fac1c8a56079a2fe18faecbb06fc2315`, based on `develop`; exact run [44040963470](https://github.com/mcpdev80/baseharbor/actions/runs/44040963470) failed Go unit shards, build, vet, and selected checks. This head is incomplete: the lane worktree has additive commit `1b5a0df37` with the production trace receiver adapter/pruning files, while the work was still restoring omitted intent-removal and project-scope regression changes. The run is not acceptance evidence.
- Latest verified BaseHarbor `origin/develop` is `4094448543359a13ba312119304f1f70d3bc40a9`. Keep 0428-108 active; require a clean complete candidate and a new exact-head CI run.
