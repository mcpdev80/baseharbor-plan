# 0427-162 FIXRUNDE — use/activate error wording + BF-02 scope verification

- Card/mission: mission-162fix (0427-162, bug-hunt fixrunde; plan f23243a1)
- Shift: r27-welle5-folge-2026-11-08 / round-2
- Worker session: laptop (session 594fd2f5-4e80-43b6-9841-92879146a85e), no subagents (4.8)
- Planning repo verified (origin/main HTTPS): `0272c4b0feee978d5537d5dd6b88b3db81901390` (`git ls-remote https://github.com/mcpdev80/baseharbor.git main`)
- Source pin (origin/HTTPS develop HEAD): `d8849198265f13d34e1ece95d6982ce6b613d2aa` (`git ls-remote https://github.com/mcpdev80/baseharbor.git develop`)
- Branch base attestation: origin/develop cdb4350a6 (local checkout HEAD) is an ancestor of the branch head `lane/0427-162-issuerfix` — single integration candidate, no foreign branch carried.
- Branch: `lane/0427-162-issuerfix` cut from cdb4350a6 on clone `/tmp/opencode/w162-issueruse-wt`.
- Source zone: /tmp/opencode/w162-issueruse-wt (fresh clone of mcpdev80/baseharbor @ develop). Working tree /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor is a 259-commit-stale stale-ref checkout and was NOT used as evidence.
- Build: go build ./cmd/baha OK on cdb4350a6 (`go version go1.26.8 linux/amd64`).

## PLAN

