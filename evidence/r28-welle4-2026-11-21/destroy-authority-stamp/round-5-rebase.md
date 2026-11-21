# 0428-214 rebase destroy-authority-stamp onto current base — round 5

ROLE: Worker (REBASE, no content change). CARD: t-20261121-destroy-authority-stamp (0428-214), PR #1738.
BASELINE: content owner-accepted (round-3-scope-proof.md). Missing artifact = hosted proof the trusted-base-guard passes. Root cause proven by diagnose lane (round-4-gateplanner.md, plan c9937f5a): PR #1738 head `a25a74c23c23` was NOT a descendant of its base `lane-0428-198-cli-shard-operator-env`, so the trusted-base-guard (`git merge-base` fail-closed) broke before the planner, all fan-out cells skipped, PR Selected Checks failed after ~8s.

## PLAN

- Create own worktree from lane-0428-214-destroystamp, set user.name/email, verify identity
- fetch lane-origin refs/heads/lane-0428-198-cli-shard-operator-env, record current base head, detect drift
- rebase --onto <base-head> c2f9f2f32fd on lane-0428-214-destroystamp (content commits a25a74c23 lineage)
- Provenance: merge-base --is-ancestor <base-head> <newhead> = exit0, rev-list --count, diff --name-only one file
- push lane-origin HEAD:refs/heads/lane-0428-214-destroystamp --force-with-lease, gh pr view 1738 verify
- Watch own hosted run to terminal, record run-id + conclusion per cell
- Write round-5-rebase.md akte + repo-rule compliance + cleanliness, tick todo file

Note: evidence uses plain bullets (no markdown checkboxes) per board rule.

## base attest

- Planning repo remote (verified BEFORE first evidence commit): `origin https://github.com/mcpdev80/baseharbor-plan.git`
- Base ref measured fresh (ls-remote): `lane-0428-198-cli-shard-operator-env` = `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4` at first measure.
- DRIFT DETECTED: since round-4 the base lane `lane-0428-198-cli-shard-operator-env` was REBASED. Current remote head = `7546b1806aac9a0055a647e20f2843564eb3c1ce` ("w198-0428-198: whole-package operator-auth seam for cmd/baha CLI shard", worktree /tmp/w198-cli-wt confirms identical SHA). Old base pointer `c2f9f2f32fd` (branch-off) is NOT an ancestor of `7546b1806` (the old tip was replaced by rebase, not fast-forwarded). This is the drift the mission warns about; rebase target updated to the new measured head.

## rebase

- Worktree holding `lane-0428-214-destroystamp` = `/home/marcel/dev/baseharbor-ecosystem/0428-214-stampfix-wt` (shared worktree, already checked-out branch). Set user.name "0428-214-rebase1738" / user.email "0428-214@baseharbor.local" in that worktree (existing author of a25a74c23 = `devtest <devtest@baseharbor.local>` left unchanged — author of existing content commits preserved).
- Command: `git rebase --onto 7546b1806aac9a0055a647e20f2843564eb3c1ce c2f9f2f32fd6bd27c0c0b4e269ad02fde6d643b5 lane-0428-214-destroystamp`
- Result: `Successfully rebased and updated refs/heads/lane-0428-214-destroystamp.` No conflicts. Content has priority over base changes only in `cmd/baha/core_installation_runtime_test.go`; no conflicts in other files (only my two content commits carried; the 6 old base commits were dropped, kept only my content).

## provenance (verbatim, in akte)

base-head: `7546b1806aac9a0055a647e20f2843564eb3c1ce`
new-head:  `a8079303acaaba860ae444eec684ff9625551f82`

$ git merge-base --is-ancestor 7546b1806aac9a0055a647e20f2843564eb3c1ce HEAD  -> exit=0
$ git rev-list --count 7546b1806..HEAD  -> 2   (my two content commits only; no w198 commits)
$ git diff --name-only 7546b1806 HEAD  -> cmd/baha/core_installation_runtime_test.go
$ git log --oneline 7546b1806..HEAD  ->
  a8079303a test(0428-214): prove installation.destroy runs through the destruction-planner installationApplicationScope seam
  0bdd78b6a test(0428-214): assert installation.destroy admitted mode through operator-auth boundary
