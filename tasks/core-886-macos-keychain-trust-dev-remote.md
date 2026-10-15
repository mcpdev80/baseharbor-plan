---
id: core-886
type: feature
release: backlog
version: ""
parent: core-818
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#886"]
source_updated: "2026-10-15T16:49:06Z"
labels: [kind/feature, area/security, area/compatibility, status/backlog]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-886 · macOS: Keychain trust and developer remote access #task #release/backlog #status/backlog

<!-- generated:links -->
**State:** backlog  
**Release:** [backlog](../releases/backlog.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** none  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#886](https://github.com/mcpdev80/baseharbor/issues/886)
<!-- /generated:links -->

## Goal



## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

Parent: #818 · **Follow-up, not part of v0.4.29 #876** · Deferred from: #822

### Context

On 2026-10-14 the v0.4.29 macOS target was set to the **full Dev Local journey** (Docker Desktop and Podman Machine). The following parts of #822's "v0.4.25 mandatory macOS delivery acceptance" were explicitly **deferred to this issue**, so that #822 does not shrink silently:

- Dev Remote enrollment/import, scoped Core mTLS, reconnection/rotation and credential-safe offboarding on macOS.
- Automatic host trust installation into the macOS Keychain.
- The independent macOS user walkthrough for Dev Remote.

In v0.4.29 macOS host trust stays **manual and honest**: `baha trust export` plus a documented `security add-trusted-cert` next action. BaseHarbor reports the trust status read-only and never claims trust it did not verify.

### Scope

##### Keychain trust backend (behind the existing `hosttrust` semantics)

- User (login) keychain vs System keychain: the user keychain is the default and needs no admin rights; System only with explicit consent.
- `security add-trusted-cert` may raise a GUI authorization prompt. Define the behavior for interactive CLI vs JSON/MCP/non-interactive callers: typed `requires_user_interaction` instead of hanging.
- Ownership: install and remove by SHA-256 fingerprint (`security delete-certificate -Z`), keeping the existing fingerprint-ownership rule that never removes a foreign or changed anchor.
- Firefox uses its own NSS store: report this explicitly and do not claim browser-wide trust.
- Tests on hosted macOS runners only where they are reversible; real verification on the self-hosted runner.

##### Dev Remote on macOS

- Enrollment/import, mTLS, rotation, revocation and offboarding using the existing Core/Node authority. Credential material in protected owner storage; Keychain storage only if the existing protected-owner semantics are preserved.

## Acceptance

- Keychain trust install/verify/remove with fingerprint ownership; non-interactive behavior typed.
- Real Dev Remote macOS journey on an exact SHA (self-hosted runner).
- Support matrix updated only from evidence.

## Required checks

- To be defined when scheduled.

## Dependencies and file ownership

- Unscheduled (`status/backlog`). Referenced source issues: none.

## Handoff

- Not scheduled.
