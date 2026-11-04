---
id: t-20261104-r27-vm-integration-runs
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-rebuild-integration, t-20261018-r27-device-enrollment, t-20261018-r27-node-service]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-vm-integration-runs · Operations: real Docker and Podman integration runs with core, demo, console and connector #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261104-r27-vm-rebuild-integration](t-20261104-r27-vm-rebuild-integration.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-rebuild-integration](t-20261104-r27-vm-rebuild-integration.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The real Docker and Podman integration suites run on the rebuilt test hosts against core, demo, console and
connector, and each combination leaves a pass/fail line with the exact revisions used, so release qualification
is based on executed runs instead of skipped gates.

## Scope

- In scope: executed integration runs per host and per repository with recorded revision pairs, cleanup of what
  each run creates, and a finding on the owning feature card for every product defect the run exposes.
- Out of scope: host rebuild (t-20261104-r27-vm-rebuild-integration), workflow and runner definitions (shared
  GitHub runners), Proxmox and productive services, release promotion or tagging, weakening a test to pass.

## Acceptance

- Eight combinations are executed (two hosts x core, demo, console, connector) and each leaves a run line with
  host, repository, source revision and result.
- A skipped or simulated run does not count; the evidence holds the command and its output.
- Product defects are filed on their own cards; this card closes when the runs themselves work.
- A worker executes the runs; the coordinator verifies on disk and publishes.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
