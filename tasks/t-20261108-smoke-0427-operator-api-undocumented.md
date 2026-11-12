---
id: t-20261108-smoke-0427-operator-api-undocumented
card_number: "0427-169"
card_short_title: "operator API runbook missing"
type: bug
areas: [docs, cli]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: A developer can start and use the Core operator API from documentation alone.
kanban_title: 0427-169 · operator API runbook missing
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-connection-client, t-20261108-smoke-0427-serve-enrollment-authority]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-smoke-0427-operator-api-undocumented · Remote Core: API route runbook missing #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/cli #area/docs #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261108-smoke-0427-serve-enrollment-authority](t-20261108-smoke-0427-serve-enrollment-authority.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

Component: documentation + `baha serve` startup surface, version 0.4.27-dev+b90a6e2f2 (develop b90a6e2f2, tested 2026-11-08).

The user story "developer PC binds the Core that runs on the remote Docker host **over the API** (not SSH)" is the intended route (homelab tutorial direction, open PR #1473). But the required startup of the operator machine API is undocumented anywhere: which process exposes `/api/v1/machine/*`, which `BASEHARBOR_*` envs are mandatory (OIDC issuer/client, TLS, connector listener), and which single command starts it on a Core host. Searching docs/ for serve/8443/operator-API env names yields no runbook; only the CLI-internal calls exist.

Evidence (real, smoke-test session 2026-11-08):
- `rg "8443|operator.*api|serve" docs/` — no startup documentation.
- `baha serve --help` documents only `--listen`/`--core-target`, not the required OIDC/TLS env contract; a run without them fails at auth verification (`machinehttp requires OIDC issuer and audience`-style errors from the handler).
- Consequently the whole §4 path had to be reconstructed from code reading (`internal/machinehttp`, `controlplaneruntime`), which no developer without internal BaseHarbor knowledge can do.

Expected: a how-to/tutorial page (or `baha serve --help` + config docs) gives the exact steps to run the operator API beside an installed Core and to point the CLI at it.

Actual: default route unusable without internal knowledge; smoke-test had to stop at that step.

Impact on E2E flow: Step 2/6 (connect remote Core) unverifiable via documented path; contributes to FAIL of remote app deployment section.

## Goal

A developer can start and use the Core operator API from documentation alone.

## Acceptance

- A docs page (how-to/tutorial) states: required env/config, TLS and OIDC prerequisites, the exact start command, and the CLI-side connection steps; each claim exercised by a test or manual acceptance run on a real Core install.
- `baha serve --help` references the doc or lists the mandatory env variables.

## Dependencies and file ownership

- Owned files or areas: docs/tutorials or docs/how-to, cmd/baha/serve.go help text.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 in E2E smoke-test (API route requirement confirmed with maintainer mid-run). Newest first.

## E2E follow-up 2026-11-08

The remote API runbook must be validated against a **working** developer-only CLI -> authenticated remote Core -> Docker connector -> app apply/status/destroy sequence. Existing env names in source are not a substitute for an independently successful startup sequence. Track this documentation card in Wait on 0427-168 and 0427-023 rather than presenting untested configuration as supported.

## Code-derived operator API inventory (unverified)

The following is **source inspection only**, not a validated installation runbook. Keep this card in **Wait** until 0427-023/168 and a physical smoke pass.

- `baha serve` distinguishes per-application broker from Core operator API using `BASEHARBOR_RUNTIME_APP_NAME`; Core startup binds a verified management host and rejects foreign/competing state ownership.
- Operator API config is loaded by `controlPlaneConfigFromEnv` from `cmd/baha/serve.go`: `BASEHARBOR_API_LISTEN_ADDR`, `BASEHARBOR_API_DATABASE_URL`, `BASEHARBOR_API_OIDC_ISSUER`, `BASEHARBOR_API_OIDC_AUDIENCES`, `BASEHARBOR_API_TLS_CERT_FILE`, `BASEHARBOR_API_TLS_KEY_FILE`, `BASEHARBOR_API_TLS_CLIENT_CA_FILE`. These are **recognized variable names**, not a verified minimal/mandatory set.
- Connector enrollment additionally recognizes `BASEHARBOR_CONNECTOR_ENROLLMENT_ENABLED`, `BASEHARBOR_CONNECTOR_AUTHORITY_TARGET`, `BASEHARBOR_CONNECTOR_LISTEN_ADDR` and `BASEHARBOR_CONNECTOR_TLS_{CERT,KEY,CA}_FILE`; workstation enrollment has `BASEHARBOR_WORKSTATION_ENROLLMENT_ENABLED`.
- Client currently uses `BASEHARBOR_CONNECTION_PROFILE` with explicit pinned HTTPS CA, installation identity, tenant-bound Target, and operator OIDC `dev` session. Machine routes: authenticated `GET /api/v1/management/installation`, `GET /api/v1/machine/discovery`, `POST /api/v1/machine/executions`, `GET /api/v1/machine/executions/{execution_id}`; 202 is admission only.
- **Do not publish a copy-paste production startup recipe** from this inspection: TLS/Keycloak provisioning and client app registration remain untested on the real Docker host.
