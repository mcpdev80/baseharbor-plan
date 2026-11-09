# EVIDENCE 0427-174 round-2 — three error-fold-back paths fixed + develop integration

LANE: w174b (0427-174 r2)
MODEL: worker-ornith1.5-laptop
DATE: 2026-11-09
MISSION: /tmp/opencode/mission-174-r2.md
CODEX REVIEW (round-1): `vm-bughunt/act-1506-review.md` — verdict KORREKTUR (fix)
PR: #1506 `0427-174-permission-truth`

## Remote witnesses (ls-remote, authoritative)

- PR #1506 head: `fb21a02eec29890c793ae3da5e8ab7d3567fa829` (refs/pull/1506/head)
- PR base: `20902f0a6ab016fd8fe6a501751e1becc5f334dd`
- develop (authoritative, explicit-SHA fetch): `b3a8042d18ea60f162a32a51df34a499cad6a237`
- Ancestry: `git merge-base --is-ancestor 20902f0a origin/develop` => true (PR base is ancestor of develop)
- Gap PR-base..develop: exactly ONE commit `b3a8042d1 fix(r27): target delete honors --yes on non-TTY (#1494)`; touches only `cmd/baha/target*` files, NO overlap with the PR target files (`deployment_list.go`, `deployment_owner_loan.go`, `deployment_store.go`, `cmd/baha/app_context.go`). Rebase window clean.
- NOTE on stale refs: the initial clone captured a stale local `origin/develop` (`f6c15edc`). The coordinator cross-checked the host and confirmed `refs/heads/develop = b3a8042d1`. All ancestry/tree witnesses below are explicit-SHA fetches against origin, not the stale ref.

## Candidate committed on PR branch (GitHub, authoritative)

- Branch head after rebase + force-push: `1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`
  (local worktree SHA after the readability trim; local commit `1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`)
- `git merge-base --is-ancestor b3a8042d1 1080ac444` => develop IS ancestor (base-refresh proven)
- `git log --oneline b3a8042d1..1080ac444` lists ONLY my own commits (2):
  - `fe7346d05 fix(cmd/baha, internal/deployment): distinguish access-denied and invalid-name from foreign installation (0427-174)` — PR #1506 original partial fix
  - `1080ac444 fix(0427-174 r2): propagate owner state errors through CLI and loan recheck; narrow foreign-fallback`
- No foreign commit carried on top. Branch provenance: `b3a8042d1` is an ancestor of the exact head; the head was cut by rebasing the fix chain onto develop, not from another candidate.

## Hosted run (GitHub-hosted CI, terminal)

- Run id `5446`, event `pull_request`, head `1080ac444`, conclusion `success` (verified via `gh run list` + commit check-runs; all non-success jobs are `skipped`, the targeted-native skip pattern — run is green).
- The `PR · Source format` job (the only failing job on the earlier force-pushed head `29bfc2458`) passes on `1080ac444`. Root cause of the earlier failure was a gofmt/line-count regression from my own read/edit while extracting helpers; fixed below. No `.github/**` file was edited (Owner scope) and no rerun/workflow_dispatch was triggered by me — the fix is a code + formatting change pushed to the existing PR branch, which is the normal PR push path.

## The three fold-back bugs (from round-1 CODEX review) and fixes

### Finding 1 — access-denied folded into "not found" at the CLI
- `internal/deployment/deployment_list.go` best-effort list tagged EVERY owner error as `DeploymentRecordStateError.Kind = "missing"`. `cmd/baha/app_context.go::resolveRegisteredApplication` only handled `Kind = "incomplete"` warnings, so an access-denied owner silently became `has no registered deployment`.
- Fix: tag non-missing owner errors distinctly via a new `classifyOwnerWarning` helper (`access-denied` / `malformed` / `missing`), and in `app_context.go` propagate a matched `access-denied` or `malformed` warning as a fail-closed `machine.Error` (cause `deployment_owner_access_denied` / `deployment_owner_malformed_state`, code `ErrorInternal`) BEFORE the generic not-found path.
- New regression `cmd/baha/app_context_owner_state_test.go::TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound`: corrupt `installation.json` (invalid JSON) at a bare named entry and assert the true owner-state cause code is returned, never foreign / not-found.

