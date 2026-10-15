---
id: core-903
title: Establish attack protection and DDoS boundaries
status: open
release: v0.4.30
parent: v0.4.30
sources: ["mcpdev80/baseharbor#903"]
---
# core-903 · Establish attack protection and DDoS boundaries

Source: [baseharbor#903](https://github.com/mcpdev80/baseharbor/issues/903). Release: [v0.4.30](../releases/v0.4.30.md). Final semantic acceptance: #174 (v0.4.31). Related: core-862 (static/vulnerability quality), core-888 (small PRs/targeted tests). Cut small executable tasks before implementation. No tasks are cut yet.

## Goal

Binding, evidenced protection boundaries against abuse and resource exhaustion — not a blanket "DDoS-/hacker-proof" claim.

## Scope

- Reuse existing security invariants, auth/mTLS, isolation, secret protection and container hardening; do not duplicate core-862.
- Inventory attack surfaces with their actual bind addresses: public gateway, login/OIDC, Console/API/MCP where offered over the network, Connector and provider/admin endpoints. Distinguish locally bound, internal and public.
- Name the owner per boundary: BaseHarbor, application, provider, host/firewall, or upstream hoster/DDoS service. Application-specific authorization/input validation stays with the application.

## Protection requirements

- Reasonable request/connection/concurrency limits, header/body limits, read/handshake/idle/backend timeouts and bounds on expensive operations. Consider upload, streaming and WebSockets where actually used.
- Login/token endpoints: suitable brute-force/abuse protection, preferably existing provider features; do not invent dangerous account-lockout or retry loops.
- Verified client-IP/proxy trust chain; never trust forwarded headers unchecked. With several gateway instances, state how effective or bypassable the limits are.
- Do not expose provider/admin access publicly by accident; prevent gateway bypass where its auth/limits are assumed.
- Rejections and overload are observable without secrets: targeted metrics/logs and manageable hints. No automatic public exposure of extra monitoring/admin endpoints.
- Large volumetric DDoS needs protection before one's own uplink (hoster/ISP/scrubbing/CDN, per protocol). BaseHarbor cannot repair saturated upstream bandwidth locally. Document responsibility and prerequisites; no specific external provider is mandatory.
- Caddy/HAProxy are not automatically a WAF or complete DDoS protection. Additional components/modules only with concrete need, verified maintainability and clear ownership. Coordinate with core-902.

## Acceptance and tests

- A short threat/protection model: surface → threat → control/owner → evidence → limit, in the existing EN/DE security documentation.
- Missing baseline controls implemented as small PRs; existing proven features are not rebuilt.
- Bounded local/disposable negative tests: unauthorized access, limited request bursts, oversized/slow requests, concurrency limits, forged forwarded headers, admin/gateway bypass and behavior after rejection. Legitimate normal access stays possible.
- No real DDoS tests and no attacks against foreign or production systems. Only small necessary provider/Docker/Podman evidence.
- Record what the product enforces, what the operator must provide and what is unqualified; missing controls are not presented as supported.
- The final v0.4.30 audit checks the agreed baseline and exact evidence.

References: [OWASP API4 – unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/), [NCSC – upstream defences](https://www.ncsc.gov.uk/collection/denial-service-dos-guidance-collection/preparing-denial-service-dos-attacks1/upstream-defences).

## Boundary

Planned for v0.4.30; no extension of active v0.4.25/v0.4.26 acceptance; no authorization for pre-release, merge, tag or publication. Newly confirmed concrete security gaps are handled separately and risk-based — not left until v0.4.30 only because of this planned audit.
