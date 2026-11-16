# round-2 — cli2-env-policy (task t-20261114-r28-cli2-env-policy, PR #1594)

Lane: `cli2-env-policy-head` (correct candidate; HEAD `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d`).

Correcturrunde (luna-r1 = REQUEST CHANGES). Recipe: evidence/r28-welle1-2026-11-15/cli2-env-policy/act-luna-r1.md.

## PLAN

- verify correct branch / candidate SHA
- reproduce the fail-open
- targeted fix in internal/operatorauth/config.go (managed = !trustedLocal + wrapper)
- table tests + build/vet
- FF commit on cli2-env-policy-head, evidence + END post

## 1. Reproduction (before)

Candidate `e5ad8a68` `internal/operatorauth/config.go` `ManagedEnvironmentWithPolicy`:

```go
func ManagedEnvironmentWithPolicy(environment string, trustedLocal bool) bool {
	if trustedLocal {
		return false
	}
	switch strings.ToLower(strings.TrimSpace(environment)) {
	case "dev", "development":
		return false
	default:
		return true
	}
}
```

Observed (reproduced with a small Go snippet, run locally, not committed):

```
name=dev        trustedLocal=false: current(managed)=false   <-- BUG: fails open
name=prod       trustedLocal=false: current(managed)=true
name=arbitrary  trustedLocal=false: current(managed)=true
name=dev        trustedLocal=true : current(unmanaged)=false
```

With `trustedLocal=false`, `dev`/`development` return `false` (unmanaged) — the environment name still fails open even though no explicit trusted-local policy was supplied. This disagrees with the recipe's required semantics and with the companion test `TestManagedEnvironmentWithPolicyFailsClosed`, which asserts `ManagedEnvironmentWithPolicy("prod", false) == true` (managed) but did not cover `dev`.

Witness: `git show FETCH_HEAD:internal/operatorauth/config.go` lines 97-113 (pre-fix body reproduced above).

## 2. Fix

`internal/operatorauth/config.go` (scope: this file only; no command-file change):

- `ManagedEnvironmentWithPolicy(environment, trustedLocal)` now derives managed state directly from the bool: `return !trustedLocal`. `trustedLocal=false` → managed for every name (dev/development/prod/arbitrary) — fails closed. `trustedLocal=true` → untrusted-managed (unmanaged) regardless of name.
- Added `TrustedLocalForEnvironment(environment)` as the sole keeper of the historical name mapping (dev/development → trusted-local), and `ManagedEnvironment(name)` now calls `ManagedEnvironmentWithPolicy(environment, TrustedLocalForEnvironment(environment))`, so the single-arg wrapper keeps its legacy behavior while the explicit-policy path no longer consults the name.
- STOP criterion: verified against the live `ManagedEnvironmentWithPolicy` in `cli2-env-policy-head`; the bool meaning (`managed = !trustedLocal`) is unambiguous and matches the existing `TestManagedEnvironmentWithPolicyFailsClosed`/`TestManagedEnvironmentWithPolicyExplicitTrustedLocal` expectations. No contract correction needed.

Witness: `git diff e5ad8a68..8510de7c -- internal/operatorauth/config.go` (below in §5).

## 3. Tests

Extended `internal/operatorauth/config_explicit_policy_test.go`:
- Updated comment on `TestManagedEnvironmentWithPolicyFailsClosed` to note the dev/development fail-open fix.
- Added `TestManagedEnvironmentWithPolicyTable`: for `["dev","development","prod","test","arbitrary-name"]`, `trustedLocal=false` must be `true` (managed) for every name; `trustedLocal=true` must be `false` (unmanaged) for every name.

Commands and output (run locally, committed evidence only):

```
$ go build ./...
BUILD OK
$ go vet ./internal/operatorauth/... ./internal/application/... ./internal/serviceaccess/...
VET OK
$ go test ./internal/operatorauth/
ok  	github.com/mcpdev80/baseharbor/internal/operatorauth	0.210s
$ go test ./internal/operatorauth/ -run 'TestManagedEnvironmentWithPolicy' -v
=== RUN   TestManagedEnvironmentWithPolicyExplicitTrustedLocal
--- PASS: TestManagedEnvironmentWithPolicyExplicitTrustedLocal (0.00s)
=== RUN   TestManagedEnvironmentWithPolicyFailsClosed
--- PASS: TestManagedEnvironmentWithPolicyFailsClosed (0.00s)
=== RUN   TestManagedEnvironmentWithPolicyTable
--- PASS: TestManagedEnvironmentWithPolicyTable (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/operatorauth	0.003s
$ go test ./internal/application/... ./internal/serviceaccess/...
ok  	github.com/mcpdev80/baseharbor/internal/application	4.528s
ok  	github.com/mcpdev80/baseharbor/internal/serviceaccess	0.093s
```

