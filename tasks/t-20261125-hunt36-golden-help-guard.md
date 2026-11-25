---
id: t-20261125-hunt36-golden-help-guard
card_number: "0428-306"
card_short_title: "add golden --help snapshot CI"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-306 · add golden --help snapshot CI
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/main_test.go#L20-L43","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/human_documentation_test.go#L74-L110","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-26/bughunt-hv36-config-surface/index.md#findings-per-row"]
---

- [x] t-20261125-hunt36-golden-help-guard · 0428 hunt H-V36: add golden --help snapshot CI guard for config/flag surface #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/main_test.go#L20-L43), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/human_documentation_test.go#L74-L110), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-26/bughunt-hv36-config-surface/index.md#findings-per-row)  
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

### Disposition: DROP

The source audit found no config, flag, help-ordering, environment-name, or default drift. Current tests already exercise root and nested help and compare the generated bilingual command index against the shipped command tree. A broad golden snapshot would lock cosmetic output without protecting a demonstrated defect and adds CI maintenance for no current release gap.

### Evidence

- Root and nested help behavior: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/main_test.go#L20-L43
- Generated EN/DE command index matches the actual command tree: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/human_documentation_test.go#L74-L110
- H-V36 audit: config/flag surface internally consistent; no blocking drift: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-26/bughunt-hv36-config-surface/index.md#findings-per-row
