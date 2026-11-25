---
id: t-20261125-hunt33-shell-failfast
card_number: "0428-301"
card_short_title: "hunt33-shell-failfast"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-301 · hunt33-shell-failfast
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L343-L350","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1254-L1262","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1694-L1698"]
---

- [x] t-20261125-hunt33-shell-failfast · 0428 hunt H-V33: hunt33-shell-failfast #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L343-L350), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1254-L1262), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1694-L1698)  
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

The finding is false on current develop (3a2ae6b1139570c98b8924e3b19975c56a289400). Both shell-matrix setup steps explicitly install zsh and fish before running the matrix. The wrapper test also exercises the supported shell selection. The proposed extra missing-binary fixture guard duplicates the existing install-and-run contract; there is no absent-shell skip that can make the gate green.

### Evidence

- First CI setup installs both shells: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L343-L350
- Second CI setup installs both shells: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1254-L1262
- Shell wrapper regression: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L1694-L1698

### Original finding

H-V33 suspected that an absent zsh or fish could silently skip matrix coverage. The live workflow installs both dependencies and fails if setup or execution fails.
