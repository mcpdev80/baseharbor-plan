---
id: core-815
card_number: "0427-003"
card_short_title: "start all greenfield stacks on"
areas: [testing]
type: acceptance
release: v0.4.27
version: ""
parent: v0.4.27
owner: coord-welle3 (lane w35)
kanban_lane: blocked
kanban_summary: Every shipped built-in greenfield stack satisfies baha app new … → generated source repo → baha up → READY on Docker and Podman…
kanban_status: blocked
kanban_title: "0427-003 · start all greenfield stacks on"
depends_on: [core-893, core-895, core-896, t-20261017-release-0-4-27-updates, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#815"]
source_updated: "2026-10-15T16:50:55Z"
labels: [kind/acceptance, area/runtime, area/evidence, area/dx]
blocker: "owner-direktive 2026-11-07: greenfield-stack tests vollstaendig in CI. nicht dispatchbar bis ci-seam 0427-021 (test-to-CI verankerung) + qualifizierte docker/podman hosts (#114/#107 ops) landen. naechster trigger: 021 accepted."
resolution: ""
evidence: []
---

- [ ] core-815 · Tests: start all greenfield stacks on native runtimes #task #release/v0-4-27 #status/blocked #view/blocked #area/testing #kind/acceptance
    <!-- generated:card -->
    **Owner:** coord-welle3 (lane w35)  
    **Blocker:** owner-direktive 2026-11-07: greenfield-stack tests vollstaendig in CI. nicht dispatchbar bis ci-seam 0427-021 (test-to-CI verankerung) + qualifizierte docker/podman hosts (\#114/\#107 ops) landen. naechster trigger: 021 accepted.  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Owner:** coord-welle3 (lane w35)  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#815](https://github.com/mcpdev80/baseharbor/issues/815)
<!-- /generated:links -->

## Goal

Every shipped built-in greenfield stack satisfies `baha app new … → generated source repo → baha up → READY` on Docker and Podman with required managed bindings and no manual source repair.

## Scope

- Remaining scope after published v0.4.23: the Go/Next.js/Quarkus build corrections were delivered in merged PR #809 / v0.4.23. Native template run [37508074031](https://github.com/mcpdev80/baseharbor/actions/runs/37508074031) at `9865135c613c2c5cb73f88f95c60a65685ee6227` passed fresh image builds for all four stacks on Docker and Podman (SQL/managed-secret contracts, no runtime credentials as build inputs) and actual Python startup/secret delivery; it does **not** qualify startup of all four stacks.
- Open: Docker/Podman generated-application startup and READY evidence for Go, Next.js, Python and Quarkus on the current candidate with exact inputs; historical v0.4.23 greens cannot substitute.
- Original defects (baseline v0.4.22 `1aa1a503facc1f4cbbd58fab21619fda53ed6d47`): Go `go.sum`/module state required `go mod tidy`; Next.js validated runtime env at build time; Quarkus Maven config did not produce `target/quarkus-app/`. Python was the control.

## Acceptance

- Go fresh scaffold builds and reaches READY without manual `go mod tidy`.
- Next.js fresh scaffold builds with runtime bindings resolved at runtime, not build import time.
- Quarkus fresh scaffold produces the artifact layout its Dockerfile consumes.
- Python remains green.
- The generated portable contract remains equivalent across stacks except app identity.
- Focused Docker + Podman scaffold acceptance, including READY for all four stacks.

## Required checks

- Targeted native template startup gates on Docker and Podman for the current candidate.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Earlier parent #571 (closed); related #210 (closed).

## Handoff

- Build part delivered; startup acceptance outstanding (pre-freeze acceptance under v0.4.31).

## Additional acceptance: control-plane default (Owner, 2026-11-06)

- Governing contract: `t-20261106-r27-control-plane-single-default`. Every fresh, unmodified `baha up` default path for all four greenfield stacks MUST demonstrate the actual SINGLE control-plane topology (exactly one instance per required service, no HA members or load balancer). Reaching `READY` alone is insufficient.
- On BOTH `baha-docker` and `baha-podman`, record product SHA, rendered default Compose configuration, container count/names, service health, and exact startup commands. Fixtures must not silently enable HA or override the default.
- Before accepting this card, demonstrate both an explicit HA positive scenario and a default-HA negative scenario from the governing contract. Older green HA-default runs do not qualify this requirement.
