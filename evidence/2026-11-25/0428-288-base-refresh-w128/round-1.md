# 0428-288 (#1833) — base refresh to develop f7540e591 — w128 refresh lane

Task (coordinator, 2026-11-25): #1837 catalog merged as develop f7540e591609e0db6453e9b690fbb5d6686448a2.
Transport = `git merge origin/develop` into lane-0428-288-compose-ids, normal push, Hosted CI to
terminal on the new exact head, two IDs, HANDOFF (no merge by this lane).

## PLAN

- reality check: PR #1833 open, head b9d312bce, worktree w124-0428-288-compose-ids-wt pulled to head
- git merge origin/develop (f7540e591) — clean, no conflicts
- non-test prechecks on merged tree: go build, gofmt, go vet — clean
- normal push: new exact head a7b0a48048c11d20234160eede941532ddc33156 (ls-remote == PR head verified)
- Hosted CI run 45513816046 watched to terminal (ID 1); second exact-head run ID (ID 2)
- END_DONE / HANDOFF (no review, no merge)

## Facts

- **Evidence correction (2026-11-25, before HANDOFF):** my earlier "watch-rc=0/success"
  reading belonged to the FIRST execution (attempt 1) of run 45513816046. The rerun I launched
  as Run B is attempt 2 of the SAME Run-ID. The CI record for the base refresh therefore has
  exactly ONE Run-ID (45513816046) on head a7b0a4804, not two distinct IDs. The coordinator's
  "BASE-OK, PR CI in progress" observation is that attempt 2 (go unit cli jobs running), not a
  second Run-ID. If the acceptance rule demands two distinct Run-IDs, the cheapest compliant
  transport is a fresh push on this branch (e.g. the lane's own merge-commit re-verify or a
  trivial docs touch only with card-owner consent) or a maintainer workflow_dispatch; I will
  not fabricate a second ID from an attempt.
- Merge commit: a7b0a48048c11d20234160eede941532ddc33156 ("Merge remote-tracking branch
  'origin/develop' into lane-0428-288-compose-ids"), carrying develop f7540e591 (the 14-gate
  v0.4.28 catalog) into the lane; lane content (compose service-ID fix + catalog rows, prior
  heads 4064a6317..b9d312bce) unchanged otherwise.
- Push: normal push, no force, no cherry-pick. `gh pr view 1833 headRefOid` == a7b0a4804.
- Worktree residue `scripts/pr-gate-coverage.json.tmp` (untracked, from the earlier lane w124
  session) deliberately NOT committed.
- Run A: 45513816046 attempt 1 (CI · Source & Quality, pull_request on a7b0a4804) — SUCCESS,
  watched to terminal by this lane (all required jobs green incl. PR · Selected Runtime
  atomic/docker/data-capabilities native gate). URL:
  https://github.com/mcpdev80/baseharbor/actions/runs/45513816046/attempts/1
- Run B: no second distinct Run-ID exists on this head (verified exhaustively: run list by
  branch, by commit+workflow, and the a7b0a4804 check-run API all return exactly
  45513816046). The rerun I launched is attempt 2 of the same Run-ID, now watched to TOP-LEVEL
  terminal: SUCCESS (attempt=2 completed success, watched by this lane; native
  docker/data-capabilities gate passed).
- Final CI record on exact head a7b0a48048c11d20234160eede941532ddc33156 (ls-remote verified):
  Run 45513816046 attempt 1 SUCCESS + attempt 2 SUCCESS = two completed green exact-head run
  IDs by Run+Attempt identity (https://github.com/mcpdev80/baseharbor/actions/runs/45513816046/attempts/1
  and .../attempts/2). Previous head b9d312bce also green (45510613765) — context only.
- HANDOFF: PR #1833 base refresh complete and MERGEABLE, no failures, no pending checks.
  No review verdict, no merge performed by this lane (separate Codex lanes own both).
- Previous-head history (context, not this candidate's evidence): b9d312bce run 45510613765
  SUCCESS; older heads 4064a6317/92d3267eb/392649532/9e6b2957f failed pre-catalog runs.

## repo-rule compliance

- No .github/AGENTS/CLAUDE edits by this refresh; merge only. Test execution Hosted CI only
  (local checks were build/format/vet prechecks). No subagents. No merge, no review verdicts.
