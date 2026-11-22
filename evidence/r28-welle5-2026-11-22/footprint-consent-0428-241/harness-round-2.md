# 0428-241 — footprint-show / record-deployment digest-consent harness (round 2)

Card: 0428-241 (footprint-show digest-consent harness).
Base (attested): `3939aa5e` = `ci(0428-248): catalog the #1597 perses dashboards cluster on the observability surfaces (#1779)`, a develop head, confirmed ancestor of current `origin/develop` via `git merge-base --is-ancestor 3939aa5e origin/develop`.
Remote: `https://github.com/mcpdev80/baseharbor.git`.
Branch: `lane-0428-241-footprint-consent` at `ef6de8504f40054eec689a7960d5a917f3859aff`.
PR: #1780 (base develop, head ef6de8504, open).

## PLAN

1. Establish reality (remote guard, branch base attestation). Branch HEAD was at a foreign commit `f0adb35d` (0428-214 merge); recovered my own committed chain `78171ae9d` -> `c95c2377c`.
2. Confirm my 3-commit chain `78171ae9d..c95c2377c` sits on develop base `3939aa5e` (ancestor verified) and lists only my commits vs current develop.
3. Wire `scripts/ci-native-pr-gate.sh`: add `run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent` to `native/docker|podman/data-capabilities` (line 83) and `native/docker|podman/coreless-lifecycle` (line 93).
4. Wire `scripts/pre-release-integration.py`: add `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` to `CORELESS_SHARD_TESTS['core-capability']` AND register it in `CORELESS_OPTIONAL_TESTS` (shard `core-capability`) so `validate_coreless_shard_partition` and the contract test `test_coreless_shards_partition_every_runtime_test_exactly_once` stay consistent.
5. Fix a self-inflicted bug: a stray `// NOTE:` Go comment had been appended to the end of the Python file `scripts/pre-release-integration.py`; removed it. Verified `python3 -c "import ast; ast.parse(...)"` is valid.
6. Contract/coverage suites: `test_pre_release_integration.py` (19 passed) and `test_pr_gate_coverage.py` (41 passed) all green; `go build ./...` and `go vet ./cmd/baha/` OK.
7. Resolve native-gate plan for my exact files: selects `native/docker/coreless-lifecycle`, `native/docker/data-capabilities`, `native/podman/coreless-lifecycle`, `native/podman/data-capabilities`.
8. Push clean branch; PR #1780 at head ef6de8504. Trigger CI run 45045737874.
9. CI run 45045737874: all Validation / Go unit / Native gate plan / Trusted Plan / Source format gates SUCCESS. Three native runtime gate jobs (docker coreless-lifecycle, docker data-capabilities, podman data-capabilities) FAILED on a pre-existing `TestApplicationCapabilityLifecycleExistingCore/secrets` broker-healthcheck flake. My test never executed: `ci-native-pr-gate.sh` runs `set -euo pipefail`, so the first failing `run_exact_test TestApplicationCapabilityLifecycleExistingCore` aborts the script before line 93 (`run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent`).
10. Write evidence; post END.

## repo-rule compliance

- Write-set: `cmd/baha/app_capability_runtime_test.go` (harness test), `scripts/ci-native-pr-gate.sh`, `scripts/pre-release-integration.py`, `scripts/test_pre_release_integration.py`. All `scripts/**` — Codeman scope, confirmed 0 `.github/**` hits on develop; no product guard, no `operatorauth`, no `.github`, no card 0428-237 touched.
- Additive commits only. `git log --oneline origin/develop..HEAD` lists only my 5 commits (0428-241).
- No subagents. No merge/comment. No force-push of foreign commits onto the delivered remote branch.
- Build/vet green. Contract suites green.

## CI execution evidence (run 45045737874)

- `PR · Native gate plan` => success (selected all four native gates).
- `PR · Validation · ci-executor-tests`, `pr-planner-tests`, `cli-vet`, `cli-gofmt`, `cli-build`, `receipt-execution-tests`, `ci-policy`, `source-contracts` => success.
- `PR · Go unit · cli-0/1/2/3` => success.
- `PR · Native · native/docker/data-capabilities` => **failure**.
- `PR · Native · native/docker/coreless-lifecycle` => **failure**.
- `PR · Native · native/podman/data-capabilities` => **failure**.
- `PR · Native · native/podman/coreless-lifecycle` => **failure**.
- Failures are identical in every gate: `TestApplicationCapabilityLifecycleExistingCore/secrets` aborts with:
  `app_capability_runtime_test.go:137: [app apply --skip-memory-preflight]: Starting secure runtime broker: application runtime broker readiness failed: application runtime broker healthcheck is unhealthy`
  container `bh-docker-dev-capability-secrets-dev-broker-1` / `-broker` in state `unhealthy` (docker and podman), image `ghcr.io/mcpdev80/baseharbor-runtime:edge`.
- `grep -c FootprintShowDigestConsent` on both gate logs = 0. My test never ran in the gate; the abort is on the pre-existing `ExistingCore/secrets` broker path (`app_broker.go:349-354` / `:415-418`), which I did not touch.
- `git diff 78171ae9d HEAD | grep -iE 'broker|secret|unhealthy|healthcheck'` returns only context lines, not my additions — my 4 files do not touch the broker/secrets apply path.

## BLOCKED

CI entblock cannot complete this shift because the native runtime gates fail on a **pre-existing, runtime-environment broker-healthcheck flake** in the EXISTING `TestApplicationCapabilityLifecycleExistingCore/secrets` (container `bh-...-capability-secrets-dev-broker` `unhealthy`). This runs BEFORE my test and aborts `ci-native-pr-gate.sh` (`set -e`) at `run_exact_test TestApplicationCapabilityLifecycleExistingCore` before my `run_exact_test TestApplicationCapabilityLifecycleFootprintShowDigestConsent` ever executes.

Root cause is outside my write-set:
- The failing assertion is `app_capability_runtime_test.go:137` in the EXISTING test (I did not modify line 137 or the secrets/broker path).
- The broker readiness failure is `app_broker.go:349-354` / `:415-418` — product runtime code, not mine.
- Fixing the broker healthcheck on the edge runtime image / runner (image/runner-timing) is a product or runtime-infra action.

Consequence: the digest-consent harness test is correctly wired into all four native gates (data-capabilities docker+podman, coreless-lifecycle docker+podman) and all surrounding gates pass, but it cannot be reached while the pre-existing `ExistingCore/secrets` broker flake aborts the gate script. The test itself builds, vets, and its contract-registration is consistent; only the shared runtime broker flake blocks a green run.

## End state

- class: END_BLOCKED (pre-existing broker-healthcheck flake in EXISTING ExistingCore/secrets aborts native gates before the harness test runs; harness wiring + all surrounding gates green)
- run-id: 45045737874 (CI run 45045737874)
- branch: `lane-0428-241-footprint-consent` @ `ef6de8504`, PR #1780 (base develop)
- Evidence on origin/main:
  git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep footprint-consent-0428-241/harness-round-2.md

## cleanliness

- No containers/networks/volumes/state dirs started on the coordinator host; CI ran on GitHub-hosted shared runners only.
- Untracked items left untouched in the worktree: `baha` (build artifact) and `0428-211-hopdevelop-wt/` (another session's worktree).
- Local working branch was repeatedly taken over by parallel 0428-214/246 sessions; the delivered remote branch `lane-0428-241-footprint-consent` was kept at the clean 5-commit chain `78171ae9d..ef6de8504`.
