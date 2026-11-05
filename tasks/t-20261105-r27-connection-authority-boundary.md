---
id: t-20261105-r27-connection-authority-boundary
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Expose, inside the already accepted boundary internal/coreinstallation (authority), a resolution call that takes the VERIFIED…"
kanban_title: "Authority: target-scoped live-connection resolution without an application context"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/connection-client/blocker-1.md]
---

- [ ] t-20261105-r27-connection-authority-boundary · Authority: target-scoped live-connection resolution without an application context #task #release/v0-4-27 #status/planned #view/ready #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/connection-client/blocker-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Expose, inside the already accepted boundary `internal/coreinstallation` (authority), a resolution call
that takes the VERIFIED INSTALLATION plus the TARGET (identity/state facts it already owns) and yields the
live management-connection issuer material that `ConnectionSelection.Resolve` must check. This unblocks the
explicit-selection verification on the real `use`/`target activate` production paths
(`t-20261018-r27-connection-client`).

## Scope

- In scope: one new exported resolver in `internal/coreinstallation` + its tests; wiring evidence for the
  consuming card.
- Out of scope (hard, measured by lane w164 2026-11-05): any change to `resolveApplication`,
  `resolveApplicationCoreRuntime`, `resolveManagementConnectionIssuer` call shape, or app-command paths
  (apply/plan/destroy). Measured fact driving this card: `use` (use_target.go:19) → `target activate.Run`
  (target.go:241) / guided activation (target_activate_wizard.go:15) never build a `resolvedApplication{}`,
  and the live issuer exists only behind `application_service_issuer.go:89→:20` which requires
  `resolvedApplication` + `bhruntime.RuntimeProvider`.

## Acceptance

- The new resolver returns the issuer material from installation+target facts alone (test on the boundary,
  no fabricated app context).
- Existing app-path resolver behavior is untouched (blob-identical files listed in evidence).
- Fail-closed: unverifiable installation or foreign target yields a named error, never a permissive empty.
- Red-first is the blocker transcript itself (w164 END_BLOCKED chain above).

## Required checks

- go test ./internal/coreinstallation ./cmd/baha -count=1, build, vet, gofmt; hosted runs to terminal.

## Handoff

Coordinator decision 2026-11-05 after lane w164 honored the STOP clause with a full call-chain witness.
Consuming candidate: PR #1380 (connection-client), which resumes on a free seat once this lands.
