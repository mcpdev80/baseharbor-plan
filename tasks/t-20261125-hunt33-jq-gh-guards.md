---
id: t-20261125-hunt33-jq-gh-guards
card_number: "0428-300"
card_short_title: "hunt33-jq-gh-guards"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-300 · hunt33-jq-gh-guards
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L667-L671","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release-runtime-suite.yml#L100-L103","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-demo-acceptance.yml#L83-L108"]
---

- [x] t-20261125-hunt33-jq-gh-guards · 0428 hunt H-V33: hunt33-jq-gh-guards #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L667-L671), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release-runtime-suite.yml#L100-L103), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-demo-acceptance.yml#L83-L108)  
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

The finding is not a false-green path on current develop (3a2ae6b1139570c98b8924e3b19975c56a289400). The cited gh, jq and base64 calls run in strict shell steps; a missing executable terminates the step rather than skipping a check or returning success. These are GitHub-hosted Ubuntu runner prerequisites, not product dependencies. Adding command -v wrappers would duplicate fail-fast shell behavior and create no user-visible fix.

### Evidence

- CI runner call sites and strict shell: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/ci.yml#L667-L671
- Runtime suite gh/JSON calls: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release-runtime-suite.yml#L100-L103
- Targeted demo gh and base64 --decode calls under set -euo pipefail: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-demo-acceptance.yml#L83-L108

### Original finding

H-V33 proposed guards for host-side gh, jq, and base64. Source recheck shows missing tools fail the invoking step; no silent-success case remains to fix.