- Read mission-162fix.md, board card, round-1 diagnostic; confirm scope (Recipe A fix)
- Verify remote truth via `git ls-remote` HTTPS (origin main/develop); attest branch base cdb4350a6 ancestor-of-HEAD
- Trace live `use/activate` path: `bindExplicitSelectionToConnection` → `VerifyCoreConnection` (Keycloak) vs old `ResolverForTargetSelection` (local base CA)
- Reproduce BF-02 faithfully via a Go repro test: verified Core (all caps) + only `service-access/issuer` removed → assert selection binds
- Confirm foreign/absent-install still fails closed
- Diagnose BF-02 vs code state (does #1460 already fix it?)
- Apply Recipe A fix: correct the misleading "baha core install" error string (unreachable subcommand) while preserving fail-closed for foreign/absent-install
- Add CI-covered regression test in cmd/baha (cli-surface/lifecycle group: `go test ./cmd/baha`) asserting verified Core selects without issuer-dir; foreign still fails closed
- Run `go test ./cmd/baha` + `go vet` + `go build`; document outcomes
- Commit evidence to baseharbor-plan evidence/ (NOT product repo); `git ls-remote origin main` before END
- END in geteilte inbox + publish board state

## Diagnostic: BF-02 does NOT reproduce on develop HEAD

- Round-1 (w162b) diagnosed BF-02 against an OLDER pin where the production `use/activate` path verified the Core through a LOCAL base CA at `<runtimeRoot>/service-access/issuer` via `coreinstallation.ResolverForTargetSelection` → `observeLocalIssuer`. An absent issuer dir failed closed → BF-02.
- The live code on develop HEAD `d884919` already migrated the path (commit `201735b03`, card 0427-133 r2 / PR #1460): `bindExplicitSelectionToConnection` now calls `VerifyCoreConnection` (cmd/baha/verify_core_connection.go), which reads the REAL Core Keycloak-bound discovery identity at `<plainTargetRoot>/providers/keycloak/shared/core` (`state.IdentityIssuer`), NOT a local base CA. `ResolverForTargetSelection` is no longer on the use/activate path.
- Faithful Go repro test on develop HEAD (`TestZZ162ReproAbsentIssuerDir`): bootstrap a genuine, verified Core (all 3 caps, Keycloak core issuer present via `bootstrapVerifiedTargetForConnectionTest`), then `os.RemoveAll(runtimeRoot/service-access/issuer)` and call `bindExplicitSelectionToConnection`. Result: **binds successfully** (no BF-02). The absent local base CA no longer blocks selection.
- Companion `TestZZ162ReproForeignStillFailsClosed`: bare target (no Core) still fails closed with a typed conflict. Foreign/foreign-identity boundary preserved.
- Conclusion: the selection-boundary fail-closed defect (BF-02) is already remediated on develop HEAD by the Keycloak-migration in #1460. This fixrunde's actionable, in-scope work is the mandatory Recipe A wording correction, which applies to BOTH options.

## Fix applied (Recipe A — wording correction)

- Root cause of the remaining defect: the production error strings still point at `baha core install`, a subcommand that does not exist (`baha core --help` → `Error: unknown command "core" for baha`). This is the exact misleading reference round-1 mandated removing ("Irrefuehrenden core-install-verweis IMMER entfernen").
- Location: cmd/baha/use_target.go — the "Install a BaseHarbor Core for this Target (baha core install) ..." guidance strings at the four failing branches (lines 91, 98, 118, 129) and cmd/baha/onboarding.go:201.
- The fix corrects these strings to name the existing recovery path (the verified Core is recovered through its real Keycloak-bound core issuer / re-selection; no unreachable subcommand), WITHOUT relaxing the fail-closed boundaries:
  - absent installation (ErrNotExist) → still fail closed (no Core installed)
  - Keycloak core issuer unavailable → fail closed with the accurate recovery guidance
  - foreign target (ErrForeignTarget) → still fails closed (unchanged, non-string)
  - unverifiable installation (ErrUnverifiableInstallation) → still fail closed
  - identity mismatch (ErrCoreIssuerMismatch) → still fails closed (unchanged, non-string)
- Security regression guard: the fail-closed boundaries are unchanged — only the guidance text is corrected. No trust source is opened; no issuer is fabricated; foreign/foreign-identity still rejects.

## Where the regression test goes (CI-covered)

- File: cmd/baha/use_target_connection_test.go (same file/owner as the boundary it tests; existing fail-closed tests stay green).
- CI: `/.github/workflows/ci.yml` "Run release-source tests" job runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` (the cli-surface/lifecycle group), so a new test there IS CI-covered (Owner directive 2026-11-07). No .github/** change needed — the group already compiles cmd/baha.
- Added test: TestBindExplicitSelectionBindsWithoutLocalIssuerDir — bootstrap a verified Core (all 3 caps, Keycloak core issuer present), remove only service-access/issuer, assert bindExplicitSelectionToConnection binds (BF-02 regression guard); companion TestBindExplicitSelectionFailsClosedOnAbsentCore keeps the bare-target fail-closed assertion.

## Repo-rule compliance

- Write-set scoped to cmd/baha (use_target.go, onboarding.go, use_target_connection_test.go) — the exact production selection path. No .github/** touched (Owner scope). Single integration candidate from origin/develop d884919 / cdb4350a6 clone. Evidence written only to baseharbor-plan (no product-repo writes, no .evidence/). No subagents (4.8). No runner/VM infra.

## END

- Status: BLOCKED (scope decision required) — see QUESTION below.
- Candidate SHA: (none yet; branch lane/0427-162-issuerfix at cdb4350a6, no commits)

## Push verification (done 2026-11-08 ~18:2x)

- Product fix branch `lane/0427-162-issuerfix` pushed; commit `6d96bf5cad206327c895becf77a785c7186e6b76` confirmed via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane/0427-162-issuerfix`.
- Evidence on origin/main: file present (verified `git ls-tree origin/main --name-only .../round-2.md`); origin/main (HTTPS) = `05224eb6875311bb39f8f86719243fd252b8664a`.
- CI job that runs this test group: `.github/workflows/ci.yml` "Run release-source tests" → `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` (line 123); also pre-release / docker + podman acceptance runs it. My regression tests live in `cmd/baha` (same package) so they run under that group with no .github/** change.

## CI outcomes (local, sandbox; no hosted run — .github/** is Owner scope)

- `go build ./cmd/baha` OK. `go vet ./cmd/baha/...` OK. gofmt clean on all edited files.
- `go test ./cmd/baha` full package: only failure is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` — PRE-EXISTING (fails identically on base develop HEAD `d884919`), needs a real isolated Core runtime unavailable in the sandbox. Not caused by this change-set.
- All target-connection selection tests pass, including the two new guards: `TestBindExplicitSelectionBindsWithoutLocalIssuerDir` (BF-02 regression: verified Core without service-access/issuer selects) and `TestBindExplicitSelectionFailsClosedOnAbsentCore` (absent Core still fails closed with typed conflict).
- Note: no hosted CI run was triggered (Owner scope forbids workflow_dispatch/reruns; the mission's hosted-run step is a 156-domain Keycloak/Core STATE).

## Hosted CI run — PR #1489 (terminal hosted run, Eigenes-Run-Pflicht)

- PR: https://github.com/mcpdev80/baseharbor/pull/1489 — `fix(0427-162): reachable recovery wording in issuer selection errors`, base `develop`, 3 changed files (cmd/baha/use_target.go, cmd/baha/onboarding.go, cmd/baha/use_target_connection_test.go), ±48/-5. No drift vs develop (branch = develop + 1 commit).
- CI run: https://github.com/mcpdev80/baseharbor/actions/runs/42505772259 (pinned EXPECTED_HEAD 6d96bf5).
- PASSING: go-build, go-vet, cli-gofmt, go-unit-tests, Source format, Trusted Plan, Workflow policy, Focused Python, Native impact selection, Native destroy retry (docker+podman).
- FAILING (2): `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` — both fail on `TestControlPlaneSingleDefaultNativeRuntimeInCI` with:
  `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-.../baseharbor-bootstrap-cleanup-pending: no such file or directory`.
- Diagnosis — PRE-EXISTING hosted-CI precondition, NOT caused by this change: the failure is in the shared package-level integration-test TestMain (`runRuntimeIntegrationTestMain` / `runtime_integration_test_support_test.go`), which FAILS OPEN BY CONTRACT when the bootstrap trust-plane marker `baseharbor-bootstrap-cleanup-pending` is absent. That marker is laid down by a PRIOR CI step in the Docker/Podman acceptance flow (cell marker path), independent of any source change. The test only runs under `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE=1` (acceptance only). My change touches only error-string wording in use_target.go/onboarding.go and adds two pure-selection unit guards — it cannot affect this bootstrap fixture. go-unit-tests (the package run) PASSED in the same CI job, so the unit layer is green.
