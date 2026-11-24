---
id: t-20261124-r28-trusted-local-failopen-seam-dead
card_number: "0428-270"
card_short_title: "trusted-local seam dead"
type: bug
areas: [security, access, cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Either the trusted-local fail-open branch in authorizeMachineOperation becomes a live, policy-driven path for trusted host-local…"
kanban_title: 0428-270 · trusted-local seam dead
priority: normal
depends_on: [t-20261120-trusted-local-operation-grant]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-trusted-local-failopen-seam-dead · ManagedEnvironment always reports managed, so the trusted-local fail-open branch in authorizeMachineOperation is unreachable for every production caller. #task #release/v0-4-28 #status/planned #view/ready #area/access #area/cli #area/security #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-trusted-local-operation-grant](t-20261120-trusted-local-operation-grant.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Either the `trusted-local` fail-open branch in `authorizeMachineOperation` becomes a live, policy-driven path for trusted host-local operators, or it is deleted together with the comment that promises it. It must not remain an unreachable seam whose documented contract and actual behaviour disagree. Witnessed on develop 3ebfb90d (bughunt-hv26 F3):

- `internal/operatorauth/config.go:89-91`: `ManagedEnvironment(environment)` returns `ManagedEnvironmentWithPolicy(environment, false)`, and `ManagedEnvironmentWithPolicy` (`config.go:108-110`) is `return !trustedLocal` — so `ManagedEnvironment` is `true` for every environment name (dev/development/prod/arbitrary alike).
- `internal/operatorauth/authorization.go:276-282`: the branch `if !ManagedEnvironment(decision.Context.Environment) && !ok { decision.Allowed = true; Actor = {Mode: "trusted-local"} }` is therefore dead for every caller of the unversioned form. On develop, `grep -rn 'ManagedEnvironmentWithPolicy(' --include='*.go'` outside tests hits only `config.go:89-90` and its own definition: no production caller ever passes `trustedLocal = true`.
- `TrustedLocalForEnvironment` (`config.go:98-100`) is likewise hard-coded `false`.
- The real host-local trust seam is `verifiedLocalWorkloadAuthority` (`cmd/baha/local_workload_authority.go:49-157`), which reaches the `local-runtime` grant at `authorization.go:270-275` through `AuthorizeMachineOperationWithLocalGrant`, never the `trusted-local` branch.

## Acceptance

1. One decision, stated in the PR: (a) wire an explicit, non-name-derived `trustedLocal` policy source into the production callers so the branch is reachable where intended, or (b) delete the `trusted-local` branch and correct the contract comments at `internal/operatorauth/config.go:86-106`. No third option: the seam ends up provably live or provably absent, never both.
2. One regression test proving fail-open is CLOSED on the affected path: with no authenticated operator and no local-runtime grant, the machine operation is denied with `operator_authentication_required` (`authorization.go:284-286`) and never carries `Mode: "trusted-local"`. The test must go RED if the branch is re-opened by environment name alone.
3. The test is picked up by the CI group that covers `internal/operatorauth` package checks (the authority-package group, "PR · Go unit"); the evidence names job, trigger and run URL (AGENTS 5.3).

## Boundaries

`internal/operatorauth/config.go`, `internal/operatorauth/authorization.go` and their tests, plus the comment sites the chosen option touches. No change to `verifiedLocalWorkloadAuthority` semantics (0428-188 owns the local grant). No `.github/**` or `scripts/**` edits — the gate-selection gap for this seam is the separate Owner card 0428-272.

## Related

- Depends on 0428-188 (`t-20261120-trusted-local-operation-grant`, closed accepted, baseharbor#1717): that card bound local operation grants to one typed operation and removed the dev-to-trusted-local auto-admit; this finding is the residue of that removal.
- Qualification gap: changes to this seam are routed to package checks only, never to a native runtime gate — Owner card [0428-272](t-20261124-r28-runtime-authority-gate-routing.md).
- Source: bughunt-hv26 F3 dossier `evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (develop 3ebfb90d).
