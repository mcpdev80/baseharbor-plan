# PR #1369 CI triage (read-only)

Date: 2026-11-04  
Task: `cx07-team-auth-triage` / `t-20261018-r27-team-auth`  
PR: [mcpdev80/baseharbor#1369](https://github.com/mcpdev80/baseharbor/pull/1369)  
Inspected candidate: `f9507ff6ee00694b0125c577a4890918695b3fa8`  
Develop: `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`

## Findings

GitHub Run [41884936792](https://github.com/mcpdev80/baseharbor/actions/runs/41884936792) is terminal `completed / failure` on the inspected PR head. It contains two failing validation jobs and one failed aggregate check. The failures in both test jobs have the same cause; they are not independent test failures.

| Run ID | Check / job | Classification | Evidence and reason |
| --- | --- | --- | --- |
| `41884936792` / job `126766941411` | `PR · Validation · cli-package-tests` | A — product | The focused `cmd/baha` suite fails at the same auth denial as the Go unit suite, on the PR candidate. This job does not show an independent environment error. |
| `41884936792` / job `126766941366` | `PR · Validation · go-unit-tests` | A — product | The `./...` suite reaches the same failing `cmd/baha` test and exits nonzero. The failure is candidate-specific: the same test passes on Develop in the local comparison below. |
| `41884936792` / job `126770680413` | `PR Selected Checks` | C — dependent aggregation/order | The final aggregate fails after `pr_validations` fails; it reports the upstream dependency and introduces no separate base-order or environment fault. |

Verbatim failure lines from the hosted run:

```text
cli-package-tests: app_input_resolver_first_run_test.go:56: initialize repository deployment inputs: The verified operator carried no claim-based tenant membership that permits this machine operation.
cli-package-tests: --- FAIL: TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation (0.00s)
go-unit-tests:     app_input_resolver_first_run_test.go:56: initialize repository deployment inputs: The verified operator carried no claim-based tenant membership that permits this machine operation.
go-unit-tests: --- FAIL: TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation (0.00s)
go-unit-tests: FAIL github.com/mcpdev80/baseharbor/cmd/baha 298.897s
PR Selected Checks: BLOCKED: required job did not succeed: pr_validations
PR Selected Checks: BLOCKED: workflow job did not succeed: pr_validations
```

The category count is A: 2, B: 0, C: 1. `PR Selected Checks` is downstream aggregation (C); the root failures are the same product-path denial (A).

## `TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation`

The test is not skipped or falsely reported as passing. The hosted logs show `=== RUN`, then a failure at `app_input_resolver_first_run_test.go:56`; they do not show `SKIP`. The test contains side-effect assertions at lines 59–84, but they are unreachable on the PR head because `runRepositoryRuntimeInitResolved` returns the authorization error at line 55 first. Thus this red execution does **not** exercise whether the deployment record/input state is written.

The `0.00s` duration is explained by the early authorization rejection, not by a zero-work successful test. The test fixture supplies only `Subject` and `Issuer`; `IssuerVerified` is false, it has no group/app-role claims, and it installs no MembershipProvider (`cmd/baha/app_input_resolver_first_run_test.go:55`). On this PR, `AuthorizeMachineOperation` requires claim membership when a principal exists, obtains the provider from context, and fails closed if resolution fails (`internal/operatorauth/authorization.go:180–199`). `WithMembershipProvider` is only an optional context attachment (`internal/operatorauth/context.go:62–67`); a SHA-exact production-source search found no call site outside test files.

### Focused two-head comparison

Ran the named test separately in detached worktrees for both exact SHAs. The isolated PostgreSQL fixture used the same `postgres:18-alpine`, database/user/password and `BASEHARBOR_TEST_DATABASE_URL` pattern as `scripts/pr-unit-database.sh`; port `55433` was used because the script's `5433` was occupied by another session. No GitHub run was started.

Command on each worktree:

```text
go test -p 2 -vet=off ./cmd/baha -run '^TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation$' -count=1 -v
```

| Source | Result |
| --- | --- |
| Develop `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1` | `--- PASS: TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation (0.05s)`; package `ok ... 0.056s`, exit 0. |
| PR head `f9507ff6ee00694b0125c577a4890918695b3fa8` | `app_input_resolver_first_run_test.go:56: initialize repository deployment inputs: The verified operator carried no claim-based tenant membership that permits this machine operation.`; `--- FAIL ... (0.04s)`, exit 1. |

Therefore this test is red only on the PR candidate in the controlled comparison; the failure is not a Develop-base failure. The fixture is incomplete for the new policy, and the production path also lacks a MembershipProvider installation, so simply skipping or weakening the test would hide a real wiring gap.

## Product gap and lane recipe

The authorization change requires a current claim-to-membership result for any principal (`internal/operatorauth/authorization.go:188–199`), but the production tree has no `WithMembershipProvider` call site; the context helper itself is only an optional attachment (`internal/operatorauth/context.go:62–67`). The repository-init entry point authorizes before doing the state work (`cmd/baha/app_input_resolver.go:299–303`). A verified production principal therefore has no provider to resolve its membership and is denied before the pending deployment/state assertions can be reached.

Recipe for the owning implementation lane:

1. Implement or connect the production MembershipProvider to the current authoritative membership and revocation source; resolve only membership bound to verified issuer+subject and group/app-role claims.
2. Install that provider in the authenticated command/runtime operation context before `authorizeApplicationOperation` is called. Keep missing, revoked, foreign-tenant and insufficient-role cases fail-closed.
3. Repair the test fixture to represent a genuinely verified principal with an asserted role and an installed provider. Keep `TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation`'s existing assertions that the deployment record and input state exist and that state is `configured`, not applied/verified. Add negative no-membership/revoked/foreign-tenant cases asserting denial before state mutation.
4. Run `go test ./cmd/baha -run '^TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation$' -count=1` and the relevant `internal/operatorauth` tests; then run the required selected hosted checks on the resulting candidate.

## Candidate and repository proof

Literal `git ls-remote` output:

```text
2ea2c6f1d344cca2b21c17e7acbebf711b1511a1	refs/heads/develop
f9507ff6ee00694b0125c577a4890918695b3fa8	refs/heads/work/w92-team-auth-claim-mapping
```

Literal `git merge-base` output:

```text
2ea2c6f1d344cca2b21c17e7acbebf711b1511a1
```

`git merge-base --is-ancestor 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 f9507ff6ee00694b0125c577a4890918695b3fa8` exited `0`.

No product source, workflow, PR metadata or status was changed. No rerun, dispatch or merge was performed. The existing shared product worktree had unrelated dirty/untracked paths before and after this triage; they were left untouched. Temporary detached worktrees, DB container and local build cache used for the comparison were removed.

## END

END_DONE cx07-team-auth-triage: klassifikation=A:2 B:0 C:1 repo-init-test=echt rot rezept=internal/operatorauth/authorization.go:188-199 | PR #1369 denies before state mutation because production claim-membership wiring is absent; the exact test passes on Develop.
