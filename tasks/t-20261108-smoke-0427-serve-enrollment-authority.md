---
id: t-20261108-smoke-0427-serve-enrollment-authority
card_number: "0427-168"
card_short_title: "serve needs local core"
type: bug
areas: [connector, cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Implement Connector enrollment against the Core's verified installation authority. The release contract already requires remote…"
kanban_title: 0427-168 · serve needs local core
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261017-release-0-4-28-updates, t-20261018-r27-connection-client, t-20261108-smoke-0427-up-ignores-target]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261108-smoke-0427-serve-enrollment-authority · Serve: enrollment needs local Core #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/connector #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261108-smoke-0427-up-ignores-target](t-20261108-smoke-0427-up-ignores-target.md)  
**Required by:** [t-20261108-smoke-0427-operator-api-undocumented](t-20261108-smoke-0427-operator-api-undocumented.md)  
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

Implement Connector enrollment against the Core's verified installation authority. The release contract already requires remote developer access; no additional scope decision is needed.

## Acceptance

- Either enrollment authority resolves against the installed Core location (remote included) with real grant issuance, or `serve`/`node add` fail with a precise, documented message that names the supported installation topology.
- Regression coverage on the production enrollment path.

## Dependencies and file ownership

- Owned files or areas: cmd/baha/connector_enrollment.go, internal/targetenrollment authority binding, docs/tutorials.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 in E2E smoke-test. Waiting for the remote Core binding implementation; no Owner scope decision remains. No fix attempted per smoke-test rules. Newest first.

## Scope confirmation 2026-11-08

The accepted core-777 / v0.4.27 contract includes an authenticated remote developer client and host-owned management Core. This is an implementation dependency, **not** an unresolved Owner scope decision. Resume once remote management binding from [0427-023](t-20261018-r27-connection-client.md) and remote bootstrap safety from [0427-167](t-20261108-smoke-0427-up-ignores-target.md) are qualified. The remote E2E remains FAIL.

## Explicit scope transfer to v0.4.28 — 2026-11-13

Deferred Connector enrollment against remotely registered Core: v0.4.27 supports workstation->Core installed on VM, executing Docker/Podman on that VM; separate remote runtime Connector topology is v0.4.28. Do not weaken workstation onboarding security.

Preserve original card ID/number, prior PR and test history. This is a release-scope move, not acceptance or implementation completion. The Coordinator must inspect current merged Core code, first-party provider contracts, real selected CI, and the existing task before dispatch; Codex independently reviews/merges. Release v0.4.27 cannot claim the deferred feature as complete.
