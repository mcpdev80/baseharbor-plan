---
id: core-902
title: Prefer native TLS and justify proxies
status: open
release: v0.4.30
parent: v0.4.30
sources: ["mcpdev80/baseharbor#902"]
---
# core-902 · Prefer native TLS and justify proxies

Source: [baseharbor#902](https://github.com/mcpdev80/baseharbor/issues/902). Release: [v0.4.30](../releases/v0.4.30.md). Final semantic acceptance: #174 (v0.4.31). Cut small provider/rule tasks with their own PRs (core-888) before implementation; no shared refactoring PR. No tasks are cut yet.

## Goal

Native TLS/mTLS first; additional proxies only for demonstrably necessary functions.

## Binding rule

- If the deployed provider supports native TLS/mTLS and auth semantics sufficiently, use them — including certificate validation, server identity, secure key projection and rotation.
- Proxy TLS only when the native path is missing or cannot safely express a concretely needed semantic. Document each exception with reason, owner and required evidence.
- Routing, HA/primary selection and additional access protection are legitimate proxy tasks of their own; native TLS does not replace them.
- One shared HTTP gateway per suitable Target/security boundary; no blanket merging of all internal networks, admin access and credentials. Under HA the gateway layer must not hide an unqualified single point of failure.
- No proxy removal through a plaintext/auth downgrade. Coordinate attack protection with core-903.

## Inventory as a starting point

Source check at `ba664d398f65b9aa47882556bd27f9412cc0773d` (re-check before implementing):

- Valkey/RabbitMQ: TLS HAProxy even for single; first candidates for native TLS.
- Management PostgreSQL/OpenBao: native TLS, yet HAProxy in the single profile; app-local PostgreSQL has a different realization.
- Keycloak/Prometheus/OTLP: native TLS endpoints plus Caddy; compare auth, fixed endpoints and HA function before removal.
- Loki/Tempo: the proxy adds access protection; do not remove it without replacement.
- App exposure/management UIs: check possible double gateway layers separately.

Sources: [backend TLS](https://github.com/mcpdev80/baseharbor/blob/ba664d398f65b9aa47882556bd27f9412cc0773d/internal/application/backend_tls.go), [single profile](https://github.com/mcpdev80/baseharbor/blob/ba664d398f65b9aa47882556bd27f9412cc0773d/internal/runtime/assets/compose-single.yaml), [HTTP gateway](https://github.com/mcpdev80/baseharbor/blob/ba664d398f65b9aa47882556bd27f9412cc0773d/internal/serviceaccess/http_gateway.go). A source finding is not yet confirmation that a native rebuild is possible.

## Acceptance

- A short normative rule in the existing provider/security specification; provider templates, guidelines and conformance link to it. EN/DE consistent; README without process rules.
- For each realized provider and single/HA/shared/app case it is traceable whether native TLS or a justified proxy task applies. Existing TLS/auth functions and secured consumers are preserved.
- Simplification in small PRs, each checking trust/SAN, rotation/reload, consumer endpoints, ownership, lifecycle, provider switch and recovery as appropriate; CLI/JSON/MCP/footprint correct.
- Targeted affected Docker/rootless Podman gates; reuse valid unaffected evidence; no full matrix per provider PR.
- Before final v0.4.30 acceptance, all selected changes and remaining justified exceptions are evidenced.

## Boundary

Implementation in v0.4.30; no additional v0.4.26 blocker; no change to active v0.4.25 qualification. No authorization for pre-release, merge, tag or publication. Possible home for the Core part of [demo-24](../tasks/demo-24-managed-exposure-https-default.md) (managed PKI issuance for app exposure) — Maintainer decision.
