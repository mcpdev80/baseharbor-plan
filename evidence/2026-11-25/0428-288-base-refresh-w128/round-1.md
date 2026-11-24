# 0428-288 (#1833) — base refresh to develop f7540e591 — w128 refresh lane

Task (coordinator, 2026-11-25): #1837 catalog merged as develop f7540e591609e0db6453e9b690fbb5d6686448a2.
Transport = `git merge origin/develop` into lane-0428-288-compose-ids, normal push, Hosted CI to
terminal on the new exact head, two IDs, HANDOFF (no merge by this lane).

## PLAN

- [x] reality check: PR #1833 open, head b9d312bce, worktree w124-0428-288-compose-ids-wt pulled to head
- [x] git merge origin/develop (f7540e591) — clean, no conflicts
- [x] non-test prechecks on merged tree: go build, gofmt, go vet — clean
- [x] normal push: new exact head a7b0a48048c11d20234160eede941532ddc33156 (ls-remote == PR head verified)
- [ ] Hosted CI run 45513816046 watched to terminal (ID 1); second exact-head run ID (ID 2)
- [ ] END_DONE / HANDOFF (no review, no merge)

## Facts

- Merge commit: a7b0a48048c11d20234160eede941532ddc33156 ("Merge remote-tracking branch
  'origin/develop' into lane-0428-288-compose-ids"), carrying develop f7540e591 (the 14-gate
  v0.4.28 catalog) into the lane; lane content (compose service-ID fix + catalog rows, prior
  heads 4064a6317..b9d312bce) unchanged otherwise.
- Push: normal push, no force, no cherry-pick. `gh pr view 1833 headRefOid` == a7b0a4804.
- Worktree residue `scripts/pr-gate-coverage.json.tmp` (untracked, from the earlier lane w124
  session) deliberately NOT committed.
- Run A: 45513816046 (CI · Source & Quality, pull_request on a7b0a4804) — in progress at last
  write; terminal state + outcome recorded below.
- Run B: second exact-head ID (rerun of the required workflow on a7b0a4804 if no new push):
  recorded below.
- Previous-head history (context, not this candidate's evidence): b9d312bce run 45510613765
  SUCCESS; older heads 4064a6317/92d3267eb/392649532/9e6b2957f failed pre-catalog runs.

## repo-rule compliance

- No .github/AGENTS/CLAUDE edits by this refresh; merge only. Test execution Hosted CI only
  (local checks were build/format/vet prechecks). No subagents. No merge, no review verdicts.
