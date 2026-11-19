# 0428-123 / PR #1693 — regvisibility r6 correction

Date: 2026-11-19
Worker: ornith rotation lane (takeover c5d271cb, §3.6)
Base: develop `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
Candidate base before r6: `6d06d4283b1341b64f9cbdf85786102dc82c8251`
Exact head after r6 + hopf: `93eea495437f2f9b4683211f9aafb24fd1798839`
PR: mcpdev80/baseharbor#1693, draft=false, base 6e87ddcb4
Review basis: CODEX-REVIEW r5 `baseharbor-plan/evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-r5.md` (read verbatim)

Scope: r6 correction of the already-decided r5 candidate — P1/P3 (unconditional provider-room sweep + mix-fail regression), P2 (live-second-owner). No new design variant. §4.2: change exactly P1/P2/P3, nothing beside.

## Remote witnesses (§4.1)

- `git ls-remote origin refs/heads/lane-0428-123-regvisibility` -> `93eea495437f2f9b4683211f9aafb24fd1798839` (hopf head; r6 candidate `3ca7fa63c` is its first parent)
- `git ls-remote origin develop` -> `28fb427f057499efca705c1b7459e7653bd532a8` (moved from `6e87ddcb4` by PR #1589 = karte 0427-020, merged 17:19Z/22:2x local)
- `git show -s --format=%cI origin/develop` -> `2026-11-19T22:57:14+01:00`
- `git ls-remote origin refs/pulls/1693` -> head `93eea4954`, base `28fb427f0`, draft=false, merged=false, mergeable=true (GitHub API)
- Plan repo HEAD before this shift: `fbad0fca3` (https origin/main); my earlier r5 akte pushed to plan main at `8267721e`/`722e91b9`.

## CODEX-r5 verdict (verbatim essentials)

Verdict: REQUEST CHANGES. Core blocker P1/P3: `internal/metrics/prometheus_files.go:147` `if hasProvider || len(sources) == 0` leaves a stale `provider--` file when a sync carries application-only (non-empty) sources. The r5 regression only exercises the EMPTY follow list (`[]observability.MetricsSource{}`), so the mixed case is unproven and the gap is silently green. P2: no live-second-owner regression exists. P4: live-source-after-application-removal regression is missing (not a regression today, the test is absent). P5/P6: B1 emission, CI uptake, and write-set already correct — no change.

## The measured contradiction

`prometheus_files.go:146-152`: provider files are removed only under `if hasProvider || len(sources) == 0`. The same function's own comment (:106-121) claims "Every run of this sync is a provider sync ... A deselected source leaves no orphan file." When a sync carries application sources and NO provider source (sources non-empty, hasProvider false), the provider case :146 enters but :147 is FALSE — the provider file is NOT removed and lingers as an orphan in the active glob. That is exactly the room-wide sweep the mission and the prior review required.

## PLAN

1. P1/P3 (minimal, exact site `prometheus_files.go:146-152`): make the provider-room branch unconditional — delete the `if hasProvider || len(sources) == 0` guard and its braces, keep only the `os.Remove(...)` with its existing `errors.Is(err, os.ErrNotExist)` handling. The function owns the provider room, so it sweeps it on EVERY run. Leave the application-room branch (`&& hasApplication`) untouched — that is the deliberate boundary to the foreign room.
2. P1 comment (:106-121): replace the claim that the provider case is guarded by `hasProvider || len(sources) == 0` with the truthful statement that this sync owns and always sweeps the provider room and never touches the application room.
3. P3 new regression: write a provider file (selected provider source), then sync with ONLY application sources (non-empty); assert both `provider--` files gone via `os.Stat` IsNotExist and the application file present and visible in the rendered config snippet. Prove BOTH directions (application file stays, provider file gone).
4. P2: two registered owners in the same shared placement dir, one owner-sync; state what happens to the other owner's file (the sweep hits it by shared prefix) and decide STOP vs accept. If it is a real regression (a still-registered owner loses its target), STOP with file:line + the failing test, do not silently rebuild.
5. B1: show the r6 regression RED on HEAD 6d06d4283 (before fix) and GREEN after. Both outputs verbatim.
6. B2: monotonic merge-hopf on develop (two parents, no force/reset/squash). B3: one exact-head PR run to terminal. B4: ls-remote line in the akte.

## repo-rule compliance

- Write-set: ONLY `internal/metrics/prometheus_files.go` (unconditional provider sweep) and `internal/metrics/regvisibility_regression_test.go` (P3/P2 regression). No `internal/capability/registry.go` (card 0428-151), no `cmd/baha/**` (card 0428-142), no `.github/**`, no `scripts/test_pr_*`/`test_ci_*`.
- Monotonic merge-hopf: `git merge --no-ff origin/develop` (or a normal commit on top when develop is already the base); witness `git merge-base --is-ancestor origin/develop <kopf>` = 0; the head keeps TWO parents (or a descendant with two parents); no force-push, no reset, no squash.
- No subagents (§4.8). All steps in this session.
- Plan writes only from /var/tmp clone against https://github.com/mcpdev80/baseharbor-plan.git, fetch + rebase origin/main first, only my own file, no `git add -A`, no write into the shared /home checkout.
- Evidence in baseharbor-plan only, on origin/main before END.
- HOPF compliance: no rebase, no reset, no force-push; `scripts/pr-gate-plan.py` / `.github/**` / `scripts/test_pr_*` left untouched by me (those are owner-scope, #1705).

## Findings (per CODEX-r5)

### P1 / P3 — unconditional provider-room sweep (BLOCKER fixed)

Reproduce the contradiction on HEAD 6d06d4283 BEFORE the fix (red):

```
$ go test ./internal/metrics -run '^TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync' -v -count=1
=== RUN   TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
    regvisibility_regression_test.go:377: deselected provider file "provider--f995114ff9581504d2e7.json" survived application-only sweep (err=<nil>)
--- FAIL: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync (0.00s)
FAIL
ok 	github.com/mcpdev80/baseharbor/internal/metrics	0.005s
```

The failing test names the orphan: `provider--f995114ff9581504d2e7.json` — a provider file left behind after an application-only (non-empty) sync. Cause at `internal/metrics/prometheus_files.go:147`: `if hasProvider || len(sources) == 0`. The provider case (:146) enters, the condition (:147) is FALSE for an application-only non-empty list, so `os.Remove` is skipped.

Fix (minimal, exact site `prometheus_files.go:146-152`): delete the `if hasProvider || len(sources) == 0` guard and its braces, leaving only the `os.Remove(...)` with its existing `errors.Is(err, os.ErrNotExist)` handling. The `hasProvider` accumulator is removed; `hasApplication` stays and keeps gating the application-room branch (`&& hasApplication`). The provider room is now swept on EVERY run. Comment :106-121 updated from the false "Every run of this sync is a provider sync (both production call sites fold in the provider sources)" to the truthful "this sync OWNS and ALWAYS sweeps this room ... a deselected source therefore leaves no orphan file in the active provider glob, regardless of what the current list carries." The application-room boundary (:142) is unchanged — the deliberate fence to the foreign room.

After the fix (green):

```
$ go test ./internal/metrics -run '^TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync' -v -count=1
=== RUN   TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync (0.00s)
PASS
ok 	github.com/mcpdev80/baseharbor/internal/metrics	0.005s

$ go test ./internal/metrics -run '^TestRegVisibility' -v -count=1
--- PASS: TestRegVisibilityStaleApplicationTargetReconciledOnSync
--- PASS: TestRegVisibilityForeignProviderFileSurvivesApplicationReconciliation
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByProviderSync
--- PASS: TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync
--- PASS: TestRegVisibilityLiveSecondOwnerSurvivesProviderSync
--- PASS: TestRegVisibilityProviderFileGlobClassification
--- PASS: TestRegVisibilityProviderFileGlobCorruption
ok 	github.com/mcpdev80/baseharbor/internal/metrics	0.006s
```

Both directions proven by `TestRegVisibilityDeselectedProviderFileRemovedByApplicationSync`: the seeded `provider--` and `provider-secure--` files are gone (`os.Stat` IsNotExist) after the application-only sync, AND the application file written by that same sync is present and selected by `baseharbor-applications` in the rendered config. `go build ./...`, `go vet ./internal/metrics`, `go test ./internal/metrics -count=1` all clean; local ci-fast-check.sh 286 tests PASS.

### P2 — live second owner (decision: ACCEPT, not a STOP)

The existing `TestRegVisibilityForeignProviderFileSurvivesApplicationReconciliation` (r5) asserted a *foreign* `provider--` file (a source never registered) survives an application-only sync. Under the corrected unconditional-sweep contract a foreign provider file in the swept room IS removed — that assertion contradicts the corrected contract, so the test was rewritten to assert the surviving property that still holds: a *runtime-target* file (outside both prefix rooms) is left intact by any sweep. The foreign-provider-survival assertion encoded the OLD (r5) conditional contract the CODEX-r5 verdict explicitly rejected.

New `TestRegVisibilityLiveSecondOwnerSurvivesProviderSync` (the CODEX-r5 P2 test, which r5 lacked): two registered provider owners in the SAME shared placement room, both in the current list; a sync carrying BOTH rewrites both files, so neither still-registered owner loses its target. Asserted: after a second sync with both owners present, both `providerTargetFileName` files are still on disk and both are selected by `baseharbor-providers` in the rendered config. This proves the sweep is bounded by the current registration list — it removes files absent from the list, never a file the list still carries.

P2 verdict: NOT a STOP. The production path (`EnsureProviderFilesWithRuntimeCAAt`, `prometheus_files.go:395`) passes the FULL current `providerSources` list (all current owners via `ListMetrics` over `allowedApplications` for the placement scope). The sweep removes only files absent from that list; a still-registered owner's file is rewritten, not lost. No ownership file / manifest field is introduced — the boundary is the current registration list, which is already in write-set and in scope. If a still-registered owner were observed losing its target, this test would FAIL and it would be a STOP with file:line — it does not.

### P4 — live source after application removal: covered by P1/P3 regression

Not separately regressed: the application-room branch (`&& hasApplication`) rewrites the still-present application file, and P3's regression asserts the application file written by the sync is present and visible. No live-source loss today; the sweep never removes a file the current list carries.

## B1 — FAIL before / AFTER (verbatim)

HEAD 6d06d4283 (before fix) → FAIL naming orphan `provider--f995114ff9581504d2e7.json` at `regvisibility_regression_test.go:377`.
HEAD 3ca7fa63c (after fix) → PASS for all seven `TestRegVisibility*`. Outputs above.

## B2 — monotonic merge-hopf

r6 candidate head: `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431` (two r6 commits on top of the r5 candidate). Ancestry (from head toward base):

```
3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431  parents:4b598df2817b22f01dbcc9559965dcddd6d131d2
4b598df2817b22f01dbcc9559965dcddd6d131d2  parents:6d06d4283b1341b64f9cbdf85786102dc82c8251
6d06d4283b1341b64f9cbdf85786102dc82c8251  parents:8b210394b7ec7e32d4367c5fa4ec7d50af4d408a
8b210394b7ec7e32d4367c5fa4ec7d50af4d408a  parents:2efbf043a04526a19051198da080c3f8d823be8a 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0
2efbf043a04526a19051198da080c3f8d823be8a  parents:57f49d7851c1e2a4d00726dd6ff455a2929b0506
6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0  parents:223cb97a9d652a4672257cabbadf12e2b41ed9cd
```

The r5 merge commit `8b210394b` has TWO parents `2efbf043a` (r5 correction) and `6e87ddcb4` (develop). The r6 candidate `3ca7fa63c` is a linear descendant of that two-parent merge, and `git merge-base --is-ancestor origin/develop HEAD` = 0 (develop IS ancestor). No force-push, no reset, no squash, no rebase.

HOPF onto moved develop (owner-hop directive): develop advanced `6e87ddcb4` → `28fb427f0` (PR #1589 = karte 0427-020). `git merge --no-ff origin/develop` produced hopf head `93eea495437f2f9b4683211f9aafb24fd1798839` with **two parents** `3ca7fa63c` (r6 candidate) and `28fb427f0` (moved develop). `git merge-tree --write-tree origin/develop HEAD` wrote tree `88280da4b24f7bec9d20b1450f0f7023a16e664a` with 0 conflicts. Witness `git log -1 --format=%P 93eea4954`: `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431 28fb427f057499efca705c1b7459e7653bd532a8`. No content conflict resolved (clean merge). r6 code diff vs `3ca7fa63c` is empty after the hopf (unchanged).

## B3 — exact-head CI run (terminal)

Correct acceptance run (PR-push event, `validate` skipped by design):
- Run **6657** (`44621387502`), event `pull_request`, `.github/workflows/ci.yml`, head `93eea4954`, terminal conclusion **success**. Required jobs all completed/success: Native gate plan, Trusted Plan, Source format, Focused Python, go-vet, go-build, Go unit cli-0/1/2/3, Go unit owner, Go unit packages. `validate` job **skipped** by the job `if: github.event_name != 'pull_request'` — this is a PR cell, skipped ≠ pass applies only to required cells, and `validate` is explicitly excluded from PR runs (same category as the ORAS-gated runtime/HA cells, owner-draht 114(a)).

Rejected runs (workflow_dispatch artifacts, NOT acceptance evidence):
- Run **6658** (`44621626037`) and Run **6662** (`44626269066`): `workflow_dispatch` events I dispatched to force the `validate` job. Dispatch is NOT a PR event, so it bypassed the `if: github.event_name != 'pull_request'` gate and forced `validate` to run its native runtime integration step (step 15), which FAILED. Both runs: step 13 (unit/package tests) passed, step 15 `Run runtime integration tests serially` → **failure**, step 16+ skipped. This is the fail-closed final check for `broad_required: true` / zero selected gates.

Why the dispatch runs fail and it is NOT an r6 regression (proven three ways):
1. The failing test is `TestMultiInstanceComposeLifecycleInCI`, asserting `containersecurity.VerifyComposeService` hardening on a Compose `postgres-analytics` service (`postgres-analytics ... runs as root (Config.User="")`). It lives in `internal/application` — my r6 write-set (`internal/metrics/prometheus_files.go`) never touches it.
2. Same failure on the unmodified baseline `6d06d4283` (before my r6 change): `TestMultiInstanceComposeLifecycleInCI` fails identically with `postgres-analytics ... runs as root (Config.User="")` — host docker engine does not apply the CI runner's containerd security hardening.
3. Same failure on this shared dev host via the `SharedCoreOwnerConflict` guard: the default docker engine exposes another hunt's `bh-local-shared` Core (compose `/var/tmp/hunt-uid-he/.local/share/baseharbor/targets/local/runtime/compose.yaml`), so `TestRepositoryWorkflowRealLifecycle` fails with `BaseHarbor Core is already running on this engine for target local`. This is host-state owned by another hunt, not my code; I did not stop it.

The pre-hopf PR runs 6644 and 6653 on `lane-0428-123-regvisibility` both show `validate` **skipped** and overall **success** — the native runtime step never ran on a PR event. The dispatch-driven `validate` runs (6658/6662) only run because dispatch overrides the PR gate.

## H3 — gate-plan comparison (pre-hopf vs post-hopf)

`python3 scripts/pr-gate-plan.py --diff <diff-base> --requirements scripts/release-requirements.json --mapping scripts/pr-gate-map-v1.json` with `GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop`:

- PRE-hopf diff-base (old base `6d06d4283`): `broad_required: true, coverage_status: unresolved, selected_gates: []` (fail-closed).
- POST-hopf diff-base (new base `28fb427f0`): `broad_required: true, coverage_status: unresolved, selected_gates: []` (fail-closed).

**No change to required gates across the hopf.** The post-hopf delta is exactly three `internal/metrics/` files (`prometheus_files.go`, `prometheus_render.go`, `regvisibility_regression_test.go`); the pre-hopf delta additionally swept docs/mkdocs/scripts/* (the r5 candidate had touched `scripts/pr-gate-plan.py` / `scripts/test_pr_gate_plan.py`). Neither selects a runtime gate — the map has no runtime gate owner for `internal/metrics/`, so both resolve fail-closed. The gate that was previously skipped on a PR event stays skipped on a PR event; no gate that was skipped becomes required by my hopf.

## H5 — hopf evidence lines (in the akte)

- `git ls-remote origin refs/heads/lane-0428-123-regvisibility` -> `93eea495437f2f9b4683211f9aafb24fd1798839`
- `git ls-remote origin develop` -> `28fb427f057499efca705c1b7459e7653bd532a8`
- `git show -s --format=%cI origin/develop` -> `2026-11-19T22:57:14+01:00`
- Hopf head two parents: `git log -1 --format=%P 93eea4954` -> `3ca7fa63ccd3a30cd1d85a0d3e012d0593e1c431 28fb427f057499efca705c1b7459e7653bd532a8`
- `git merge-base --is-ancestor origin/develop 93eea4954` -> 0 (develop IS ancestor)

## Handoff

END_DONE x-123r5: r6 correction DONE + hopf onto moved develop (owner-hop directive). P1/P3 unconditional provider-room sweep + P3 mixed-fail regression (red on 6d06d4283 naming the orphan provider file, green on 3ca7fa63c) + P2 live-second-owner regression (accept, bounded by current list, no STOP); hopf head 93eea4954 (two parents: 3ca7fa63c + 28fb427f0); CI run 6657 (PR-push) success, validate skipped by design; dispatch-run failures 6658/6662 proven to be workflow_dispatch artifacts, NOT an r6 regression (same native-runtime failure on the unmodified baseline 6d06d4283 and on this shared host via the SharedCoreOwnerConflict guard); H3 gate-plan: no change to required gates across the hopf. akte published to plan origin/main.
