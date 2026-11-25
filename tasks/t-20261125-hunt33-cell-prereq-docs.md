---
id: t-20261125-hunt33-cell-prereq-docs
card_number: "0428-296"
card_short_title: "hunt33-cell-prereq-docs"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Document the actual host and container prerequisites of the existing runtime acceptance lanes for maintainers, so local…"
kanban_title: 0428-296 · hunt33-cell-prereq-docs
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/runtime-s3-acceptance.yml#L190-L198","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/docs/development/pre-release-readiness.md#L1-L33"]
---

- [ ] t-20261125-hunt33-cell-prereq-docs · 0428 hunt H-V33: hunt33-cell-prereq-docs #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/runtime-s3-acceptance.yml#L190-L198), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/docs/development/pre-release-readiness.md#L1-L33)  
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

Document the actual host and container prerequisites of the existing runtime acceptance lanes for maintainers, so local reproduction distinguishes host Docker/Compose from utilities supplied inside provider images.

## Scope

- In scope: add a short maintainer-facing prerequisite note to docs/development/pre-release-readiness.md, including the existing runtime gates and that SeaweedFS acceptance invokes weed shell inside the SeaweedFS container image.
- Out of scope: product user documentation, changing workflow commands or images, new jobs/pipelines, and pinning the GitHub-hosted runner image.

## Acceptance

- State the host requirements separately from tools provided by test containers.
- Name the existing Docker and rootless Podman acceptance routes and identify the SeaweedFS image-provided weed shell dependency.
- Keep the note consistent with workflow behavior; no workflow or product-code changes.
- Run the existing documentation audit/build checks for the edited page only as selected by current CI routing.
