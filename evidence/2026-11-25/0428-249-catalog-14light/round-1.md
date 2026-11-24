# 0428-249 — Catalog PR: 14 atomic docker/podman gates required for v0.4.28 (lane w128)

Mission: coordinator/missions/w139-catalog-14light.txt (owner-approved separate catalog PR;
approval recorded in coordinator PROTOCOL + card 0428-249). GO confirmed by owner 2026-11-25.
Prior #1834 track (card 0428-286) closed-superseded; this lane does not merge.

## PLAN

- read mission; base worktree on develop tip (SHA reported below)
- add EXACTLY the 14 approved gate IDs to required_for v0.4.28 in scripts/release-requirements.json
- verify nothing added to v0.4.27 (count stays 62), no other files, no policy change
- minimal expectation update of the existing required-ID-set test (named below)
- focused local python unittest prechecks (data/planning only, not a test suite run)
- normal push, PR open, Hosted CI watched to terminal on exact head (two run IDs below)
- END_DONE with head + run IDs + the 14-ID list (no merge; separate Codex reviews)

## Facts

- Base develop tip: 9d7e22902f368c78f489021432c8112eb54cb74e (ls-remote verified).
- Branch: lane-0428-249-catalog-14light, head d57a8253b478f461e616d5058c42331d50c4662e (ls-remote verified).
- PR: https://github.com/mcpdev80/baseharbor/pull/1837 (separate catalog PR, not tied to a card PR).
- Diff is exactly 2 files: scripts/release-requirements.json (+14 `"v0.4.28"` tags, no other
  change; diffstat: 14 lines each side, all the same pattern), scripts/test_pre_release_check_plan.py
  (expectation update).
- The 14 IDs (each gains required_for v0.4.28 only; all keep v0.4.27 untouched):
  atomic/docker/guided, atomic/docker/lifecycle, atomic/docker/policy, atomic/docker/connectivity,
  atomic/docker/reconciliation, atomic/docker/failure, atomic/docker/full-destroy,
  atomic/podman/guided, atomic/podman/lifecycle, atomic/podman/policy, atomic/podman/connectivity,
  atomic/podman/reconciliation, atomic/podman/failure, atomic/podman/full-destroy.
- Post-change v0.4.28 required set = the 14 above + atomic/static/ci-fast-check + atomic/static/mcp
  (pre-existing; not added by this PR). v0.4.27 count = 62 (unchanged).

## Existing-green-test audit / expectation update

- The ONLY existing test that asserts the v0.4.28 required-ID set is
  scripts/test_pre_release_check_plan.py :: test_v0428_adds_only_fast_check_and_moves_no_other_gate
  (asserted v0428 == {ci-fast-check, mcp}; card 0428-208/#1746 decision). Updated minimally:
  the expected set now names the 14 approved additions alongside; comment records the 0428-249
  authorization. Named in the PR body per mission.
- test_ci_v0427_gate_catalog.py asserts per-gate v0.4.27 membership only — unaffected (v0.4.27
  set unchanged; passes). No other test asserts the v0.4.28 ID set (grep over scripts/test_*).

## Local prechecks (non-test-suite; read-only planning)

- python3 -m unittest: test_pre_release_check_plan, test_ci_v0427_gate_catalog,
  test_pr_gate_coverage, test_pre_release_runtime_reuse, test_pr_gate_dependencies,
  test_targeted_atomic_plan — all OK. (test_pr_gate_plan is slow/matrix-style; left to Hosted CI.)
- JSON validity + counts verified programmatically (14 tags added, 62 v0.4.27 preserved).
- Test execution authority remains Hosted CI (Owner rule 2026-11-24); the python checks above
  are the affected selectors' own unit assertions run pre-push as the mission's "minimal
  expectation update" verification, full CI is the acceptance path.

## Hosted CI (exact head d57a8253b478f461e616d5058c42331d50c4662e)

- Run A: 45511970224 attempt 1 (CI · Source & Quality, pull_request) — SUCCESS, watched to
  terminal by this lane (Eigenes-Run-Pflicht).
- Run B: 45511970224 attempt 2 (independent rerun of the same required workflow on the exact
  head, launched via `gh run rerun`) — SUCCESS, watched to terminal, including
  PR · Validation · pr-planner-tests and PR Selected Checks.
- Two exact-head runs green: https://github.com/mcpdev80/baseharbor/actions/runs/45511970224/attempts/1
  and .../attempts/2
- `gh pr checks 1837`: 0 failing/pending non-skipped checks (remainder skipped by path rules).
- PR merge-ref SHA e9ff7c05b9d5ad0d2ae0a7d2ba351a7851820a4e verified to contain head
  d57a8253b as ancestor (merge commit into 9d7e22902; no extra content diff).

## repo-rule compliance

- Files touched: only scripts/release-requirements.json and scripts/test_pre_release_check_plan.py
  (both explicitly in mission scope). No .github edits, no AGENTS/CLAUDE edits, no policy change.
- Normal branch push from develop tip; no force-push, no cherry-pick.
- No subagents (AGENTS §4.8). No merge (separate Codex lanes review+merge).
