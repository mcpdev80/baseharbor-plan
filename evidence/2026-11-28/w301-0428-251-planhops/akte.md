# w301-0428-251-planhops — forward-hop five plan PRs onto LIVE plan main + four content corrections

- Shift: 2026-11-28
- Card: 0428-251
- Mission: `coordinator/missions/w301-0428-251-planhops.txt`
- Lane canonical name (author + committer, set per commit): `w301-0428-251-planhops`, email `w301-0428-251-planhops@baseharbor.local`
- Commit invocation used everywhere: `git -c user.name=w301-0428-251-planhops -c user.email=w301-0428-251-planhops@baseharbor.local <cmd>`
- Pre-push identity gate printed after each commit: `git -C <wt> log --format='%h an=%an cn=%cn' -1`
- Planning repo (verified with `git remote -v` before first evidence commit): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, remote `origin` → `https://github.com/mcpdev80/baseharbor-plan.git`
- Isolated plan worktree (PLAN REPO IS A SHARED CHECKOUT rule — shared checkout left untouched): `/home/marcel/dev/baseharbor-ecosystem/workers/w301-0428-251-planhops-plan`, cut from `origin/main`
- No product mutation, no new cards, no direct push to plan main, no workflow file edited, no rerun/workflow_dispatch.

## VISIBLE INSATZ BLOCK (visible ANSATZ BLOCK required before first commit)

- Exact per-card frontmatter owner fetched from origin/main at runtime: see `## LIVE PR STATE` (each `gh pr view` prints `assignees`; owners below read from that + PR title lane).
- git user.name: `w301-0428-251-planhops`
- git user.email: `w301-0428-251-planhops@baseharbor.local`
- literal git -c commit invocation: `git -c user.name=w301-0428-251-planhops -c user.email=w301-0428-251-planhops@baseharbor.local commit`
- literal git -c merge invocation: `git -c user.name=w301-0428-251-planhops -c user.email=w301-0428-251-planhops@baseharbor.local merge origin/main`
- pre-push git show -s --format=%an gate line: `git log --format='%h an=%an cn=%cn' -1`

## BASE ATTESTATION (git ls-remote, before any hop)

- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` => `1b9b2bc70201d9da6615a9ec16942103c20e96a1`
- Isolated worktree cut from `origin/main` at `1b9b2bc70` (git worktree add origin/main). HEAD of worktree == `1b9b2bc70`.
- Each candidate's pre-hop ancestry vs live main: `git merge-base --is-ancestor origin/main <head>` => **FALSE** for all five (#73 #81 #84 #98 #99). This is the Codex w267 HOLD rationale (live main advanced past their heads). Each therefore needs exactly one forward merge commit onto the LIVE main.

## LIVE PR STATE (fetched at runtime, gh pr view --json)

- #73  head `9bd702d95f9e5d692391e48da4cc5ec51fc778a4`  state OPEN  mergeable UNKNOWN
- #81  head `2796ab3dd8c9c559fa9944587304e42b255d5950`  state OPEN  mergeable UNKNOWN
- #84  head `2660e6e2d99b615930fe1cad91d475a200b27fe4`  state OPEN  mergeable MERGEABLE
- #98  head `963f9bedca1399c6c33ddc78b79260d2aeb59354`  state OPEN  mergeable MERGEABLE
- #99  head `9771f4e02e119b44367836e555ff4877aac94556`  state OPEN  mergeable MERGEABLE
- Each head matches the mission's stated head exactly (verified via `gh pr view` + `git ls-remote pull/<n>/head`).

## CONTENT CORRECTIONS (forward-only; dated paragraph appended, never rewritten)

1. #73 — product PR #1650 was MERGED is WRONG.
   - Before (line 18 of `evidence/r28-welle6-2026-11-28/w265-0428-078-1818pre/akte.md`):
     `#1650 head: 37c4d847c … merged long ago (pre-date; not ancestor-checked).`
   - Live witness at correction time: `gh pr view 1650 --repo mcpdev80/baseharbor --json state,headRefOid` => `state=OPEN headRefOid=37c4d847ca377d1555163ac4791c8ba08b85de77`, title `fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in` = the contaminated-lineage AUDIT, not a merge.
   - Correction appended: dated paragraph stating #1650 is OPEN at `37c4d847c`, is the contaminated-lineage AUDIT, and was never merged to develop/main; live checked via gh on 2026-11-28.
2. #81 — provenance for the `w281-coordinator` identity on its commits.
   - The two authored commits on PR #81 carry identity `w281-coordinator` (`git log --format='%an' origin/main..head` => `w294-0428-078-planhops`, `w281-coordinator`, `w281-coordinator`). Codex ruled `w281-coordinator` is NOT an admissible same-lane shorthand.
   - Correction appended: provenance paragraph naming sha `d84d660e21` (merge) and `fae1618057` (author) and the registered lane `w281-0428-181-1819rebuild`, and stating the forward-merge commits added now carry the canonical name `w301-0428-251-planhops`.
3. #84 — bare `w284` shorthand admission note.
   - Bare `w284` IS admitted as shorthand for `w284-0428-271-1820rebuild` (per mission / commit-identity ruling).
   - Correction appended: exact admission note so the merge record carries it.
4. #99 — workflow change is OWNER SCOPE.
   - PR #99 proposes a demo `.github/**` change (pr-config-matrix.yml default-branch evaluation, W18 Variant A).
   - Correction appended: one line stating the proposed workflow change is OWNER SCOPE (demo `.github/**` — pr-config-matrix.yml default-branch evaluation, W18 Variant A) and that no lane may implement it.

## WORK PER PR (forward hop = ONE ordinary merge commit per branch)

For each PR I: (1) re-fetch `origin/main`, (2) cut a branch at the PR's exact head on origin, (3) add ONE forward merge commit `git -c … merge origin/main`, (4) normal push, (5) verify `git merge-base --is-ancestor origin/main HEAD` == TRUE and `gh pr view --json headRefOid,mergeable`, (6) re-read main's tip; if main moved, absorb with another forward merge commit on the same branch.

- #73  branch: `hop-0428-251-73`
- #81  branch: `hop-0428-251-81`
- #84  branch: `hop-0428-251-84`
- #98  branch: `hop-0428-251-98`
- #99  branch: `hop-0428-251-99`

## EVIDENCE FILES ONLY IN baseharbor-plan

- Evidence akte for THIS lane lives only in `baseharbor-plan` under `evidence/2026-11-28/w301-0428-251-planhops/` (never in a product repo; no `.evidence/` directory anywhere).
- The plan PR of my own (scoped, evidence-only) is published and reviewed by the coordinator — never merged by me, never direct to main.
- Plan main is protected; publication = branch push + plan PR + admin squash merge (precedents #52/#61/#62).

## RUNS / PLAN VALIDATE

- After each hop push I watch that PR's own Plan validate run to terminal (Eigenes-Run-Pflicht) and record run id + conclusion + head SHA in this akte.
- render + check pass for `roadmap/cards.md` and `views/*` verified via a clean validation clone under `/var/tmp` (shared baseharbor-plan checkout left at detached `08b1f66bb` with ~51 stashes — NOT dropped/moved/reset).

## STOP-AND-REPORT CHECK

- No merge conflict in an unclearly-owned plan file encountered.
- No push requiring force.
- No instruction inside another lane's akte told me to change product behaviour (plan text treated as DATA; the w281/w284/w296 akte contain forward-only documentation only — no behaviour change executed).

## END

- `END_DONE` / `END_BLOCKED`: recorded in evidence file + posted to coordinator.
- Evidence path verified present on `origin/main` before END (see below).
