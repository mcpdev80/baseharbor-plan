---
id: t-20261108-smoke-0427-operator-api-undocumented
card_number: "0427-169"
card_short_title: "operator API runbook missing"
type: bug
areas: [docs, cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "Codex (Marcel, Wait sweep excluding #1615)"
kanban_status: wait
kanban_lane: wait
wait_reason: "PR #1587 is merged and its exact required run 44885697655 passed at head c43d816120651c33a7a9c02f6ee805ae78440602. Read-only strict-TLS probes against the running test-VM Core returned healthz 200, readyz 200, anonymous machine discovery 401, and plaintext healthz 400 (evidence: operator-api-smoke.md). The authenticated workstation-to-Core path is still unverified: the workstation has no baseharbor-core Target, and no enrollment/login or authenticated CLI request was performed. Do not close until the real workstation enrollment and authenticated path are exercised. #1615 remains untouched."
kanban_summary: A developer can start and use the Core operator API from documentation alone.
kanban_title: 0427-169 · operator API runbook missing
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-connection-client]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1587"]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/operator-api-smoke.md", "https://github.com/mcpdev80/baseharbor/pull/1587", "https://github.com/mcpdev80/baseharbor/actions/runs/44885697655", "https://github.com/mcpdev80/baseharbor/actions/runs/44873370844"]
early: true
---

- [ ] t-20261108-smoke-0427-operator-api-undocumented · Remote Core: API route runbook missing #task #release/v0-4-28 #status/wait #view/wait #area/cli #area/docs #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (Marcel, Wait sweep excluding \#1615) · **Priority:** normal  
    **PR:** [baseharbor#1587](https://github.com/mcpdev80/baseharbor/pull/1587)  
    **Waiting:** PR \#1587 is merged and its exact required run 44885697655 passed at head c43d816120651c33a7a9c02f6ee805ae78440602. Read-only strict-TLS probes against the running test-VM Core returned healthz 200, readyz 200, anonymous machine discovery 4…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/operator-api-smoke.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1587), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44885697655), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44873370844)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
**Owner:** Codex (Marcel, Wait sweep excluding #1615)  
**Priority:** normal  
**PRs:** [baseharbor#1587](https://github.com/mcpdev80/baseharbor/pull/1587)  
**Source:** 
<!-- /generated:links -->

## Current scope clarification — 2026-11-14

Document and verify only the supported authenticated workstation-to-Core operator API path on the selected Core host. The archived Connector topology and its dropped enrollment-authority card are not prerequisites. Historical smoke notes below are evidence, not current requirements; do not claim unverified paths work.

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

### 2026-11-21 — merged PR and real-Core read-only probes

- PR [#1587](https://github.com/mcpdev80/baseharbor/pull/1587) is merged as `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef`. Exact ready-PR run [44885697655](https://github.com/mcpdev80/baseharbor/actions/runs/44885697655) passed at head `c43d816120651c33a7a9c02f6ee805ae78440602`; source is now present in develop `97b2ba5543f07b820b5c18a688058fd932c4516f`.
- On the already-running test-VM Core, strict-TLS read-only probes using its managed API CA returned `/healthz` 200, `/readyz` 200, unauthenticated `/api/v1/machine/discovery` 401, and plaintext `/healthz` 400. Exact results are in [operator-api-smoke.md](../evidence/r28-welle4-2026-11-21/operator-api-smoke.md). No server, container, or Core state was changed.
- This does not cover the card's full authenticated workstation-to-Core flow. The workstation has no `baseharbor-core` Target configured, no workstation enrollment or operator login was used, and there is no authenticated discovery or CLI status proof. Keep the card in Wait until that acceptance path is run safely; #1615 was not inspected or changed.

- 2026-11-21 Codex Wait sweep: PR [#1587](https://github.com/mcpdev80/baseharbor/pull/1587) moved from Draft to ready; merge commit `962d852fa42f69836bf618279cfbdfba674b5b21` brought current develop `40cb28c758b02960356434b630086a341ebe1738` into the PR branch without rewriting history. The diff against current develop remains the same nine docs/help files. Exact required run [44873370844](https://github.com/mcpdev80/baseharbor/actions/runs/44873370844) is terminal FAILURE: source format, trusted plan, workflow policy, build, vet, English/German MkDocs, docs audit, pages build, focused Python, and owner shard pass; CLI-0..3 fail on the managed-operator-auth gate belonging to excluded #1615; packages fails the Loki fixture tests tracked by 0428-212/#1734; `PR Selected Checks` fails on incomplete required Go shard coverage. GitHub rejected merge before the current-base run because `PR Selected Checks` was absent; no bypass attempted. Do not close until these shared gates are green. #1615 was not read or modified.
- 2026-11-15 lane flash (0427-169): runbook published as draft PR [#1587](https://github.com/mcpdev80/baseharbor/pull/1587) (docs-only candidate 20e0537cc3332c53500091ca1776fc6b408670d0, base develop 0e9ccb582f5bdcdc74049bbe3996263cdce6500c, ancestry verified; CI run 43709246427 completed/success observed). Scope kept to the supported authenticated workstation-to-Core path; unverified topology stays labeled spec-only per the 2026-11-14 clarification. Evidence file: [akte.md](https://github.com/mcpdev80/baseharbor-plan/blob/8a65515263b712bac757ac137e14f6265c518d61/evidence/r28-welle1-2026-11-15/operator-runbook/akte.md) (immutable at the review-publishing commit). Awaiting CODEX-REVIEW and merge; no product behavior change.
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

## Explicit scope transfer to v0.4.28 — 2026-11-13

Deferred legacy `baha serve`/Connector operator API runbook details to follow the Connector enrollment topology card in v0.4.28; v0.4.27 still must have accurate `baha up`/`baha onboard` developer-to-VM documentation.

Preserve original card ID/number, prior PR and test history. This is a release-scope move, not acceptance or implementation completion. The Coordinator must inspect current merged Core code, first-party provider contracts, real selected CI, and the existing task before dispatch; Codex independently reviews/merges. Release v0.4.27 cannot claim the deferred feature as complete.
