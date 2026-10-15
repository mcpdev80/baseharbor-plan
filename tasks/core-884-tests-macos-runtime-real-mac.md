---
id: core-884
areas: [testing]
type: acceptance
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#884"]
source_updated: "2026-10-15T16:49:18Z"
labels: [kind/acceptance, area/runtime, area/evidence, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-884 · Tests: verify the macOS runtime on a real Mac #task #release/v0-4-29 #status/planned #view/queued #area/testing #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Later release** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** none  
**Required by:** [core-822](core-822-macos-darwin-adapters.md), [core-823](core-823-tests-platform-conformance-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#884](https://github.com/mcpdev80/baseharbor/issues/884)
<!-- /generated:links -->

## Goal

Real macOS runtime evidence comes from a dedicated self-hosted Apple Silicon Mac registered as a GitHub Actions runner (decision 2026-10-14). Manual developer-machine receipts are not the release gate. Consumed by core-822 and core-823.

## Scope

- Why: hosted Apple Silicon runners lack the nested virtualization needed for Docker Desktop/Podman Machine journeys; Intel/native-build results are not Apple Silicon runtime evidence.
- Machine: dedicated Apple Silicon Mac, current macOS, Docker Desktop and Podman (`podman machine`); own macOS user account; no personal data or credentials.
- Registration: repository-scoped runner with labels such as `self-hosted, macOS, ARM64, baha-macos-runtime`; jobs select it only through these labels.
- Hardening: never run untrusted code — `workflow_dispatch`/protected-branch triggers only, never fork `pull_request`, gated by a protected GitHub environment; ephemeral or cleaned workspace per job; clean owned containers, volumes, networks, Podman Machine state and BaseHarbor state after every job and keep the cleanup evidence; no secrets on the host beyond the runner registration.
- Runtime state control: jobs set and record the VM allocation (Docker Desktop resources, `podman machine` CPUs/memory); jobs start/stop both engines so stopped-VM negatives are possible.
- Licensing: confirm Docker Desktop subscription terms for this CI use and record the decision.
- Inventory per run: macOS version, architecture, Docker Desktop version, Podman version and machine image, matching the exact-SHA evidence receipts.
- Wire lanes into the existing workflow surface (core-823); change `scripts/ci-workflow-policy.sh` only if a new workflow file is unavoidable.

## Acceptance

- Runner registered, labelled and restricted to trusted triggers.
- A smoke job proves Docker Desktop and Podman Machine start, report their VM capacity and clean up.
- Licensing decision recorded.
- Per-run environment inventory captured in evidence receipts.

## Required checks

- Smoke job on the runner; cleanup evidence.

## Dependencies and file ownership

- No task dependencies (infrastructure). Needs hardware and a licensing decision from the Maintainer.

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
