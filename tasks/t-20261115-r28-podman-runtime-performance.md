---
id: t-20261115-r28-podman-runtime-performance
card_number: "0428-095"
card_short_title: "Speed up Podman lifecycle"
type: task
areas: [runtime, ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "ChatGPT"
kanban_status: closed
kanban_lane: closed
kanban_summary: "Reduce rootless Podman lifecycle latency without weakening project ownership, Quadlet systemd controls, readiness or security;…"
kanban_title: 0428-095 · Speed up Podman lifecycle
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1600]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1600"]
---

- [x] t-20261115-r28-podman-runtime-performance · Speed up Podman lifecycle #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #area/runtime #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT · **Priority:** high  
    **PR:** [baseharbor#1600](https://github.com/mcpdev80/baseharbor/pull/1600)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1600)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** ChatGPT  
**Priority:** high  
**PRs:** [baseharbor#1600](https://github.com/mcpdev80/baseharbor/pull/1600)  
**Source:** 
<!-- /generated:links -->

## Implementation PR

- [baseharbor#1600](https://github.com/mcpdev80/baseharbor/pull/1600)

## Goal

Reduce rootless Podman lifecycle latency without weakening project ownership, Quadlet systemd controls, readiness or security; retain equivalent Docker behavior.

## Verified hotspots

- `internal/providers/runtime/podman/lifecycle.go`: `InspectProjectResources` does per-resource existence and ownership inspections; `StopOwnedProjectContainers` repeats one `podman inspect` for each running container after the inventory.
- `internal/runtime/compose_resources.go` and `scripts/ci-runtime-reset.sh` already batch inventory/inspect; preserve these implementations.
- Existing evidence: [historical 2.45x reproduction](https://github.com/mcpdev80/baseharbor/issues/376), [successful pre-release run](https://github.com/mcpdev80/baseharbor/actions/runs/37713017303).

## Acceptance

- Update existing Podman unit/integration/regression tests as necessary and add dedicated new batch inspection and command-count tests. Register each added/changed test in the existing test-to-CI-gate mapping; evaluate/update `scripts/pr-gate-plan.py`, `scripts/release-requirements.json` and Docker/rootless Podman workflow triggers with the CI owner.
- Prove affected-path gate selection, unrelated-path non-selection and actual successful candidate-SHA execution. Missing mapping, skipped required native run or unverified Docker equivalence blocks acceptance.


- Batch Podman resource ownership inspections by kind and reuse the existing container snapshot for Quadlet-unit labels.
- Fail closed on missing, malformed, conflicting or foreign ownership; do not silently skip partial failures.
- Preserve systemd managed stop semantics, resource cleanup and current public API behavior.
- Add focused tests for mixed owned/foreign resources, missing names, multiple containers, no-unit and unit-backed containers, including command-count assertions.
- Compare exact same Docker/Podman Pre-Release gate command counts and step durations; report candidate SHA and before/after measurements. No artificial sleeps or skipped verifications.
- One implementation PR against `develop`; do not merge until CI and review are green.

## References

- [Podman implementation](https://github.com/mcpdev80/baseharbor/blob/develop/internal/providers/runtime/podman/lifecycle.go)
- [Runtime inventory](https://github.com/mcpdev80/baseharbor/blob/develop/internal/runtime/compose_resources.go)

BOARD-KORREKTUR (§3.7): die karte stand auf active, aber PR #1600 ist merged=true und sein merge-commit 0234e9aa8 (2026-11-16T15:24Z) IST ANCESTOR von origin/develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a — inhalt ist also laengst im zweig. Der 3-dot-diff origin/develop...4159e10a4 zeigt 0 dateien, weil develop ihn schon enthaelt. Kein laufender kandidat, keine lane noetig
