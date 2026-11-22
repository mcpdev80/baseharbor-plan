# 0428-241: #1780 selected core-capability test-only fixes landed

## PLAN
1. Read mission `m_ffe_1780sel.md.g`; establish reality. Remote guard: `lane-origin = https://github.com/mcpdev80/baseharbor.git`. Branch `lane-0428-241-footprint-consent`. Base `3939aa5e` confirmed ancestor of develop `b27b2ebe`.
2. Fix #1 (:376) add the podman provider override block after `configureTestTargetEmpty`, mirroring `TestApplicationCapabilityLifecycleExistingCore` (:34-47), so `BASEHARBOR_TEST_RUNTIME=podman` selected gate does not see rootful docker.
3. Fix #2 (:430) extract the confirm digest from the combination `err.Error()` + `out.String()` — the digest lives in the usage Hint rendered to captured stdout, not in `err.Error()` (which carries only the message). Negative-control (first-refusal-then-consent) left intact.
4. Fix #3 (:409) replace the `resetCoreBootstrapFixtureApplication` defer with `approvedNativeFixtureCleanup` under a `defer func()` that chdir's back to `root` first, so teardown runs via the verified-owner path even after a mid-test fail.
5. `go build ./...` + `go vet ./cmd/baha/` OK; test compiles/skips cleanly; contract suites green (19 + 41).
6. Additive hop on develop `b27b2ebe` (`git merge --no-ff origin/develop`, no force) + COMMIT `87ba9bac2` + PUSH -> PR #1780.
7. Hosted rerun 45051176104: 16 success, 10 skipped, 4 native failures on the pre-existing broker flake.
8. Write evidence, commit to baseharbor-plan origin/main, post END with head + run-id + 'native waiting-1770'.

## HEAD / PR
- Head: `87ba9bac257de089a3723bbfc0884c4e9b722241`
- PR #1780: head `87ba9bac2`, state `OPEN`, non-draft.
- Remote guard (first git action): `https://github.com/mcpdev80/baseharbor.git`
- `git diff origin/develop..HEAD --name-only`:
  - `cmd/baha/app_capability_runtime_test.go`
  - `scripts/ci-native-pr-gate.sh`
  - `scripts/pre-release-integration.py`
  - `scripts/test_pre_release_integration.py`
  - `scripts/pr-gate-coverage.json` (develop change folded in, not mine)
- `git log --oneline origin/develop..HEAD` lists ONLY my own commits (5 original + hop) — no foreign candidate carried.
- Hop `92ba5d810` parents: first parent `ef6de8504` (my chain), second parent `b27b2ebe` (develop). Base `3939aa5e` is an ancestor of develop and of HEAD.

## The three fixes (test-only, `cmd/baha/app_capability_runtime_test.go`)
- Fix #1 (:376) — podman provider override. After `target := configureTestTargetEmpty(t)` the block:
  ```
  if os.Getenv("BASEHARBOR_TEST_RUNTIME") == "podman" {
    cfg, err := deployment.LoadConfig()
    ...
    definition.Runtime.Provider = "podman"
    ...
    target, err = cfg.ResolveTarget("", "")
  }
  ```
  Mirrors `TestApplicationCapabilityLifecycleExistingCore` exactly. Before this, the podman-selected core-cap gate (job 137281323994) failed "detected Docker endpoint rootful vs Target rootless".