### Finding 2 — loan recheck folded read errors into `ErrDeploymentOwnerForeign`
- `internal/deployment/deployment_owner_loan.go` loan-recheck mapped any non-`os.ErrNotExist` `coreinstallation.Load` failure into `ErrDeploymentOwnerForeign`.
- Fix: propagate read/engine errors fail-closed — `ErrDeploymentOwnerAccessDenied` (via `isAccessDeniedLoadError` on the classified loader `resolveInstallationLoad`) or the concrete unchanging error; `ErrDeploymentOwnerForeign` stays reserved for the positive hash/target mismatch that `VerifyDeploymentOwnerAgainstOwner` establishes once a state actually loads. Replaced the direct `coreinstallation.Load` call with `resolveInstallationLoad` and removed the now-unused coreinstallation import.
- New regression `internal/deployment/deployment_owner_loan_recheck_test.go::TestDeploymentOwnerLoanRecheckPropagatesReadError`: inject a deterministic permission-denied through the package-internal seam during the loan recheck and assert it is `ErrDeploymentOwnerAccessDenied`, NOT `ErrDeploymentOwnerForeign`.

### Finding 3 — foreign-fallback mapped every non-missing load error to foreign
- `internal/deployment/deployment_store.go` foreign-fallback mapped every non-`os.ErrNotExist`, non-FS `coreinstallation.Load` error to `ErrDeploymentOwnerForeign`, including present-but-malformed states.
- Fix: add `ErrDeploymentOwnerMalformedState` (new sentinel) and `isMalformedInstallationLoadError`: a Core state that LOADS but is invalid/incomplete/inconsistent is its own fail-closed named error; only a positively-loaded divergent identity stays foreign. Updated the existing `deployment_owner_binding_test.go` corrupt-owner seam test, which encoded the old malformed->foreign behaviour, to assert the corrected `ErrDeploymentOwnerMalformedState`.

### Helper extraction (readability cap)
- `classifyOwnerWarning`, `isAccessDeniedLoadError`, `isMalformedInstallationLoadError` extracted to a new `internal/deployment/deployment_owner_classification.go`; `internal/deployment/deployment_store.go` kept at 798 lines (under the 800 cap) and gofmt-clean.

## Local verification (all on the rebased head)

```
go build ./...                      -> BUILD OK
go vet ./internal/deployment/       -> clean
go test ./internal/deployment/      -> ok
go test ./cmd/baha/ -run 'TestResolveRegisteredApplication|TestAppContext|Incomplete|Duplicate|...Propagates'  -> ok (10.7s)
gofmt -l <all changed files>        -> empty (clean)
scripts/source-readability-audit.sh -> PASS (file size, function span, regression ratchet)
```

## Repo-rule compliance

- No `.github/**` file edited (Owner scope). The CI source-format failure was a defect in my own pushed code, corrected by a code/format change pushed to the existing PR branch — the normal PR push path, not a workflow rerun.
- No subagents (directive 4.8): every step run in this session.
- Evidence written only to baseharbor-plan (evidence/...), never into the product repo. No `.evidence/` directory anywhere.
- No runner infrastructure built/registered/repaired. No docker/podman compose projects started (no VM smoke test named by mission) — nothing to bring down.
- No product-repo writes outside the PR branch. Product repo pins: baseharbor = this PR chain.

## END

END_DONE 0427-174: fix — PR #1506 `0427-174-permission-truth` head `1080ac444` (develop `b3a8042d1` ancestor, 2 own commits), CI 5446 success. Evidence: vm-bughunt/bughunt-permission-lies-foreign-install/round-2.md.
