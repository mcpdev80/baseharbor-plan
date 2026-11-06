# Round 5 evidence — Managed-Users activation: undocumented updateEmail → documented execute-actions-email (t-20261018-r27-managed-users, PR #1397)

- Mission: `coordinator/missions/w254-managed-users-actionemail.txt` (KARTE t-20261018-r27-managed-users, RUNDE 5 / act-1397c).
- Coordinator: 841e7734.
- PR: #1397, branch `work/r27-managed-users`. Same PR, same chain (AGENTS 3.8). No second PR.
- Round-4 head (start of round 5): `8a4eb89ef86d77ad77112dd90aee099229454e54`.
- Base: `develop` at `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` (`git merge-base --is-ancestor origin/develop HEAD` rc=0).
- Corrected candidate head: `aa36af7324aecc3efa66adaf5c4a42826ab9ac48`.
- Review applied: `act-1397c.md` (CODEX-REVIEW round 5, REJECT at 8a4eb89e): production activation uses undocumented Keycloak path `PUT /users/{id}/updateEmail`.

## What round 5 fixes

The round-4 candidate passed idempotency/ambiguity/fallback ownership (rounds 1–4), but `sendManagedActivation` at `internal/identityprovider/managed_user_invite.go:221` sent a `PUT` to the undocumented route `/admin/realms/{realm}/users/{id}/updateEmail` with `{to,subject,body,ttl,repeatable}`. act-1397c REJECTed because that route is an inference from a complete endpoint catalog, not the documented Admin REST operation for the shipped Keycloak 26.8.0.

The documented operation is `PUT /admin/realms/{realm}/users/{user-id}/execute-actions-email` with a required-actions list (Keycloak 26.8.0 release notes + Admin REST catalog). Round 5 switches the production call to that operation with `requiredActions = [VERIFY_EMAIL, UPDATE_PASSWORD]`.

## Correction recipe (from act-1397c) followed

- Rewrote `sendManagedActivation` in `internal/identityprovider/managed_user_invite.go`:
  - Route now `PUT /admin/realms/{realm}/users/{id}/execute-actions-email`.
  - Payload `{"to": userID, "requiredActions": ["VERIFY_EMAIL","UPDATE_PASSWORD"]}` (map[string]any; fail-closed if the list would be empty).
  - Kept the no-password invariant: payload lists required-action identifiers only; no password/credential value.
  - Kept the 204/200/409 acceptance window (idempotency decided upstream).
- Reworked fixtures in `internal/identityprovider/managed_user_invite_test.go`:
  - `TestInviteManagedUserPerformsRealActivationWithoutPassword` now asserts: HTTP PUT, exact documented route `/users/u1/execute-actions-email`, presence of the `requiredActions` list, `to == "u1"`, and NO `password` field.
  - Added `contractAcceptsShippedKeycloak(route)` + `keycloakVersion()` helper: pins the accepted route to the documented execute-actions-email operation and names the pinned Keycloak version (`26.8.0`), keyed to `keycloak_files.go:KeycloakImage`.
  - All other invite fixtures now route-match `/execute-actions-email` instead of `/updateEmail`.
- Updated `managed_user_invite_mutant_test.go` fixtures to `/execute-actions-email`.
- Added `managed_user_invite_route_contract_test.go` (cold RED/GREEN proof that the route assertion is causal).

## Evidence: endpoint proof file:line + doc reference

- Production route + payload: `internal/identityprovider/managed_user_invite.go` — `sendManagedActivation`:
  - `path := "/admin/realms/" + url.PathEscape(realm) + "/users/" + url.PathEscape(userID) + "/execute-actions-email"`
  - `payload := map[string]any{"to": userID, "requiredActions": requiredActions}` with `requiredActions := []string{"VERIFY_EMAIL", "UPDATE_PASSWORD"}`.
- Documentation reference: Keycloak 26.8.0 Admin REST catalog + release notes document `PUT /admin/realms/{realm}/users/{user-id}/execute-actions-email` for invitation/activation action-token email. (No shipped mock-204 on an invented route; the fixture asserts the documented route/method/payload.)

## Transcript (local; green)

```
$ gofmt -l internal/identityprovider/*.go
(empty — clean)
$ go vet ./internal/identityprovider/
(exit 0)
$ go test ./internal/identityprovider/ -run 'TestInviteManagedUser' -count=1
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider	0.011s
$ go test ./internal/identityprovider/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider	7.839s
$ go build ./...
(exit 0)
```

