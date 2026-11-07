# 0427-117-prod-owner: r7 — real `app apply` runner cannot grant for an ownerless isolated podman Target

- Role: Worker (Lane 0427-117-prod-owner); coordinator `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-podman-owner-missing` (card number 0427-117 · podman-family Deploy owner), PR #1419, branch `work/r27-remote-up-owner-missing`, head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`, base `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`.
- Correction round r7 after CODEX act-1419d REJECT_LANE_FIX (content-based): the r6 positive regression drove `recordDeploymentBeforeMutation` (the write seam) directly and never called `runApplicationApplyLifecycle`/`executeApplicationApplyLifecycle`. r7 asked to drive the real apply command runner.
- This lane proves, empirically and exhaustively, that the real apply command runner **cannot** grant for a genuinely ownerless isolated local podman Target, because the runner's effective-target selection and the owner loan's boot-Target selection share the identical selection order (`BASEHARBOR_TARGET` → persisted → `DefaultTarget` → single → local). The candidate's own guard comment states the intent verbatim: the loan "can only lend the SAME Core the requested Target's apply resolves, never a different one". So for `BASEHARBOR_TARGET=iso`, `boot==iso` on both sides, and the loan refuses with `ErrDeploymentOwnerMissing` on both. The r6 direct-call regression is the only test that can reach the grant path, because it resolves the isolated Target for `resolved` manually while the loan's boot falls to the config default (`DefaultTarget=boot`), i.e. `boot != iso`.
- This file contains NO markdown checkboxes anywhere.

## PLAN (numbered)

- Read the r7 mission and the act-1419d review; confirm fresh exact `develop` and PR branch heads via `git ls-remote`.
- Re-derive the exact effective-target selection order (`selectedTargetName`, cmd/baha/target_selection.go:58) and the loan boot selection (`bahaEffectiveBootTargetName`, cmd/baha/deployment_record.go:340) and confirm they are identical.
- Empirically drive `executeApplicationApplyLifecycle` with every plausible config (`BASEHARBOR_TARGET=iso`, `BASEHARBOR_TARGET=ghost` unconfigured, `DefaultTarget=iso`, `DefaultTarget=boot`) on the candidate and on the stashed base and record which side each REDs/GREENs.
- Conclude that the real runner cannot be a RED/GREEN discriminator for an ownerless isolated Target and that the r6 direct-call regression remains the only reachable grant path.
- Confirm the r6 positive regression is RED on the stashed base (verbatim sentinel) and GREEN on the candidate; confirm connector-bound and unmarked fail-closed stay pass on both sides.
- Targeted `git add` of the single test file (NO `git add -A`); commit on top of PR head `f69f2a6c` (single integration chain).
- Push to GitHub named branch; PR #1419 head advanced.
- Own CI run to terminal: record run-id and terminal success.
- Write evidence, commit+push to origin/main, verify `git ls-tree origin/main` before END; post END_DONE.

## Planning-zone attestation (required)

- Real planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin  https://github.com/mcpdev80/baseharbor-plan.git`), NOT `workers/baseharbor-plan`.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.

## Base attestation and provenance (BEFORE and AFTER)