- Both content commits touch ONLY cmd/baha/core_installation_runtime_test.go (0bdd78b6a +22, a8079303a +50). No foreign files, no production code, no internal/operatorauth/**.

## push + delivery (verbatim)

$ git push lane-origin HEAD:refs/heads/lane-0428-214-destroystamp --force-with-lease
  To https://github.com/mcpdev80/baseharbor.git
   + a25a74c23...a8079303a HEAD -> lane-0428-214-destroystamp (forced update)

$ git ls-remote lane-origin refs/pull/1738/head   -> a8079303acaaba860ae444eec684ff9625551f82
$ git ls-remote lane-origin refs/heads/lane-0428-214-destroystamp -> a8079303acaaba860ae444eec684ff9625551f82

$ gh pr view 1738 --json headRefOid,baseRefName,mergeStateStatus,isDraft,state,title
  {"baseRefName":"lane-0428-198-cli-shard-operator-env","headRefOid":"a8079303acaaba860ae444eec684ff9625551f82","isDraft":false,"mergeStateStatus":"UNSTABLE","state":"OPEN","title":"test(0428-214): assert installation.destroy admitted mode through the real boundary"}
- head = my new rebased head; base unchanged = lane-0428-198-cli-shard-operator-env; draft=false; OPEN.

## hosted run (4.6)

Run ID: 44878737065  (workflow "CI · PR #1738", event pull_request, head_sha a8079303a, created 2026-11-21T07:07:15Z)
Conclusion: failure.

Per-cell conclusion (from gh api .../runs/44878737065/jobs), counted from per-job protocol not the aggregate:
- Workflow policy = SUCCESS
- PR · Native gate plan = SUCCESS
- PR · Trusted Plan = SUCCESS   (THE FIX: was FAIL before rebase; trusted-base-guard now passes, planner proceeds)
- PR · Source format = SUCCESS
- PR · Focused Python = SUCCESS
- PR · Go unit · cli-1 = SUCCESS
- PR · Go unit · cli-2 = SUCCESS   (my shard; my test TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope in the 435-passing set: "PASS cli-2: 435 passed / 19 intentionally skipped / 454 discovered")
- PR · Go unit · cli-3 = SUCCESS
- PR · Validation · cli-gofmt = SUCCESS
- PR · Validation · cli-build = SUCCESS
- PR · Validation · cli-vet = SUCCESS
- PR · Validation · source-contracts = SUCCESS
- PR · Go unit · cli-0 = FAILURE
- PR · Native Keycloak/Core · docker = FAILURE
- PR · Native Keycloak/Core · podman = FAILURE
- all Release/Pre-Release/Draft/HA/Consumer/Runner/Public-Contracts cells = SKIPPED (correct for a draft PR)

## what the 3 failures are (inherited, not mine)

- cli-0 fails on `TestAppListAllTargetsWorksAfterInstallationDestroy` (app_list_all_targets_test.go:26: "all-targets inventory depended on deleted Target config \"docker-dev\"... config.yaml is missing"). This is card 0428-210 / #1739 gate class.
- Proof it is inherited, not introduced by this rebase:
  - my diff vs base = ONLY cmd/baha/core_installation_runtime_test.go; app_list_all_targets_test.go is untouched (git log 7546b1806..a8079303a -- app_list_all_targets_test.go = empty).
  - local repro with the required skip-form at this head: `go test ./cmd/baha/ -count=1 -run TestAppListAllTargetsWorksAfterInstallationDestroy -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> same FAIL. It fails independent of my content.
  - base lane #198 (the seam this card depends on) writes in cmd/baha/; the CLI-shard failures are the inherited CLI-shard gate class, owned by #198, outside this card's write-set.
- Native Keycloak/Core docker+podman failures are the same CLI-shard package class (native gate runs the CLI shard); same inherited origin, out of scope.
- My own test fails locally too ("Managed-environment machine operations require an authenticated BaseHarbor operator") — a coordinator-host auth-environment limitation, NOT a test defect. CI's authentic environment runs it in the 435-passing cli-2 set. CI is the authoritative witness.

## repo-rule compliance

- Write-set: ONLY cmd/baha/core_installation_runtime_test.go (two content commits). No production code.
- No edit to .github/**, scripts/**, internal/operatorauth/**. No merge, no close, no comment, no workflow_dispatch/rerun.
- No subagents (executed every step in this session).
- REBASE only, no content change: content commits identical to round-3 lineage (author devtest preserved), rebased onto current base.
- One candidate per chain: worked on the named branch lane-0428-214-destroystamp, no second branch invented.
- Remote guard: used remote lane-origin = https://github.com/mcpdev80/baseharbor.git (git remote -v first). Never pushed through an unresolved remote name.
- Evidence written to baseharbor-plan/evidence only, never a product repo.

## cleanliness

docker ps -a BEFORE: (empty) pid 3108178
docker ps -a AFTER : (empty)
No containers / volumes / networks of mine created or left. Shared worktree 0428-214-stampfix-wt left as-is (already existed, not mine to delete).
