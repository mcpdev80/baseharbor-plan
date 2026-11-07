# 0427-117-prod-owner: r5 — production (ungated) owner resolution for the authorized remote-podman apply path

- Role: Worker (Lane 0427-117-prod-owner); coordinator `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-podman-owner-missing` (card number 0427-117 · podman-family Deploy owner), PR #1419, branch `work/r27-remote-up-owner-missing`, head `438895466eed1838bd50f3f9838184e4b7d7ebc1`, base `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`.
- Correction round r5 after CODEX act-1419b REJECT_LANE_FIX: the prior owner loan was `testing.Testing()`-gated (test-scope only), so the production remote-podman `app up` path still failed `ErrDeploymentOwnerMissing`; the regression only called the seam directly, never the real CLI apply.
- This lane resolves the genuine owner from the effective CLI/apply target context WITHOUT the test gate, keeping the fail-closed one-installation-owner invariant, and proves it with an un-gated unit regression that runs in GitHub CI.
- This file contains NO markdown checkboxes anywhere.

## PLAN (numbered; mirrors workers/todos/0427-117-prod-owner.json)

- Read mission, card, act-1419a/b, round-3 evidence; verify planning-repo zone and PR #1419 remote head/base via `git ls-remote`.
- Design decision on scope-split (Owner clarification 2026-11-04): post a QUESTION, got Boot-CORE-ONLY local-READY + un-gated unit regression.
- Fresh isolated worktree `/tmp/opencode/0427-117-prod-owner-wt`; base `develop eee11d50` ancestor-of HEAD (rc0) before first commit.
- Implement `productionLoanAuthorityForTarget` + `bahaEffectiveBootTargetName`/`productionBootRuntimeRoot`; drop `bahaTestProcessEnvironment` gate; preserve `ErrDeploymentOwnerMissing` sentinel.
- Add un-gated regression: pass cell GREEN with fix, RED with `ErrDeploymentOwnerMissing` without fix; connector + unmarked stay fail-closed on both sides.
- Local: `go build ./...`, `go vet ./cmd/baha/`, `go test ./cmd/baha/` (excl. the one docker-integration test that fails identically on base), `go test ./internal/deployment/...`, gofmt clean.
- Targeted `git add` of 6 files (NO `git add -A`); commit on top of PR head `c0ac3bef` (single integration chain).
- Push to GitHub named branch; PR #1419 head `c0ac3bef..43889546`.
- Own CI run 4989 (auto `pull_request`) to terminal: record run-id; `cli-package-tests` + `PR Selected Checks` SUCCESS; docker/podman skipped owner-gate.
- Write evidence, commit+push to origin/main, ls-tree present before END; post END_DONE.

## Planning-zone attestation (required)

- Real planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin  https://github.com/mcpdev80/baseharbor-plan.git`), NOT `workers/baseharbor-plan`.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.

## Base attestation and provenance (BEFORE and AFTER)

- Fresh remote witness (`git ls-remote origin` on a clean clone in /tmp/opencode): `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`; PR #1419 head `c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5`.
- **Base is an ancestor of my head** (`git merge-base --is-ancestor eee11d50... 43889546...` rc0).
- Branch cut on top of the EXACT old PR #1419 head `c0ac3bef` (the single integration chain that already integrated the old w280 candidate). `git log --oneline origin/develop..HEAD`:
  - `43889546` fix(cli,deployment): resolve podman-family deployment owner for authorized remote up path (card 0427-117) — THIS LANE, my single commit
  - `c0ac3bef` Merge remote-tracking branch 'origin/develop' into work/r27-remote-up-owner-missing-117 (old candidate tip, base-refreshed)
  - `7b25276c`, `68190cdc`, `8b5075d2`, `9ffc036e`, `801fdbc7`, `c5cacec5`, `5c2c7106`, `14ec6674` (old candidate, single chain)
  - Only my one commit sits on top of the old PR head; the old commits are ancestors in the single chain.
- Parent of my first fix commit `43889546` is exactly `c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5` (the old PR head).

## Fix (file:line)

- `cmd/baha/deployment_record.go:121-219`: `productionLoanAuthorityForTarget` replaces the test-gated `testLoanAuthorityForTarget`. It grants a loan authority ONLY when every condition holds, and returns a non-nil failure on ANY other shape:
  - the effective target is a LOCAL access Target (not connector/remote);
  - the boot installation the CLI's OWN effective-target selection (`bahaEffectiveBootTargetName`, effective-target order activated -> persisted -> default -> single -> "local") resolves is a GENUINE, READY Core installation physically present on this machine;
  - the boot Target differs from the requested one;
  - no startup-bound management installation is bound in the current command context (the w273 remote expectation stays fail-closed).
  - `AssertStateIsGenuineInstallation` + `Ready` + `Spec.Target == bootTargetName` guards replace the marker + `testing.Testing()` triggers; no new public API.
- `cmd/baha/deployment_record.go:302-360`: `bahaEffectiveBootTargetName` (renamed from `bahaTestBootTargetName`) + `productionBootRuntimeRoot` (renamed from `bahaTestBootRuntimeRoot`).
- `cmd/baha/deployment_record.go:234`: `deploymentTargetLoanVerifier` now calls `productionLoanAuthorityForTarget`; the seam keeps the original `ErrDeploymentOwnerMissing` sentinel on any refusal.
- `cmd/baha/deployment_record.go`: removed the now-unused `bahaTestProcessEnvironment` / `bahaTestProcessEnv` (the narrow test-provenance gate) and its `init()` binding in `test_isolation_support_test.go`; the production loan no longer depends on any test-process hook.
- `internal/deployment/deployment_store.go` and `internal/deployment/deployment_owner_loan.go`: doc updates — the loan is no longer described as TEST-SCOPE ONLY; the fail-closed guarantees and the `ErrDeploymentOwnerMissing` sentinel are preserved.

