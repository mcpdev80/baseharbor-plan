# CODEX-REVIEW — PR #1384 (read-only)

Verdict: **REJECT** — exact candidate `06479fe042d4fa6c0512c2f81bbf320e08fdc7e5`.

## Identity, write set, and chain isolation

PR #1384 is open/draft, base `develop` at `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`; the PR API head and remote `work/access-profiles` both equal `06479fe042d4fa6c0512c2f81bbf320e08fdc7e5`. The base is an ancestor of the candidate. The complete name-only diff has four files:

- `internal/orgconfig/profiles.go`
- `internal/orgconfig/profiles_test.go`
- `internal/policy/assignment.go`
- `internal/policy/assignment_test.go`

No machinehttp, credential/native, or devaccess file is changed. Representative blob checks are identical across develop and candidate: `internal/machinehttp/handler.go` = `e6dd9990ee91de58f5a39903e77ba1aae1fa0484`, `internal/credential/native/sshagent.go` = `69e0e9208cd3ee3cadf38275a7172acd6def9aa7`, and `internal/devaccess/domain.go` = `631c1d5c282d4ff6e505cd0ff9f1d5c48bac34d8`.

## Six requested cases

At the exact candidate, `go test ./internal/orgconfig ./internal/policy -count=1 -v` passed. The tests and independent probes establish:

| Case | Evidence | Result |
|---|---|---|
| Valid assignment | `internal/policy/assignment_test.go:12-24`, `TestResolveAssignsAllowProvesAssignmentAdapter` | Adapter returns `Allow` for an assigned operation. |
| Revocation takes effect | `internal/orgconfig/profiles_test.go:32-57` checks removal from the manager; my temporary probe resolved through an existing adapter before and after `Revoke` | The second resolution denies with unknown-profile error. |
| Ambiguous name fails closed | `profiles_test.go:219-229`, conflicting same-name create | Rejected as `ErrDuplicateProfile`; no ambiguous selection. |
| Stale revision rejected | No revision or expected-revision field/parameter exists in `Profile`, `Manager.Update`, or `Adapter.Resolve`; no stale-revision test exists | **Not implemented / not evidenced.** |
| Foreign tenant rejected | `profiles_test.go:195-214` isolates two in-memory installation managers, but `Profile` has no tenant identity and neither API accepts a tenant context | **Not implemented / not evidenced.** Foreign installation-name preservation is not a tenant authorization check. |
| Profile edition cannot escalate | `profiles_test.go:174-187` rejects undeclared target/environment, but does not constrain an authorized operation-set increase. My temporary probe created a `read` profile, updated it to `admin`, then observed `Adapter.Resolve(..., OpAdmin) == Allow` | **Fails:** profile edit widens privilege. |

The temporary probe was created and removed only in a detached reviewer worktree; candidate files were unchanged. The escalation follows directly from `Manager.Update` (`profiles.go:316-338`): it validates shape and target/environment, then replaces the definition, with no authorization input, revision precondition, or upper-bound check on operations.

## Adapter and decision authority

`policy.Adapter` only reads a `orgconfig.Manager`, but `Adapter.Resolve` (`internal/policy/assignment.go:53-66`) directly returns the top-level `policy.Allow` or `policy.Deny`. It does not produce a finding for the existing `policy.Aggregate` path. Candidate-wide `git grep` finds `NewAdapter` only in its declaration and `assignment_test.go`; there is no production caller. This is therefore an unused second decision surface, not a connected mediator on the existing production authorization path. The card explicitly says a standalone unused adapter is incomplete.

## Hosted checks

Run `41970216583` is terminal success on the exact SHA. `PR · Source format` and `Workflow policy` passed. `PR Selected Checks`, all validation/runtime jobs, and release preflight were skipped for the draft PR; there is no successful selected-check result at this SHA. The local domain package tests passed, but do not fill the missing required cases or production integration.

## Recipe

- **Files:** `internal/orgconfig/profiles.go`, `internal/orgconfig/profiles_test.go`, `internal/policy/assignment.go`, `internal/policy/assignment_test.go`, plus the already-owned production caller/interface once identified by the card owner.
- **Change:** enforce an expected revision on update and reject stale writes; bind profile operations to the existing actor/tenant authority; prevent an edit from exceeding the actor's current authorized operation set. Make the adapter contribute a constrained finding/input to the existing aggregate decision path, and connect it to the production caller. Do not add a parallel final `Allow` authority or treat installation separation as a tenant check.
- **Test requirement:** retain the six positive/negative cases; specifically verify revoked profiles deny through the same adapter, stale revision conflicts, foreign-tenant requests deny, and a `read` actor cannot edit a profile to `admin`. Add a production-path test proving the existing policy authority consumes the adapter result and still applies other mandatory denies. Run the task's selected checks and obtain a terminal `PR Selected Checks` success on the exact changed SHA.
- **Stop criterion:** stop and reject if a profile edit can widen effective permissions, if stale revisions or foreign tenants are not rejected, or if profile decisions can bypass the existing aggregate policy path.

No PR, merge, comment, or card action was taken.
