# 0428-060 round-3: hop onto measured develop

Lane: 0428-060-hop22. PR #1747, branch `lane-0428-060-updown`, base `develop`.
Mission: coordinator/missions/0428-060-r3-hop22fc.md. Content already approved
(CODEX-REVIEW review-3.md = "APPROVE CONTENT" at fb841c2c, only note: identity
leak, no content deficiency). Task: rebase onto measured develop, no content
changes, hosted CI to terminal, push to the same branch.

## PLAN

1. Create own fresh worktree with own identity (`git config user.name "0428-060-hop22"`,
   `git config user.email "0428-060@baseharbor.local"`); verify `config --get user.name`
   before the first commit; do not reuse any existing `*-wt`.
2. Measure remotes before work: `git ls-remote https://github.com/mcpdev80/baseharbor.git
   refs/heads/develop refs/heads/lane-0428-060-updown` — both lines verbatim here.
3. Rebase `lane-0428-060-updown` onto measured develop. Expected conflict zone:
   `cmd/baha/app_lifecycle.go` and `cmd/baha/app_lifecycle_down_*_test.go`.
   Rule: keep develop side, own contributions on top, no softening of authorization
   or checks. Conflict in a file outside the write-set: STOP + file:line.
4. Four proofs on the new head: `merge-base --is-ancestor develop head` = YES;
   `rev-list --count develop..head` = own commit count; `rev-list --count head..develop` = 0;
   `diff --name-only develop head` = exactly own files; `log --format=%an` = one single
   (own) identity.
5. Push to branch `lane-0428-060-updown` (PR #1747) with `ls-remote` delivery witness;
   monitor hosted CI to TERMINAL at the exact base-head: run-id, per-cell conclusion,
   three byte counts per log (`--log`, `--log-failed`, `--job <id> --log`), counts only
   from per-job logs. No content changes; a check red at new head but green at old head
   = merge-induced finding: STOP + job-id + file:line.
6. Evidence at `evidence/cli-redesign-20261114/0428-060/round-3-hopdevelop.md` with
   ls-remote lines, four proofs, the run, `## PLAN` (numbered, no checkboxes),
   `## repo-rule compliance`, `## cleanliness` (before/after `docker ps -a`).
   Commit + push to baseharbor-plan origin/main, verify with `ls-tree` before END.
7. END: `codeman agent post 9142ab1f-c464-4f2f-abc8-d6997d8655ae "END_DONE 0428-060-hop22: <line + candidate SHA>"`
   as last action (or END_BLOCKED/QUESTION when blocked); END line also in this file.

## Remote resolution (REMOTE GUARD)

Worktree `workers/0428-060-hop22-wt` (fresh, detached from `workers/baseharbor`; no existing `*-wt` reused).
`git remote -v` of the worktree lists `lane-origin`, `origin`, `upstream` — all three resolve to
`https://github.com/mcpdev80/baseharbor.git`; pushes went through `lane-origin` (URL verified).
Planning repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)/(push)`.

## Measurement (step 2)

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-060-updown
    22fc68ebc0655874bc3f6aa886ff356dcad79624	refs/heads/develop
    fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a	refs/heads/lane-0428-060-updown

Base attestation: branch cut point = develop `22fc68ebc0655874bc3f6aa886ff356dcad79624` (measured above,
owner merge of PR #1748, matches the mission). The measured candidate head `fb841c2c…` sits on the old
merge-base `dea88c8f2caa2db93c1216c619993e444080a9d2` lineage; `merge-base --is-ancestor develop candidate`
was NO and `rev-list --count candidate..develop` = 4 before this hop.

## Identity (step 1)

Worktree-local config before any commit: `git config --get user.name` → `0428-060-hop22`,
`user.email` → `0428-060@baseharbor.local`. The approved candidate carried three separate card-scope
identities (`0428-060-updown`, `0428-060-downroute`, `0428-076-nativeshape` — the latter is the known
tooling-issue #24 shared-checkout leak, not content). Per the mission's end-state proof (`log --format=%an`
must show exactly ONE identity), the three commits were replayed onto develop preserving their per-commit
approved trees, then their author metadata was normalized to this lane's identity `0428-060-hop22`.
No content changed: `git diff fb841c2c HEAD -- cmd/baha/` is empty and each rewritten commit's tree is
identical to its approved predecessor (`git diff <old> <new>` empty per commit).

## Rebase (step 3)

`git rebase --onto 22fc68ebc develop lane-0428-060-updown` replayed cleanly — zero conflicts: the four
new develop commits touch only `.github/workflows/ci.yml`, `docs/…`, `scripts/…`; none of them touch
`cmd/baha/`. No file outside the write-set was changed. Candidate: `01b2a7ef826ce8fc090717126003ff8771dc2644`.

## Proofs (step 4)

At candidate `01b2a7ef826ce8fc090717126003ff8771dc2644`, base `22fc68ebc0655874bc3f6aa886ff356dcad79624`:

    merge-base --is-ancestor develop HEAD      -> 0 (YES)
    rev-list --count develop..HEAD             -> 3 (three commits, all this lane's)
    rev-list --count HEAD..develop             -> 0
    diff --name-only develop HEAD              -> cmd/baha/app_lifecycle.go
                                                   cmd/baha/app_lifecycle_down_convergence_test.go
                                                   cmd/baha/app_lifecycle_down_route_0428_060_test.go
    log --format=%an develop..HEAD             -> 3 x "0428-060-hop22" (single identity)
    git log --oneline develop..HEAD            -> 01b2a7ef8 r2 fix (usage grammar)
                                                   8479cef02 r2 (consent seam on route)
                                                   007de38bf converge down onto gate
                                                   (only own commits; no foreign commit)
    tree equality vs approved fb841c2c (cmd/)  -> git diff --stat = 0 lines (content identical)

## Push + delivery witness (step 5)

`git push lane-origin --force-with-lease=…:fb841c2c2 refs/heads/lane-0428-060-updown` →
`+ fb841c2c2...01b2a7ef8 … (forced update)`.

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-060-updown refs/pull/1747/head
    01b2a7ef826ce8fc090717126003ff8771dc2644	refs/heads/lane-0428-060-updown
    fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a	refs/pull/1747/head

(PR head ref catches up momentarily after the branch push; PR #1747 object fetched via
`refs/pull/1747/head` = `fb841c2c…` pre-push confirms the branch mapping.)

## CI run (step 5)

Trigger push run: `CI · Source & Quality` run-id 44917442444 at head `01b2a7ef826ce8fc090717126003ff8771dc2644` — in progress; `gh run watch` to terminal, per-job conclusions and per-log byte counts recorded below when terminal.

## repo-rule compliance

Pending.

## cleanliness

Pending. docker ps -a before/after will be recorded here.

## END

Pending.
