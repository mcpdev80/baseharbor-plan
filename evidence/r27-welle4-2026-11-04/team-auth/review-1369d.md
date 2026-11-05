# CODEX-REVIEW — PR #1369 (read-only)

Verdict: **REJECT** — exact reviewed head `6ec7a5db8e116da928cb90bb5ce9b2879529cf02`.

## Candidate and base refresh

The PR API recorded head `6ec7a5db8e116da928cb90bb5ce9b2879529cf02`; its commit has parents `a7fa573d5bff6e043fbecbb2aeb79833605dc304` and `ea3fb38e8f372ab2da38c10d964f3ea452fb8561`. The merge commit is the base refresh from `origin/develop`. The tree delta from `a7fa573d` contains 19 paths, all from the refreshed develop side; the `internal/operatorauth` implementation and `cmd/baha` provider wiring are unchanged. The PR has since been merged by the Owner at `1a84726d90aa5441d7346d20fa403d38667a61e9`; this review makes no PR or card changes.

## Findings

The production authorization path does call `resolveClaimMembershipToTenant` from `internal/operatorauth/authorization.go:188-201`, and fails closed if resolution returns an error. The claim-to-membership resolver at `internal/database/identity_tenant_resolver.go:103-115` reduces both `group:team-a` and `app-role:editor` to the role string `team-a` / `editor`; its query at lines 132-138 then filters memberships only by issuer, subject, and `lower(m.role) = ANY(claimRoles)`. It does not bind a team/group claim to a tenant.

The purported foreign-tenant coverage at `internal/operatorauth/authorization_claims_test.go:192-212` uses only `Groups: [team-a]` while its stub returns `tenant-b/editor`. That is denied because `editor` is absent from the claims; it does not exercise the foreign tenant case when the user actually has the `editor` role.

I added a reviewer-only probe in an isolated temporary worktree, without changing the candidate: a verified principal with `Groups:[team-a]` and `AppRoles:[editor]` was given a provider result `tenant-b/editor`, then passed to `AuthorizeMachineOperation`. The authorization returned `allowed=true, err=nil`; the probe failed its expected-denial assertion. This reproduces the missing team-to-tenant binding on the reviewed source. The candidate's existing focused `TestClaimMappingTwoTeamIsolation` itself passes (`go test ./internal/operatorauth -run '^TestClaimMappingTwoTeamIsolation$' -count=1 -v`), but its test data does not cover the claimed role combination above.

## Recipe

- **Files:** `internal/database/identity_tenant_resolver.go`, `internal/operatorauth/authorization_claims_test.go` (and the narrow provider contract/type if needed).
- **Change:** preserve the identity claim's team/group identifier through membership resolution and require an explicit trusted mapping from that identifier to the returned tenant. Role equality alone must not authorize a tenant. Keep failures and ambiguous mappings fail-closed.
- **Tests:** add an authorization-level positive case mapping `team-a` to `tenant-a`; add a negative case with `team-a` plus claimed `editor` resolving to `tenant-b`; retain the existing multi-tenant ambiguity denial. Demonstrate the negative case fails on the current implementation and passes after the fix.
- **Stop criterion:** stop and reject if the trusted source for team/group-to-tenant mapping cannot be identified, or if any mismatch/ambiguous mapping authorizes an operation.

## Status evidence

- `PR Selected Checks`: terminal `success`, GitHub Actions integration `15368`, run `41919808966`.
- The PR is already merged by Owner; feature ref no longer exists in `ls-remote`. `origin/develop` observed at `0476164a96d7e8bccdacf4ffc1f2179a6b73f70e`.
- Candidate source SHA remains recorded by the PR API as above. No PR, branch, or card action was taken in this review.
