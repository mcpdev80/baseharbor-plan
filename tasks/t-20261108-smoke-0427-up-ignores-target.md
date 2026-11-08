---
id: t-20261108-smoke-0427-up-ignores-target
card_number: "0427-167"
card_short_title: "up installs local"
type: bug
areas: [cli, remote]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ChatGPT (remote bootstrap safety)
kanban_status: wait
kanban_lane: wait
kanban_summary: "Core bootstrap/install respects the effective or explicitly selected target; when the target cannot host the control plane, a…"
kanban_title: 0427-167 · up installs local
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1492"]
sources: []
blocker: ""
wait_reason: "Sicherheitsfix #1492 gemergt; Remote-Happy-Path bleibt separater Folgeumfang. Ausstehende Remote-Client-/Connector-Integration wird parallel in #1473 bearbeitet; diese Karte bis Scope-/Acceptance-Abgleich geparkt."
resolution: ""
evidence: []
---

- [ ] t-20261108-smoke-0427-up-ignores-target · Remote core: up installs local #task #release/v0-4-27 #status/wait #view/wait #area/cli #area/remote #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (remote bootstrap safety) · **Priority:** high  
    **PR:** [baseharbor#1492](https://github.com/mcpdev80/baseharbor/pull/1492)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md)  
**Owner:** ChatGPT (remote bootstrap safety)  
**Priority:** high  
**PRs:** [baseharbor#1492](https://github.com/mcpdev80/baseharbor/pull/1492)  
**Source:** 
<!-- /generated:links -->

## Problem

Component: `cmd/baha` (Core install/bootstrap), version 0.4.27-dev+b90a6e2f2 (develop HEAD b90a6e2f2, tested 2026-11-08).

E2E smoke-test (developer PC → remote Docker host via API route): the operator wants the Core management plane to run on the remote Docker host. `baha up --control-plane-only` has no target selection and always installs into the developer machine's local state (`~/.local/share/baseharbor/targets/local`), even when an active non-local target exists.

Repro (real commands, developer PC):

```bash
baha use app-node-01          # remote docker target registered via target create --access-provider baseharbor-node-connector
baha up --control-plane-only --yes --plain
```

Expected: Core is installed/reconciled against the effective (remote) target, or the CLI emits a clear "control plane install requires --target <name>" usage error.

Actual: Core installs on the local docker daemon; no error mentions the active target. The remote host was never contacted (`docker ps` on 192.168.6.178 showed no baseharbor containers). This is distinct from closed 0427-124 (BASEHARBOR_TARGET env read) — here the `up --control-plane-only` install path itself has no target binding at all.

Impact on E2E flow: Step 2 ("Core auf Remote-Docker-Host") fails through the default path; only manual execution of the CLI on the host itself worked (`ssh host '~/dev/baha up --control-plane-only'`), which is not the documented route.

## Goal

Core bootstrap/install respects the effective or explicitly selected target; when the target cannot host the control plane, a specific error names the required step.

## Acceptance

- `baha up --control-plane-only` (with or without `--target`) either installs against the selected remote target or fails with an actionable error that never silently installs locally.
- A CLI regression test asserts the error/installation binding on the production path (not a test-only env).

## Dependencies and file ownership

- Owned files or areas: cmd/baha (up/core install target binding), docs/cli.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 in E2E smoke-test (CLI 0.4.27-dev+b90a6e2f2, host 192.168.6.178). No fix attempted per smoke-test rules. Newest first.

## Implementation update 2026-11-08

- PR [#1492](https://github.com/mcpdev80/baseharbor/pull/1492) introduces a safe interim guard: a selected remote Target cannot silently bootstrap Core on the developer workstation. Production entry-point regression added.
- This **does not** implement remote Core installation. The full developer-PC-to-remote-host happy path remains unverified and the E2E verdict remains FAIL until real deployment evidence exists.

- CI proof for #1492: [run #5300](https://github.com/mcpdev80/baseharbor/actions/runs/42509941118), HEAD `0e1e0c4746980c2f7896d1dcf79fd98f43c1f66b`: **all selected required checks PASS**, including Docker/Podman native destroy, Go unit/build/vet and PR Selected Checks. Squash merged into develop at `171e9569d4bdea0b03faca663dc88a41e185f75f`. The full remote bootstrap capability is STILL OPEN; this receipt covers the no-local-fallback safety fix only.

## Kanban-Pause 2026-11-08

- Sicherheitsfix #1492 gemergt; Remote-Happy-Path bleibt separater Folgeumfang. Ausstehende Remote-Client-/Connector-Integration wird parallel in #1473 bearbeitet; diese Karte bis Scope-/Acceptance-Abgleich geparkt.
- Status `wait` als Ressourcen-/Abnahme-Pause, **nicht** als technischer Blocker. Owner bleibt bestehen; Reaktivierung nach konkreter Uebergabe bzw. Acceptance.
