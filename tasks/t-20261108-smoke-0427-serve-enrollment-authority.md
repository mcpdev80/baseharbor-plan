---
id: t-20261108-smoke-0427-serve-enrollment-authority
card_number: "0427-168"
card_short_title: "serve needs local core"
type: bug
areas: [connector, cli]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: blocked
kanban_lane: blocked
kanban_summary: Decide and implement (or explicitly scope out) a Core authority model for Connector enrollment that works with a remote-hosted…
kanban_title: 0427-168 · serve needs local core
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261108-smoke-0427-up-ignores-target]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Owner decision required: should ConnectorEnrollmentHTTP accept a remote-Core authority (OpenBao over API) or is Core-on-remote explicitly out of scope for v0.4.27?"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-smoke-0427-serve-enrollment-authority · Serve: enrollment needs local Core #task #release/v0-4-27 #status/blocked #view/blocked #area/cli #area/connector #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Blocker:** Owner decision required: should ConnectorEnrollmentHTTP accept a remote-Core authority (OpenBao over API) or is Core-on-remote explicitly out of scope for v0.4.27?  
    **Needs:** [t-20261108-smoke-0427-up-ignores-target](t-20261108-smoke-0427-up-ignores-target.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261108-smoke-0427-up-ignores-target](t-20261108-smoke-0427-up-ignores-target.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

Component: `cmd/baha` (`baha serve` / connector_enrollment path), version 0.4.27-dev+b90a6e2f2 (develop b90a6e2f2, tested 2026-11-08).

The API route for remote management (per docs/tutorials/homelab.md and open PR #1473) requires the operator Core to expose the machine API plus the Connector enrollment/authority surface. On develop, `ConnectorEnrollmentHTTP` hard-requires a **local** Docker/Podman authority target: effective target name must equal the configured authority target AND `AccessProvider == "local"`, and the CSR issuer runs `docker compose exec` into the **local** openbao container. A Core host that registered the node through a remote connector therefore cannot sign enrollments, and a developer machine cannot run this server against a remote-only Core.

Repro (real commands, host running the Core):

```bash
BASEHARBOR_CONNECTOR_ENROLLMENT_ENABLED=true \
  baha serve --listen 0.0.0.0:8443 --core-target local
# effective target on this host resolves via remote binding ->
# "Connector enrollment requires an explicit Core authority Target" / authority-target access-provider check fails
baha node add dev-box --target app-node-01 --node mcp178 --core-address https://192.168.6.178:8443
# same enrollment grant path -> capability-missing, no grant issued
```

Expected: enrollment authority works wherever the Core is installed (per PR #1473 design) or the CLI states which installation can serve enrollment.

Actual: enrollment grant creation is bound to a locally reachable docker/podman `local` target; remote-Core API route dead-ends. Related but distinct: open #1473 (client-side selection), closed 0427-042 (trust/rotation), blocked 0427-134 (CA trust + PKCE login).

Impact on E2E flow: Steps 2+4 (bind remote Core from developer PC, remote app deploy via API route) cannot complete on develop without product changes.

## Goal

Decide and implement (or explicitly scope out) a Core authority model for Connector enrollment that works with a remote-hosted Core.

## Acceptance

- Either enrollment authority resolves against the installed Core location (remote included) with real grant issuance, or `serve`/`node add` fail with a precise, documented message that names the supported installation topology.
- Regression coverage on the production enrollment path.

## Dependencies and file ownership

- Owned files or areas: cmd/baha/connector_enrollment.go, internal/targetenrollment authority binding, docs/tutorials.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 in E2E smoke-test. Blocked pending Owner scope decision (see blocker). No fix attempted per smoke-test rules. Newest first.
