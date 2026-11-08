# Evidence: Bug t-20261108-bughunt-0427-test-bootstrap-leak (0427-127) — round 3

Shift r27-welle5-folge-2026-11-08. Lane mission `mission-127-r3.md`, candidate branch `work/0427-127-test-bootstrap-leak` (PR #1454), single candidate per chain (AGENTS 3.8).

## PLAN

- Read the full r3 mission and the full recipe `act-1454-review-r2.md` (origin/main 24f1b7c5 lineage); confirm PR #1454 head 8cadc33a8 and develop base 07ae6c3e9 via `git ls-remote` only.
- Cut the worktree on the named candidate branch only; write the exact base SHA into this evidence and prove it is an ancestor of the first commit.
- Recipe (1): in `cmd/baha/runtime_integration_test_support_test.go` make the package-teardown AND the orphan-adoption path FAIL-OPEN — propagate the teardown error out of `destroyBootstrapTrustPlaneAtPackageEnd` into `runRuntimeIntegrationTestMain`'s named return `code` so `TestMain`'s `os.Exit` is non-zero on a real teardown failure; the marker must survive an adoption that did not succeed (no marker removal after a failed destroy); no teardown error may end as silent success.
- Recipe (3): add an injected-failure regression that proves a forced bad teardown red-makes the run (CI-covered), and confirm the CI selector runs the new `TestBootstrap*` proofs.
- Recipe (2): update `round-3.md` OWN-BLOCK so the reviewer recipe names EXACTLY `.github/workflows/ci.yml:255-256` and `:342-349` as the Owner-change that lets a PR job run the runtime-integration suite with the fixture — carry the exact line numbers into the OWN-BLOCK (Owner scope, do not edit).
- Recipe (4): drift-merge develop, run affected-package + go-unit terminal checks, `git log` own-commits-only, `ls-remote` cleanliness, publish evidence to baseharbor-plan origin/main, END.

## Base attestation

Planning repo (authoritative) — one-line witness as required:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
origin: https://github.com/mcpdev80/baseharbor-plan.git
```

(NOT the workers/baseharbor-plan directory; no evidence was committed to any product repo.)

Product repo remote truth measured via `git ls-remote` from a fresh clone only (the quarantined workers/baseharbor checkout is never cited):

```
$ git ls-remote origin refs/heads/develop refs/pull/1454/head refs/heads/work/0427-127-test-bootstrap-leak
07ae6c3e91b081a189266ca4b162ba705d4aa78f    refs/heads/develop
8cadc33a8a6101a2b071bb092176a36b1a699109    refs/heads/work/0427-127-test-bootstrap-leak
8cadc33a8a6101a2b071bb092176a36b1a699109    refs/pull/1454/head
```

- Branch cut (BASE ATTESTATION): the mission names the existing candidate branch; the worktree is cut from the exact remote head `8cadc33a8a6101a2b071bb092176a36b1a699109` (PR #1454 head == branch head). The develop base at cut is `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; that SHA is an ancestor of the first commit and is listed as the only prior history before the first local commit. No branch cut from another PR head is carried.
- Drift-merge: `origin/develop` latest is merged before pushing; `git merge-base --is-ancestor origin/develop HEAD` exit 0 (DRIFT-MERGE-OK).

## What r3 changed vs r2 (the FAIL-OPEN gap)

Recipe (1) — `cmd/baha/runtime_integration_test_support_test.go`:

- `destroyBootstrapTrustPlaneAtPackageEnd` (was `...:154-162`) now returns the `errors.Join` of the destroy error and the marker removal instead of only logging to stderr.
- `runRuntimeIntegrationTestMain` gains a named return `code`; the deferred `destroyBootstrapTrustPlaneAtPackageEnd(marker)` writes into `code` (`code = 1`) when the package teardown failed, so `TestMain`'s `os.Exit(code)` is non-zero on a real teardown failure. A teardown failure is never a silent success. The exact `defer destroyBootstrapTrustPlaneAtPackageEnd(marker)` line and the `return m.Run()` form are preserved for the structural guard `TestBootstrapTestMainStructureGuaranteesTeardown`.
- `destroyOrphanedBootstrapMarkers` now returns an aggregated error (config-load, unread-marker, missing-persisted-target, unresolvable-provider, any destroy failure all make the return non-nil).
- `adoptBootstrapLeftoverMarkerFromDeadProcess` returns an error and removes the marker ONLY after `destroyOrphanedBootstrapMarkers` reports success; on a config-load / inventory / destroy failure it keeps the marker and surfaces a visible stderr error (`orphan adoption FAILED …`) so the next run fails closed. This is the recipe's "marker survives a failed adoption" rule.
- `destroyBootstrapTrustPlane` keeps the marker when the teardown could not even begin (config unavailable, target unconfigured, provider unresolvable — detected by the new `isUnbeginningTeardownError`), so the next run fails closed; a teardown that ran but reported residuals still consumes the marker (preserving r2's `TestBootstrapCleanupRunsAfterSetupFailure` contract for the "ran-and-reported" case).

Recipe (3) — injected-failure regression in `cmd/baha/runtime_integration_cleanup_coverage_test.go`:

- `TestBootstrapInjectedTeardownFailureRedMakesTheRun`: stage one claims the target and marker via the production TestMain path and returns normally (no `t.Fatalf`), so the only way that subprocess can exit non-zero is the fail-open package teardown; stage two adopts a dead owner's marker and asserts the orphan destroy failure is surfaced, the marker kept and the run exits non-zero (fail-closed). The regression is genuinely discriminating: neutralising the fail-open wiring makes stage one exit 0 and the parent assertion fails.
- Package-global `init()` injects `runtimeBootstrapTeardownFailure` and `runtimeBootstrapOrphanDestroyFailure` when `BASEHARBOR_TEST_INJECTED_TEARDOWN=1`; a `sync/atomic` flag records the forced failure so the stage-one body can return normally while the fail-open wiring still makes the run red.

## CI coverage (recipe 3 — verified against current develop)

Finding: the r2 OWN-BLOCK 2 claim that no PR-CI selector matches `^TestBootstrap` no longer holds on current develop. The `cli-package-tests` selector in `scripts/pr-check-runner.py:196` runs `go_package_tests(repository, ['./cmd/baha'], …)` which invokes `go test ./cmd/baha -count=1 -json` (pr-check-runner.py:118) — the WHOLE `cmd/baha` package, no `-run` filter. So every new `TestBootstrap*` proof in `cmd/baha/` runs under `PR · Validation · cli-package-tests` on every PR. The injected-teardown regression is therefore CI-durable, not a local-only witness.

The r2 runtime-integration OWN-BLOCK still stands for the heavyweight runtime_integration consumers:

- `.github/workflows/ci.yml:255-256` — the `validate` job gate excludes `pull_request` events.
- `.github/workflows/ci.yml:342-349` — the `runtime_integration` step runs a narrow `-run '^(TestRepositoryWorkflowRealLifecycle|…)$'` pattern that does not include `TestBootstrap*`, and is skipped silently on PRs.

Owner-scope note (recipe 2): the reviewer recipe in `act-1454-review-r2.md` must name these EXACT lines as the Owner change that lets a PR job run the runtime-integration suite with the fixture. `.github/**` is NOT touched and no rerun/dispatch is triggered by this lane; a failing/skipped check is reported as STATE here.

## Verification record

- Local (candidate 8cadc33a8): `go build ./...` OK; `go vet ./cmd/baha` clean; `gofmt -l` empty. All `TestBootstrap*` proofs pass under `-shuffle=on` (r3 structural guard updated for the fail-open named-return form; `TestBootstrapCleanupRunsAfterSetupFailure` updated so an unbeginning teardown keeps the marker per the recipe). The injected-teardown regression `TestBootstrapInjectedTeardownFailureRedMakesTheRun` passes WITH the fail-open fix and fails when the fix is neutralised — discriminating.
- Ancestry: `git merge-base --is-ancestor 07ae6c3e9 HEAD` exit 0 (ANCESTOR-OK); `git log --oneline origin/develop..HEAD` lists only this card's chain (f03b12bdd round-1 candidate of the same card allowed). No foreign candidate commit is carried.
- The single pre-existing shuffle-ordering flake `TestMaintenanceHistoryAppendFailureLeavesNoAdvancedCurrentRecord` fails only under broad `-run` shuffles and passes in isolation; it is unrelated to this change (different package, does not touch any r3 file) and is host/state contamination, not a regression.

## Compose/VM

- No containers/compose projects were started by this lane on this host (directive 2026-11-05); no VM smoke test is named in this mission. All started compose projects are brought DOWN by this lane's last action.

## END line format

`END_DONE|END_BLOCKED mission-127-r3.md: … candidate 8cadc33a8` via `codeman agent post 594fd2f5-4e80-43b6-9841-92879146a85e`.

## repo-rule compliance

- Evidence lives only in baseharbor-plan `evidence/r27-welle5-folge-2026-11-08/bughunt-test-bootstrap-leak/round-3.md`; no `.evidence/` dirs, no product-repo main writes.
- `.github/**` untouched; no reruns, no workflow_dispatch. Failing/skipped checks are reported as STATE only.
- One candidate per chain: only `work/0427-127-test-bootstrap-leak` is worked; no second branch.
- No subagents (4.8); all steps executed in this session.
- Reality witnesses via `ls-remote`/fresh clone only; the quarantined `workers/baseharbor` checkout is never cited.
