---
id: core-209
title: Track future capabilities and integrations
status: open
release: backlog
parent: ""
sources: ["mcpdev80/baseharbor#209"]
---
# core-209 · Track future capabilities and integrations

Source: [baseharbor#209](https://github.com/mcpdev80/baseharbor/issues/209) (`status/backlog`). Unscheduled ecosystem work; promoting an item needs an explicit scope decision. Children: core-100, core-181 (see [views/epics.md](../views/epics.md)).

## Goal



## Content

Carried over from the source with minimal editing.

### Purpose

This issue is the **post-v0.5 ecosystem backlog** for useful capabilities, providers and integrations that are intentionally **not required to complete the BaseHarbor core platform**.

The v0.5 line is now focused on productizing the existing architecture instead of continuously adding products.

> **Simple by default. Secure by default. Explicit when needed.**

BaseHarbor core owns application intent, capability semantics, provider contracts, policy, lifecycle, state, reconciliation, verification and evidence. Infrastructure products remain replaceable providers/integrations.

### Deferred from the former v0.4.x capability expansion

The following work remains valuable, but moves behind the v0.5 core/product milestone:

- Grafana visualization integration (former #166)
- messaging semantics/providers: queue, pub/sub, streams (former #167)
- AI inference/model-access capability (former #168)
- application MCP provide/consume capability (former #169; distinct from BaseHarbor's pre-v0.5 agent MCP interface #215)
- vector search/RAG bindings (former #170)
- second traffic/exposure provider such as Traefik (former #171)

These items are **not cancelled as ideas**. They are deliberately deferred so they can validate the provider/capability ecosystem after the core platform is stable.

### Post-v0.5 developer/admin tooling

Provider-native administration and developer UIs are useful, but they do not belong in the pre-v0.5 contract freeze unless a later architecture finding proves otherwise.

Candidate tooling:

- PostgreSQL: pgAdmin as optional developer/admin UI;
- Managed Identity: Keycloak Admin Console as optional provider-native administration UI;
- Cache/Valkey: Valkey Admin as optional developer/admin UI where Valkey is the selected provider;
- Secrets/OpenBao: OpenBao UI as optional provider-native administration UI;
- Observability: Grafana as the preferred cross-tool visualization UI for metrics/logs/traces where applicable;
- Prometheus native UI remains diagnostic tooling rather than an application capability.

Desired BaseHarbor developer experience may later converge on a provider-neutral convenience surface such as:

```text
baha open sql
baha open cache
baha open identity
baha open secrets
baha open observability
```

The exact command shape is intentionally **not frozen here**.

BaseHarbor should resolve the selected provider and open or expose the appropriate native tool without making pgAdmin, Keycloak, Valkey Admin, OpenBao UI, Grafana or another product part of portable application intent.

##### Environment policy expectations

Administrative/developer UIs must follow environment-aware secure defaults:

```text
dev
  -> convenient local/private availability

test
  -> restricted/private by default

prod
  -> restricted/private or explicit on-demand access
  -> never publicly exposed by default
```

This follows the same principle as Swagger/OpenAPI developer tooling: convenience in development must not imply public production exposure.

Provider-native administration may remain available to operators for expert drill-down even when normal BaseHarbor users and agents primarily use `baha`, JSON or MCP.

##### Security expectations

- no provider admin UI receives broader credentials than required;
- no permanent admin credential is injected merely for UI convenience;
- prefer short-lived/dynamic credentials where providers support them;
- PostgreSQL admin tooling should be compatible with OpenBao-issued dynamic database credentials;
- Keycloak provider administration remains separate from application OIDC endpoints;
- tooling exposure must respect environment policy, ownership, authentication and audit/evidence;
- adding an admin UI must not create a new application capability or leak provider-specific fields into portable intent.

##### Identity credential boundary

Application-user passwords remain owned and verified by the selected identity provider and must not be mirrored into OpenBao.

OpenBao remains appropriate for machine/provider secrets such as:

- provider administrative credentials;
- OIDC client credentials where symmetric credentials are required;
- mTLS private keys/certificates;
- PostgreSQL/database credentials;
- other BaseHarbor-managed machine secrets.

Where passwordless or passkey authentication is configured, BaseHarbor should prefer provider-native enrollment/recovery flows rather than handling end-user credential material itself.

Related pre-v0.5 identity foundation: #363.

### Rule for future additions

Before any deferred item enters the implementation roadmap, answer:

1. Is this a BaseHarbor **core primitive**, or can it be implemented as a provider/integration?
2. Does it require a genuinely new portable application capability?
3. Can it use the existing provider protocol, lifecycle, placement, policy and conformance model?
4. Can it be added without product-specific branching through the core?
5. Does it preserve the minimal developer experience?
6. Does it preserve fail-closed, least-privilege and secret-safe behavior?

If a feature needs broad core changes, first treat that as an architecture finding rather than adding a product-specific shortcut.

### Post-v0.5 candidate order

No fixed release numbers yet. Likely sequence:

- optional visualization integrations such as Grafana;
- second/reference providers to prove provider portability;
- messaging;
- AI inference/model access;
- application MCP provide/consume semantics;
- vector search/RAG;
- additional provider implementations and community/vendor integrations.

Kubernetes/OpenShift/cloud runtimes remain separate later runtime tracks and are not part of this ecosystem backlog.

### Provider ecosystem target

The desired path after v0.5 is:

```text
Capability Specification
        ↓
Provider SDK / Starter Kit
        ↓
Provider implementation
        ↓
Conformance
        ↓
Registry / discovery
        ↓
Use without BaseHarbor Core changes
```

### Non-goals

- no pressure to ship every listed integration;
- no logo-driven roadmap;
- no mandatory Grafana/AI/messaging stack;
- no application-contract fields that exist only to satisfy one product;
- no weakening of secure defaults for developer convenience.

### Other post-v0.5 platform tracks

The following platform work is also intentionally outside the v0.5 core milestone:

- managed human identity / OIDC / RBAC / JIT production access (#100);
- topology / HA intent beyond the current single-host Compose runtime (#103);
- air-gapped operation, private OCI registry policy and offline bundles (#181);
- Kubernetes/OpenShift/cloud runtime implementations in their dedicated later tracks.

Environment-aware secure defaults themselves are **not deferred**; they moved into v0.4.13 (#211). Human identity/JIT and HA topology remain later concerns.

### Important MCP distinction

Two separate concerns exist:

1. **#215 — BaseHarbor agent MCP interface (pre-v0.5, mandatory):**
   BaseHarbor itself exposes safe semantic tools/resources so coding agents can inspect, plan and operate BaseHarbor.

2. **#169 — application MCP capability (post-v0.5, deferred):**
   an application declares that it provides or consumes MCP as portable application semantics.

The first is a BaseHarbor interface. The second is an application capability. They must not share lifecycle/domain logic merely because both use MCP transport concepts.

## Acceptance

- Not defined in the source.