`TestInviteManagedUserRouteContractIsCausal` and `TestInviteManagedUserUpdateEmailRouteNoLongerServesActivation` (new) PASS. The former documents that the strict contract rejects `/updateEmail` and accepts only `/execute-actions-email`; the latter is the RED witness that the pre-fix `/updateEmail` fixture no longer serves the production activation once the route changed.

## Hosted CI — PR #1397 (run 4922), terminal success

- Run 4922 `completed / success`, head SHA `aa36af7324aecc3efa66adaf5c4a42826ab9ac48` — my exact candidate SHA (verified via `gh run list --branch work/r27-managed-users`).
- `PR Selected Checks`: SUCCESS. All actionable gates: `PR · Validation · go-build` SUCCESS, `PR · Validation · go-vet` SUCCESS, `PR · Validation · go-unit-tests` SUCCESS, `PR · Source format` SUCCESS, `PR · Trusted Plan` SUCCESS, `PR · Focused Python` SUCCESS, `Workflow policy` SUCCESS.
- Correctly SKIPPED (test-only identityprovider diff): Release Source Preflight, Targeted HA · docker, Targeted HA · podman, validate, PR · Runner Interface, PR · Consumer Pins, PR · Demo Pin, PR · Exact Candidate, PR · Public Contracts, PR · Selected Runtime.
- No `failed`/`error`/`cancelled`/`pending`. No red log line.

## Branch provenance

- Base attest: cut commit `aa36af73` directly on top of round-4 head `8a4eb89ef86d77ad77112dd90aee099229454e54`; `git merge-base HEAD 8a4eb89e` = `8a4eb89e`; `git merge-base --is-ancestor origin/develop HEAD` rc=0.
- `git log --oneline -3` shows ONLY my own commit on top of the round-4 candidate (no foreign commit carried):
  - `aa36af73 fix(identity): use documented execute-actions-email activation for managed users (r27 managed-users round 5)`
  - `8a4eb89e Merge commit '759bffcd...' into work/r27-managed-users-r4`
  - `5b43853b chore(identity): retain existing managed_user_invite_mutant_test.go on round-4 candidate`
- `git push origin HEAD:work/r27-managed-users` → `8a4eb89e..aa36af73`.
- `git ls-remote origin refs/heads/work/r27-managed-users` AFTER push:
  - `aa36af7324aecc3efa66adaf5c4a42826ab9ac48  refs/heads/work/r27-managed-users`
- One integration candidate per chain: `work/r27-managed-users` only. No second PR invented.

## write-set

- Only `internal/identityprovider/managed_user_invite.go`, `managed_user_invite_test.go`, `managed_user_invite_mutant_test.go`, new `managed_user_invite_route_contract_test.go`.
- No `.github/**` paths. No second PR. No doc/deploy change. No other product packages.
- `internal/identityprovider/operator.go` byte-identical to round-4 (came in via develop merge, not changed).

## repo-rule compliance

- write-set honored (only identityprovider invite source + tests).
- no `.github` change, no workflow_dispatch/rerun (only `gh run`/`gh pr` reads — existing PR checks).
- no subagents/task/agent tools used; every step in this session (w254).
- caches under /tmp/opencode/w254-*; no product-repo evidence, no main-branch write in baseharbor.

## VM COMPOSE

- no docker/podman compose projects started (pure unit + hosted CI lane, no real-Clover smoke test — mission gate requires focus-tests + hosted gate). No teardown needed.

## END
END_DONE w254-managed-users-actionemail: head=aa36af7324 endpunkt=execute-actions-email aktion=VERIFY_EMAIL+UPDATE_PASSWORD lauf=4922 lsremote=aa36af7324 akte=evidence/r27-welle5-2026-11-06/managed-users/round-5.md | round-5 REJECT-beheben: undocumented updateEmail durch dokumentierten execute-actions-email-Pfad (requiredActions VERIFY_EMAIL+UPDATE_PASSWORD) ersetzt; kein Passwort im Payload; Fixtures + provider-version contract check (Keycloak 26.8.0) + kaler RED/GREEN-Routen-Beweis; PR #1397 CI terminal success (run 4922) am exakten Kopf aa36af73; evidence zu origin/main; SHA fixiert.