## 4. CI coverage (no workflow change needed)

New test in `internal/operatorauth` runs under the existing GitHub CI job **"Exercise enrollment and operator boundary races"** in `.github/workflows/ci.yml` line 128-131:
`go test -race -p 2 ./internal/coreinstallation ./internal/operatorauth ./internal/machinehttp ./internal/targetenrollment ./internal/targetsession ./internal/runtimeexplorer ./internal/runtime/terminal -count=1`.

Trigger for that job: `.github/workflows/ci.yml` `on:` block (lines 5-12) — `workflow_dispatch`, `push` (line 7), and `pull_request` (line 12). The native PR-impact job (ci.yml:478) additionally runs on PRs whose base is `develop` or a `lane-*` branch. The path `internal/operatorauth` is covered by an existing CI group with no `.github/**` change required — Owner scope, no edit made.

## 5. ls-remote witnesses (both paths, for clarity of the branch mixup)

Direct GitHub URL (local `git ls-remote origin` transport is unavailable in this clone):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git HEAD cli2-env-policy-head
aff1532c2f6c6782a8c13afad83245d1351815e7	HEAD
e5ad8a6882550168ea262b18dfbdf8c2e4518c1d	refs/heads/cli2-env-policy-head
$ git ls-remote https://github.com/mcpdev80/baseharbor.git cli2-org-env-reconcile
b651e614a9f0003d94199c2ad6063f9c3eb868d0	refs/heads/cli2-org-env-reconcile
```

- `cli2-env-policy-head` = `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` — exact recipe/luna SHA (verified head).
- `cli2-org-env-reconcile` = `b651e614a9f0003d94199c2ad6063f9c3eb868d0` — the branch the earlier BLOCKED round had mistakenly checked out; NOT the candidate.

## 6. Branch provenance (proof)

- Base attest: cut from `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` (HEAD of `cli2-env-policy-head`).
- `git merge-base --is-ancestor e5ad8a6882550168ea262b18dfbdf8c2e4518c1d HEAD` → YES.
- `git log --oneline -3`:
  ```
  8510de7c fix(operatorauth): ManagedEnvironmentWithPolicy managed=!trustedLocal
  e5ad8a68 Merge remote-tracking branch 'origin/develop' into cli2-env-policy-head
  14d8f17d Merge pull request #1624 from mcpdev80/ci/load-pr-gate-coverage
  ```
  Only my single commit sits on top of the base head; no foreign commit carried on the branch.
- Fast-forward check: `origin/cli2-env-policy-head` = `e5ad8a68`; my working head `8510de7c` is exactly 1 commit ahead (git rev-list left-right count = `0` left / `1` right). Fast-forwardable, no force-push.

## 7. repo-rule compliance

- Scope = `internal/operatorauth/config.go` (+ its own test). No command-file, no contract, no `.github/**` edit.
- Fast-forward only; no force-push; PR #1594 stays draft, base unchanged.
- No merge, no `ready_for_review`, no CI dispatch/rerun, no subagent (§4.8).
- Evidence written only in baseharbor-plan (planning repo). No product-repo writes.

## 8. diff (config.go)

```
-	return ManagedEnvironmentWithPolicy(environment, false)
+	return ManagedEnvironmentWithPolicy(environment, TrustedLocalForEnvironment(environment))
 
-// ...legacy switch doc...
-func ManagedEnvironmentWithPolicy(environment string, trustedLocal bool) bool {
-	if trustedLocal {
-		return false
-	}
-	switch ... {
-	case "dev", "development":
-		return false
-	default:
-		return true
-	}
-}
+// TrustedLocalForEnvironment: historical name mapping (dev/development → trusted-local).
+func TrustedLocalForEnvironment(environment string) bool { ... }
+
+// ...managed = !trustedLocal...
+func ManagedEnvironmentWithPolicy(environment string, trustedLocal bool) bool {
+	return !trustedLocal
+}
```

## END

END_DONE
DONE — fix applied and verified on candidate branch `cli2-env-policy-head` @ `8510de7c` (FF from base `e5ad8a68`). Local build/vet and operatorauth/application/serviceaccess tests green; CI coverage confirmed in ci.yml line 128-131 (no workflow change). PR #1594 stays draft; CI/merge handled by coordinator.
