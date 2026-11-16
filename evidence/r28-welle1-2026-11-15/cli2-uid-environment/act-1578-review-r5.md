# CODEX-REVIEW — PR #1578 UID environment follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-cli2-uid-environment`
**Candidate:** `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283`
**Base:** `lane-0428-uid-app` @ `22c545d8242f8cfc2acff2a5152ab5ea4f07d170`
**Exact-head CI:** run `43831549541`, event `pull_request`, `completed/success`, exact head; status independently verified from the GitHub Actions API at `2026-11-16T08:28:54Z`–`08:33:29Z`.
**Diff:** exact base-to-head has five added files, including `cmd/baha/command_target_env.go`, `environment_identity.go` and tests, and environment-domain files; `git diff --check` clean. The candidate log contains the app-base merge, prior UID implementation/correction commits, and the r6 scope-revert commit.

## Verdict: REQUEST CHANGES

### 1. Rename can still overwrite a destination created after its pre-lock check

`RenameEnvironment` checks `newPath` before taking `WithDeploymentRegistryWriteLock`. In the locked source-still-present branch it rereads the source, but does not revalidate `newPath`; it then installs with `os.Rename(tmpName, newPath)`, which replaces an existing destination on the supported Unix path. A concurrent `GetEnvironment(target, newName)` can create a different destination after the pre-lock check, acquire/release the shared lock, and then have its valid UID silently overwritten by this rename. Existing collision tests cover a destination present before the call and concurrent same-pair renames, not this interleaving.

### 2. The delivered diff still includes the CLI command declared reverted/out of scope

The round-6 evidence says CLI exposure was reverted and the slice is domain-only. Yet `cmd/baha/command_target_env.go` remains newly added in the exact PR diff. It is unregistered/orphaned (no production command-tree reference), but it is still scope content and contradicts the recorded delivery boundary. Remove it from this PR; any CLI entry belongs to the separately scoped follow-up.

## Recipe / stop

- **File/change:** `internal/deployment/environment_identity.go`; under the write lock, validate the destination for the source-still-present path as well as the source. Install only when absent, or converge only when it already has the same validated identity. Use an atomic no-replace operation or equivalent so a concurrent creator cannot be overwritten.
- **Tests:** add a deterministic regression for destination creation between the initial check and locked install (for example, coordinate a `GetEnvironment(target, newName)` creator); prove its identity is preserved and the rename fails/converges according to the contract. Retain the existing pre-existing foreign-destination and same-rename convergence tests. Ensure the tests are selected by the applicable GitHub CI group.
- **Scope:** remove `cmd/baha/command_target_env.go` from this domain-only PR and reconcile the evidence with the exact delivered file list.
- **Checks:** focused deployment/environment tests and exact-head `pull_request` SUCCESS for the corrected SHA.
- **Stop:** do not accept if the destination can be replaced after the precheck, or if the CLI file remains in this domain-only candidate without an explicit contract/scope change.

Exact-head run success does not supersede these content findings. Evidence reviewed: `round-6.md`, prior `act-1578-review-r4.md`, exact candidate diff/source/tests. Read-only review; no tests rerun, no product files changed, no merge.
