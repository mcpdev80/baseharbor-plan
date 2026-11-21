---
id: t-20261121-destroy-authority-stamp
card_number: "0428-214"
card_short_title: "0428-214 destroy stamp"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget shows which authority mode admitted installation.destroy, instead…"
kanban_title: 0428-214 · 0428-214 destroy stamp
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-destroy-authority-stamp · installation.destroy authorization assertion runs on a stamped context #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` shows **which authority mode** admitted
`installation.destroy`, instead of printing an authorization green that its own stamp produced.

## Why

H-V23 section 1 (akte `evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, Karte A) is the single confirmed
falschlich-authentifiziert case: `cmd/baha/core_installation_runtime_test.go:323` asserts that the fixture cleanup context
is AUTHORIZED for `installation.destroy` in environment `prod`, inside a test whose contract is that cleanup authority is
bound to its local target. The context is stamped at `:298-306`
(`WithEnforcement` -> `WithVerifiedPrincipal` -> `WithMembershipProvider`), and `WithVerifiedPrincipal` implies
`WithEnforcement` (`internal/operatorauth/context.go:54-57`), so `internal/operatorauth/authorization.go:285` is
unreachable by construction. The green demonstrates the fixture, not production authority.

## Scope

Allowed write-set:

- `cmd/baha/core_installation_runtime_test.go`

Forbidden: production code, `internal/operatorauth/**` (Owner rail), every other `cmd/baha/` file — 0428-204 owns those
while it runs, so this card stacks behind it.

## Acceptance criteria

1. Either the authorization is asserted through the boundary the cleanup path really takes
   (`ensureOperatorAuthForBoundary`, `cmd/baha/operator_auth_boundary.go:55`), or the assertion moves to a positive-path
   test and the denial test stays unstamped.
2. The denial subtests (remote AccessProvider, unrelated verified principal) keep passing with the same assertions.
3. The output names the admitting mode (`authenticated` from a session, or `local-runtime` from the grant); an unstamped
   synthetic principal is not acceptable proof.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-214` |
| Route | `auto-discovery` |

## Dependencies

Needs the seam helper that 0428-204 introduces (content, not a merge wait). Do not commission while 0428-204 writes in
`cmd/baha/`.

## Stop and report

If the mode cannot be observed without touching `internal/operatorauth/**`, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-1.md`.

kommissioniert auf dem freien ornith-sitz: branch vom head der basis-lane 0428-204 (7db142852d22), base-ref des PRs auf den lane-branch 'lane-0428-204-cli-operator-entrypoints'. write-set genau eine datei: cmd/baha/core_installation_runtime_test.go. konfliktfrei gegen 213 und 207. lane 5b17f066, modell verifiziert.
