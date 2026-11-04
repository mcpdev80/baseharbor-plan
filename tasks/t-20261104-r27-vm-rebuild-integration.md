---
id: t-20261104-r27-vm-rebuild-integration
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "coord-welle4 (lanes w116, w117)"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-enrollment, t-20261018-r27-node-service]
repos: [mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-vm-rebuild-integration · Operations: reproducible rebuild of the Docker and Podman test VMs and real cross-repo integration runs #task #release/v0-4-27 #status/active #view/active #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (lanes w116, w117) · **Priority:** critical  
    **Needs:** [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
**Owner:** coord-welle4 (lanes w116, w117)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Both test hosts are rebuilt from their own setup scripts instead of patched by hand, and afterwards the real
Docker and Podman integration suites run against core, demo, console and connector with compatible source
references, so release qualification rests on executed runs rather than skipped gates.

## Scope

- In scope: scripted rebuild and full cleanup of the Docker test VM and the Podman test VM (pure test
  environments, Owner authorization 2026-11-04), functional proof of each runtime, then executed integration
  runs of core, demo, console and connector on both hosts with recorded revision pairs.
- Out of scope: Proxmox hosts and any productive service, GitHub workflow and runner definitions (shared GitHub
  runners only), release promotion or tagging, and weakening any test to make a host pass.

## Acceptance

- Each host rebuild is reproducible: the run uses the host setup script, and any deviation is recorded as a
  script diff on the host, not as an undocumented manual step.
- Shared stacks are preserved; every destructive action is preceded by the recorded three-point check.
- Runtime is proven per host: version, a rootless run without sudo, a port mapping test, and a build cache test.
- The integration runs are executed on the hosts, not simulated on the coordinator: core, demo, console and
  connector each produce a pass/fail line per host with the exact source revision used.
- Product defects found by the runs are filed on their own feature card; they do not block this card, which
  closes when the hosts and the runs themselves work.
- A worker executes this; the coordinator dispatches and verifies on disk.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Handoff

- Owner directive 2026-11-04 (16:0x): test VMs are pure test environments, full cleanup and rebuild authorized,
  prefer reproducible rebuild over manual repair, Proxmox and productive services untouched, then run the real
  Docker/Podman integration tests with core, demo, console and connector, in parallel to the PR fixes.
- Lanes w116 (Docker host) and w117 (Podman host) execute the rebuild phase. A second pair of lanes executes
  the integration phase once both hosts report functional.
