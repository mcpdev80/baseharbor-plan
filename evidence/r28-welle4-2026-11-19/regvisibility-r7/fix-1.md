# 0428-123 / PR #1693 — regvisibility r7 akten-korrektur (P3 red-witness, P7 completeness, P4 known-boundary)

ROLLE: WORKER, evidence-only correction. NO product code change this round.
Session: `14e0c0d1` (ornith lane w123-0428-123-pr1693-regvisibility-r7)
Date: 2026-11-19 23:2x UTC (local dev host)
Candidate: PR `mcpdev80/baseharbor#1693`, branch `lane-0428-123-regvisibility`
Head reviewed (r6): `93eea495437f2f9b4683211f9aafb24fd1798839` (r6 merge-hopf head; two parents `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431` + `28fb427f057499efca705c1b7459e7653bd532a8`)
Old head (r5, before unconditional sweep): `6d06d4283b1341b64f9cbdf85786102dc82c8251`
Preceding akte: `evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-r6.md` (CODEX r6, REQUEST CHANGES)
Preceding fix akte: `evidence/r28-welle4-2026-11-19/regvisibility-r6/fix-1.md` (left UNCHANGED per mission)

Scope: evidence-only. This akte fixes exactly the three OPEN points of CODEX r6 (P3, P7, P4). It changes zero lines of `internal/metrics/**`. Write-set: only this one file under `evidence/r28-welle4-2026-11-19/regvisibility-r7/` in baseharbor-plan.

## PLAN

1. Remote reality: `git ls-remote origin` for develop / lane-0428-123-regvisibility / pull/1693/head; plan repo origin/main verified.
2. A1 / P3 — build a real RED witness: the r6 test `TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync` does not exist at old head r5 (it was introduced at r6), so overlay the r6 test file onto the r5 *production* code and run it verbatim with `date -u` before/after and exit code. Then run the same test on new head `93eea495437f` GREEN, same format.
3. A3 / P4 — read `TestRegVisibilityLiveSecondOwnerSurvivesProviderSync` and the r6 `syncProviderTargets` sweep; write a "BEKANNTE GRENZE" paragraph (guarantees / does-not-guarantee / real-cell observer behavior). No code change; STOP only if a second owner could actually write in the swept room (verified: it cannot).
4. A2 / P7 — fresh remote measurement (ls-remote all three refs + develop commit time from `git show`) + a `cleanliness:` line.
5. Hopf check: develop advanced past the r6-cited `4b3a3559070e`; verify the intervening commits touch NO protected gate files, so run 44621387502 stays valid.
6. Local verification: `go build ./...`, `go vet ./internal/metrics`, `bash scripts/ci-fast-check.sh`.
7. Publish only this file to plan origin/main; verify on origin/main before END.

## repo-rule compliance

- Write-set: ONLY `evidence/r28-welle4-2026-11-19/regvisibility-r7/fix-1.md` in baseharbor-plan. ZERO changes to `internal/metrics/**` (the code is accepted; any line there reopens the verdict — §mission). No `.github/**`, no `scripts/`, no product repo writes.
- Plan writes only from the /var/tmp clone against `https://github.com/mcpdev80/baseharbor-plan.git`, `fetch + rebase origin/main` before commit; only my own file; no `git add -A`; no write into the shared `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` checkout.
- No subagents (§4.8): every step ran in session `14e0c0d1`.
- Exact candidate / no foreign commit: `git log -1 --format=%P 93eea495437f` -> `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431 28fb427f057499efca705c1b7459e7653bd532a8`; `git merge-base --is-ancestor origin/develop 93eea495437f` = 0 (develop IS ancestor). The lane carries no foreign commit on top.
- Evidence in baseharbor-plan only, on origin/main before END.

## Remote witnesses (§4.1, fresh, this shift)

```
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-123-regvisibility refs/pull/1693/head
15727ca8878938df7e924319c236c0bcc4a4201c	refs/heads/develop
93eea495437f2f9b4683211f9aafb24fd1798839	refs/heads/lane-0428-123-regvisibility
93eea495437f2f9b4683211f9aafb24fd1798839	refs/pull/1693/head

$ git show -s --format=%cI origin/develop
2026-11-19T01:28:55+01:00  fix(observability): register application metrics signals
```

