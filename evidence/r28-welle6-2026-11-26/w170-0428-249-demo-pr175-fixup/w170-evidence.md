# w170-0428-249-demo-pr175-fixup

**Card:** 0428-249 (owned by lane `w170-0428-249-demo-pr175-fixup`)
**PR:** #175 — `fix(demo): reconcile IN_SYNC apply immutable no-op (test-only consent drive, #1812)`
**Mission:** `coordinator/missions/w170-demo175-identity-fixup.txt`
**Handoff target:** w136 (CODEX-REVIEW verdict = CHANGES)
**Shift / evidence root:** `baseharbor-plan/evidence/r28-welle6-2026-11-26/w170-0428-249-demo-pr175-fixup/`

## PLAN

- Read mission w170-demo175-identity-fixup.txt and verify PR #175 state (base=develop, head=9dc5f7af, draft)
- Verify repo remotes and planning-repo remote BEFORE first evidence commit
- Diagnose defect #1: HEAD commit author.name=Flash (identity admission violation)
- Diagnose defect #2: PR base targeting (main tip df4867c7 != b4112772 -> keep develop base, rely on workflow_dispatch)
- Fix defect #1: additive lane-identity commit, no tree change; verify %an at new head == lane string
- Mechanical identity pre-push check: git show %an HEAD == w170-0428-249-demo-pr175-fixup (STOP on mismatch)
- Push branch to GitHub, prove delivery via git ls-remote refs/pull/175/head
- Run TWO same-head Hosted qualification runs (workflow_dispatch on 9dc5f7a) to terminal (per_page=100)
- Write evidence file under baseharbor-plan evidence/r28-welle6-2026-11-26/
- Commit evidence to baseharbor-plan, verify on origin/main before END
- Tear down any compose project (ps witness), post END_DONE + HANDOFF to w136

## repo-rule compliance

- Product repo: `baseharbor-demo` (mcpdev80/baseharbor-demo), remote `origin` = https://github.com/mcpdev80/baseharbor-demo.git (verified via `git remote -v`; the only github.com/mcpdev80 URL).
- No product consent/auth delta: only an additive empty commit + workflow_dispatch runs. Test files untouched.
- Scope: additive commit only, no rewrite, no force-push, no cherry-pick.
- Evidence written ONLY under baseharbor-plan (never in product repo). No `.evidence/` directory in the product repo.

## bases attestation

- Planning repo remote (verified before first evidence commit):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Demo repo remote (verified via `git remote -v`, only github.com/mcpdev80 URL used):
  `origin	https://github.com/mcpdev80/baseharbor-demo.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-demo.git (push)`

## PR #175 state (reality witnesses)

- `git ls-remote origin refs/pull/175/head` => `9dc5f7afbb19c3f9ece6d15edd5d5320bf602ea0` (matches mission head)
- gh pr 175: baseRefName=develop, headRefName=`w152-0428-249-demo-reconsent-fix`, isDraft=true, state=OPEN, 1 commit.
- `git ls-remote origin refs/heads/develop` => `b41127723e523134a1c14ee3c36cf133237162ce`
- `git ls-remote origin refs/heads/main` => `df4867c7540774eba8b8811cb64946b4adc0c8ab`

## defect #2 diagnosis: base targeting

- Mission rule: retarget PR #175 to `main` ONLY IF `b4112772 == main tip`.
- Demo `main` tip = `df4867c7` — this is NOT `b4112772`. Therefore per the literal rule the base is KEPT on `develop`.
- Rely on `workflow_dispatch` runs (they run on any head SHA, as proven by the two w136 green runs 45590658205/45590834599 on head 9dc5f7a).
- Note for the Owner (workflow scope): `pr-guided-consent.yml` fires `pull_request` only against `branches:[main]` (line 4-5) + `workflow_dispatch`. Because PR #175's base is `develop`, its PR-targeted CI does not fire natively; the Hosted qualification comes from `workflow_dispatch`. This is a scope finding only (Owner owns `.github/**`); no workflow file edited.

## branch provenance

- Branch under work: `w152-0428-249-demo-reconsent-fix` (the branch named by PR #175 / w136 verdict).
- `git merge-base --is-ancestor 9dc5f7af... origin/develop` => NOT an ancestor of develop (head was committed on an older base; carried forward intentionally by w136). Documented, not a new-branch cut.
- `git log --oneline origin/main..9dc5f7a` = 9dc5f7a, b411277, 019bd38, 87f5b28, 7d9eb21, c23bd9a (all w136/w-work commits, no foreign candidate carried on top of this lane beyond the single documented head).
- `git diff origin/develop...HEAD --name-only` will be recorded after the additive commit.

## defect #1 fix: head identity alignment

- HEAD commit `9dc5f7a` author = `Flash` / `flash@baseharbor.local` — violates the candidate-commit identity admission rule (author.name must equal the owning lane).
- Fix ADDITIVELY (never rewrite):
  `git -c user.name='w170-0428-249-demo-pr175-fixup' -c user.email='w170-0428-249-demo-pr175-fixup@baseharbor.local' commit --allow-empty -m 'chore(ci-test): head identity alignment (additive, no tree change)'`
- Then verify `%an` at new head == `w170-0428-249-demo-pr175-fixup` AND == card frontmatter owner.

## CI / qualification plan

- Same-head Hosted qualification: two `workflow_dispatch` runs of `Demo · PR guided consent regressions` on the NEW exact head, waited to terminal (cancelled/skipped void). `per_page=100` when listing runs.
- Proof of delivery after push: `git ls-remote origin refs/pull/175/head refs/heads/w152-0428-249-demo-reconsent-fix`.

## qualification runs (same-head Hosted, workflow_dispatch)

Two `workflow_dispatch` runs of `Demo · PR guided consent regressions` on the NEW exact head `49328fbc8047f4997545dcb1ba9a3e68d1e42bed` (branch `w152-0428-249-demo-reconsent-fix`), waited to terminal. Dispatched via `curl -X POST .../actions/workflows/pr-guided-consent.yml/dispatches` with `{"ref":"w152-0428-249-demo-reconsent-fix"}` (raw SHA rejected by the dispatch API; branch ref head is 49328fb).

- Run `45593701391` (run_number 87): status=completed conclusion=success head_sha=49328fb job `Guided consent · production-path regressions` (job 139134154995) = success. created 2026-11-25T10:18:22Z updated 10:19:07Z.
- Run `45593726801` (run_number 88): status=completed conclusion=success head_sha=49328fb job `Guided consent · production-path regressions` (job 139134239625) = success. created 2026-11-25T10:18:32Z updated 10:19:18Z.
- Both terminal (not cancelled/skipped). Required coverage = the demo guided-consent fixture + guided decision-path regressions, which pass on this head.

## END state

END_DONE w170-0428-249-demo-pr175-fixup: head identity aligned via additive empty commit 49328fb (%an == w170-0428-249-demo-pr175-fixup at new head); base KEPT on develop (demo main tip df4867c7 != b4112772, per mission rule); PR #175 now heads 49328fb (proven via git ls-remote refs/pull/175/head); two same-head workflow_dispatch qualification runs (45593701391 / 45593726801) both success; HANDOFF to w136 for ready+merge. No compose projects started this shift (docker ps -a witness: n/a, no containers launched).
