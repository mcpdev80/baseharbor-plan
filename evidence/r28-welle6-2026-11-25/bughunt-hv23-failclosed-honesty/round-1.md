# H-V23 FAIL-CLOSED-HONESTY census

**Lane:** w87-0428-216-hv23failclosed
**Type:** Read-only bug-hunt (Befund only; no product/PR/merge/subagents)
**Date:** 2026-11-24

## PLAN

- Attest develop SHA via git ls-remote against the real github.com remote
- Scan baseharbor source for denial tests routed through test-only seams (fake-pass class 1)
- Scan baseharbor source for silent-success (no-such-file / skipped / empty treated as success, class 2)
- Build the two census tables (seam-dependent? / production-reachable denial?) and (silent-success)
- For a genuine finding file one schema-correct card in an atomic commit; else befundlos
- Commit + push evidence atomically (pull --rebase origin main first)
- Verify evidence on origin/main, post END, leave cleanliness line

## Reality witnesses

Remote attest (git ls-remote, github.com/mcpdev80):

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2	refs/heads/develop
```

develop SHA = 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2

Planning repo remote (verified before first commit):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Scanned `origin/develop` (git grep against sha 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2, no checkout mutation). 83 test files use the operator-seam helper `runWithIOAsTestOperator` / `testOperatorContext` / `WithVerifiedTestOperator`.

## Census table 1: denial tests that are secretly authenticated (class 1)

Scope: tests that assert an operation is DENIED (AuthorizationResult deny / exit non-zero / fail-closed) but whose setup routes the denied operation through the operator-seam stamp helper (`runWithIOAsTestOperator` / `WithEnforcementIfAbsent` / `promptConfirmCandidate`) so the asserted denial is satisfied by a test-only code path that production never takes.

Key mechanism (verified in source): `runWithIOAsTestOperator` -> `operatorauth.WithVerifiedTestOperator` -> `WithVerifiedPrincipal` (implies `WithEnforcement`) installs a verified test-operator principal + `ReadGrantingMembershipProvider`. Because `WithVerifiedPrincipal` implies `WithEnforcement`, a test that stamps a verified principal through the seam silences exactly the operator-auth refusal it later asserts (precedent card 0428-218 / task t-20261121-mcp-operator-seam-uncovered, line: `internal/operatorauth/context.go:54-57`, `cmd/baha/test_operator_context_test.go:17-23`).

Honest design in this codebase: the operator seam is used for SUCCESS-path setup; operator-auth denials are asserted on bare `context.Background()` (no seam). Definitive intersection check — NO test asserts `authentication_failed` / "require an authenticated BaseHarbor operator" while also using the seam:

```
grep -rl "authentication_failed\|require an authenticated BaseHarbor operator" *_test.go  -> 2 files
  cmd/baha/app_list_all_targets_test.go (denial asserts on bare context; seam only on the success twin)
  cmd/baha/mcp_operator_seam_test.go   (explicitly tests BOTH directions: stamped=success, anonymous=denied)
```

| test | file:line | seam-dependent? (Y/N) | production-reachable denial? (Y/N) | note |
| --- | --- | --- | --- | --- |
| TestCorelessFreshWorkloadRuntimeLifecycle (`up` on empty repo denied) | cmd/baha/app_coreless_runtime_test.go:81 | N (seam present but denial comes from a production guard) | Y | `up --yes` denied by `requireResolvedApplicationCore` (app_up_lifecycle.go:48), which fires BEFORE `authorizeApplicationProviderChanges`/operator-auth (app_up_lifecycle.go:51). Empty-repo deny is production-reachable regardless of seam. Acceptance-gated (BASEHARBOR_CORELESS_ACCEPTANCE=1). |
| TestAppListAllTargetsStillRequiresAuthorizationWithoutTargetConfig | cmd/baha/app_list_all_targets_test.go:49-60 | N | Y | asserts operator-auth denial on bare `context.Background()`; seam only on the success twin TestAppListAllTargetsWorksAfterInstallationDestroy (line 29). |
| TestMCPWorkspaceManagedDenialPrecedesMutation | cmd/baha/mcp_workspace_mutation_test.go:89-118 | N | Y | uses `workspaceMutationClientUnauthenticated` (bare context); authenticated client only for success twin line 57. |
| TestMCPAuthoringAuthorizationDenialPrecedesIdentityPersistence | cmd/baha/mcp_application_authoring_test.go:153-170 | N | Y | uses `workspaceMutationClientUnauthenticated` (bare context). |
| TestSelectiveSecretsPlanHasStableConsentWithoutAuthorityChanges | cmd/baha/application_provider_authorization_test.go:80 | N | Y | asserts `ErrorApprovalRequired` via direct `authorizeApplicationProviderChanges(ctx,...)` call (the production function), not via the seam. |

Result class 1: befundlos for a genuine fake-pass. The seam-installed verified principal is NOT used to satisfy an asserted operator-auth denial anywhere; the two files that assert the verbatim operator-auth gate message both use bare context. The empty-repo `up` denial (the only `runWithIOAsTestOperator` + `err==nil`-as-fatal pairing) is honored by a production guard upstream of operator auth.

## Census table 2: silent-success (class 2)

Scope: any place a CLI path treats 'no such file or directory' / a skipped sub-step / an empty result as SUCCESS.

| silent-success | file:line | note |
| --- | --- | --- |
| (none found) | — | Scanned `os.Stat`/`errors.Is(err, os.ErrNotExist)` + `err == nil` + `len(...) == 0` handling in cmd/baha/*.go. All observed absence-handlers are conditional guards (file-optional / "intentionally absent from previous applied workload", app_native_backend_observation.go:104-107) or legitimate success, not swallowed errors treated as success. No CLI path returns SUCCESS on a missing required file without an ErrNotExist distinction. |

## Findings summary

befundlos. No genuine fake-pass (class 1) and no genuine silent-success (class 2) found on origin/develop sha 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2. The fail-closed-HONESTY invariant holds: operator-auth denial assertions are made on the unauthenticated (bare-context) production path; the operator seam is scoped to success-path setup; and empty/absent results are treated as intentional absence, not success.

## Fund->Karte

befundlos -> no card. Inventing nothing (mission: "if befundlos, say so and invent nothing").

## END

`END lane w87-0428-216-hv23failclosed DONE`
