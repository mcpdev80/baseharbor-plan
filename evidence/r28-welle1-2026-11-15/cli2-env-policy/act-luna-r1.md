# CODEX-REVIEW — PR #1594

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-cli2-env-policy`  
**Candidate:** `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d`  
**Exact-head CI:** run `43794356032`, COMPLETED SUCCESS (exact SHA); affected package checks passed.  
**Scope:** SHA-exact comparison against `lane-0428-env-registry` at `b85efaf6c94cd158de68a6b8f837dc4a23be455a`; own feature commit `018b4e58` changes six policy/auth files. The wide base-to-head tree includes develop ancestry and is not all authored by this PR. `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/operatorauth/config.go` policy-aware `ManagedEnvironmentWithPolicy(environment, trustedLocal)` returns false for `trustedLocal=true`, but for false it falls back to the legacy environment-name switch. Consequently `trustedLocal=false` still treats names such as `dev`/`development` as unmanaged. The explicit policy can therefore fail open for an environment name that should be governed by the supplied policy; this disagrees with the explicit bool semantics used by the other policy-aware paths.

## Recipe

- **File/change:** `internal/operatorauth/config.go`; make the policy-aware helper derive managed state directly from the supplied `trustedLocal` policy (`managed = !trustedLocal`). Preserve legacy name-based behavior only in the compatibility wrapper by passing `TrustedLocalForEnvironment(environment)` explicitly.
- **Tests:** add table cases proving explicit `trustedLocal=false` is managed for `dev`, `prod`, and an arbitrary name, while explicit true remains trusted-local; retain legacy wrapper behavior tests. Run `go test ./internal/operatorauth ./internal/application ./internal/serviceaccess` and the exact-head CI required by the lane.
- **Stop:** stop if the intended meaning of the bool is not the one encoded by `ResolveWithPolicy`; obtain a contract correction before changing semantics.

Read-only review; no merge performed.
