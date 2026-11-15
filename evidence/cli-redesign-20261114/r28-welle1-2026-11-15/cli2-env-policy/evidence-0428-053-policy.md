# Evidence: 0428-053 — Replace name-based env policy + env CLI wiring

Shift r28-welle1-2026-11-15 · card t-20261114-r28-cli2-env-policy · mission-053-policynote.md
Worker session: 227fd65a · model: Ornith (confirmed at spawn)

## PLAN

- Read mission, base lane card, brief, command-map; establish ground truth via git
- Create worktree from lane-0428-env-registry (b85efaf6) in /tmp/opencode
- Claim the task via plan-remote (plan.py claim) and push before editing
- Map the exact name-based policy decision points owned by this slice
- Replace name-based dev/test/prod policy with explicit policy; preserve protections
- Wire baha env CLI (cmd/baha/commands*) to explicit policy; schema unchanged
- Add/update focused tests; route into existing CI group; fail-first
- Run go test/vet/build locally; record exact SHA results
- Commit evidence to baseharbor-plan only; publish evidence to origin/main
- Draft PR (retarget base lane; no develop PR); END post; bring down VMs

## BASE ATTESTATION

- Cut ref (base): `lane-0428-env-registry` @ `b85efaf6c94cd158de68a6b8f837dc4a23be455a` (0428-054 delivered HEAD).
- Candidate head branch: `cli2-env-policy-head` @ `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc` (my single commit on top of b85efaf6).
- `git merge-base --is-ancestor b85efaf6c... cli2-env-policy-head` → true (base is ancestor of my commit 018b4e58a).
- Only my commit sits on top of the base:
  ```
  018b4e58a fix(0428-053): replace name-based env policy with explicit trustedLocal policy
  b85efaf6c internal/deployment: env-registry app/target/node association on environment.json (0428-054, owner ruling B)
  ```
- PR: #1594 (draft), base `lane-0428-env-registry` (b85efaf6, stack-rule), head `cli2-env-policy-head`. No develop PR (owner ruling).

## SCOPE (card + owner note 2026-11-15)

