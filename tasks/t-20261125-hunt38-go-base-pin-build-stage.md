---
id: t-20261125-hunt38-go-base-pin-build-stage
card_number: "0428-309"
card_short_title: "pin unpinned Go base image in"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Pin the generated Go development-extension build-stage image to an explicit version and immutable digest in…
kanban_title: 0428-309 · pin unpinned Go base image in
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/development/goadapter/adapter.go#L360-L368"]
---

- [ ] t-20261125-hunt38-go-base-pin-build-stage · 0428 hunt H-V38: pin unpinned Go base image in build-stage Dockerfile #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/development/goadapter/adapter.go#L360-L368)  
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

Pin the generated Go development-extension build-stage image to an explicit version and immutable digest in internal/development/goadapter/adapter.go, preserving the existing Go 1.25 Alpine build behavior.

## Scope

- In scope: the Dockerfile string returned by renderDockerfile in the Go development adapter.
- Out of scope: runtime image references, dependency versions, WSL2/macOS enablement, or a new image-management mechanism.

## Acceptance

- Use the intended Go 1.25 Alpine image by explicit digest and retain a readable version tag.
- Keep the generated Dockerfile stages, commands, and runtime behavior otherwise unchanged.
- Update the existing goadapter/image rendering test to assert the immutable image reference.
- Record the verified upstream image digest and the exact source SHA in the handoff.

## Evidence

- Current generated build-stage reference: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/development/goadapter/adapter.go#L360-L368
