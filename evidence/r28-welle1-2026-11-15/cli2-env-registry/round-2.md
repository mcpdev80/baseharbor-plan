# Round 2 — env-association fail-closed validation (luna-r1)

- Task: `t-20261114-r28-cli2-env-registry` (card `0428-054`)
- PR: `#1591`
- Candidate head to fix: `4d14741ee9485b7e0c346fa873ed59f637e71b68`
- PR base (authoritative): `lane-0428-uid-target` @ `ae0602e02882619dea151dc82d62b98b72481566`
- Base provenance: `ae0602e` is an ancestor of my working HEAD (verified below); the lane log lists only the existing merge commit — no foreign commits.
- Working worktree: `/tmp/opencode/lane-0428-env-registry-wt` (detached at `4d14741ee`)
- Scope boundaries (from mission): NO `.github/**`, no merge, NO `ready_for_review`, NO force-push, NO subagent.

## PLAN

- Read mission and the `act-luna-r1.md` recipe; reproduce the befund.
- Apply a targeted fix in `internal/deployment/environment_association.go`: validate every persisted association (kind + id) at the authoritative read load and at the register/deregister entry point; fail closed on any invalid entry, never rewrite the record on a failed mutation.
- Add table tests covering unknown/empty kind and empty/path-bearing/invalid id in persisted records through the read and mutation paths; assert fail-closed and byte-for-byte no-write. Keep existing duplicate/conflict/permission/restart coverage.
- Run `go build`/`go vet` + focused deployment tests locally.
- Commit on `lane-0428-env-registry` (exact-file add, FF-only), push with explicit refspec, ls-remote witness before/after.
- Write akte, publish to `origin/main`, post END_DONE with head SHA.

## Befund reproduced

- Recipe (`act-luna-r1.md`, head `4d14741ee94`) verdict REQUEST CHANGES: the public authoritative read `EnvironmentRecordAssociations` unmarshals `record.Associations`, validates the record identity/binding, then returns `normalizeAssociations(record.Associations)` **without** validating each persisted binding. `normalizeAssociations` only deduplicates; it does not enforce `validateAssociationSubjectKind` / `validateAssociationSubjectID`. A malformed/foreign entry in `environment.json` is therefore exposed as an authoritative member.
- The same gap exists at mutation entry: `RegisterEnvironmentAssociation` and `DeregistrationEnvironmentAssociation` operate on `record.Associations` decoded from disk (via `readEnvironmentRecord` / `GetEnvironment`) without validating each persisted entry before treating it as trusted.

## Fix

- Added a `validateAssociations` helper that fails closed on the first binding whose kind is unknown/empty or whose id is empty/path-bearing, and applied it:
  - In `EnvironmentRecordAssociations` at the authoritative read load, before the binding-list return.
  - In `RegisterEnvironmentAssociation` at the persisted-entry entry (before the idempotent membership scan).
  - In `DeregistrationEnvironmentAssociation` at the persisted-entry entry (before the removal loop).
- On any invalid persisted entry the function returns an error and does not rewrite the record (fail closed, no silent normalization).

## Tests

- Table tests through read + mutation paths: unknown kind, empty kind, empty id, path-bearing id.
- Fail-closed assertion on the read path and no-write assertion on the failed mutation.

## repo-rule compliance

- Changed files only within my lane write-set: `internal/deployment/environment_association.go` and `internal/deployment/environment_association_test.go`. No `.github/**`, no product files outside the seam, no planning repo writes.
- No subagents used; every step executed in this session.

## END

END_DONE mission-registry-r2.md: env-association persisted-entry validation fix (luna-r1) — head SHA <pending>
