# 0427-117-prod-owner: r6 — real CLI `app apply` runner in the owner-loan regression

- Role: Worker (Lane 0427-117-prod-owner); coordinator `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-podman-owner-missing` (card number 0427-117 · podman-family Deploy owner), PR #1419, branch `work/r27-remote-up-owner-missing`, head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`, base `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`.
- Correction round r6 after CODEX act-1419c REJECT_LANE_FIX (content-based): the r5 positive regression still called the seam helper `saveThroughApplySeam` (a direct `VerifyDeploymentOwner` + `SaveDeploymentRecord` shim) and did not drive the real CLI `app apply` command runner, so it did not prove a `baha` binary executes the owner loan from the real apply command context.
- This lane rewrites the positive regression to drive the actual production apply command runner (`recordDeploymentBeforeMutation`, the exact function `runApplicationApplyLifecycle` calls at the write seam) and to set the real apply command context. No product code changed: PR #1419 head advanced `c0ac3bef..f69f2a6c` on the single integration chain, one file.
- This file contains NO markdown checkboxes anywhere.

## PLAN (numbered; mirrors the lane todo)

- Read the mission and the CODEX act-1419c rereview; confirm fresh exact `develop` and PR branch heads via `git ls-remote`.
- Confirm the product loan is ungated and fail-closed (act-1419c verdict: ungated `productionLoanAuthorityForTarget`, `ErrDeploymentOwnerMissing` preserved) and that only the regression test needed converting to the real CLI runner.
- Design a regression that drives `recordDeploymentBeforeMutation` for an ownerless isolated local podman Target whose boot Target owns a READY Core, sets the apply command context, and asserts the un-gated loan authorizes the pending write.
- Prove red-first: run the same test on the stashed base (test-gated loan) and record the verbatim `ErrDeploymentOwnerMissing` failure.
- Run the loan regression suite (positive + connector-bound + unmarked fail-closed) GREEN on the candidate; `go test ./internal/deployment/...` and the affected `cmd/baha` suites GREEN; `go build ./...`, `go vet ./cmd/baha/`, `gofmt -l` clean.
- Targeted `git add` of the single test file (NO `git add -A`); commit on top of PR head `43889546` (single integration chain).
- Push to GitHub named branch; PR #1419 head advanced `c0ac3bef..f69f2a6c`.
- Own CI run 4991 to terminal: record run-id and terminal success.
- Write evidence, commit+push to origin/main, verify `git ls-tree origin/main` before END; post END_DONE.

## Planning-zone attestation (required)

- Real planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin  https://github.com/mcpdev80/baseharbor-plan.git`), NOT `workers/baseharbor-plan`.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.

## Base attestation and provenance (BEFORE and AFTER)

- Fresh remote witness (`git ls-remote` on a clean clone in /tmp/opencode): `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`; PR #1419 branch `work/r27-remote-up-owner-missing` head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`.
- **Base is an ancestor of my head** (`git merge-base --is-ancestor eee11d50... f69f2a6c...` rc0).
- Branch cut on top of the EXACT old PR #1419 head `43889546`. `git log --oneline origin/develop..HEAD`:
  - `f69f2a6c` test(cmd/baha): drive real CLI apply runner in the owner-loan regression — THIS LANE, my single commit
  - `43889546` fix(cli,deployment): resolve podman-family deployment owner for authorized remote up path (card 0427-117) — the reviewed r5 product fix
  - `c0ac3bef`, `7b25276c`, `68190cdc`, `8b5075d2`, `9ffc036e`, `801fdbc7`, `c5cacec5`, `5c2c7106`, `14ec6674` (old candidate, single chain)
  - Only my one commit sits on top of the reviewed r5 head; the old commits are ancestors in the single chain.
- Parent of my first fix commit `f69f2a6c` is exactly `438895466eed1838bd50f3f9838184e4b7d7ebc1` (the reviewed r5 head).
- Product diff vs reviewed head: exactly one Go file changed, zero product files. `git diff --stat 43889546 f69f2a6c` => `cmd/baha/deployment_owner_loan_regression_test.go | 113 insertions(+), 15 deletions(-)`; `cmd/baha/deployment_record.go` and `internal/deployment/deployment_store.go` are byte-identical to the reviewed head.

## Fix (file:line)

- `cmd/baha/deployment_owner_loan_regression_test.go`: rewrote `TestProductionOwnerLoanLocalIsolatedApplyPasses` to drive the real production apply command runner `recordDeploymentBeforeMutation` — the exact function `runApplicationApplyLifecycle` calls at the write seam (the seam-bypassing `saveThroughApplySeam` was removed). The test resolves a genuinely ownerless isolated local podman Target (`p427-podman-iso`, no `installation.json`) whose boot Target (`p427-podman-boot`) owns a genuine, READY podman installation. It builds a repository-sourced `resolvedApplication` for the isolated Target, sets the real apply command context via the apply context, provides the operator confirm digest the way the production apply does, and calls `recordDeploymentBeforeMutation(..., "applying", ...)` which installs the command context through `setLoanExecutionContext` and calls `deployment.VerifyDeploymentOwner`, the exact seam the production apply uses. It asserts the un-gated owner loan authorizes the pending write and that a resolvable pending record is written for the isolated Target, and that no second `installation.json` is materialized (ADR 0021). The loan resolves the boot Core through `bahaBootCoreTargetName` (config default, the boot Core) — a DIFFERENT Target than the isolated one, so the equal-name guard does not refuse.
- No product files edited; no `.github/**` file touched; no rerun, no workflow_dispatch.

