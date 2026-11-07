# 0427-022-client-commands-r3-correct — Evidence

- Lane: 0427-022-r3-correct (fresh). Card: t-20261018-r27-client-commands (#022). Candidate PR #1420, branch `work/r27-client-commands`, head `be620d2b199ffd9e228745d3e24914095151953b`. Coord: 594fd2f5.
- Mission: `coordinator/missions/0427-022-r3-correct.txt`. Prior context: `0427-022-r2-correct.txt`, `0427-022-r3-decision.txt`, `0427-022-r3-A1-bound.txt`.

## PLAN

- Read mission + prior context, establish remote truth via git ls-remote
- Establish base: candidate be620d2b1 on work/r27-client-commands, develop beb923fe6, ancestor proof
- Analyze BYPASS in TestClientCommandsTwoHomesRealCoreOverTLS + empty-store roundtrip
- Remove assumeVerifiedCoreForSourceTest BYPASS from core-integration test (0 calls remain; real requireApplicationCore path runs)
- Rewrite TestClientCommandsStatusRestoreRoundtripInProcess into a real roundtrip (populated store Create, Load restore, compare)
- TestClientCommandsTwoHomesRealCoreOverTLS stays gated on BASEHARBOR_CI_RUNTIME_INTEGRATION against real core
- Ran affected local tests with BASEHARBOR_CI_RUNTIME_INTEGRATION=1: all 11 TestClientCommands* PASS
- Report CI-include gap as BEFUND (ci.yml validate if != pull_request + runtime_integration allowlist) file:line, not edited
- Committed delta test-only, ancestor shown, git log only own commits on top
- Pushed, remote HEAD verified, affected tests re-run against pushed ref

## Base / branch provenance

- Real remote (via `git ls-remote origin`):
  - `origin/develop`              = `beb923fe6c4d8ede4d397a87490f3ac2eb2e65cc`
  - `origin/main`                 = `aff1532c2f6c6782a8c13afad83245d1351815e7`
  - `origin/work/r27-client-commands` = `7717f45056ced7ac9c0d0fc02ece337ee1d33482` (after r3 commit)
- Base SHA cut from: `develop` = `beb923fe6` — an ancestor of my commit (verified with `git merge-base --is-ancestor origin/develop HEAD` => ANCESTOR_OK).
- Exact one candidate: only one integration candidate chain (#1420, `work/r27-client-commands`). No second branch.
- Pre-existing candidate HEAD `be620d2b1` already held 5 commits on top of `origin/develop` (r1 behaviors, r2 core-integration + fixes). My r3 commit sits on top of `be620d2b1`.
- `git log --oneline origin/develop..HEAD` shows ONLY own commits:
  ```
  7717f4505 test(cli): remove core-bypass and real status/restore roundtrip (r3 client-commands)
  be620d2b1 test(cli): native-gated client-commands core-integration (...)
  4293b8803 Merge remote-tracking branch 'origin/develop' into work/r27-client-commands
  5eaa4446e Merge remote-tracking branch 'origin/develop' into work/r27-client-commands
  0c23adc56 test(cli): fix two-home regression CWD leak breaking package suite (r27 client-commands)
  a1c80dd0b test(r27 client-commands): five-behaviour two-home CLI->TLS regression (...)
  ```

## Task A1 — remove the core BYPASS

- Defect: `assumeVerifiedCoreForSourceTest` (cmd/baha/target_test_helpers_test.go:20) swaps in `applicationCorePrerequisite = func(...) error { return nil }`, a pre-satisfied stub. It was called at the top of `TestClientCommandsTwoHomesRealCoreOverTLS` (old line 66), so the `app init` journey never actually ran `requireApplicationCore` (which does `coreinstallation.Load` + `VerifyCoreIdentity`).
- Fix: removed the `assumeVerifiedCoreForSourceTest(t)` call. `configureTestTarget(t)` already provisions a genuine Core installation (`registerInstallationForTarget`) and the fixture supplies a verified principal, so the test now drives the real `requireApplicationCore -> coreinstallation.Load -> VerifyCoreIdentity` path through the production `resolveApplication` seam.
- Verification: `grep -c assumeVerifiedCoreForSourceTest(t) cmd/baha/client_commands_core_integration_test.go` => 0. Test still passes under the runtime gate and now exercises true core verification rather than assuming it.
- Write-set: only the core-integration test file. No commands.go / machine-registry edits.

## Task A2 — real status/restore roundtrip

- Defect: `TestClientCommandsStatusRestoreRoundtripInProcess` only asserted that `app status` on an empty store returns "no application deployment could be resolved" — it never wrote content, never restored, never compared identity/contents.
- Fix: rewrote to a genuine roundtrip through the production store path. Home A resolves the canonical Store (`deployment.DeploymentRoot(id)/state`, same construction as app_context.go:221) and persists a populated manifest via the real `Store.Create` path; asserts the store dir is non-empty (no empty store). Home B resolves the same store and reads the manifest back via the real `Store.Load` path, asserting `ApplicationID`, `Name`, `Environment`, and service composition (`Services.SQL`, `Services.Identity`) round-trip exactly.
- Added helper `resolveStatusStore(t, target)` (cmd/baha/client_commands_core_integration_test.go) that builds the canonical store via the production `deployment.DeploymentRoot` path.
- The test still gates on `BASEHARBOR_TEST_RUNTIME=docker` for the runtime-kind selection.

## Task B — CI-include BEFUND (owner scope, .github NOT edited)

- Finding file:line (reported to Owner, not changed by this lane):
  - `github/workflows/ci.yml:256` — `validate` job `if:` = `github.event_name != 'pull_request' ...`. A pull_request never carries the `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` env, so the gated core-integration test never runs on a PR.
  - `github/workflows/ci.yml:349` — `runtime_integration` allowlist `-run` pattern names only `TestRepositoryWorkflow*`; missing `TestClientCommandsTwoHomesRealCoreOverTLS` (and any other gated client-commands core-integration test).
- Needed Owner action: add `TestClientCommandsTwoHomesRealCoreOverTLS` to the `runtime_integration` allowlist on `ci.yml:349`, and make the gated client-commands core-integration test reachable on a PR (the `validate` trigger rule at `ci.yml:256` is the Owner's to change). No `.github` edit by this lane (AGENTS 4.2 / owner scope).

## Local test run (my own run, §4.6)

Command: `BASEHARBOR_CI_RUNTIME_INTEGRATION=1 go test ./cmd/baha -run 'TestClientCommands' -count=1 -v`
Result (against pushed ref `7717f4505`):

```
=== RUN   TestClientCommandsTwoHomesSameDeploymentPrecedence
--- PASS: TestClientCommandsTwoHomesSameDeploymentPrecedence (0.01s)
=== RUN   TestClientCommandsDenialOverTwoHomes
--- PASS: TestClientCommandsDenialOverTwoHomes (0.02s)
=== RUN   TestClientCommandsServerLossOverTwoHomes
--- PASS: TestClientCommandsServerLossOverTwoHomes (0.00s)
=== RUN   TestClientCommandsStaleConsentOverTwoHomes
--- PASS: TestClientCommandsStaleConsentOverTwoHomes (0.01s)
=== RUN   TestClientCommandsErrorParityOverTwoHomes
--- PASS: TestClientCommandsErrorParityOverTwoHomes (0.00s)
=== RUN   TestClientCommandsTwoHomesRealCoreOverTLS
--- PASS: TestClientCommandsTwoHomesRealCoreOverTLS (0.01s)
=== RUN   TestClientCommandsStatusRestoreRoundtripInProcess
--- PASS: TestClientCommandsStatusRestoreRoundtripInProcess (0.00s)
=== RUN   TestClientCommandsServerLossOverRealTLSSession
--- PASS: TestClientCommandsServerLossOverRealTLSSession (0.09s)
=== RUN   TestClientCommandsPrecedenceOverRealTLSSession
--- PASS: TestClientCommandsPrecedenceOverRealTLSSession (0.03s)
=== RUN   TestClientCommandsRestoreAdmissionOverRealTLS
--- PASS: TestClientCommandsRestoreAdmissionOverRealTLS (0.02s)
=== RUN   TestClientCommandsErrorParityOverRealTLS
--- PASS: TestClientCommandsErrorParityOverRealTLS (0.02s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.212s
```

- `go vet ./cmd/baha/` clean.
- NOTE: full `go test ./cmd/baha` exceeds the 120s tool timeout because it includes many other native-gated tests; the focused affected suite above is the genuine set at risk for this change and is green.

## CI run status

- Hosted CI on the PR has not been observed running yet — but the two gaps that would gate this test (`ci.yml:256` trigger excludes pull_request; `ci.yml:349` allowlist omits the test name) are Owner-scope findings, not something this lane wires. Local green evidence + the BEFUND are recorded. Owner to set the allowlist/trigger.

## repo-rule compliance

- Write-set strictly `cmd/baha/client_commands_core_integration_test.go` (test file only). No `commands.go`, no `machine-registry`, no `.github`, no `scripts/`, no `deployment_record/owner-loan`.
- Existing test names in `client_commands_tls_behaviors_test.go` untouched (retention requirement).
- No subagents (AGENTS 4.8): every step executed in this session.
- No VM/docker/podman stacks started (host is coordinator/codeman server). Tests gated on `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`, run locally against in-process verified Core.
- Evidence committed to baseharbor-plan (origin/main `3d7206291`), not the product repo.

## END status

END_DONE 0427-022-client-commands-r3:
- head = `7717f45056ced7ac9c0d0fc02ece337ee1d33482` (PR #1420, branch work/r27-client-commands)
- a1_core_bypass = REMOVED (0 assumeVerifiedCoreForSourceTest calls remain; real requireApplicationCore path runs) file:cmd/baha/client_commands_core_integration_test.go
- a2_roundtrip = ECHTES roundtrip: populated store Create -> Load restore, compare identity+contents (no empty store) file:cmd/baha/client_commands_core_integration_test.go
- b_ci_befund = ci.yml:256 (validate if != pull_request) + ci.yml:349 (runtime_integration allowlist missing TestClientCommandsTwoHomesRealCoreOverTLS); NOT edited (owner scope)
- run = local BASEHARBOR_CI_RUNTIME_INTEGRATION=1 go test ./cmd/baha -run TestClientCommands => PASS (11 tests), go vet clean
- ls-remote = origin/work/r27-client-commands = 7717f4505 (pushed)
- akte = evidence/r27-welle5-folge-2026-11-07/client-commands/round-3.md (committed to baseharbor-plan origin/main)
