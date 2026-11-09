# 0427-175 round 2 — corrections on PR #1512 (source format, owner-state test, base drift)

Mission: `/tmp/opencode/mission-175-r2.md`. Lane: worker-flash (session zone `workers/.models/flash`).
Candidate: branch `0427-175-initlock`, commit `135c8be1abd80b7351432d7ffe0ffb886ace0d5f`.
PR: https://github.com/mcpdev80/baseharbor/pull/1512. No `.github/**` files changed by this lane.
Review basis: `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1512-review.md` (plan 3d09e15c),
which confirmed the parallelism/fail-closed design and blocked the candidate on three concrete
red checks of hosted run 42593160991 on head f32f35576.

Planning-repo witness (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel`
→ `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (canonical; `workers/baseharbor-plan` is a
directory inside the workers bookkeeping repo and is NOT the planning repo).

## PLAN

- Read mission + review; fetch remote truth (PR head, develop, plan origin/main)
- Establish remote reality (mission named a nonexistent branch; resolve to the true PR head branch)
- Close base drift against develop (merge + resolve the merge's duplicate-symbol breakage), push to the real branch
- Confirm the three review items on the exact head and let the hosted run settle them
- Local verification on the exact candidate (build/vet/gofmt/readability/tests, parity vs a clean develop clone)
- Watch my own hosted run to a terminal state and record per-job outcomes
- Publish this evidence on baseharbor-plan main; END with ls-remote witnesses

## Remote-state witnesses (measured 2026-11-09 via `git ls-remote origin` and own GitHub API reads)

- Final: `refs/heads/0427-175-initlock` = `refs/pull/1512/head` = `135c8be1abd80b7351432d7ffe0ffb886ace0d5f`; `refs/heads/develop` = `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`.
- Mission text named branch `0427-175-dblinit`: it does not exist remotely (`git ls-remote origin | grep -iE '175|dblinit'` -> only `0427-175-initlock`). The PR head branch is `0427-175-initlock`
  (`gh pr view 1512 --json headRefName,headRefOid` → `0427-175-initlock`, `f32f35576379eeb961bfb292a5b003be3a1dff3f` at mission start). I worked on that real branch; no second branch was pushed.
- Head movement during my session: `f32f35576` (reviewed red head) → `f442b7e99` (11:12:33 +0100, by another
  session; see Authorship) → my push `135c8be1a` (11:31:54 +0100). My earlier local merge candidate
  (branch `0427-175-initlock-r2`, `5d6dfbfcc`) was NEVER pushed — witness:
  `git ls-remote origin 'refs/heads/*initlock-r2*'` → empty; it was superseded and its tree edits deleted.
- Ancestry of my final head (all `git merge-base --is-ancestor`, rc=0):
  `f32f35576` ✓, mission's develop pin `e072e142e` ✓, current develop `fea92f379` ✓ → base drift 0 at push.
- My own commits on the pushed chain (`git log --oneline f442b7e99..HEAD`, listing every entry so a
  foreign candidate on top could not hide): `abe3ba837` (my merge of develop `fea92f379`) and
  `135c8be1a` (my resolution of the merge's duplicate symbol), plus only develop's own commits
  (`fea92f379`,`bf7e7d3ec`,`c8a0103a3`,`27f72992b`,`42ee56fa0`,`fe16127ac`,`e072e142e`) that the merge
  legitimately brought in. No other lane's candidate is carried.

## Authorship (one session per fact, corrected after measurement)

An earlier revision of this file asserted that this lane authored `f442b7e99` (the file split and the
owner-state test fix). That claim is WITHDRAWN as unfounded, and an even earlier guess ("Owner push")
is withdrawn too. Two decisive witnesses:

1. My OWN session transcript for r2 shows the only product-code edits this lane made were (a) creating
   four extraction files in the never-pushed `0427-175-initlock-r2` worktree and (b) deleting the
   duplicated `DeleteDeploymentRecord`; the r2 evidence file I wrote listed only `abe3ba837` and
   `135c8be1a` as my commits. I never authored `f442b7e99`.
2. `git reflog show --date=iso 0427-175-initlock` in `/home/marcel/dev/baseharbor-ecosystem/baseharbor`:

    9de8c993b 2026-11-09 11:43:23 +0100: pull --rebase=false origin 0427-175-initlock: Merge made by the 'ort' strategy.
    54d9b9ef1 2026-11-09 11:42:54 +0100: commit: docs(0427-175): document unique registration and the uuid-addressed poison repair ...
    f442b7e99 2026-11-09 11:12:33 +0100: commit: fix(cmd/baha, internal/deployment): integrate develop owner-state prologue; registry-conflict door on the uuid path
    b4dff2caf 2026-11-09 10:26:05 +0100: merge origin/develop: Merge made by the 'ort' strategy.
    f32f35576 ...  commit: fix(deployment,cmd/baha): serialize first registrations ... (0427-175)

`b4dff2caf` and `f442b7e99` were committed on the shared branch checkout
`/home/marcel/dev/baseharbor-ecosystem/work/0427-175-wt` — the other session's worktree (its own
reflog shows `checkout: moving from 0427-175-initlock to 0427-175-initlock` then the commit, i.e. the
commit landed in THAT session), never in this lane's `/tmp/opencode/w175r2-wt/1512`. All lanes push
under the same Owner author identity, so the commit author field carries no lane signal — only
reflog/worktree evidence does.
Consequences stated plainly: review items (1) source format and (2) the owner-state test were CLOSED
by that other session's commits, which this lane carried by merging the branch head. This lane's own
remote-visible work is item (3): the base-drift closure `abe3ba837` + `135c8be1a`, including resolving
the compile break that merge introduced, plus verification and this evidence. That other session also
made `54d9b9ef1`/`9de8c993b` (docs pages: `docs/cli/applications.md`, `docs/de/cli/applications.md`)
locally AFTER my push; those two are NOT on the remote (`git ls-remote origin | grep -c 9de8c993b` →
0) and are left untouched here — a coordination finding, not this lane's work.

## The three review items on the exact head 135c8be1a

(1) PR Source format (`deployment_store.go` 836 > 800): CLOSED — the file is 778 lines on this head,
    because `f442b7e99` (other session) moved the registry/guard helpers into `registry_conflict.go`
    (286 lines). Verified on my head: `bash scripts/source-readability-audit.sh` PASS and hosted
    `PR · Source format` SUCCESS. No audit or baseline file was touched.
(2) `TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound`: CLOSED and NOT pre-existing —
    measured on a clean `origin/develop` clone at `e072e142e` the cell PASSES, so the review's
    pre-existing gate is not satisfied and the red was an OWNED regression of this card (172-r2
    precedent respected). The fix is in `f442b7e99` (other session): the test seeded its deployment
    with a bare `store.Create`, leaving no `deployment.json`; that shape is the legitimate
    `incomplete` kind (0427-144/160), not an owner-state warning, so the CLI correctly resolved and
    `app_context_owner_state_test.go:62` saw no error. The fixture now persists through the production
    seam before corrupting `installation.json`. Verified on my head: focused cell ok 7x, and hosted
    `PR · Validation · go-unit-tests` SUCCESS. This lane did not write that fix.
(3) `PR Selected Checks`: follows from (1)/(2); no separate lever. Hosted result recorded below (SUCCESS).

Additional defect found and fixed BY THIS LANE: merging develop `fea92f379` (which contains #1505,
which extracted `DeleteDeploymentRecord` into `internal/deployment/deployment_identity_drift.go:21`)
auto-merged a SECOND, plain copy of that function into `registry_conflict.go` — a text artifact of the
card's file split. The package did not compile (`DeleteDeploymentRecord redeclared in this block`).
`135c8be1a` removes the duplicated plain copy and keeps develop's drift-aware version, so the drift
guard that `app prune` and the destroy path depend on stays the single authority. Without this the
candidate could not build, and the red of the Owner-side dispatch run 42599950208 (its only failed
step: `Run unit and package tests`) is consistent with that breakage.

## Local verification on the exact candidate 135c8be1a

- `go build ./...` OK; `go vet ./internal/deployment/...` clean; `gofmt -l` clean on changed files.
- `bash scripts/source-readability-audit.sh` → PASS (no file above 800 except documented baselines).
- `go test ./internal/deployment ./internal/stableid -count=1` → ok.
- Focused cells: `TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound` ok 7x;
  `TestResolveRegisteredApplication|TestConcurrentInit|TestRegistryPoison|TestSaveDeploymentRecord|TestAppPrune|TestDetectApplicationIDCollisions` ok;
  `TestUpNameResumesThroughCommandEntrypoint` ok 5x + `-count=2` ok (the single cell that failed in
  dispatch run 42599950208). `-race` on `TestConcurrentInit` ok.
- Full-package parity, this host's shared home-state: clean develop `e072e142e` run vs candidate run
  produced the IDENTICAL 14-name failure set (`TestQuickInit*/TestGuidedInit*/TestDeterministicInit*/
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle`; diff of sorted `--- FAIL` names empty) —
  environmental (`p427-podman-boot` residue: "application id ... must be a UUIDv4"), not regression.
  `./internal/...` on both trees: same two environmental package failures
  (`internal/controlplaneruntime`, `internal/database`, native postgres cells); `internal/deployment` ok both.
  Hosted CI is the authority and it is green.

## Hosted run on the exact candidate (self-run duty, own API reads)

- Run `42601589418`, event `pull_request`, `head_sha = 135c8be1abd80b7351432d7ffe0ffb886ace0d5f`,
  created 2026-11-09T10:32:26Z, TERMINAL: `completed` / `success` (updated 10:42:34Z). Started by my
  push. PR base ref at that moment: `fea92f379` (`gh api pulls/1512` → base=fea92f379 head=135c8be1a).
- Executed jobs, all SUCCESS: Workflow policy, Native impact selection, Source format, Trusted Plan,
  Focused Python, go-build, cli-gofmt, go-vet, authority-package-tests, deployment-package-tests,
  go-unit-tests, Native destroy retry (docker + podman), PR Selected Checks.
- SKIPPED (reported as skipped, not as passing): validate, Release Source Preflight, Draft focused
  checks, Targeted HA docker + podman, Public Contracts, Exact Candidate, Demo Pin, Consumer Pins,
  Runner Interface, Native Keycloak/Core, Selected Runtime.
- Other runs in scope, terminal: reviewed red 42593160991 on `f32f35576` = completed/failure (source
  format + go-unit-tests + PR Selected Checks); Owner-side validation dispatch 42599950208 on
  `f442b7e99` = completed/failure (unit step, i.e. before my merge fix).

## repo-rule compliance

- plan → preflight → apply → verify preserved; runtime, capability and delivery untouched and not mixed.
- No `.github/**` edit, no rerun/workflow_dispatch started by this lane; failing checks reported as STATE only.
- No subagents (AGENTS §4.8); every step executed in this session; only targeted `git add`.
- Evidence lives only in baseharbor-plan; no product-repo evidence writes, no product main-branch writes.
- Worktree only under `/tmp/opencode/w175r2-wt/...`; caches under the existing shared `go-cache`; nothing created in the ecosystem root.
- No container/compose project was started by this lane (pure-Go scope) → nothing to tear down; ps-witness: no `baha-*` project created by this session.
- Ancestry and own-commit witnesses above; single integration candidate per chain preserved.

## Findings for the Coordinator (not blockers for this task)

- Mission branch name `0427-175-dblinit` does not exist; the real branch is `0427-175-initlock`. Cards/missions should cite `gh pr view` head branch, not remembered names.
- Two sessions commit to the same PR branch (`work/0427-175-wt` vs this lane's `/tmp/opencode/w175r2-wt/1512`). It resolved only because both pushed forward-merges; a docs-only local chain (`54d9b9ef1`, `9de8c993b`) is now unpushed on the shared branch — someone must land or drop it explicitly.
- Run 42593160991 sat `queued` in the PR rollup for ~70 min while its attempt-1 jobs were already `completed/failure` (`/attempts/1/jobs`); a stale queued run on a superseded head can mask a current head's state. No lane-side cancel was possible (`Cannot cancel a workflow run that is completed`).

## State at END

- Candidate: `135c8be1abd80b7351432d7ffe0ffb886ace0d5f` on branch `0427-175-initlock`.
- `git ls-remote origin refs/pull/1512/head refs/heads/0427-175-initlock refs/heads/develop`
  → `135c8be1a  refs/heads/0427-175-initlock` / `135c8be1a  refs/pull/1512/head` / `fea92f379  refs/heads/develop`
- `git status --porcelain` in this lane's worktree → 0 lines (clean).
- Hosted run 42601589418 → completed/success on that exact head (all executed jobs green; skips listed above).

END_DONE mission-175-r2.md: candidate 135c8be1abd80b7351432d7ffe0ffb886ace0d5f on branch 0427-175-initlock (refs/pull/1512/head verified); hosted run 42601589418 completed/success — source format, go-unit-tests and PR Selected Checks green, base drift 0 vs develop fea92f379; items (1)/(2) carried from another session's commits, item (3) plus the DeleteDeploymentRecord merge fix are this lane's own.