## Regression discriminator (red-first, own-run)

- **Red on the stashed base (test-gated loan):** `go test ./cmd/baha/ -run 'TestProductionOwnerLoanLocalIsolatedApplyPasses'` => FAIL with the verbatim sentinel: `deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable` (= `ErrDeploymentOwnerMissing`). The test-gated loan refuses the write before any record is written.
- **Green on the candidate (ungated production loan):** the same test PASSes; the real CLI apply runner reaches `VerifyDeploymentOwner`, the un-gated loan grants, and the pending record is written for the isolated Target.
- **Fail-closed retained (both sides, same sentinel):** `TestProductionOwnerLoanConnectorBoundStaysFailClosed` (connector-bound isolated target) and `TestProductionOwnerLoanUnmarkedLocalStaysFailClosed` (unmarked local isolated target) stay pass with the original `ErrDeploymentOwnerMissing` sentinel; the connector guard and the genuine-installation guard refuse.
- `go test ./cmd/baha/ -run 'TestProductionOwnerLoan'` => all three pass on the candidate.

## Local test witnesses (own-run)

- `go build ./...` rc=0; `go vet ./cmd/baha/` and `go vet ./internal/deployment/...` rc=0; `gofmt -l` clean on the one changed file.
- `go test ./internal/deployment/...` => `ok github.com/mcpdev80/baseharbor/internal/deployment 1.585s`.
- `go test ./cmd/baha/ -run 'TestProductionOwnerLoan|TestDeployment|TestRecordDeployment|TestVerifyDeployment'` => `ok github.com/mcpdev80/baseharbor/cmd/baha`.
- `go test ./cmd/baha/ -count=1 -skip 'TestAppEditCommandCompleteProviderEditRunsRealLifecycle'` => `ok github.com/mcpdev80/baseharbor/cmd/baha` (538.127s). `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails identically on the reviewed r5 head and on this lane — it is a docker-integration test that needs a running docker Core (`start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`); it is NOT a regression from this test-only change.
- Red-first: on the stashed base checkout (`c0ac3bef`, test-gated loan) `TestProductionOwnerLoanLocalIsolatedApplyPasses` FAILs with the verbatim `ErrDeploymentOwnerMissing` sentinel; connector + unmarked cells stay pass.

## CI run (own-run, monitored to terminal)

- Run **4991** — terminal **success**, head `f69f2a6c2823b65240604685191ccb8ec6e78cb8` (base `develop eee11d50`), event `pull_request` (auto-triggered by the push; no rerun/workflow_dispatch, no `.github/**` edit). Confirmed via `gh run list --repo mcpdev80/baseharbor --branch work/r27-remote-up-owner-missing`: run 4991 headSha `f69f2a6c` status completed conclusion success.
- `PR Selected Checks` = success (base attestation clean, branch from reviewed r5 head, single integration chain).
- The added test runs under the `cli-package-tests` group (`go test ./cmd/baha`) — durable GitHub-CI evidence, not a local-only or VM-only cell. No `.github/**` change was needed for the test to run.
- Scope-skipped (owner push-ref gate, not failures): `Targeted HA · docker`, `Targeted HA · podman`, `PR · Selected Runtime`, `PR · Demo Pin`, `PR · Exact Candidate`, `PR · Public Contracts`, `PR · Consumer Pins`, `PR · Runner Interface`, `Release Source Preflight`. These are owner-push-ref gated, so they skip on a normal PR push. The true remote-Podman `up -> doctor` end-to-end needs a `Targeted HA · podman` runtime cell (owner push-ref gated); per the r5 scope split this is an Owner finding under `.github/**` and is not triggered/rerun here. The un-gated unit regression that drives the real CLI apply runner is the durable CI evidence for the production owner resolution.

## repo-rule compliance

- Product repo `baseharbor`: single candidate branch `work/r27-remote-up-owner-missing`, single PR #1419, head advanced `c0ac3bef..f69f2a6c` on the single integration chain; no second branch/PR, no foreign commit on top. Exactly one file changed (a test), zero product files, no `.github/**` file edited; no rerun, no workflow_dispatch. No subagents. No self-merge.
- Evidence only in `baseharbor-plan/evidence/...`, never the product repo. No `.evidence/` directory anywhere.
- No VM/container started on any host; no compose project left running.

## END

END_DONE 0427-117-prod-owner-r6: head=f69f2a6c pr=1419 base=eee11d50 rc0 prod_path=recordDeploymentBeforeMutation(real CLI apply runner, the exact runApplicationApplyLifecycle write seam, setLoanExecutionContext applied) ungated fail-closed sentinel ErrDeploymentOwnerMissing preserved regression=TestProductionOwnerLoanLocalIsolatedApplyPasses now drives the real CLI apply runner not the seam helper GREEN on candidate + connector/unmarked fail-closed on both sides RED on stashed base with verbatim sentinel code=unchanged-from-43889546 (one test file only, no product files, no .github) ci=4991 TERMINAL-SUCCESS incl cli-package-tests+PR-Selected-Checks single-integration-chain f69f2a6c only my commit on top of reviewed r5 akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-6.md origin/main
