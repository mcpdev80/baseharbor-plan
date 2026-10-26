---
id: t-20261022-r27-ci-runtime
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-evidence-acceptance]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-ci-runtime · ci runtime #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-remote-docker-web](t-20261018-r27-remote-docker-web.md), [t-20261018-r27-remote-material](t-20261018-r27-remote-material.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W1/W2/W3 within the single shared pool**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

For runtime: W1 owns trusted selection/discovery changes; W2 owns the domain producer/executor fixture; W3 owns bounded result/receipt verification and negative cases. Coordinator reserves exact disjoint files against the accepted domain interface before dispatch. Use three total workers across ready domains, never three workers per domain or simultaneous writers to shared central files.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.



# Trusted CI readiness: runtime

## Goal
Independently qualify the smallest trusted planner/executor/finalcheck checks for the runtime domain before its new implementation files are exercised. This is a bounded CI prerequisite, not blanket approval for unrelated domains.

## Covered slices
- node-service
- node-trust
- node-streams
- node-cli
- remote-material
- remote-docker-web
- remote-podman-web
- remote-rollout
- state-recovery
- maintenance-client

## Acceptance
- Inventory existing production paths and check mapping, required check names, runner capabilities, test entrypoints and exact trust inputs; avoid speculative new checks.
- Add only missing coverage with executable positive and negative regressions, including changed-file detection and failure propagation.
- Independently review any trusted policy/coverage changes; preserve source/integration SHA and runner isolation.
- No self-qualification, full matrix, blanket bypass or merge without normal gates.
- Different domains may be worked in parallel by Codeman, maintainer sessions or contributors, but central CI workflow/policy files require explicit single-writer integration sequencing.
- Record exact accepted SHA and available check identity for dependent product slices.
