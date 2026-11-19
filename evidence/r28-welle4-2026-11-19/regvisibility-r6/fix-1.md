# 0428-123 / PR #1693 — regvisibility r6 correction

Date: 2026-11-19
Worker: ornith rotation lane (takeover c5d271cb, §3.6)
Base: develop `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
Candidate base before r6: `6d06d4283b1341b64f9cbdf85786102dc82c8251`
Exact head after r6: TBD (monotonic merge-hopf on develop)
PR: mcpdev80/baseharbor#1693, draft=false, base 6e87ddcb4
Review basis: CODEX-REVIEW r5 `baseharbor-plan/evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-r5.md` (read verbatim)

Scope: r6 correction of the already-decided r5 candidate — P1/P3 (unconditional provider-room sweep + mix-fail regression), P2 (live-second-owner). No new design variant. §4.2: change exactly P1/P2/P3, nothing beside.

## Remote witnesses (§4.1)

- `git ls-remote origin heads/lane-0428-123-regvisibility` -> `6d06d4283b1341b64f9cbdf85786102dc82c8251` (r5 candidate head)
- `git ls-remote origin develop` -> `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
- `git ls-remote origin refs/pulls/1693` -> head `6d06d4283`, base `6e87ddcb4`, draft=false, merged=false, mergeable=true (GitHub API)
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

## CLEANLINESS

containers: none started (no docker/podman run this shift)
networks: none
volumes: none
state: n/a
cleanliness: clean — no test containers/networks/volumes/state created this shift
