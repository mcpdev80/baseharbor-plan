# r27 managed-users — Round 1 (Welle 5, 2026-11-06)

**Lane:** w206 (Worker) · **Coordinator:** 841e7734 · **Card:** t-20261018-r27-managed-users (active)
**Repo:** mcpdev80/baseharbor · **Branch (named):** work/r27-managed-users → PR vs develop
**Evidence path (planning only, baseharbor-plan):** evidence/r27-welle5-2026-11-06/managed-users/round-1.md

## PLAN
- Read mission + full task card; bounded scope (invite via native provider admin adapter; IdP owns activation; STOP+MELDEN on foreign intent)
- Establish base: ls-remote develop == head 21d8d05c, ancestor rc=0, write SHA in evidence
- Implement managed invite adapter on develop (real provider-admin call; idempotent/ambiguous decision; bounded; production-wired)
- Add bounded tests: invite/repeat/ambiguity/denial + tolerance mutant (red) + counter-test (green)
- Local checks: race, build, vet, gofmt
- Commit, push branch work/r27-managed-users, open draft PR vs develop (ancestor + log-only-mine)
- Hosted CI TERMINAL run at PR head; record run id + terminal line
- Verify ls-remote echt == head (WORDLICH name-only); evidence ls-tree on origin/main; END to coord

## Base attestation (BEFORE branch cut)
- Base ref: `origin/develop` = `21d8d05cf1acf04729077e05eb350fcd3bb018ed`
- `git merge-base --is-ancestor origin/develop HEAD` → rc=0, ancestor YES (clean develop baseline)
- No prior `work/r27-managed-users` branch exists on origin (fresh cut from develop head)

## Scope (from mission + task card)
- Outcome: optional managed Identity path — discover/invite owned users through least-privilege native API. IdP owns password/activation/MFA.
- Explicit idempotency/ambiguity and unsupported capability handling. Profile assignment remains a separate authorized action.
- NO generic application-user management or shared admin credentials.
- Write-set (bounded reservations): `internal/identityprovider/developer_user_profile.go` + bounded managed-user admin adapter/tests.
- Foreign intent / shared admin creds → STOP + MELDEN (protected-credentials precedent).
- Predecessor: access-profiles (accepted, PR #1384). Must wire into production path; a standalone unused adapter is not complete.

## Design decision
- Existing `reconcileUserWithPolicy` sets a password directly (developer bootstrap). Managed invite must NOT set a password; it must trigger the provider-native activation/credential-set flow (Keycloak `updateEmail` → send activation link), because "IdP owns activation".
- Double-invite of identical email: KARTENTEXT decides. Decision: IDENTICAL re-invite of an already-owned, enabled, verified user is IDEMPOTENT (return nil, no duplicate side effect); a genuinely different account under the same email is AMBIGUOUS → error. Justification in akte below.
- Bounded reservate: only the managed invite endpoint; never read/write foreign scope.

## Implementation
- New file: `internal/identityprovider/managed_user_invite.go`
  - `func (a *keycloakAdmin) inviteManagedUser(ctx, realm, email string) error`
  - Verified owned realm (operator realm ownership map) before any call.
  - Exact-match user lookup by email; >1 result = ambiguous error; 0 = create-owned user (no password set) then send activation; 1 owned+enabled+verified = idempotent no-op.
  - Uses real Keycloak admin PUT `/users/{id}/updateEmail` (POST fallback) — a genuine provider call, not echo-only.
- Wired into production path in `operator.go` alongside the developer bootstrap so the adapter is not standalone.

## Tests (bounded, deterministic fixtures)
- invite new user: POST/PUT path, activation sent, no password stored.
- invite repeat identical (owned enabled verified): idempotent, zero writes.
- invite ambiguous (two accounts same email): error, no writes.
- invite foreign/unverified realm: error, no writes.
- Tolerance mutant (mutant injected): suppression of the ambiguous check → test FAILS (red). Counter-test: reverted code → green.

## Repo-rule compliance
- Only touched `internal/identityprovider/` bounded files. No `.github/`. No shared registration files.
- No credentials in source/test fixtures (protected-credentials precedent).
- No compose/docker on this host. Caches under /tmp/opencode/w206.

## End status
- Draft-stage CI on PR #1397 (run 42137046299, pull_request, draft) COMPLETED SUCCESS: Workflow policy SUCCESS, PR · Source format SUCCESS; full matrix SKIPPED (draft). Run: https://github.com/mcpdev80/baseharbor/actions/runs/42137046299
- PR marked ready (non-draft) per coordinator direction 2026-11-06; full terminal matrix triggered. Run: 42137459404 (pull_request, head work/r27-managed-users, https://github.com/mcpdev80/baseharbor/actions/runs/42137459404).
- DONE (terminal CI): run 42137459404 COMPLETED success at PR head b3cb622a2e2ad8488c543f983ccebb8ecad5800b. Jobs: PR · Source format SUCCESS, Workflow policy SUCCESS, PR · Trusted Plan SUCCESS, PR · Focused Python SUCCESS, PR · Validation · go-unit-tests SUCCESS, go-vet SUCCESS, go-build SUCCESS, PR Selected Checks SUCCESS. go-unit-tests log → `ok github.com/mcpdev80/baseharbor/internal/identityprovider 8.611s`, no FAIL.

## Final verification (pre-END)
- Branch: work/r27-managed-users. Base attestation: origin/develop = 21d8d05cf1acf04729077e05eb350fcd3bb018ed; `git merge-base --is-ancestor origin/develop HEAD` rc=0 (ancestor YES); fresh cut, no prior origin branch existed.
- PR: #1397 vs develop, draft=false, head=b3cb622a.
- ls-remote echt==head (name-only): `b3cb622a2e2ad8488c543f983ccebb8ecad5800b refs/heads/work/r27-managed-users`.
- PR head (gh) == commit == ls-remote == b3cb622a.
- log-only-mine: `git log origin/develop..HEAD` lists exactly one commit (mine); no foreign commit carried on top.
- Evidence on origin/main: blob `724b74ba161d67d5dee5352f631ab76bcfa0ae9b` at evidence/r27-welle5-2026-11-06/managed-users/round-1.md (ls-tree witness). Commit 0639811.
- No compose/docker started on this host; no stacks to bring down; no daemon pools consumed.
- Caches under /tmp/opencode/w206-* (removed worktree).
- Repo-rule compliance: only internal/identityprovider/ bounded files (operator.go + managed_user_invite.go + two test files). No .github/, no shared registration, no credentials in fixtures.
