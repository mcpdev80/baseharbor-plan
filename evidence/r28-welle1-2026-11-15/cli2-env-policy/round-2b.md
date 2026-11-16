# r2b — cli2-env-policy (task t-20261114-r28-cli2-env-policy, PR #1594)

Lane: `cli2-env-policy-head` (correct candidate; base `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d`).

Correction round r2b (predecessor built the fix locally as `8510de7c` but never pushed it — work lost). This round re-implements the fix on the live candidate branch and delivers it.

## PLAN

- read both predecessor accounts (round-2.md, act-luna-r1.md) and verify the correct candidate branch SHA
- cut a detached worktree from base `e5ad8a68` and attest ancestry
- apply fix in `internal/operatorauth/config.go`: `managed = !trustedLocal` + `TrustedLocalForEnvironment` wrapper + table test
- run `go build` / `go vet` + targeted `operatorauth` / `application` / `serviceaccess` tests
- FF commit on candidate, push, and witness new head with `git ls-remote`
- write evidence, END post

## 1. Reproduction (confirmed from predecessor account + live base)

Base `e5ad8a68` `internal/operatorauth/config.go` `ManagedEnvironmentWithPolicy`:

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

With `trustedLocal=false`, `dev` / `development` return `false` (unmanaged) — the environment name fails open even though no explicit trusted-local policy was supplied. The fix derives managed state directly from the bool: `managed = !trustedLocal`, so `trustedLocal=false` is managed for every name (fails closed), `trustedLocal=true` is unmanaged for every name.

## 2. Fix

`internal/operatorauth/config.go` (scope: this file + its own test; no command-file, no contract, no `.github/**`):

- `ManagedEnvironmentWithPolicy(environment, trustedLocal)` now returns `!trustedLocal` — the explicit policy fails closed, environment name kept out of the decision.
- `TrustedLocalForEnvironment(environment)` is the sole keeper of the historical name mapping (dev/development → trusted-local); `ManagedEnvironment(name)` now calls `ManagedEnvironmentWithPolicy(environment, TrustedLocalForEnvironment(environment))`, preserving legacy single-arg behavior.
- STOP criterion met: the bool meaning (`managed = !trustedLocal`) matches the existing `TestManagedEnvironmentWithPolicyFailsClosed` / `TestManagedEnvironmentWithPolicyExplicitTrustedLocal` expectations and luna's recipe.

## 3. Tests

Extended `internal/operatorauth/config_explicit_policy_test.go`:

- Updated comment on `TestManagedEnvironmentWithPolicyFailsClosed` to note the dev/development fail-open fix; added `dev` and `development` fail-closed assertions.
- Added `TestManagedEnvironmentWithPolicyTable`: for `["dev","development","prod","test","arbitrary-name"]`, `trustedLocal=false` must be `true` (managed) for every name; `trustedLocal=true` must be `false` (unmanaged) for every name.

Commands and output (run locally in worktree `/tmp/opencode/r2b-env-policy-wt`):

```
$ go build ./...
BUILD OK
$ go vet ./internal/operatorauth/...
VET OK
$ go test ./internal/operatorauth/
ok  	github.com/mcpdev80/baseharbor/internal/operatorauth	0.209s
$ go test ./internal/operatorauth/ -run 'TestManagedEnvironmentWithPolicy' -v
=== RUN   TestManagedEnvironmentWithPolicyExplicitTrustedLocal
--- PASS: TestManagedEnvironmentWithPolicyExplicitTrustedLocal (0.00s)
=== RUN   TestManagedEnvironmentWithPolicyFailsClosed
--- PASS: TestManagedEnvironmentWithPolicyFailsClosed (0.00s)
=== RUN   TestManagedEnvironmentWithPolicyTable
--- PASS: TestManagedEnvironmentWithPolicyTable (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/operatorauth	0.003s
$ go test ./internal/application/...
ok  	github.com/mcpdev80/baseharbor/internal/application	3.494s
$ go test ./internal/serviceaccess/...
ok  	github.com/mcpdev80/baseharbor/internal/serviceaccess	0.109s
```

