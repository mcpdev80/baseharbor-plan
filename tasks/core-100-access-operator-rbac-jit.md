---
id: core-100
areas: [security]
type: feature
release: backlog
version: ""
parent: core-209
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#100"]
source_updated: "2026-10-15T16:54:56Z"
labels: [kind/feature, area/security, area/identity, status/backlog]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-100 · Access: operator RBAC and just-in-time access #task #release/backlog #status/backlog #view/backlog #area/security #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** backlog  
**Release:** [backlog](../releases/backlog.md)  
**Parent:** [core-209](../epics/core-209-future-capabilities-integrations.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#100](https://github.com/mcpdev80/baseharbor/issues/100)
<!-- /generated:links -->

## Goal

Add a managed identity and authorization layer for non-local environments, especially production, without turning BaseHarbor into its own password-based identity provider.

BaseHarbor authenticates users through OIDC-compatible identity providers, maps identities to roles/policies and supports just-in-time elevation for sensitive production actions.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

> **Roadmap placement (updated for v0.4.17)**
>
> This is a **post-v0.5 advanced operator-governance track**. The minimal operator-authentication foundation moved into #363 / v0.4.17 so test/prod are not anonymously operable before the v0.5 contract freeze.
>
> v0.4.17 owns standards-compliant OIDC login, Authorization Code + PKCE/native-client flow, short-lived reusable local sessions, target/environment-aware enforcement, dev trusted-local mode and operator attribution in Audit/Evidence.
>
> This issue starts **after authentication** and owns advanced authorization/governance: role/delegation models, JIT elevation, approvals, break-glass, separation of duties, access recertification and privileged-access governance.

This issue builds on the local developer action model from v0.3 and the portable application/environment separation from v0.4. It must not block the earlier Compose-focused releases.

### Product principle

Authentication answers: Who are you?

Authorization answers: What are you allowed to do?

Environment policy answers: Under which conditions may this action happen here and now?

These concerns remain separate.

### Authentication foundation

The basic authentication flow is delivered by #363 / v0.4.17:

```text
baha login
  -> browser + Authorization Code + PKCE (or another standards-compliant native-client flow)
  -> OIDC provider
  -> short-lived reusable local operator session
```

This issue consumes the authenticated operator principal and adds advanced authorization/governance. It must not introduce a second login/session implementation.

### Authorization / roles

Support mappings such as developer, operator, admin and auditor. Role meaning is evaluated together with environment and action policy rather than hard-coded globally.

### JIT / breakglass production access

Sensitive production actions may require authenticated identity, permitted role, reason/purpose, bounded duration, MFA where configured, optional approval and complete audit trail.

The user-facing action names established earlier should remain stable. Example:

```text
baha app psql
  -> local dev: direct
  -> managed prod: policy + elevation + temporary access
```

Where technically possible, BaseHarbor and the selected secrets/database provider should issue temporary credentials rather than reveal persistent credentials.

### Non-goals

- do not require login for trusted local development
- do not make Keycloak or any specific IdP part of the Application Contract
- do not introduce Kubernetes/OpenShift solely to implement identity; runtime-provider work is separate

## Acceptance

- consume the standards-compliant authenticated operator principal/session delivered by #363
- define identity -> role/group mapping model
- integrate identity with the shared BaseHarbor action-policy model
- support JIT/elevated access requests with bounded lifetime
- support reason/purpose capture and audit IDs
- leave extension points for MFA and approval workflows
- use dynamic/temporary credentials where providers support them
- make persistent secret reveal a separate more-privileged action
- document advanced authorization/governance layered on top of the #363 local-trust/managed-authentication modes
- add security tests for revoked authorization, denied actions, elevation expiry and governance controls

## Required checks

- To be defined when scheduled.

## Dependencies and file ownership

- Unscheduled (`status/backlog`). Referenced source issues: none.

## Handoff

- Not scheduled.
