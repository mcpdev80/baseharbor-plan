# H-V58 run-state ledger — all open core PRs + demo #178/#179

Lane: w225-0428-216-huntv58 (pure Befundung; no PR/run actions, no cards, read-only).
Snapshot taken: 2026-11-25 evening (UTC), re-checked at akte write time.
Tooling: `gh api` against https://github.com/mcpdev80/{baseharbor,baseharbor-plan,baseharbor-demo,baseharbor-console,baseharbor-node-connector}.

## ANSATZ (identity block)

- Card: bug-hunt slice H-V58, mission `coordinator/missions/w225-huntV58-runledger.txt`. No per-card frontmatter owner exists for hunt slices; lane identity from the mission: `w225-0428-216-huntv58`.
- git user.name: `w225-0428-216-huntv58`
- git user.email: `w225-0428-216-huntv58@baseharbor.local`
- Invocation: `git -c user.name=w225-0428-216-huntv58 -c user.email=w225-0428-216-huntv58@baseharbor.local commit -m ...`
- Pre-push gate: `git show -s --format=%an HEAD` must print `w225-0428-216-huntv58`; on mismatch: STOP + report.
- Plan repo remote witness (per wrong-zone rule):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
  → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` (and push) — real planning repo confirmed. This akte lives in isolated worktree `workers/w225-plan` cut from `origin/main` @ `6b61a0e8c`.

## PLAN

1. Verify plan repo remote + origin/main freshness.
2. Census open PRs: core `pulls?state=open`, plus demo; sweep console/node-connector/other repos.
3. Per PR: head sha, base ref, compare ahead/behind/files vs current develop tip.
4. Per PR: every pull_request run on the exact head (id, status, conclusion, job census executed-vs-skipped, per_page=100).
5. Classify per two-greens rule: QUALIFIES / NEEDS-SECOND / VOID-BASE / VOID-SKIP.
6. Cross-check VOID-witness mentions in coordinator/PROTOCOL.md for completeness.
7. Publish this akte via plan-PR flow from isolated worktree, with ls-tree witness.
8. END post.

## Base heads used

- core develop tip: `fcd449117e189c555c7530b9527cd22d3f6f25ff` (= merge commit of #1852, merged 21:23:47Z)
- demo develop tip: `5ca92a7cd2f746934890cfd7096a48068bdf218e` (= merge commit of demo #177)
- PRs created before 21:23:47Z cannot contain the current base tip on their branch; greens older than it are stale-by-base (VOID-BASE pattern).

## Rule definitions used for classification

- QUALIFIES — two distinct `pull_request` runs on the exact current head, both terminal SUCCESS with required gates executed (aggregate `PR Selected Checks` = success, non-empty job census; a SUCCESS with all gates skipped is VOID-SKIP, precedent PROTOCOL.md:1314 "Trusted Plan = SKIPPED on both dispatch runs -> greens VOID").
- NEEDS-SECOND — exactly one qualifying `pull_request` SUCCESS on the current head.
- VOID-BASE — branch does not contain the current develop tip (base-ancestry fail; mergeState BEHIND); older greens do not count for acceptance (PROTOCOL.md:1192 "BEHIND, old-base greens VOID").
- VOID-SKIP — a run whose selected gates were skipped/cancelled, a run on a superseded head, or a push/dispatch run not on the exact PR head.
- two-greens doctrine: PROTOCOL.md:1050/1094/1111 (two same-head full PR-event greens required at acceptance).

## Ledger — core repo (mcpdev80/baseharbor), 11 open PRs

All pull_request runs found on each exact head, with job census (executed/skipped of completed runs; per_page=100):

| PR | head (current) | base | ahead/behind/files vs fcd44911 | pull_request runs on exact head | classification |
| --- | --- | --- | --- | --- | --- |
| 1853 | 030e584893 | develop | 4/4/7 | 45699482849 completed/failure (32 jobs: 11 exec / 21 skip; reds: PR Selected Checks, Validation·ci-executor-tests, Focused Python) | VOID-BASE + terminal RED |
| 1851 | f89f506f50 (carrier branch) | develop | 2/17/0 | 45683813229 completed/failure (29 jobs: 5 exec / 24 skip; Trusted Plan RED "no independently executable PR validation checks") | VOID-BASE + terminal RED |
| 1850 | 6b153b8da1 (MOVED mid-census from e4e3e050bed) | develop | re-cut onto fcd44911 (carrier #1852 merged) | on e4e3e050bed: 45678903831 completed/failure (Trusted Plan red: uncataloged runtime_identity_workload sources), 45677961079 all-skipped SUCCESS; on 6b153b8da1: 45707597763 cancelled (VOID), 45707682812 in_progress at snapshot (21 exec / 16 skip / 2 running) | GREENS-IN-FLIGHT (old-head greens VOID-SKIP/VOID-BASE) |
| 1842 | 48bac372f9 | develop | 5/16/5 | 45666678375 completed/success (39 jobs: 19 exec / 20 skip; Selected Checks success) | NEEDS-SECOND + stale base (behind 16) |
| 1835 | 41cda5f9ff | develop | 10/4/0 | 45698449498 completed/failure (29 jobs: 5 exec / 24 skip; Trusted Plan RED "no independently executable PR validation checks") | VOID-BASE pattern + terminal RED |
| 1833 | a7b0a48048 | develop | 6/28/3 | 45513816046 completed/success (35 jobs: 18 exec / 17 skip; Selected Checks success) | NEEDS-SECOND + stale base (behind 28) |
| 1820 | 34142a2a0a | develop | 5/4/0 | 45698338888 completed/failure (29 jobs: 5 exec / 24 skip; Trusted Plan RED "no independently executable PR validation checks") | VOID-BASE pattern + terminal RED |
| 1819 | b3c5055ad2 | develop | 11/4/4 | 45694363486 completed/success (40 jobs: 24 exec / 16 skip), 45699760220 completed/success (40 jobs: 24 exec / 16 skip); both Selected Checks success | NEEDS-SECOND + stale base (behind 4 after #1852; greens were on tip 63f4609) — see defect D1 |
| 1818 | 20fc1cb7d4 | develop | 4/40/8 | 45316544436 completed/success (40 jobs: 23 exec / 17 skip) | VOID-BASE (stale: created 2026-11-24, base fcd44911 cannot be in branch) |
| 1812 | f166a49f26 | develop | 8/4/1 | 45698501695 completed/success (33 jobs: 12 exec / 21 skip), 45701927620 completed/success (33 jobs: 12 exec / 21 skip); both Selected Checks success | NEEDS-SECOND + stale base (behind 4 after #1852) — thin-execution caveat D3 |
| 1650 | 1c33e91007 | develop | 9/16/4 | 45663047993 completed/success (43 jobs: 27 exec / 16 skip; Trusted Plan success on head) | NEEDS-SECOND + stale base (behind 16) |

Notes:
- `PR · Trusted Plan` red on 1820/1835/1851 is identical: `ValueError: no independently executable PR validation checks`; on 1850 (old head) it was uncataloged-source coverage (`internal/application/runtime_identity_workload*.go` rows) — resolved on develop by carrier #1852 (merged, catalog-only).
- PR 1853 red detail: `test_planner_validation_route_includes_planner_and_coverage_suites` AssertionError (ci_check_routes lists differ) in `PR · Validation · ci-executor-tests` + `PR · Focused Python`.
- Non-PR-event witnesses on census range (first core run id 41842672092, 406 pull_request runs scanned): 45700681346 SUCCESS belongs to run-name "CI · PR #1854" whose head 3247864c66 is NOT #1854's real PR head 903991f3b8 (PR #1854 is MERGED) — mislabeled/dispatch-named run, not a witness for any open PR.
- #1852 (carrier, MERGED fcd44911) head d3db4d898: superseded by the merge; run 45700681346 above.
- PR 1650 conflict with PROTOCOL.md:1247 (20fc1cb7 "contaminated ... VOID", canonical 8e2c50c1) applies to #1818 below, not 1650.

## Ledger — demo repo (mcpdev80/baseharbor-demo)

| PR | state | head | base | ahead/behind/files vs 5ca92a7cd | pull_request runs on exact head | classification |
| --- | --- | --- | --- | --- | --- | --- |
| 179 | OPEN draft | cda6aa70e8 | develop | 0/4/3 | ZERO pull_request runs (only 45688177820 push-event pr-config-matrix.yml failure — VOID witness kind) | NO-RUN-YET (trigger gap) |
| 170 | OPEN draft | b086cf58bb | develop | (created 2026-11-24, base stale) | ZERO pull_request runs (only 45663390190 push-event failure — PROTOCOL.md:1348 void-listed) | VOID-BASE + NO-RUN-YET |
| 178 | CLOSED unmerged 2026-11-25T19:45:14Z | 99fdb64f43 | develop | — | ZERO pull_request runs (only 45685104924 push-event failure) | n/a — superseded by #179 (opened 2 s after close, same title) |

## Demo pull_request workflow census finding

`pull_request`-event runs in demo exist ONLY on branch names `w198-0428-284-demo-parser` (45646543061, 45648782687) — i.e. while PR #176 (merged 6371ca55) still carried that branch and the sibling #178/#179 lifecycle. For BOTH currently-open demo PRs (#179 head cda6aa70 and #170 head b086cf58/b086cf58-era and 9acd0c56) only push-event runs of `.github/workflows/pr-config-matrix.yml` exist, and those all complete FAILURE with 0 counted PR-gate jobs. Root-cause lead (not edited, Owner scope): the `pull_request` trigger on pr-config-matrix.yml appears effective only for branches whose PR context matched at trigger creation; per PROTOCOL.md:1348/1357 the coordinator already ordered an additive empty-commit synchronize workaround — no such event run materialized on either open head. This matches the mission's `STATE` reporting duty: check name `pr-config-matrix (pull_request)`, failing line: run absent (0 workflow_runs with event=pull_request for head sha).

## Classification summary

- QUALIFIES (two greens on a CURRENT base): NONE in the open set at akte write time. #1819 and #1812 each had two greens on the then-tip 63f4609 but #1852 merged after them (behind=4).
- NEEDS-SECOND + stale base: #1842 (45666678375), #1833 (45513816046), #1650 (45663047993) behind 16/28/16; #1819 (45694363486 + 45699760220) and #1812 (45698501695 + 45701927620) behind 4. Per strict doctrine all five need a base-hop + two fresh same-head greens, not merely a second run.
- VOID-BASE: #1818 (single green on 2026-11-24 base), #1853, #1851, #1835, #1820 (all red AND behind base at snapshot), #170 (demo).
- VOID-SKIP examples in-census: #1850 old-head 45677961079 (Selected Checks conclusion=skipped in a top-level SUCCESS), #1850 45707597763 (cancelled).
- GREENS-IN-FLIGHT: #1850 (45707682812 in_progress at snapshot on the corrected head 6b153b8da1).
- NO-RUN-YET: demo #179.

## PROTOCOL.md VOID-witness cross-check

Named run IDs in coordinator/PROTOCOL.md VOID/cancel context vs live API (all core unless marked):

| run id | PROTOCOL claim | live truth | verdict |
| --- | --- | --- | --- |
| 45452717131 | void-registered (line 801) | completed/success PR run #1826 @22e101ce | void = stale-by-base, consistent |
| 45428812940, 45438096326, 45440440221 | void-listed for #1812 (line 897) | (older heads of #1812) | consistent with superseded-head rule |
| 45505198117 | void-added (line 933) | completed/failure CI·PR #1812 @3859d466 | consistent |
| 45504224635 | VOID wrong-gates (line 931) | Pre-Release dispatch completed/failure @2ea41620 | consistent |
| 45522275641 | void-stale (line 982) | completed/cancelled PR #1832 @67a1eb3a | consistent |
| 45461617246 | phantom (line 835) | not resolvable check; superseded @22e101ce era | unverified (no live claim needed) |
| 45465811271, 45465885966, 45452743772 | VOID superseded bases (line 860) | success/success/success (20830c81/22e101ce) | consistent (green but superseded) |
| 45473575858 | VOID (line 866) | completed/cancelled PR #1826 @0d8b9c61 | consistent |
| 45476058997 | VOID (line 876) | completed/cancelled PR #1832 @3d5330f | consistent |
| 45636081059 | VOID added (line 1260) | completed/cancelled dispatch @903991f3 | consistent |
| 45616699580 | VOID wrong-target demo (line 1186) | 404 in BOTH core and demo run APIs | run unreadable (deleted/inaccessible) — be found |
| 45661078349 | VOID witness demo #170 (line 1348) | demo push-event completed/failure | consistent |
| 45619615511, 45619474538 | VOID pre-merge (line 1193) | dispatch failure/failure | consistent |
| 45627034676 | failed dispatch (line 1260) | Pre-Release dispatch failure @50c6d84e | consistent |
| 45631228584 | Selected-Checks PASS but not accepted (line 1260) | completed/success PR #1842 @50c6d84e | consistent (head superseded by 48bac372) |
| 45570397690 | Leg-B id (line 1004) | 404 in core API; 45570395768 = Pre-Release dispatch success | be found: one leg-B id unreadable |
| 45571397690, 45572854473 | VOID cancelled (lines 1004/1012) | both dispatch completed/cancelled @55d17d43 | consistent |
| 45573394850 | dispatch #1833 (line 1012) | Pre-Release v0.4.28 dispatch completed/failure @a7b0a480 | consistent |
| 45571699415 | (same a7b0a480) | push-event Pre-Release failure | not in PROTOCOL VOID list — be found: omission below |
| 45619972563, 45620233713 | qualifying pair #1844 (line 1199) | both PR-event success @54a879b0 | consistent (PR since merged 99d9dde) |
| 45675267908 / 45663933016 | #1846 hop/supersede (line 1409) | success / cancelled @04921de8 | consistent (PR #1846 not open anymore in census) |

Completeness findings (gap list):
- VOID-CLASS RUNS ON CURRENT OPEN HEADS ABSENT FROM PROTOCOL.md: #1818 green 45316544436 is implicitly void via the "derived greens VOID" clause (line 1247) but the run ID itself is nowhere listed; the #1833-era push/dispatch runs 45571699415 (push failure on a7b0a480) and 45698338888/45698449498/45683813229/45699482849 (current red PR runs, terminal failure) are correctly NOT void-listed (red, not voided green).
- All greens on now-stale bases (#1842 45666678375 before #1852, #1650 45663047993 before #1852, #1833 45513816046) became VOID-BASE at fcd44911 merge (21:23:47Z) and are not yet listed anywhere in PROTOCOL.md — be found: the void-witness list lags the #1852 merge.
- Two cited run IDs (45616699580, 45570397690) return 404 on the API — likely deleted dispatch runs; their void claims are unverifiable and should be marked as such.

## Ledger defects (be found)

- D1: base-timing race on #1819: both greens (45694363486 + 45699760220) executed while 63f4609 was develop tip, then #1852 merged at 21:23:47Z and the same head became behind=4. Whether these two greens still satisfy the two-greens rule is a classification decision for Codex/Owner, not for this hunt — the ledger records both readings (QUALIFIES-at-run-time vs VOID-BASE-now) with the merge timestamps. PROTOCOL.md:1247/1050 chain-gates #1819 behind #1812 acceptance anyway.
- D2: same race, #1812's pair (45698501695 + 45701927620), the second one finishing 21:13Z, minutes before fcd44911. Ledger net: at akte write time NO open PR has two greens on the CURRENT base.
- D3: #1812 executed only 12 of 33 jobs per run (heavy gates skipped per policy) — thin evidence; per PROTOCOL precedent (line 1012: CANCELLED with shards cut = VOID both ways) a SUCCESS with big skip census deserves an executed-job manifest check before acceptance. Not void per rule (aggregate success), flagged for reviewer.
- D4: #1850 head moved twice during this census (e4e3e050bed → 6b153b8da1) driven by #1852 carrier merge — any earlier per-head statements in flight are already stale; run 45707682812 was still in_progress when this akte was written.
- D5: demo #179 (open, draft) has NO pull_request run of any kind on its head; its whole evidence base is one push-event failure. Same trigger gap already logged for #170 (PROTOCOL.md:1348) — now reproducible on a second branch, so the gap is workflow-wide (`.github/workflows/pr-config-matrix.yml` trigger), not branch-specific.
- D6: run-name "CI · PR #1854" on head 3247864c66 (SUCCESS, 21:0xZ) while #1854's actual head is 903991f3b8 — a dispatch-run named after a PR whose head does not match; do not count for #1854 or any open PR.

## cleanliness

- Read-only desk: no containers, no compose, no writes to product repos, no PR/run actions (zero pushes, zero reruns, zero cancels, zero comments). `docker ps -a` untouched (no docker use).
- Working artifacts kept under /tmp/opencode/w225-huntv58 (census zips/tsvs).

## witnesses

- open-PR census: `gh api repos/mcpdev80/baseharbor/pulls?state=open&per_page=100` (11 rows above); demo `pulls?state=open` (#179, #170); console/node-connector/districenter/hawser/container-manager/managment-plan: zero open PRs.
- compares: `gh api repos/.../compare/<base-tip>...<head>` per row.
- runs: `gh api repos/.../actions/runs?head_sha=<head>&event=pull_request` + first-page 406-row pull_request census of core (page scan from 41842672092).
- job census: `gh api repos/.../actions/runs/<id>/jobs?per_page=100`.
- aggregate: `.../check-runs?check_name=PR Selected Checks` per head (conclusions table above).
- log witnesses: Trusted Plan ValueError lines from job logs (139433831371, 139450992437, 139501551081, 139510287605), 1853 reds from jobs 139505586492/139505586177.

## Publishing + ls-tree witness

Candidate commit: `9a8b3af7686a7dca5b25354e279c69220ad0f9c4` (author gate `git show -s --format=%an HEAD` → `w225-0428-216-huntv58`).
Base: origin/main tip at worktree creation `6b61a0e8c`, rebased cleanly onto `48ec76bea` before push (only own commit in `git log origin/main..HEAD`).

Second-to-last action, exact output:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/hunt-v58
evidence/hunt-v58/2026-11-25/h-v58-run-ledger.md
```

## END marker

END_DONE w225-0428-216-huntv58: H-V58 run-state ledger published at 9a8b3af76 (14 PR rows classified; VOID-witness cross-check + 6 ledger defects D1–D6). Read-only throughout; no PR/run actions.
