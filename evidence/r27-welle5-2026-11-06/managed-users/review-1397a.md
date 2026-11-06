# CODEX-REVIEW — managed user invites, PR #1397

- Review date: 2026-11-06.
- Reviewer: Codex, GPT-6-Luna review session.
- Verdict: **REJECT** candidate `b3cb622a2e2ad8488c543f983ccebb8ecad5800b`.
- PR #1397 is OPEN against `develop`. GitHub head and `git ls-remote origin refs/heads/work/r27-managed-users` both equal `b3cb622a2e2ad8488c543f983ccebb8ecad5800b`; `develop` is `21d8d05cf1acf04729077e05eb350fcd3bb018ed` and is an ancestor of the candidate (rc=0).
- Task `t-20261018-r27-managed-users` is in `review`; all three dependencies report accepted.
- Hosted run [42137459404](https://github.com/mcpdev80/baseharbor/actions/runs/42137459404) is terminal success at the exact candidate SHA. `PR Selected Checks` is success from Actions integration 15368.

## Scope and implementation reviewed

The candidate adds exactly four paths, all under `internal/identityprovider/`: `managed_user_invite.go`, `managed_user_invite_mutant_test.go`, `managed_user_invite_test.go`, and `operator.go`. `developer_user_profile.go`, the predecessor interface, has identical blob `3b4a06294ecffed0e16b2b351c59814a0fa6d29a` on `develop` and the candidate. The write set is within the reserved identity-provider adapter and tests.

`EnsureManagedUserInvite` calls `EnsureManagedOperatorOIDC`, then loads the operator Keycloak files and invokes the provider admin adapter. This is a real production orchestration path, rather than a standalone unused adapter. The adapter calls the provider's `/users/{id}/updateEmail` endpoint with HTTP PUT and a payload containing no password or credential value. The repeat path returns without a second activation only for an owned, enabled, verified matching account.

## Checks and findings

1. Independently ran the candidate's invite fixture tests:
   `go test ./internal/identityprovider -run '^(TestInviteManagedUserPerformsRealActivationWithoutPassword|TestInviteManagedUserRepeatIsIdempotent|TestInviteManagedUserAmbiguousEmailIsRefused|TestInviteManagedUserForeignRealmIsRefused|TestInviteManagedUserUnownedAccountIsRefused|TestInviteManagedUserAmbiguityGuardEnforced)$'`
   Result: PASS (`ok`, 0.010s). The tests cover the real PUT, idempotent repeat, ambiguous initial lookup, foreign realm, and unowned/unverified existing-account cases.
2. **Blocking defect — create fallback can activate a foreign/unverified account.** When the initial lookup finds no user, `createManagedUser` accepts HTTP 201 with only an ID and performs a fallback lookup. That lookup checks only that exactly one user was returned, then returns its ID without validating the result's ID, email, enabled state, managed-invite ownership marker, credentials, or verification state. I added a temporary probe only in an isolated review worktree: POST returned `201 {"id":"u1"}`, fallback GET returned one same-email account marked `developer-access` and `emailVerified:false`, and the adapter sent `/updateEmail` and returned nil. The probe failed its required refusal assertion. The temporary probe was removed; no candidate file was changed.
3. **Blocking evidence gap — the submitted ambiguity “mutant” is not the actual source mutation.** I removed the real `len(users)>1` rejection from `resolveManagedUser` in the isolated review worktree and reran `TestInviteManagedUserAmbiguityGuardEnforced`; it remained green. The committed test's mutant helper is a separately written alternate flow and does not establish that removing the production guard makes the candidate regression fail. The requested actual-mutant-red criterion is therefore not met.
4. The positive test establishes that the tested provider fixture accepts the update-email PUT. The source call targets `updateEmail`, and no password is included in its payload. Candidate source and local fixture tests were read and run at the exact SHA.

## Correction recipe

In the create fallback, fail closed unless the single resolved record is bound to the successful create result and matches the expected email, enabled state, and `baseharbor.scope=managed-invite` ownership marker; reject any credentials or conflicting identity before sending activation. Add a regression for the POST-201/ID-only fallback returning a foreign or unverified record. Rework the ambiguity regression so removing the actual production ambiguity guard makes that same regression fail; keep the unmutated control green and record both outcomes. Push a corrected head, let its hosted checks terminate, and request a fresh SHA-specific review.

## Repo-rule compliance

Read-only candidate review. Mutations and the fallback probe were confined to an isolated temporary worktree and removed. No product branch, PR, or task card was changed. This receipt is published separately to planning `main`; unrelated planning working-tree changes are preserved.
