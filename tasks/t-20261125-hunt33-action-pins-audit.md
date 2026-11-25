---
id: t-20261125-hunt33-action-pins-audit
card_number: "0428-298"
card_short_title: "hunt33-action-pins-audit"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Pin the confirmed mutable third-party GitHub Actions refs in existing workflows to verified immutable commit SHAs, preserving…"
kanban_title: 0428-298 · hunt33-action-pins-audit
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/artifact-gc.yml#L25-L28","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-integration.yml#L178-L182"]
---

- [ ] t-20261125-hunt33-action-pins-audit · 0428 hunt H-V33: hunt33-action-pins-audit #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/artifact-gc.yml#L25-L28), [proof 5](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-integration.yml#L178-L182)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Pin the confirmed mutable third-party GitHub Actions refs in existing workflows to verified immutable commit SHAs, preserving each action's current version and workflow behavior.

## Scope

- In scope: the three actions/setup-node@v6 uses in .github/workflows/pre-release.yml; tag-only actions/checkout@v4 and actions/setup-python@v5 in .github/workflows/artifact-gc.yml; and actions/checkout@v7.0.1 plus actions/setup-go@v7 in .github/workflows/targeted-integration.yml. Inventory other external uses in the current workflow tree before declaring the audit complete.
- Out of scope: new workflows or CI frameworks, changes to triggers/jobs, and unrelated runner-image or product-code work.

## Acceptance

- Every external uses reference in the workflow tree is recorded as immutable SHA, mutable tag, or local reusable workflow; each mutable external ref has an explicit decision.
- Pin the confirmed tag-only refs to full commit SHAs verified against the corresponding action release; retain a human-readable version comment.
- Preserve job, trigger, permission, and artifact behavior.
- Validate workflow syntax with the existing workflow checks; no new pipeline or broad runtime matrix.
- Record the source SHA and changed workflow lines in the handoff.

## Evidence

- Three setup-node@v6 refs: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503, https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720, https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937
- Tag-only checkout and setup-python refs: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/artifact-gc.yml#L25-L28
- Tag-only checkout and setup-go refs: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/targeted-integration.yml#L178-L182