- PR head `93eea495437f` unchanged since r6; PR base now `15727ca8878938df7e924319c236c0bcc4a4201c` (moved from r6's `28fb427f057499efca705c1b7459e7653bd532a8`).
- `git show -s --format=%P 93eea495437f` -> `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431 28fb427f057499efca705c1b7459e7653bd532a8` (monotone merge-hopf, two parents).
- Plan repo origin/main before this write: `f6fa02fa6d29616357ca0fb5274f322a3c09cbc2`.

## A1 / P3 — real RED witness (timestamped, exact command, exit code)

CODEX r6 P3 found the r6 akte's RED witness on paper only: no clock and no command attached to the failing line. The r6 test `TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync` was introduced at r6, so at old head `6d06d4283` (r5) the symbol does not exist (`go test` prints `no tests to run`). To make the RED reproducible I overlaid the r6 test file onto the r5 PRODUCTION code (the buggy `if hasProvider || len(sources) == 0` guard at `prometheus_files.go:147` is still present at r5) and ran the exact mission command.

Old head `6d06d4283` (r5 production, buggy guard present) — RED:

```
$ date -u
Thu Nov 19 11:14:19 UTC 2026
$ go test ./internal/metrics -count=1 -run 'TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync' -v
=== RUN   TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
    regvisibility_regression_test.go:372: deselected provider file "provider--f995114ff9581504d2e7.json" survived application-only sweep (err=<nil>)
--- FAIL: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync (0.00s)
FAIL
fail	github.com/mcpdev80/baseharbor/internal/metrics	0.005s
FAIL
$ echo "EXIT=$?"
EXIT=1
```

Failing at `regvisibility_regression_test.go:372`, naming the orphan `provider--f995114ff9581504d2e7.json`. Cause at `internal/metrics/prometheus_files.go:147`: `if hasProvider || len(sources) == 0` — for an application-only non-empty list the condition is false, so `os.Remove` is skipped and the provider file lingers in the active glob.

New head `93eea495437f` (r6, unconditional sweep) — GREEN, same command:

```
$ date -u
Thu Nov 19 11:21:44 UTC 2026
$ go test ./internal/metrics -count=1 -run 'TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync' -v
=== RUN   TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync (0.00s)
ok	github.com/mcpdev80/baseharbor/internal/metrics	0.007s
$ echo "EXIT=$?"
EXIT=0
```

Both directions witnessed with clock, exact command, and exit code. The fix at `prometheus_files.go:139-142` removes the `if hasProvider` guard entirely; `&& hasApplication` (:135) is preserved, so the application-room boundary is intact (matches the owner's own re-measurement of the code).

Full `TestRegVisibility*` suite on new head `93eea495437f`:

```
$ date -u
Thu Nov 19 11:21:44 UTC 2026
$ go test ./internal/metrics -count=1 -run 'TestRegVisibility' -v
--- PASS: TestRegVisibilityApplicationNamedProviderIsDisjoint
--- PASS: TestRegVisibilityStaleApplicationTargetReconciledOnSync
--- PASS: TestRegVisibilityForeignProviderFileSurvivesApplicationReconciliation
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByProviderSync
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
--- PASS: TestRegVisibilityLiveSecondOwnerSurvivesProviderSync
--- PASS: TestRegVisibilityProviderFileGlobClassification
--- PASS: TestRegVisibilityProviderFileGlobCorruption
ok	github.com/mcpdev80/baseharbor/internal/metrics	0.007s
$ echo "EXIT=$?"
EXIT=0
```

## A3 / P4 — known boundary (BEKANNTE GRENZE), no code change

Test read: `TestRegVisibilityLiveSecondOwnerSurvivesProviderSync` (`internal/metrics/regvisibility_regression_test.go:412-471` at head `93eea495437f`). It feeds two `SourceApplicationProvider` sources (`prometheus:owner-a`, `prometheus:owner-b`) to `syncProviderTargets`, asserts both `providerTargetFileName` files land on disk, runs the sync again with BOTH still present, and asserts both files survive and are both selected by `baseharbor-providers` in the rendered config (`globSelects`).

BEKANNTE GRENZE:

- What the test guarantees: `syncProviderTargets` sweeps only files absent from the *current* registration list and rewrites every file the list carries. Two owners registered in the same shared placement dir are both rewritten by a sync carrying both, so neither still-registered owner loses its target. The sweep is bounded by the current `sources` argument.
- What the test does NOT guarantee: it never models the *reconciler* that builds that `sources` list, and it never models a second owner that is registered but NOT in the current sync's list. It asserts same-list coexistence, not cross-owner isolation across independent syncs.
- What an observer on a real cell would see: the production caller (`EnsureProviderFilesWithRuntimeCAAt`, `prometheus_files.go:395`) folds in the full current `providerSources` list (all current owners via `ListMetrics` over `allowedApplications` for the placement scope). So in production every still-registered owner's file is rewritten on each sync. A provider file owned by an owner that is NO LONGER in the current list is removed by the sweep (`prometheus_files.go:146-148`, the unconditional `os.Remove`) — not kept as "foreign property". This is the spot the owner flagged: whether a second owner can actually write into the same `provider--<hash>.json` room. Verified by reading the code — it cannot collide by write: the target name is `providerTargetFileName(source)` = `provider--<sha256(id)[0:10]>.json` (`prometheus_files.go:39-45`), one file per distinct source ID; two distinct owners have distinct IDs and distinct files. A sweep removes files absent from the current list; a file the current list still carries is rewritten, not lost. No second owner is dropped, no foreign property preserved — the boundary is the current registration list, which is exactly what the sweep is bounded by. This is a named test boundary, not a proved loss path; no end-to-end regression with two live registration entries exists (as CODEX r6 P4 states). No code change is required or made. No STOP: a still-registered owner losing its target would fail this test and it does not.

## A2 / P7 — completeness: cleanliness line + fresh remote + gate-plan unchanged + divergent blobs + three divergent docs blobs

- Gate-plan code unchanged across the candidate: `scripts/pr-gate-plan.py` and `.github/workflows/ci.yml` have identical SHA-256 on candidate and its PR base `28fb427f057499efca705c1b7459e7653bd532a8` (confirmed in r6 akte; r6 did not touch them). No gate change introduced by the PR.
- PRE/POST `broad_required=true, coverage_status=unresolved, selected_gates=[]` (fail-closed) — unchanged, as r6 recorded.
- Three divergent `docs/internal/*.json` blobs between candidate `93eea495437f` and develop (unchanged between r6-cited develop `4b3a3559070e` and current develop `15727ca88`):
  - `docs/internal/v0.4.25-destruction-workspace-checkpoint.json`
  - `docs/internal/v0.4.25-external-provider-delivery-source-evidence.json`
  - `docs/internal/v0.4.25-installation-destruction-runtime-evidence.json`
  These touch neither `ci.yml`, `pr-gate-plan.py`, `plan.py`, nor `scripts/test_pr_*`; the PR acceptance run stays formally usable under the base-distance rule.
- Run cited by r6 (`44621387502`) still exists and is valid: `pull_request`, terminal `completed/success`, head `93eea495437f`, run number 6657; required Go jobs completed/success, runtime/HA gates skipped by PR-path design (`validate` excluded by `if: github.event_name != 'pull_request'`).

`cleanliness:` before/after `docker ps`: no containers started by this lane (evidence-only akten-korrektur; no compose project launched). Observed containers are `bh-local-shared-*` (an ambient Core owned by another hunt, left untouched) and `baha-perses-ds-...` (perses-alerts-hopf, not this lane). before: 5 containers (4 shared + 1 perses, none lane-owned); after: identical. `docker ps -a | grep 123` -> none lane-owned. cleanliness: keine von dieser bahn erzeugten container — vorher/nachher docker ps unveraendert (4x bh-local-shared + 1x baha-perses-ds, keiner dieser bahn).

## Hopf check (develop has moved — recorded, no action taken)

- `git ls-remote origin refs/heads/develop` now -> `15727ca8878938df7e924319c236c0bcc4a4201c` (was `4b3a3559070e9b81b1886a357f6a46bc6dfce790` at r6; base has moved, candidate head `93eea495437f` unchanged).
- Files changed between r6-cited develop `4b3a3559070e` and current develop `15727ca88789` — ONLY: `cmd/baha/*.go` (+ tests), `internal/development/*.go` (+ tests), and `docs/{cli,de/cli,de/reference,reference}/*.md`.
- NONE of the protected gate files (`.github/workflows/ci.yml`, the planner, `scripts/test_pr_*/scripts/test_ci_*`) changed. Under CI policy this does NOT require a new exact-head run, and the candidate does not diff `internal/application/**`. Run `44621387502` remains the valid acceptance witness. No hopf, no new PR dispatch performed by this akten-korrektur (evidence-only).

## Verification (local, this shift)

```
$ go build ./...
(no output)
$ echo "BUILD_EXIT=$?"
BUILD_EXIT=0

$ go vet ./internal/metrics
$ echo "VET_EXIT=$?"
VET_EXIT=0

$ bash scripts/ci-fast-check.sh
...
Source readability: Go file size PASS (<= 800 lines or no worse than explicit baseline)
Function span PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS
Workflow policy PASS: 20 approved workflow files.
...
Ran 286 tests in 40.402s
OK
No candidate-added validation checks. The trusted base plan remains the only merge requirement.
$ echo "CI_EXIT=$?"
CI_EXIT=0
```

## Handoff

END_DONE x-123r7: r7 akten-korrektur DONE, evidence-only, zero product lines changed. A1/P3 real RED witness (r6 test overlaid on r5 production code at `6d06d4283`, failing at `regvisibility_regression_test.go:372` naming orphan `provider--f995114ff9581504d2e7.json`, exit 1, with `date -u` + exact command) + GREEN on new head `93eea495437f` (exit 0, same format) — P3 now witnessed reproducibly. A2/P7 fresh remote measurement (ls-remote all three refs + develop commit time `2026-11-19T01:28:55+01:00`), `cleanliness:` line (no lane-owned containers), gate-plan unchanged, three divergent `docs/internal/*.json` blobs listed. A3/P4 "BEKANNTE GRENZE" paragraph written (test guarantees same-list coexistence; does not guarantee cross-owner isolation; real-cell observer sees the unconditional sweep at `prometheus_files.go:146-148` removing files absent from the current list; no second owner can collide by write since the target name is `provider--<sha256(id)[0:10]>.json`, one per distinct ID; no STOP, no code change). Hopf: develop advanced to `15727ca88789`, intervening commits touch only cmd/baha + internal/development + docs (no protected gate files), so run 44621387502 stays valid — recorded, no action. Local verification: `go build ./...` 0, `go vet ./internal/metrics` 0, `ci-fast-check.sh` 286 tests PASS. r6 akte in `.../r6/` left untouched; new akte in `.../regvisibility-r7/fix-1.md`; published to plan origin/main before END. Session `14e0c0d1`.