## 4. CI coverage (no workflow change needed)

The new test in `internal/operatorauth` runs under the existing GitHub CI job "Exercise enrollment and operator boundary races" in `.github/workflows/ci.yml` (lines 128-131): `go test -race -p 2 ./internal/coreinstallation ./internal/operatorauth ./internal/machinehttp ./internal/targetenrollment ./internal/targetsession ./internal/runtimeexplorer ./internal/runtime/terminal -count=1`.

Trigger: `.github/workflows/ci.yml` `on:` block — `workflow_dispatch`, `push`, and `pull_request` (lines 5-12). The native PR-impact job additionally runs on PRs whose base is `develop` or a `lane-*` branch. `internal/operatorauth` is covered by an existing CI group with no `.github/**` change required — Owner scope, no edit made. CI dispatch is handled by the coordinator.

## 5. Branch provenance (proof)

- Base attest: cut detached worktree from `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` (HEAD of `cli2-env-policy-head`).
- `git merge-base --is-ancestor e5ad8a6882550168ea262b18dfbdf8c2e4518c1d HEAD` → YES (base is ancestor of my commit).
- `git log --oneline -3`:
  ```
  ae2d022c8 fix(operatorauth): ManagedEnvironmentWithPolicy managed=!trustedLocal
  e5ad8a688 Merge remote-tracking branch 'origin/develop' into cli2-env-policy-head
  14d8f17d1 Merge pull request #1624 from mcpdev80/ci/load-pr-gate-coverage
  ```
  Only my single commit `ae2d022c8` sits on top of the base head; no foreign commit carried on the branch.
- Left/right count vs base: `0` left / `1` right — only my own commit ahead.
- PR #1594 (GitHub API): state `open`, `draft`, base `lane-0428-env-registry` (@ `b85efaf6c94cd158de68a6b8f837dc4a23be455a`), head `cli2-env-policy-head` (@ `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d`). Base unchanged.

## 6. Delivery state — BLOCKED on push (not a defect in the fix)

The fix is built, committed, and locally verified (see §3). Every push attempt is rejected by the transport as `non-fast-forward`:

```
$ git push origin cli2-env-policy-head
 ! [rejected]            cli2-env-policy-head -> cli2-env-policy-head (non-fast-forward)
error: failed to push some refs ... non-fast-forward
```

Diagnosed as impossible by graph evidence (all reproduced with independent witnesses):

- My commit's parent SHA = `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` (`git rev-parse HEAD^`).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/cli2-env-policy-head` = `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` (re-confirmed multiple times, including after a full `git fetch` and after deleting + re-fetching the local tracking ref).
- The base I cut from (`e5ad8a68`) exactly equals the current remote head; my branch is exactly 1 commit ahead, 0 left. A fast-forward push from a parent that equals the remote tip cannot be a non-fast-forward.

Attempts made to clear the refusal without touching the fix or the remote content:

- Deleted and re-fetched `refs/remotes/origin/cli2-env-policy-head` (fresh tracking ref = `e5ad8a68`).
- Tried `--no-force` and default push; same rejection.
- Verified remote URL is standard `https://github.com/mcpdev80/baseharbor.git` (not a local/file remote).

Resolution held back on purpose: a force-push (`--force-with-lease`) is forbidden by scope (no force-push / no branch-protection bypass). The candidate is verified and committed; only the delivery push remains. This needs an Owner / Coordinator action to clear the transport refusal (e.g. confirm no concurrent writer, or push from an uncontended ref) — the fix itself needs no change.

## END

END_BLOCKED
BLOCKED — fix built, committed (`ae2d022c8`, 1 commit ahead of base `e5ad8a68`, zero foreign), locally verified (build/vet + operatorauth/application/serviceaccess green). Push rejected as non-fast-forward despite my parent SHA exactly matching the remote head (`e5ad8a68`, witnessed by `git ls-remote`). Force-push is out of scope; delivery push needs an uncontended ref from the Owner/Coordinator. PR #1594 stays draft, base unchanged.
