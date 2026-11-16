# CODEX-REVIEW — PR #1591

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-cli2-env-registry`  
**Candidate:** `4d14741ee9485b7e0c346fa873ed59f637e71b68`  
**PR base:** `lane-0428-uid-target` @ `ae0602e02882619dea151dc82d62b98b72481566`  
**Exact-head CI:** run `43815697313`, event `pull_request`, created `2026-11-16T06:17:04Z`, COMPLETED SUCCESS, exact head. `git diff --check` clean.

## Verdict: REQUEST CHANGES

The association write paths validate incoming kind and ID, but the public authoritative read path `EnvironmentRecordAssociations` unmarshals persisted `record.Associations`, validates the record identity/binding, then returns `normalizeAssociations(record.Associations)` without validating each persisted binding. `normalizeAssociations` deduplicates; it does not enforce `validateAssociationSubjectKind` or `validateAssociationSubjectID`. A malformed or foreign entry in `environment.json` can therefore be exposed as an authoritative member even though the file comments promise fail-closed handling of corrupt bindings. The read is a central contract surface, not just a malformed-write case.

## Recipe / stop

- **File/change:** in `internal/deployment/environment_association.go`, validate every decoded association's kind and ID before returning it. Apply the same validation to every persisted association before register/deregister logic can treat or preserve it as trusted. On any invalid entry, return an error and do not rewrite the record.
- **Required tests:** table-test unknown/empty kind and empty/path-bearing/invalid ID in persisted records through the read and mutation paths; assert fail-closed behavior and byte-for-byte no-write on failed mutation. Keep existing duplicate, conflict, permission, and restart coverage.
- **Checks:** rerun the focused deployment tests and relevant build/vet locally; ensure the required PR checks execute these tests on the corrected exact head.
- **Stop:** if a compatibility requirement permits legacy malformed entries, obtain an explicit contract ruling and define a safe migration; do not silently normalize invalid membership into authoritative state.

Read-only SHA-exact review; no product files changed; no merge.