- 0428-053 OWNS the `baha env ...` CLI wiring (cmd/baha/commands* write set), NOT 0428-054.
- 0428-054 already delivered env registry/identity (association in per-Target environment.json, ruling B) on lane-0428-env-registry (PR #1591, review).
- This card's goal: replace hardwired dev/development/test/prod NAME-based policy with explicit policy; preserve operator auth / runtime security / service security / password reveal; no weakening during migration.
- environment.json-association (ruling B) = use only, do not re-engineer. Schema unchanged.
- Entry points owned: `internal/serviceaccess/policy.go`, `internal/operatorauth/config.go`, `internal/application/workload_security.go` + associated policy tests.
- Reserved (NOT edited): shared parser/machine registry, generated command index (CI-owned), `.github/**` (Owner scope), release notes.
- Acceptance: two names with identical settings behave equally; varied policy differs only by explicit settings; historical guarded environments do not weaken; deny/unauthorized preserved.

## DESIGN (owner 2026-11-15, confirmed via QUESTION)

Explicit `trustedLocal` param approach; scope = 3 named entry points only.

- `serviceaccess/policy.go`: added `EnvironmentPolicy{TrustedLocal bool}` + `ResolveWithPolicy(env, provider, auth, policy)`. `Resolve(name)` wraps with `TrustedLocal: TrustedLocalForEnvironment(name)`. New fail-closed path: `ResolveWithPolicy(..., EnvironmentPolicy{})` → managed/auth-required. The name no longer sits inside the switch; the decision is an explicit argument.
- `operatorauth/config.go`: added `ManagedEnvironmentWithPolicy(env, trustedLocal bool)`. `ManagedEnvironment(name)` wraps with `trustedLocal=false`. trustedLocal=true overrides name → unmanaged; false → historical name mapping.
- `application/workload_security.go`: added `ResolveWorkloadSecurityPolicyWithDevPolicy(m, devMode bool)` + `TrustedLocalForDevEnvironment(name)`. `ResolveWorkloadSecurityPolicy(m)` wraps with the historical mapping. Env override still cannot downgrade managed→development.
- Fail-closed default everywhere: unset/unknown policy = managed, so a name can never silently weaken guarantees.

## TESTS (exact IDs, packages, CI routing)

New regression tests, fail-first:

- `internal/serviceaccess/policy_explicit_test.go`
  - `TestResolveNameNoLongerDrivesAuthentication` — two names with same explicit policy behave equally.
  - `TestResolveExplicitTrustedLocalAllowsOptionalAuth` — trusted-local keeps auth optional, TLS mandatory.
  - `TestResolveDefaultPolicyIsManagedFailsClosed` — empty policy = managed.
  - `TestResolveByDefaultWrapsNameMapping` — Resolve(name) preserves historical dev=trusted-local/else=managed.
  - `TestTrustedLocalForEnvironment` — single name→trusted mapping.
- `internal/operatorauth/config_explicit_policy_test.go`
  - `TestManagedEnvironmentWithPolicyExplicitTrustedLocal` — explicit trustedLocal overrides name.
  - `TestManagedEnvironmentWithPolicyFailsClosed` — no policy → managed.
  - `TestManagedEnvironmentPreservesNameMapping` — ManagedEnvironment(name) historical mapping.
- `internal/application/workload_security_explicit_policy_test.go`
  - `TestResolveWorkloadSecurityPolicyExplicitDevMode` — explicit dev policy → development mode.
  - `TestResolveWorkloadSecurityPolicyPreservesNameMapping` — historical mapping preserved.
  - `TestTrustedLocalForDevEnvironment` — single name→dev mapping.

CI routing (Owner rule: every new test must run under GitHub CI):
- Group: `validate` in `.github/workflows/ci.yml`, line ~122: `go test ./contracts/... ./internal/... ./spec/...`
- Trigger: `pull_request` to branches `develop`/`main` (ci.yml push trigger lines ~8-16).
- My test path `internal/serviceaccess/...` is covered by the `./internal/...` wildcard of this existing group — no `.github/**` change required (Owner scope). No parallel CI framework, no full matrix.

## ACTUAL LOCAL RESULTS at candidate SHA 018b4e58a (build exit 0, vet exit 0)

```
$ go build ./...                          # exit 0
$ go vet ./internal/serviceaccess/ ./internal/operatorauth/ ./internal/application/   # exit 0
$ go test ./internal/serviceaccess/ ./internal/operatorauth/ ./internal/application/ ./internal/logs/ ./internal/runtimebroker/ ./internal/telemetry/ ./internal/traces/ ./internal/objectstorage/ ./internal/metrics/ ./internal/identityprovider/ ./internal/orgconfig/ ./internal/runtime/
ok  github.com/mcpdev80/baseharbor/internal/serviceaccess        0.224s
ok  github.com/mcpdev80/baseharbor/internal/operatorauth         0.503s
ok  github.com/mcpdev80/baseharbor/internal/application          4.464s
ok  github.com/mcpdev80/baseharbor/internal/logs                 0.074s
ok  github.com/mcpdev80/baseharbor/internal/runtimebroker        (cached)
ok  github.com/mcpdev80/baseharbor/internal/telemetry            0.234s
ok  github.com/mcpdev80/baseharbor/internal/traces               0.069s
ok  github.com/mcpdev80/baseharbor/internal/objectstorage        5.165s
ok  github.com/mcpdev80/baseharbor/internal/metrics              0.175s
ok  github.com/mcpdev80/baseharbor/internal/identityprovider     7.891s
ok  github.com/mcpdev80/baseharbor/internal/orgconfig            0.077s
ok  github.com/mcpdev80/baseharbor/internal/runtime              0.278s
```

Baseline (base lane b85efaf6) was green before any change; all above green after. No weakening of prod/test/managed behavior.

## CI STATE (Owner scope — reported, not fixed)

- Draft PR #1594 (base `lane-0428-env-registry` b85efaf6, head `cli2-env-policy-head` 018b4e58a).
- GitHub CI on lane-PRs: no run has picked up `018b4e58a`. The `validate` group's `push` trigger (ci.yml lines ~8-16) only fires on `runtime-validation/**` branches; `pull_request` fires only on develop/main. A lane PR (#1594 → lane-0428-env-registry) matches neither, and CI runs on other lane SHAs are currently failing under the ongoing CI repair.
- This is a CI-routing/infra condition during repair, NOT caused by this change (all affected local suites green). Per Owner scope-split: `.github/**` not edited, no rerun/workflow_dispatch issued. Finding: lane PRs need a CI trigger (e.g. add `lane-0428-*` or a broader lane pattern to ci.yml push branches, or route lane PRs through develop) so new tests become durable evidence — Owner scope.

## EVIDENCE LAYOUT (baseharbor-plan ONLY, never a product repo)

- Path: `baseharbor-plan/evidence/cli-redesign-20261114/r28-welle1-2026-11-15/cli2-env-policy/evidence-0428-053-policy.md`
- No `.evidence/` directory in any product repo. No main-branch writes in baseharbor.

## HANDOFF

- Head branch/commit: `cli2-env-policy-head` @ `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc` (base b85efaf6c, only my commit on top).
- PR: #1594 (draft), base `lane-0428-env-registry` (b85efaf6, stack-rule), head `cli2-env-policy-head`. No develop PR (owner ruling).
- Tests → check/gate → trigger → result: above.
- Remaining gap: CI has not executed on this SHA (routing during repair, Owner scope). Acceptance must be blocked until actual execution is proven OR the Owner routes lane PRs into a CI-triggering group.
- No release/tag authorized.

## END

- DONE