- Fix #2 (:430) — digest extraction from `err.Error() + "\n" + out.String()`. `cli.UsageError.Error()` returns only `e.Message` (internal/cli/cli.go:46), so the confirm digest never appeared in `err.Error()`. The digest is in the usage Hint that `main.go` renders to captured stdout. The negative-control assertion (first apply fails closed with `--confirm-candidate`, then the consented re-run binds it) is unchanged. Before this, the docker-selected core-cap gate (job 137281323791) could not find the confirm-hash.
- Fix #3 (:409) — robust teardown. The old `defer resetCoreBootstrapFixtureApplication(...)` calls `resolveApplication(... "destroy")`, which requires verified existing target/deployment ownership and fails closed once the cell is torn down. Replaced with:
  ```
  defer func() {
    if _, werr := os.Getwd(); werr == nil { _ = os.Chdir(root) }
    cleanupCtx, cleanupCancel := context.WithTimeout(context.Background(), 3*time.Minute)
    defer cleanupCancel()
    if err := approvedNativeFixtureCleanup(t, testOperatorContext(machineNoninteractiveContext(cleanupCtx)), &bytes.Buffer{}); err != nil {
      t.Errorf("footprint-consent fixture cleanup: %v", err)
    }
  }()
  ```
  Same verified-owner path `ExistingCore` uses at :73-77.

## Verification
- `go build ./...` OK
- `go vet ./cmd/baha/` OK
- `go test ./cmd/baha/ -run '^TestApplicationCapabilityLifecycleFootprintShowDigestConsent$' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` => `ok github.com/mcpdev80/baseharbor/cmd/baha 0.007s` (skips the isolated exact-SHA runtime; compiles and the skip path runs).
- `python3 -m pytest scripts/test_pre_release_integration.py` => 19 passed
- `python3 scripts/test_pr_gate_coverage.py` => 41 tests OK

## Hosted rerun — run 45051176104 (head 87ba9bac2)
- Total: 16 success, 10 skipped, 4 failure.
- 4 native runtime gates all fail: `native/docker/coreless-lifecycle`, `native/podman/coreless-lifecycle`, `native/docker/data-capabilities`, `native/podman/data-capabilities`.
- My test `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` appears 0 times in every native-gate log.
- Cause: the gates abort via `set -e` at `TestApplicationCapabilityLifecycleExistingCore/secrets` BEFORE reaching my test (which sits at line 93, after `ExistingCore` at line 91 in `scripts/ci-native-pr-gate.sh`).
- The aborting failure is the pre-existing `ApplicationRuntimeBroker` healthcheck flake on the runtime edge image `ghcr.io/mcpdev80/baseharbor-runtime:edge`:
  - docker: `"application runtime broker healthcheck is unhealthy"` -> `bh-docker-dev-capability-secrets-dev-broker`
  - podman: `"inspect Podman runtime broker container state: runtime container ls -aq: signal: killed"`
  - This is `#0428-237 / #1770` (the `:edge-broker-red` pin), NOT my defect and NOT a gate reorder. My write-set touches only my test and the gate wiring; none of it touches the broker or secrets path.

## selected core-capability cells
- Mission states the selected core-capability cells go green "kein broker noetig". My test lives in the `core-capability` shard (`pre-release-integration.py` `CORELESS_SHARD_TESTS['core-capability']`) which runs in its own isolated `go test`, separate from `ExistingCore`, so it does not hit the broker flake. The native `ci-native-pr-gate.sh` gates (data-capabilities / coreless-lifecycle) run `ExistingCore` in the same shell and abort before my test — that is the broker flake, not a regression from my changes.

## END status
- head `87ba9bac257de089a3723bbfc0884c4e9b722241`
- run-id `45051176104`
- `:376/:430/:409 fixed: ja`
- native waiting-1770 (broker pin blocks the native data-cap/coreless gates; my 3 fixes are delivered in #1780, PR open/non-draft).

## cleanliness
- No containers, compose projects, volumes, or network started on this host. Native CI runs on GitHub-hosted shared runners only; this session host stays clean.
- `docker ps -a` witness (this host, expected empty of baseharbor stacks):
  - (none)
- No scratch/cache files left in the ecosystem root. `/tmp/*.log` gate dumps from the read-only GitHub log API are ephemeral; nothing written to the product repo or planning repo outside evidence.

## repo-rule compliance
- Write-set limited to test-only fixes + CI wiring. No product code, no `.github/**` edit, no gate reorder, no merge, no subagents.
- Branch provenance: additive hop on develop `b27b2ebe` (second parent of hop confirmed), my chain on top, no foreign candidate carried.
- Remote delivered and proven via `git ls-remote`.
