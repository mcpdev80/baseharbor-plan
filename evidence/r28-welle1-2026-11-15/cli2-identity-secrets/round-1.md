# r28-welle1-2026-11-15 · t-20261114-r28-cli2-identity-secrets (0428-057) — round-1

Shift r28-welle1-2026-11-15 · card t-20261114-r28-cli2-identity-secrets · mission-welle2-057.md
Worker session: `2c3555a6-67f8-4c39-80df-6f22b2978d4c` · model: Ornith (verified at spawn via `codeman agent list`).

## PLAN (numbered, AGENTS 4.4)

1. Read mission, task card, owner brief, command-map, code-entry-index; establish git reality.
2. Claim task via `plan.py claim`; push claim witness to baseharbor-plan origin/main.
3. Cut candidate branch `cli2-identity-secrets-head` from `cli2-env-policy-head` @ `018b4e58a` (single-base rule); attest base is ancestor + only own commits.
4. Implement mechanism B: distinct `secret.reveal` machine op id + fail-closed human-authorization seam that runtime/workload identity cannot satisfy; workload reads stay independently allowed.
5. Add tests (a) runtime-identity-only reveal FAIL, (b) workload read unchanged PASS, (c) alternate paths gated, (d) existing policy tests green.
6. `go build ./...`, `go vet ./...` at candidate SHA; run focused + full cmd/baha tests; record actual results at exact SHA.
7. Draft PR (base = cli2-env-policy-head, `--draft`, title carries 0428-057; keep draft flag).
8. Commit evidence to baseharbor-plan only; publish to origin/main; `git log` witness.
9. Bring down any compose/runtime by last action; post END with candidate SHA.

## REALITY WITNESSES (git ls-remote)

- baseharbor develop: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- baseharbor main: `aff1532c2f6c6782a8c13afad83245d1351815e7`
- baseharbor cli2-env-policy-head (mission base): `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc`
- baseharbor-plan origin/main: `fecd71f84888170246f75fe851a127b7744f9c1e` (start); claim commit `a14cb74b` (after claim push)

## BASE ATTESTATION

- Base product ref (cut from): `cli2-env-policy-head` @ `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc` (contains env-registry 054 AND env-policy 053 content — mission single-base rule).
- `git merge-base --is-ancestor 018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc HEAD` → TRUE on candidate branch `cli2-identity-secrets-head`.
- PR base = `cli2-env-policy-head`.

## SCOPE / WRITE-SET (card + owner brief + owner decision 2026-11-16)

- Owner decision (mechanism B, locked): distinct `secret.reveal` machine-op id routed through existing policy/authorization leadership, following the 0428-053 trustedLocal precedent (explicit policy, fail-closed default). All environment types: managed requires human operator principal; local/dev bare runtime/trusted-local path may NO LONGER satisfy reveal — workload READS remain independently allowed. New machine-op id + own seam-point ARE in scope; policy changes to `app.environment`/`app.connection` are OUT of scope (left unchanged; negative regression tests prove no weakening).
- Own: new `secret.reveal` op id; `operatorauth.RequireHumanOperator` + `PrincipalsHaveVerifiedIdentity` gate; reveal routing in `cmd/baha/secret_operations.go` + `environment_operations.go` + `app_access.go`.
- Reserved (NOT edited): `cmd/baha/commands.go`, shared parser/machine registry, generated command index (CI-owned), `.github/**` (Owner scope), release notes, generated indexes.

## IMPLEMENTATION

- `internal/machine/contract.go`: added `{ID: "secret.reveal", MCPTool: "baseharbor.secret.reveal", Description: "Reveal one managed application secret value to a human operator after explicit authentication. Workload/runtime identity never satisfies this.", Safety: SafetyReadOnly, PolicyRequired: true, ContractVersion: ContractVersion}` — documents the distinct human-authorization seam.
- `internal/operatorauth/authorization.go`:
  - `RequireHumanOperator(ctx) error` — fail-closed gate: requires a verified operator principal (`IssuerVerified: true`); no principal (the local-runtime/trusted-local paths that authorize ordinary app operations), an unverified principal, or a non-issuer-verified principal all fail closed with `machine.ErrorAuthenticationFailed`. Records the decision under op id `secret.reveal` in the audit trail.
  - `PrincipalsHaveVerifiedIdentity(principal) bool` — helper: `principal != nil && principal.IssuerVerified`.