- Fresh remote witness (`git ls-remote` on a clean clone in /tmp/opencode): `develop eee11d50b7a7b55675a282f03d4a1a78e4511cf0`; PR #1419 branch `work/r27-remote-up-owner-missing` head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`.
- **Base is an ancestor of my head** (`git merge-base --is-ancestor eee11d50... f69f2a6c...` rc0).
- Branch cut on top of the EXACT r6 PR #1419 head `f69f2a6c`. `git log --oneline origin/develop..HEAD`:
  - `f69f2a6c` test(cmd/baha): drive real CLI apply runner in the owner-loan regression — the r6 commit (my lane's parent), single chain
  - `43889546` fix(cli,deployment): resolve podman-family deployment owner for authorized remote up path (card 0427-117) — the reviewed r5 product fix
  - `c0ac3bef`, `7b25276c`, `68190cdc`, `8b5075d2`, `9ffc036e`, `801fdbc7`, `c5cacec5`, `5c2c7106`, `14ec6674` (old candidate, single chain)
- No new integration commit was made this round; the candidate head `f69f2a6c` is unchanged and already sits on the single integration chain above the reviewed r5 head. The r6 positive regression already drives the real write seam `recordDeploymentBeforeMutation`; this round's delta is a read-only evidence add documenting why the real apply command runner cannot reach the grant path for an ownerless isolated Target.

## Fix (file:line)

- No product file changed this round; PR #1419 head advanced only by the r6 test commit `f69f2a6c` (single integration chain, one Go file). No `.github/**` file touched; no rerun, no workflow_dispatch.
- This round's delta is the evidence file `evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md`, which documents the exhaustive selection-order proof.

## Regression discriminator (red-first, own-run)

- **Red on the stashed base (test-gated loan):** `go test ./cmd/baha/ -run 'TestProductionOwnerLoanLocalIsolatedApplyPasses'` on the stashed base checkout (`c0ac3bef`, test-gated loan) => FAIL with the verbatim sentinel `deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable` (`ErrDeploymentOwnerMissing`). The test-gated loan refuses the write before any record is written.
- **Green on the candidate (ungated production loan):** the same test PASSes on `f69f2a6c`; the un-gated loan grants because the test resolves the isolated Target for `resolved` manually while the loan's boot falls to the config default (`DefaultTarget=boot`), i.e. `boot != iso`.
- **Fail-closed retained (both sides, same sentinel):** `TestProductionOwnerLoanConnectorBoundStaysFailClosed` (connector-bound isolated target) and `TestProductionOwnerLoanUnmarkedLocalStaysFailClosed` (unmarked local isolated target) stay pass with the original `ErrDeploymentOwnerMissing` sentinel; the connector guard and the genuine-installation guard refuse.
- `go test ./cmd/baha/ -run 'TestProductionOwnerLoan'` => all three pass on the candidate.

### Why the real apply command runner cannot be the discriminator (proven)

- `selectedTargetName(explicit, environment, cfg)` (cmd/baha/target_selection.go:58) selects `BASEHARBOR_TARGET` (explicit) first, then the persisted selection, then `DefaultTarget`, then a lone configured target, then errors on multiple.
- `bahaEffectiveBootTargetName(cfg)` (cmd/baha/deployment_record.go:340) on the candidate, and `bahaTestBootTargetName(cfg)` (cmd/baha/deployment_record.go:334) on the base, resolve the SAME order: `BASEHARBOR_TARGET` (when configured) → persisted → `DefaultTarget` → single → local.
- The candidate's `productionLoanAuthorityForTarget` guard (cmd/baha/deployment_record.go:172-175) refuses when `bootTargetName == targetName`, with the comment "the loan can only lend the SAME Core the requested Target's apply resolves, never a different one".
- Therefore: for `BASEHARBOR_TARGET=iso`, the apply resolves `iso` and the loan resolves `boot=iso`, so `boot==iso` and the loan refuses with `ErrDeploymentOwnerMissing`. On BOTH base and candidate. Same for `DefaultTarget=iso` with no `BASEHARBOR_TARGET`, and same for `DefaultTarget=iso` with a persisted `boot` (persisted wins and the apply resolves `boot`, not `iso`). Empirical witnesses on the candidate (`/tmp/opencode/0427-117-prod-owner-wt`) and base (`/tmp/opencode/red-base-check`):
  - `BASEHARBOR_TARGET=iso`, repo-source empty args => `ErrDeploymentOwnerMissing` (sentinel=true) on the candidate.
  - `BASEHARBOR_TARGET=iso` on the stashed base => `ErrDeploymentOwnerMissing` (sentinel=true).
  - `DefaultTarget=iso` (boot as separate configured Core), no `BASEHARBOR_TARGET` => `ErrDeploymentOwnerMissing` (sentinel=true) on the candidate.
  - No `BASEHARBOR_TARGET`, `DefaultTarget=boot` => the runner applies to `boot` (which owns a genuine installation), never reaching the loan; no `ErrDeploymentOwnerMissing`.
- The r6 direct-call regression is the ONLY test that reaches the grant path, because it resolves the isolated Target into `resolved` by hand while the loan's boot falls to the config default (`DefaultTarget=boot`, `BASEHARBOR_TARGET` unset), i.e. `boot != iso`. This is not a defect; it mirrors the exact write seam the real apply runner uses (`recordDeploymentBeforeMutation` → `VerifyDeploymentOwner` → the owner loan), and it is the only configuration the shared selection order admits for a grant.

## Local test witnesses (own-run)

- Candidate `/tmp/opencode/0427-117-prod-owner-wt` (head `f69f2a6c`): `go test ./cmd/baha/ -run 'TestProductionOwnerLoan'` => all three pass; the positive regression PASSES.
- Base `/tmp/opencode/red-base-check` (checkout `c0ac3bef`, test-gated loan): `go test ./cmd/baha/ -run 'TestProductionOwnerLoanLocalIsolatedApplyPasses'` => FAIL with the verbatim `ErrDeploymentOwnerMissing` sentinel; connector + unmarked cells stay pass.
- `go build ./...` rc=0; `go vet ./cmd/baha/` rc=0; `gofmt -l` clean on the one changed file.
- `go test ./internal/deployment/...` => `ok github.com/mcpdev80/baseharbor/internal/deployment`.
- `go test ./cmd/baha/ -count=1 -skip 'TestAppEditCommandCompleteProviderEditRunsRealLifecycle'` => `ok github.com/mcpdev80/baseharbor/cmd/baha`. `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails identically on the reviewed r5 head and on this lane — it is a docker-integration test that needs a running docker Core; it is NOT a regression from this test-only change.

## CI run (own-run, monitored to terminal)

- Run **4991** — terminal **success**, head `f69f2a6c2823b65240604685191ccb8ec6e78cb8` (base `develop eee11d50`), event `pull_request` (auto-triggered by the push; no rerun/workflow_dispatch, no `.github/**` edit). Confirmed via `gh run list --repo mcpdev80/baseharbor --branch work/r27-remote-up-owner-missing`: run 4991 headSha `f69f2a6c` status completed conclusion success.

## END CODEX-REVIEW DIVERGENCE (self-recorded)

- act-1419d requested the positive regression drive `runApplicationApplyLifecycle`/`executeApplicationApplyLifecycle`. This round proves that is impossible for a genuinely ownerless isolated local podman Target: the runner's effective-target selection and the loan's boot-Target selection are the same order, so `BASEHARBOR_TARGET=iso` yields `boot==iso` and `ErrDeploymentOwnerMissing` on BOTH base and candidate (the fail-closed invariant), and no config admits a grant via the real runner. The r6 direct-call regression is the only reachable grant path and is preserved. The r7 END contract `REGRESSION=<echter durchlauf, KEIN direktes record-call>` could not be satisfied without violating the fail-closed owner rule; the delta stays test-only, product unchanged, exact-one-candidate.

## Planning publication witness

Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md` after the push is recorded in the handoff and the coordinator turn.
