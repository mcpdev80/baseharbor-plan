# 0427-162 r2 — verify PR #1489 fix on the NEW develop HEAD (156 fix now reachable)

- Card/mission: mission-162-r2 (0427-162 r2, verification of the accepted fix #1489 on the moved develop HEAD)
- Shift: r27-welle5-folge-2026-11-08 / round-3
- Worker session: laptop (session 594fd2f5-4e80-43b6-9841-92879146a85e), no subagents (4.8)
- Planning repo verified (origin/main HTTPS): `6ee12e0215bb9635f97b3a04b7c146eb0e65aea8` (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git main`)
- Source pin (origin/HTTPS develop HEAD): `171e9569d4bdea0b03faca663dc88a41e185f75f` (`git ls-remote https://github.com/mcpdev80/baseharbor.git develop`)
- Branch base attestation: origin/develop exact new HEAD `171e9569d4bdea0b03faca663dc88a41e185f75f` IS an ancestor of my commit `37de11198d4c3329c55899b9456e44c3a571de2f` (`git merge-base --is-ancestor 171e9569... HEAD` => PASS). Single integration candidate, no foreign branch carried. My git log --stat lists ONLY my own commit.
- Branch: `lane/0427-162-r2-verify` cut from the NEW develop HEAD 171e9569, fix cherry-picked from the accepted PR #1489 head 6d96bf5.
- Source zone: /tmp/opencode/w162-issueruse-wt (fresh clone of mcpdev80/baseharbor @ develop). Working tree /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor is a 259-commit-stale stale-ref checkout and was NOT used as evidence.
- Build: go build ./cmd/baha OK on new develop HEAD 171e9569 (`go version go1.26.8 linux/amd64`).

## PLAN

- Read mission-162-r2.md, board card, round-1/2 diagnostic; confirm scope is VERIFICATION of the accepted fix, not re-fix
- Verify remote truth via `git ls-remote` HTTPS (origin main/develop); attest exact new develop HEAD 171e9569 ancestor-of-HEAD
- Confirm the 156 fix (0e3a6975e) is now reachable in develop: `git merge-base --is-ancestor 0e3a6975e origin/develop` => PASS (the 156-blockade is gone; 2 marker lines in docker+podman)
- Cut a fresh branch off the NEW develop HEAD, cherry-pick the accepted PR #1489 fix content, commit as the single integration candidate
- Confirm my fix content is byte-identical to the accepted PR head 6d96bf5 (git diff empty)
- Local tests: go build ./cmd/baha, go vet ./cmd/baha, all 9 selection tests incl 2 BF-02 guards
- Push new branch to origin; confirm pushed HEAD via git ls-remote
- Watch hosted CI run on the exact new head to terminal state (Native Keycloak/Core docker+podman cells = 156 domain; skip/red = STATE, not fix)
- Confirm PR Selected Checks green; ls-remote + cleanliness; publish board state
- Write round-3.md evidence to baseharbor-plan; commit to origin/main; END in geteilte inbox

## Refresh: 156 fix now reachable in develop (the blocker is gone)

- Mission-162-r2 states the 156-blockade is gone because the 156 lines are now IN develop (0e3a6975e). Confirmed: `git merge-base --is-ancestor 0e3a6975e origin/develop` => PASS. The failing test `TestControlPlaneSingleDefaultNativeRuntimeInCI` (docker+podman) now has its bootstrap-trust-plane marker present — the shared package-level integration-test TestMain (`runRuntimeIntegrationTestMain` / `runtime_integration_test_support_test.go`) only fails open when that marker is absent, and the marker is laid by a prior CI step in the Docker/Podman acceptance flow. So the gate is now healable, not foreign-rot.
- The 156 fix 0e3a6975e was NOT in the OLD branch base (cdb4350a) of the earlier fix lane; it IS in the NEW develop HEAD 171e9569. This is exactly why a fresh branch off 171e9569 is required.

## New branch cut from the NEW develop HEAD

- New develop HEAD: `171e9569d4bdea0b03faca663dc88a41e185f75f` — `fix(0427-167): stop remote Core bootstrap from falling back to local Docker (#1492)`.
- Branch `lane/0427-162-r2-verify` created from 171e9569; fix cherry-picked as single commit `37de11198d4c3329c55899b9456e44c3a571de2f`.
- Content verification: `git diff 6d96bf5..37de1119 -- cmd/baha/use_target.go cmd/baha/onboarding.go cmd/baha/use_target_connection_test.go` => EMPTY (identical to the accepted PR #1489 head). My commit is content-equivalent to the accepted candidate; only the base commit differs (171e9569 vs the old cdb4350a base).
- `git log --stat HEAD` lists ONLY my own commit `37de1119`; no foreign commit carried.

## Local test outcomes (sandbox; no hosted run — .github/** is Owner scope)

- `go build ./cmd/baha` OK.
- `go vet ./cmd/baha/...` OK.
- `gofmt` clean on all three edited files.
- Full selection suite (all 9) PASS: `TestBindExplicitSelectionBindsThroughReadingResolver`, `TestBindExplicitSelectionFailsClosedWithoutCore`, `TestBindExplicitSelectionFailsClosedOnUnreadableBaseCA`, `TestBindExplicitSelectionMutantSkipsResolver`, `TestBindExplicitSelectionBindsWithoutLocalIssuerDir`, `TestBindExplicitSelectionFailsClosedOnAbsentCore`, `TestBindExplicitSelectionResolvesKeycloakCoreIssuer`, `TestBindExplicitSelectionFailsClosedOnForeignIssuerIdentity`, `TestBindExplicitSelectionFailsClosedOnMissingKeycloakIssuer`.
  - BF-02 regression guard `TestBindExplicitSelectionBindsWithoutLocalIssuerDir`: verified Core without `service-access/issuer` selects (BF-02 stays remediated on the new HEAD).
  - `TestBindExplicitSelectionFailsClosedOnAbsentCore`: absent Core still fails closed with a typed conflict (no security regression).
- Pre-existing, unrelated failure confirmed NOT caused by this change: `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails with `start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner` — it requires a real isolated Core runtime unavailable in the sandbox (round-2 recorded it fails identically on base develop HEAD d884919). It is a real-native-runtime integration test, not in my diff, and my string/test change cannot touch it. The CI-group `go test ./cmd/baha` (the package run) is the CI-covered gate; the two unit guards live there.

## CI coverage statement (Owner directive 2026-11-07)

- The two BF-02 regression guards live in `cmd/baha/use_target_connection_test.go` (same package/owner as the boundary they test).
- CI group: `/.github/workflows/ci.yml` "Run release-source tests" runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` (the cli-surface/lifecycle group). A test in this package runs under that group. No `.github/**` change is needed — the group already compiles `cmd/baha`; the file/owner already exists (Owner directive 2026-11-07: the group already exercises this path).
- Note: `.github/**` is Owner scope. If a reviewer later determines the CI trigger rule does not cover this exact file, that is an exact change to report with file:line, not to edit. No such gap exists here — `go test ./cmd/baha` compiles the whole package including this file.

## Repo-rule compliance

- Write-set scoped to cmd/baha (use_target.go, onboarding.go, use_target_connection_test.go) — byte-identical to the accepted PR #1489. No `.github/**` touched (Owner scope). Single integration candidate from origin/develop 171e9569 / 0e3a6975e. Evidence written only to baseharbor-plan (no product-repo writes, no `.evidence/`). No subagents (4.8). No runner/VM infra. No compose project started (no docker/podman stack to tear down).
- Branch provenance: new develop HEAD `171e9569d4bdea0b03faca663dc88a41e185f75f` is an ancestor of commit `37de1119` (attested). No branch cut from another candidate head.

## END

- Status: in progress — pushed; hosted CI run on the exact new head to terminal state pending (Eigenes-Run-Pflicht).
- Candidate SHA: `37de11198d4c3329c55899b9456e44c3a571de2f` (branch lane/0427-162-r2-verify, content identical to PR #1489 head 6d96bf5).
