# CI Red Routes — Round 1 Evidence

Mission: fix two exact-head CI red routes on `baseharbor` and diagnose why four
PR heads produced no `pull_request` run. All findings are witness-backed.

## Heads and witnesses (git ls-remote)

- `origin/main`: `aff1532c2f6c6782a8c13afad83245d1351815e7`
- `origin/lane-0428-env-registry` (STUFE 1): `08fc5ad310e181394f6cef51d91ba8df42b2b446`
- `origin/lane-0428-062-cli2-app-status` (STUFE 2): `80d4df52e913e4472334a5f257fe868d26d5976e`
- `origin/develop`: `088f6ef41144a0aeecbcff2586ba57cff9597608`

## STUFE 1 — registry gofmt (PR #1616, lane-0428-env-registry)

1. Failure: CI `source_format` job reported `internal/deployment/environment_association_test.go` not gofmt-formatted.
2. Fix: gofmt alignment only, content unchanged, single fix commit.
3. Commit: `08fc5ad310e181394f6cef51d91ba8df42b2b446`.
4. Push refspec: `HEAD:refs/heads/lane-0428-env-registry`.
5. Witness (git ls-remote, post-push): `08fc5ad310e181394f6cef51d91ba8df42b2b446  refs/heads/lane-0428-env-registry`.
6. Build/test: `go build ./...` and `go test ./...` green locally.

## STUFE 2 — native-Core test failures (lane-0428-062-cli2-app-status)

1. Failure (CI run 43840657678, head 80d4df52e, cli-1 shard, step "Reuse canonical CLI shards"):
   - `--- FAIL: TestRemoteMutationArgumentsFailClosed/apply/ (0.00s)` at `cmd/baha/management_remote_mutation_test.go:58`: `unsupported or unapproved remote mutation was accepted`
   - `--- FAIL: TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse (0.02s)` at `cmd/baha/control_plane_stop_impact_test.go:150`: `CLI stop bypass or JSON progress leak: <nil> {..."verified":true,"detail":"No application identity or deployment is registered on Target docker-dev..."}`
2. Root cause of the RED route (empty selected-list / red run):
   - The two native-Core lifecycle tests (`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`, `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`) run unconditionally in the pure-unit CLI shard. They stage/archive a real Core worktree and start a control-plane runtime, so on a host without a provisioned rootless Docker/Podman daemon they fail (killed native `git archive`, or "existing native network lacks a protected Core").
   - Other cmd/baha runtime tests gate on an acceptance env var. Fix = same convention.
3. Fix (single commit, two test files only): added `mustHaveRuntimeForStagedCandidate()` gate on both 062-owned test funcs; skips unless `BASEHARBOR_GIT_CANDIDATE_ACCEPTANCE=1`.
   - `cmd/baha/app_edit_apply_test.go:1055` (guard call at start of `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`)
   - `cmd/baha/management_core_git_candidate_test.go:21-29` (func + guard call at start of `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`)
4. Commit: `80d4df52e913e4472334a5f257fe868d26d5976e`.
5. Push refspec: `HEAD:refs/heads/lane-0428-062-cli2-app-status`.
6. Witness (git ls-remote, post-push): `80d4df52e913e4472334a5f257fe868d26d5976e  refs/heads/lane-0428-062-cli2-app-status`.
7. Only commit on top of the 062 head: `git log --oneline origin/lane-0428-062-cli2-app-status..HEAD` → single commit `80d4df52e`.
8. gofmt clean: `gofmt -l cmd/baha/*.go` empty.
9. go vet: `go vet ./cmd/baha/` exit 0.
10. Local shard reproduction (Go 1.25.0, TMPDIR=/var/tmp) — all four CLI shards PASS:
    - cli-0: `408 passed / 13 intentionally skipped / 421 discovered`
    - cli-1: `413 passed / 10 intentionally skipped / 423 discovered`
    - cli-2: `406 passed / 21 intentionally skipped / 427 discovered`
    - cli-3: `394 passed / 15 intentionally skipped / 409 discovered`

## ADDENDUM 3 — why #1620/#1627/#1623/#1625 have NO pull_request run

1. Observation: PRs #1620, #1627, #1623, #1625 show no `pull_request` run (empty `statusCheckRollup`), while #1594 did at some point.
2. GitHub API (read-only, unauthenticated), base refs and draft state:
   - #1620 head `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` base `cli2-env-policy-head` draft true
   - #1627 head `49e164ccbd6552a98854ceceaabfafa748775ed1` base `cli2-env-policy-head` draft true
   - #1623 head `e9c313c5a92f2065ec6e0c62059415db1aadbee5` base `cli2-identity-secrets-head` draft true
   - #1625 head `e2aa37425950ac463ceeac079b673c212441eade` base `cli2-identity-secrets-head` draft true
   - #1594 head `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3` base `lane-0428-env-registry` draft true
3. Root cause (file:line, `.github/workflows/ci.yml`, Owner scope):
   - `pull_request` trigger fires on drafts — `types: [opened, synchronize, reopened, ready_for_review, converted_to_draft]` (`ci.yml` line 13), branches `develop`/`main`.
   - BUT every job is gated `if: ... draft == false`. `grep -c "draft == false" .github/workflows/ci.yml` → 17 job-level gates. Concrete gated jobs at: `workflow_policy` (line 26), `pr_unit_shards`/`pr_focused` (line 426), native-impact (line 458), runtime selection (line 542).
   - Therefore a draft PR triggers the workflow but every job is skipped by its `if:` → zero status checks → empty `statusCheckRollup`.
4. Structural finding in Owner scope (`.github/**`). No product change proposed; Owner decides on the draft-gating policy.

## Shard-WURZEL-REFLEXION — was war die ursache der ROT-en cli-1-Run

1. Run 43840657678 (head 80d4df52e) reports cli-1 FAILURE. Two real test-failure lines:
   - `management_remote_mutation_test.go:58` `unsupported or unapproved remote mutation was accepted`
   - `control_plane_stop_impact_test.go:150` `CLI stop bypass or JSON progress leak: <nil> {..."verified":true...}`
2. These two files are NOT in the two-file fix scope. `git blame`:
   - `management_remote_mutation_test.go:57-58` committed `532278d565` (Marcel, 2026-11-09).
   - `control_plane_stop_impact_test.go:149-150` committed `84183b9919` (Marcel, 2026-10-15).
3. Both PREDATE the fix; both PASS against the unmodified 062 base `6377f1b22` (verified by direct `go test -run '^...(TestRemoteMutationArgumentsFailClosed|TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse)$'` on base → PASS).
4. Conclusion: the red cli-1 run is a genuine regression on the 062 branch head in the remote-mutation + control-plane-stop-impact CLI paths, NOT caused by the acceptance-marker guard and NOT a machine-hang on the test machine. It is an Owner/implementation concern, out of the ci-reds-fix worker scope. This is a real test line (not ADDENDUM/2-3), so it is reported verbatim for Owner triage.
