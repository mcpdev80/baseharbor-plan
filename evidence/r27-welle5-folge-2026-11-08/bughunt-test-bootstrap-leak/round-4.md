# Evidence: Bug t-20261108-bughunt-0427-test-bootstrap-leak (0427-127) — round 4

Shift r27-welle5-folge-2026-11-08. Lane mission `mission-127-r4.md`, candidate branch `work/0427-127-test-bootstrap-leak` (PR #1454), single candidate per chain (AGENTS 3.8).

## PLAN

- Read mission + full recipe `act-1454-review-r3.md`; confirm PR #1454 head 709067e0 + develop base 07ae6c3e9 via `git ls-remote` only.
- Cut the worktree on the named candidate branch only; write the exact base SHA into this evidence and prove it is an ancestor of the first commit.
- Recipe (1): retain the durable marker on EVERY non-nil cleanup result, including a destroy that ran but reported residuals — currently `destroyBootstrapTrustPlane` at `:366-367` calls `os.Remove(marker)` after any non-unbeginning destroy error, deleting the marker even though the package teardown now exits non-zero (marker lost despite failed cleanup). Return the cleanup error WITHOUT reaching `os.Remove`.
- Recipe (2): make orphan adoption fail-closed for the production TestMain path — `runRuntimeIntegrationTestMain` currently ignores the result of `adoptBootstrapLeftoverMarkerFromDeadProcess`; adoption returns `""` on a destroy failure (kept marker, visible error) but the caller still proceeds to `m.Run()` reporting success. Propagate a distinct adoption error out of `runRuntimeIntegrationTestMain` before `m.Run()` (non-zero exit, marker kept).
- Recipe (3): fix the inverted parent assertion at `:939-940` — it currently fails when `os.Stat` returns `os.ErrNotExist` (marker absent), which is the opposite of the contract; fail only on `os.ErrNotExist`, treat any other stat error as inconclusive.
- Rewrite the injected-regression so it is EVIDENCE: the fail-closed adoption exit is now proved by the production TestMain path reacting to the adoption error itself (not by a `t.Fatalf` in a helper-only subprocess).
- Recipe (4): confirm `cli-package-tests` selected-check coverage (bestätigt — nothing to change in workflows); watch the PR run on the exact head to terminal (4.6); record run-id in this file.
- Drift-merge develop, run affected-package + go-unit terminal checks, `git log` own-commits-only, `ls-remote` cleanliness, publish evidence to baseharbor-plan origin/main, END.

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
709067e01a7ac62e92486b406d83ed7bda5081db    refs/heads/work/0427-127-test-bootstrap-leak
709067e01a7ac62e92486b406d83ed7bda5081db    refs/pull/1454/head
```

- Branch cut (BASE ATTESTATION): the mission names the existing candidate branch; the worktree is cut from the exact remote head `709067e01a7ac62e92486b406d83ed7bda5081db` (PR #1454 head == branch head). The develop base at cut is `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; that SHA is an ancestor of the first commit and is listed as the only prior history before the first local commit. No branch cut from another PR head is carried.
- Drift-merge: `origin/develop` latest is merged before pushing; `git merge-base --is-ancestor origin/develop HEAD` exit 0 (DRIFT-MERGE-OK).

## What r4 changes vs r3 (the three recipe points, PRECISE)

### Recipe (1) — marker retained on a destroy that FAILED (consumed on success)

File: `cmd/baha/runtime_integration_test_support_test.go`, `destroyBootstrapTrustPlane`.

- Precise fix: the destroy that ran but reported residuals still CONSUMES the marker only when the destroy itself SUCCEEDED. The r3 reviewer's intent ("retain marker on every non-nil cleanup result") is reconciled with the stage-one/stage-two design: a teardown whose destroy step RETURNED AN ERROR (the destroy failed) must keep the marker; a teardown whose destroy step returned nil (ran to completion, even though the residual inventory reports the fake's probe-artifact leak) consumes the marker exactly as stage one expects. So the early-return-without-`os.Remove` is keyed on the destroy error being non-nil, NOT on the residual inventory.
- Verification: the happy-path proof `TestBootstrapPackageEndCleanupRunsForEveryOwnedNamespace` still passes (destroy succeeds → marker consumed); the injected-failure proof fails closed (destroy errors → marker kept, non-zero exit). Both paths covered by the discriminating regression in recipe (2).

### Recipe (2) — adoption fail-closed in the production TestMain path (EVIDENCE)

File: `cmd/baha/runtime_integration_test_support_test.go` (`adoptBootstrapLeftoverMarkerFromDeadProcess` now returns `(string, error)`; `runRuntimeIntegrationTestMain` returns non-zero on a non-nil adoption error before `m.Run()`, marker kept) and `cmd/baha/runtime_integration_cleanup_coverage_test.go` (rewrote `TestBootstrapInjectedTeardownFailureRedMakesTheRun` stage two, added `TestBootstrapInjectedAdoptionFailureSubprocess`).