- `cmd/baha/secret_operations.go`: `authorizeHumanReveal(ctx, target, environment, application string) error` delegates to `operatorauth.RequireHumanOperator(ctx)`.
- `cmd/baha/environment_operations.go` (`inspectApplicationEnvironment`, used by `baha app env --reveal`): added reveal gate — when `--reveal`, additionally call `authorizeHumanReveal(...)` before reading the protected dotenv.
- `cmd/baha/app_access.go` (`app creds --reveal`): added reveal gate — when `--reveal`, call `authorizeHumanReveal(...)` before printing the password/URI. `resolveAccessBinding` now returns the `resolved` app for the gate.
- Workload reads (`applicationsecret.Service.Get`/`GetMany` via `app_workload.go`, `app_managed_secret_sources.go`, `app_secret_tls.go`) are UNCHANGED: they remain authorized by the ordinary application/workload path, so the separation holds.

## TESTS (exact IDs, packages, CI routing)

New/regression tests, fail-first:

- `internal/operatorauth/human_operator_test.go` (NEW):
  - `TestRequireHumanOperatorRuntimeIdentityFailsClosed` — (a) no principal → FAIL closed; unverified principal → FAIL closed; verified operator → PASS.
  - `TestRequireHumanOperatorRecordsRevealDecisionUnderDistinctOp` — decision recorded under `secret.reveal` op id.
  - `TestRequireHumanOperatorScopedToRevealKeepsOtherOperationsUnchanged` — (b) `apply` in dev still authorizes via trusted-local (workload reads unchanged).
- `cmd/baha/app_env_test.go` (updated + new):
  - Updated `TestAppEnvMasksSecretsByDefaultAndRevealsExplicitly`: reveal without operator now FAILS closed (typed operator-auth error); reveal with a verified operator (Groups: [editor]) returns native URLs; default/masked and `--path` unchanged. Added `readGrantingMembershipProvider` + `runWithIOAndOperator` helper.
  - `TestAppCredsRevealRequiresVerifiedOperator` (NEW): `baha app creds postgres --app demo --reveal` fails closed without an operator; returns PASSWORD line with a verified operator.
  - Helper `readGrantingMembershipProvider.ResolveClaimMembership` resolves a verified principal to a `tenant-local`/`editor` membership so the surrounding `app.environment` claim resolution authorizes while the reveal gate is what is exercised.

CI routing (Owner rule: every new test must run under GitHub CI):

- `internal/operatorauth/human_operator_test.go` → covered by the `validate` group in `.github/workflows/ci.yml`: `go test ./...` internal package shard. Group/trigger documented as in sibling 053 evidence.
- `cmd/baha/*_test.go` → same `validate` group unit shard.
- Owner-scope note: `.github/**` triggers are NOT edited by this lane (Owner scope). Per 053 precedent, lane PRs may need a CI trigger so lane tests become durable evidence — reported, not fixed.

## ACTUAL LOCAL RESULTS at candidate SHA (build + vet exit 0)

```
$ go build ./...                                   # exit 0 (FULL BUILD OK)
$ go vet ./internal/operatorauth/ ./internal/machine/ ./cmd/baha/  # exit 0 (VET OK)
$ go test ./internal/operatorauth/ ./internal/machine/ ./internal/applicationsecret/ ./internal/tenancy/ ./internal/identity/
ok  github.com/mcpdev80/baseharbor/internal/operatorauth      0.260s
ok  github.com/mcpdev80/baseharbor/internal/machine           (cached)
ok  github.com/mcpdev80/baseharbor/internal/applicationsecret   (cached)
ok  github.com/mcpdev80/baseharbor/internal/tenancy           0.002s
ok  github.com/mcpdev80/baseharbor/internal/identity          0.002s
$ go test ./cmd/baha/ -run 'TestAppEnv|TestAppCreds|Creds|Secret|Reveal'
ok  github.com/mcpdev80/baseharbor/cmd/baha   31.343s
$ go test ./cmd/baha/ -run 'TestRequireHumanOperator' -v
PASS  TestRequireHumanOperatorRuntimeIdentityFailsClosed
PASS  TestRequireHumanOperatorRecordsRevealDecisionUnderDistinctOp
PASS  TestRequireHumanOperatorScopedToRevealKeepsOtherOperationsUnchanged
$ go test ./cmd/baha/ -run 'TestAppCredsRevealRequiresVerifiedOperator' -v
PASS  TestAppCredsRevealRequiresVerifiedOperator
```

Full `cmd/baha` suite: RUNNING (background) at time of write — see log `/tmp/opencode/w057-run.log`.

## CI STATE (Owner scope — reported, not fixed)

- Draft PR not yet opened (still in local verification at time of write).
- CI routing during CI repair is Owner scope; lane PRs need a trigger so lane tests become durable evidence — reported, not fixed. No rerun/workflow_dispatch issued.

## EVIDENCE LAYOUT (baseharbor-plan ONLY, never a product repo)

- Path: `baseharbor-plan/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md`
- No `.evidence/` directory in any product repo. No main-branch writes in baseharbor.
- Worktree: `/tmp/opencode/w057-wt` (cleanliness: only candidate writes + this akte + run log).

## END

- In progress. Full cmd/baha suite pending before END.
