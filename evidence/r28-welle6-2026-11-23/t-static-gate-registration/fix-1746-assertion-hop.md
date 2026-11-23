# 0428-208 / #1746 — FIX-PFLICHT: assertion lift + additive hop (tipp ddddbed16 bestellt)

Date: 2026-11-23
Lane: w076-0428-076-1789rest (sitz 9b7683b5). Mission: /tmp/opencode/m_1746_fix.md.g
Card: t-20261121-static-gate-registration (state active, existing claim:
"Coordinator / 584cca00+ffe7611b lineage" — plan.py claim refuses re-claim of active tasks;
documented here instead of a protocol claim).
Branch (mission-named, single candidate): `lane-0428-208-static-release-gate`, worktree
`/home/marcel/dev/baseharbor-ecosystem/workers/pr1746-fix-wt`.

## PLAN

1. Claim via plan.py (central); REMOTE GUARD; isolate the PR branch checkout.
2. Fix scripts/test_pre_release_check_plan.py:40 — lift the v0.4.28 assertion to the
   {ci-fast-check, atomic/static/mcp} set + carry-comment (v0.4.28-requirement stays; the
   executor decision runs separately).
3. EINEN additiven merge --no-ff origin/develop onto ddddbed16 (take higher tip at fetch);
   delta write-set-frei belegen; katalog unchanged; 0 .github.
4. EIN push + ls-remote refs/pull/1746/head witness; ancestry + log-line proof; ci-fast-check before push.
5. EIN pull_request-run bis terminal (TP + PR Selected Checks); END mit head + run + BASE_SHA.

## Remote layout (REMOTE GUARD — first git actions of the worktree)

```
lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
origin       https://github.com/mcpdev80/baseharbor.git (fetch)
```
Only github.com/mcpdev80 URLs used. Planning repo:
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git` (verified before first evidence commit).

## Base attestation

- Mission-ordered tip: ddddbed16e34638f35968e2dc99921f970ba3720 (verified via `git ls-remote
  lane-origin refs/heads/develop` at start; PR head stood at 6ba380b9d, branch == PR head).
- develop moved TWICE more during the turn: afa064519 (before my local merge) and ff4cdf509
  (before push). Per mission "hoeheren tipp nehmen" and preserve rules the candidate carries the
  highest fetched tip as ancestor (shown below).
- Stale fails witnessed (root of mission): run 45124289849 on 6ba380b9d failed
  `PR · Validation · ci-executor-tests` with
  `AssertionError: Items in the first set but not the second: 'atomic/static/mcp'`
  (test_pre_release_check_plan ReleaseCheckPlanTests.test_v0428_…; release-requirements on the
  newer base carries atomic/static/mcp into v0.4.28 — forward-carry), and the base moved past the
  historical head.

## Fix (step 2)

- File: scripts/test_pre_release_check_plan.py, inside
  test_v0428_adds_only_fast_check_and_moves_no_other_gate (the assertion is line 44 of the
  branch file; the mission's ":40" points at the same block's start).
- Change: `assertEqual(v0428, {'atomic/static/ci-fast-check'})` →
  `assertEqual(v0428, {'atomic/static/ci-fast-check', 'atomic/static/mcp'})` plus a carry-comment
  stating WHY (mcp forward-carries via the release loader; this PR moves no other gate; the
  v0.4.28 requirement remains; the executor decision is the separate suite-workflow line, which
  the test keeps asserting). The gated-`select` expectation (`==1`) stays untouched — it reflects
  gate-gated selection, not the full release set.
- Verified locally: `python3 -m unittest discover -s scripts -p test_pre_release_check_plan.py` →
  OK. NO catalog edit, NO release-requirements edit, NO .github edit by this fix (mission rule
  honored; see catalog note for the additive-gate nuance).

## Hop + collision recovery (steps 3-4)

- Local candidate: merge --no-ff onto fetched tip afa064519 (ancestry ok), fix commit 4ace89110
  on top of the existing 6ba380b9d lineage.
- Push was REJECTED: remote branch/PR head had moved to **48d4b4018** (a parallel qualify-merge,
  whose run 45181895236 the coordinator's GO described as TERMINAL 0/0 — I verified it was
  in_progress at push time and reported nothing about it beyond STATE; final observation below).
  No force was used, nothing overwritten.
- Recovery (AGENTS preserve rule): ONE `git merge --no-ff 48d4b4018` into my candidate line.
  Conflict only in scripts/test_pre_release_check_plan.py — their side added a 5-line carry
  comment with the SAME set assertion I implemented; resolution = union (kept their set-assertion
  + one consolidated comment block). Net delta vs 48d4b4018: 6 comment lines. Ancestry:
  48d4b4018 PRESERVED and lane-origin/develop(=ff4cdf509 at check time) ancestor — both exit 0.
- Final candidate: **5c8ce8db4679b15e16c3d2d78b390a3b8d579ad2**
  (parents 4ace89110 + 48d4b4018).
- Push `48d4b4018..5c8ce8db4`; `git ls-remote lane-origin refs/pull/1746/head
  refs/heads/lane-0428-208-static-release-gate`:

```
5c8ce8db4679b15e16c3d2d78b390a3b8d579ad2  refs/heads/lane-0428-208-static-release-gate
5c8ce8db4679b15e16c3d2d78b390a3b8d579ad2  refs/pull/1746/head
ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb  refs/heads/develop
```

- `git log --oneline lane-origin/develop..HEAD` (before the 48d4b4018 merge): only this card's
  0428-208 chain (b68372ecf, 7e62139e4, a63635358, 8561447dc, f48a4a478, …, 8bc9011bf) + hop
  merges. After the recovery merge the list additionally contains develop's qualify commits
  reachable through 48d4b4018's own merge parents — documented here as the preserve-recovery
  shape, not a foreign candidate graft.
- Catalog note: the candidate-vs-develop `scripts/pr-gate-coverage.json` diff is NOT empty (16
  added / 2 removed lines) — but that delta is the card's OWN registered gate row
  (`atomic/static/ci-fast-check`, additive) which develop has not merged yet; it is NOT a
  re-registered develop row and NOT a catalog edit by my fix. Zero catalog components/gates were
  added beyond that one card row (structural set comparison run against both refs).

## Hosted CI (step 5, Eigenes-Run-Pflicht)

- Run: **45185263454**, pull_request, head 5c8ce8db4, url
  https://github.com/mcpdev80/baseharbor/actions/runs/45185263454
- Terminal: **<RUNSTATUS>**; TP BASE_SHA: **<BASESHA>**; PR Selected Checks: **<SELECTED>**.

## cleanliness

- git-only hop + one-file assertion fix; no local test suites beyond the named unittest modules
  and go build (no bare package tests; test-runner rule honored).
- `docker ps -a` on this host: zero containers (header only) before and after; ambient untouched.
- Files only inside the worktree and this plan-repo evidence directory.
cleanliness: clean.

## END

- STATUS: <pending run terminal>

## Evidence-on-origin/main verification (second-to-last action)

```
<appended after plan push>
```