## Regression test (un-gated, runs in GitHub CI)

- `cmd/baha/deployment_owner_loan_regression_test.go`: appended three un-gated cells that run with NO `bahaTestProcessEnv` seam and WITHOUT `testing.Testing()` provenance, exercising the exact production path `recordDeploymentBeforeMutation` runs from a normal `baha` binary:
  - `TestProductionOwnerLoanLocalIsolatedApplyPasses` — genuinely ownerless isolated podman Target with Local access passes the owner seam against the boot installation the CLI selects (GREEN with fix).
  - `TestProductionOwnerLoanConnectorBoundStaysFailClosed` — connector-bound isolated target stays `ErrDeploymentOwnerMissing` (RED on both sides).
  - `TestProductionOwnerLoanUnmarkedLocalStaysFailClosed` — unmarked local isolated target stays `ErrDeploymentOwnerMissing` (RED on both sides).
- Red-first proven locally: on the stashed base commit (test-gated loan) the pass cell fails with the verbatim sentinel "deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable" (RED); connector + unmarked cells stay pass; with the fix all three pass (GREEN).
- Runs under `cli-package-tests` (`go test ./cmd/baha`) — durable GitHub-CI evidence, not a local-only or VM-only cell. No `.github/**` change needed for the test to run.

## CI run (own-run, monitored to terminal)

- Run **4989** — terminal **success**, head `438895466eed1838bd50f3f9838184e4b7d7ebc1` (base `develop eee11d50`), event `pull_request` (auto-triggered by the push; no rerun/workflow_dispatch, no `.github/**` edit).
- `PR Selected Checks` = success (base attestation clean, branch from develop chain, single integration chain).
- `cli-package-tests` = success (my un-gated regression runs here), `cli-build` = success, `cli-gofmt` = success, `cli-vet` = success, `deployment-package-tests` = success, `source-contracts` = success, `PR · Source format` = success, `PR · Trusted Plan` = success, `PR · Focused Python` = success, `Workflow policy` = success.
- Scope-skipped (owner push-ref gate, not failures): `Targeted HA · docker` (128313901403), `Targeted HA · podman` (128313924845), `PR · Selected Runtime`, `PR · Demo Pin`, `PR · Exact Candidate`, `PR · Public Contracts`, `PR · Consumer Pins`, `PR · Runner Interface`, `Release Source Preflight`, `validate`. These are owner-push-ref gated, so they skip on a normal PR push.
- The true remote-Podman `up -> doctor` end-to-end needs a `Targeted HA · podman` runtime cell (owner-push-ref gated). Per the mission scope-split that is an Owner finding under `.github/**` and is NOT triggered/rerun here; the un-gated unit regression is the durable CI evidence for the production owner resolution.

## Local test witnesses (own-run)

- `go build ./...` rc=0; `go vet ./cmd/baha/` rc=0; `gofmt -l` clean on all six changed files.
- `go test ./internal/deployment/...` => `ok github.com/mcpdev80/baseharbor/internal/deployment 1.810s`.
- `go test ./cmd/baha/ -run 'TestProductionOwnerLoan' -v` => all three pass (GREEN with fix).
- Red proven: with the fix stashed, `go test ./cmd/baha/ -run 'TestProductionOwnerLoan'` => `TestProductionOwnerLoanLocalIsolatedApplyPasses FAIL` with the verbatim `ErrDeploymentOwnerMissing` sentinel; connector + unmarked cells stay PASS.
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` FAILS on BOTH base and candidate — it is a docker-integration test that needs a running docker Core (`start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`); it is NOT a regression from this change (fails identically on the stashed base).

## repo-rule compliance

- Product repo `baseharbor`: single candidate branch `work/r27-remote-up-owner-missing`, single PR #1419, head advanced `c0ac3bef..43889546` on the single integration chain; no second branch/PR, no foreign commit on top. No `.github/**` file edited; no rerun, no workflow_dispatch. No subagents. No self-merge.
- Evidence only in `baseharbor-plan/evidence/...`, never the product repo. No `.evidence/` directory anywhere.
- No VM/container started on any host; no compose project left running.

## END

END_DONE 0427-117-prod-owner: head=438895466eed1838bd50f3f9838184e4b7d7ebc1 pr=1419 base=eee11d50 rc0 prod_owner=productionLoanAuthorityForTarget real resolved via CLI effective-target (BASEHARBOR_TARGET-first) genuine+READY local Core NOT test-gated fail-closed sentinel ErrDeploymentOwnerMissing preserved regression=un-gated TestProductionOwnerLoanLocalIsolatedApplyPasses GREEN + connector/unmarked RED on both sides (RED on stashed base with verbatim sentinel) ci=4989 TERMINAL-SUCCESS incl cli-package-tests+PR Selected Checks docker/podman skipped owner-gate single-integration-chain (c0ac3bef..43889546 only my commit on top) 6 files no .github local-go build/vet/test/gofmt clean akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-5.md origin/main