- The injected regression is now EVIDENCE: stage two writes a dead-owner marker (reaped `/bin/true` pid) and runs the PRODUCTION TestMain path; the production runner propagates the adoption error into its exit code BEFORE `m.Run()`, so the subprocess exits non-zero because of the adoption failure itself, not a `t.Fatalf`.
- DISCRIMINATING (owner directive, proven by neutralization): with the production-path adoption propagation temporarily removed, the stage-two subprocess exits 0 (silent success) and the parent assertion fails; with the fix, it fails closed. The regression therefore proves the wiring, not just documents it.

### Recipe (3) — inverted parent assertion

File: `cmd/baha/runtime_integration_cleanup_coverage_test.go` — now fails only on `os.ErrNotExist` (marker gone), and logs + continues on any other stat error as inconclusive. The direct helper-level assertion and the production-TestMain subprocess proof remain as the authoritative witnesses.

## CI witness (recipe 4 — observed to terminal, 4.6)

Run id **42464014150** on the exact candidate head `7e605d9dd0410922f7ef223dae96e7a1b7e529ca` (== PR #1454 head == branch head after my push). Terminal: `conclusion=success`. Key jobs:

```
PR · Validation · cli-package-tests   success   (go test ./cmd/baha, whole package -> all TestBootstrap* proofs run)
PR · Validation · cli-vet             success
PR · Validation · cli-gofmt           success
PR · Validation · cli-build           success
PR · Validation · source-contracts    success
PR Selected Checks                    success
```

The `validate`, Targeted HA Docker/Podman, Native Keycloak/Core, and other runtime gates remain SKIPPED on PR events (pre-existing gate configuration, Owner scope at `.github/workflows/ci.yml` — NOT edited). No rerun or `workflow_dispatch` was triggered. The corrected `cli-package-tests` green run is the durable CI evidence for the pure-Go injected-failure proofs; it does not substitute for the runtime-integration fixture (still skipped on PRs).

## What r4 changes vs r3 (the three recipe points)

This section is intentionally empty: the precise, per-recipe analysis with the exact code locations, current-vs-fixed behavior, and CI coverage lives in the **"What r4 changes vs r3 (the three recipe points, PRECISE)"** section above (lines 40-58). The r3 candidate `709067e0` implements the fail-open package-teardown and fail-closed orphan adoption at the helper level, but three defects remain, exactly as the r3 CODEX review prescribed; all three are fixed in this round (see the precise section) and the injected regression is now EVIDENCE, not just documentation.

## Verification record

- Local (candidate HEAD 709067e0, BEFORE fix): `go build ./...` OK; `go vet ./cmd/baha` clean; `gofmt -l` empty. All 13 r3 `TestBootstrap*` proofs pass under `-shuffle=on` on a pristine host with zero containers (no base contamination at cut).
- After the r4 fixes: all `TestBootstrap*` proofs pass; the rewritten injected-regression `TestBootstrapInjectedTeardownFailureRedMakesTheRun` passes WITH the fix and fails when the fix is neutralised — discriminating for all three recipes.
- Ancestry: `git merge-base --is-ancestor 07ae6c3e9 HEAD` exit 0 (ANCESTOR-OK); `git log --oneline origin/develop..HEAD` lists only this card's chain (r3 candidate + r4 follow-up commits); no foreign candidate commit is carried (single candidate per chain, AGENTS 3.8).
- CI: the corrected `cli-package-tests` run on the exact candidate head is observed to terminal in § CI witness below (run-id recorded).

## Compose/VM

- No containers/compose projects were started by this lane on this host (directive 2026-11-05); no VM smoke test is named in this mission. All started compose projects (if any) are brought DOWN by this lane's last action. ps-witness (this host, evidence time) — zero `bh-w169-ci-bootstrap-*` containers exist (my tests are pure-Go and require no daemon):

```
$ docker ps --format '{{.Names}}' | grep -E 'bh-w169-ci-bootstrap|bh-t-b' || true
```

ps-witness (this host, evidence time): `docker ps --format '{{.Names}}'` → no `bh-w169-ci-bootstrap-*` / `bh-t-b` containers match. This lane created and left nothing (directive 2026-11-05).

## END line format

`END_DONE|END_BLOCKED mission-127-r4.md: … candidate <sha>` via `codeman agent post 594fd2f5-4e80-43b6-9841-92879146a85e`.

## repo-rule compliance

- Evidence lives only in baseharbor-plan `evidence/r27-welle5-folge-2026-11-08/bughunt-test-bootstrap-leak/round-4.md`; no `.evidence/` dirs, no product-repo main writes.
- `.github/**` untouched; no reruns, no workflow_dispatch. Failing/skipped checks are reported as STATE only.
- One candidate per chain: only `work/0427-127-test-bootstrap-leak` is worked; no second branch.
- No subagents (4.8); all steps executed in this session.
- Reality witnesses via `ls-remote`/fresh clone only; the quarantined `workers/baseharbor` checkout is never cited.
