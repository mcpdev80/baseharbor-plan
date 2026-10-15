---
id: core-815
type: acceptance
release: v0.4.x
version: ""
parent: v0.4.x
owner: ""
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#815"]
source_updated: "2026-10-15T16:50:55Z"
labels: [kind/acceptance, area/runtime, area/evidence, area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-815 · Tests: start all greenfield stacks on native runtimes #task #release/v0-4-x #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** unassigned  
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
