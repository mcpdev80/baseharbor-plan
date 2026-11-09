---
id: t-20261101-ha-prep-fix
card_number: "0427-095"
card_short_title: "prepare rootless runtime"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: "ha-prep-fix worker (ornith1.5)"
kanban_lane: closed
kanban_summary: The Targeted runtime job of .github/workflows/targeted-integration.yml is the only heavy job without a Prepare verified rootless…
kanban_status: closed
kanban_title: "0427-095 · prepare rootless runtime"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1254]
sources: [mcpdev80/baseharbor#1254]
blocker: ""
resolution: superseded
superseded_by: t-20261018-r27-ci-lanes
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1254", "https://github.com/mcpdev80/baseharbor/actions/runs/41321042904", "https://github.com/mcpdev80/baseharbor/actions/runs/41320875840", "https://github.com/mcpdev80/baseharbor/commit/a6e79c768215b5a36a20e88f688d06aa46fe155c"]
---

- [x] t-20261101-ha-prep-fix · targeted-integration: prepare rootless runtime context in Targeted runtime job (docker-leg parity fix) #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** ha-prep-fix worker (ornith1.5)  
    **PR:** [baseharbor#1254](https://github.com/mcpdev80/baseharbor/pull/1254)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1254), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/41321042904), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/41320875840), [proof 4](https://github.com/mcpdev80/baseharbor/commit/a6e79c768215b5a36a20e88f688d06aa46fe155c)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** ha-prep-fix worker (ornith1.5)  
**Priority:** not set  
**PRs:** [baseharbor#1254](https://github.com/mcpdev80/baseharbor/pull/1254)  
**Source:** [baseharbor#1254](https://github.com/mcpdev80/baseharbor/issues/1254)
<!-- /generated:links -->

## Goal

The `Targeted runtime` job of `.github/workflows/targeted-integration.yml` is the only heavy job without a `Prepare verified rootless runtime` step for the docker matrix leg, so the active docker context was never set (engine selection fell to the rootless socket → `unix:///run/user/1001/docker.sock unavailable; no fallback` FAIL in 0.39s; etcd/Patroni never reached). Add the missing step for parity with the reference heavy jobs (lines 73/144/182/225/274).

## Scope

- In scope: exactly `.github/workflows/targeted-integration.yml` — add the `Prepare verified rootless runtime` step for the docker leg; YAML validation; PR #1254; evidence.
- Out of scope: product code, other files, matrix restructuring, gate-skip, merge (merge is Coordinator/Owner).

## Acceptance

- The `Targeted runtime` job now calls `bash scripts/ci-core-rootless-runtime.sh` on the docker leg, matching reference-job semantics (gated to docker-only because this job keeps an explicit podman-only `Prepare hosted Podman runtime` step).
- YAML validates (`python3 -c 'import yaml;yaml.safe_load(open(".github/workflows/targeted-integration.yml"))'`).
- PR #1254 against develop with run evidence + reference-job line list.
- Run 2 (41321042904, workflow_dispatch, gate=shared-postgres) proves the docker leg now prepares the rootless runtime (no 0.39s FAIL); the 0.39s failure is gone.

## Required checks

- `go build ./...` OK, `go vet ./internal/application/` OK on the fix tree.
- `PR Selected Checks` = fail-closed BY DESIGN: the CI verifier requires native runtime qualification of any `.github/workflows/` change; a workflow file cannot self-prove its runtime effect (bootstrap pattern cf #1251).
- Lifecycle-gate blocker is a pre-existing Go production test failing identically on clean base 5777c02d; unrelated to this fix.

## Dependencies and file ownership

- Owned files: `.github/workflows/targeted-integration.yml` (baseharbor CI).
- No shared-file coordination needed — single-file change.

## Handoff

- Newest first.
- PR #1254 https://github.com/mcpdev80/baseharbor/pull/1254 · head `a6e79c76` · base develop (5777c02d).
- Push-target `runtime-validation/ci/ha-prep-a6e79c7` = `a6e79c76` (hosts the lifecycle gate).
- Run 2 proof: run 41321042904 (workflow_dispatch, gate=shared-postgres) — docker leg now runs `ci-core-rootless-runtime.sh`, rootless `dockerd` up, `DOCKER_HOST=unix:///run/user/1001/docker.sock` set; 0.39s FAIL gone. Job `failure` only on pre-existing Go production test (also fails on clean base).
- Run 1: run 41320875840 — environmental `address already in use` on host port 5432 (shared runner), not the fix.
- **Merge decision = Coordinator/Owner.**

## Reconciliation 2026-11-07

PR #1254 is closed unmerged. Successor PR #1257 is also closed unmerged; no delivered fix is inferred. This historical lane is concluded, with any remaining runtime-parity work requiring a new current task.
