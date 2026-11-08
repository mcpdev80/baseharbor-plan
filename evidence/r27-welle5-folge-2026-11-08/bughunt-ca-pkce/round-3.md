# 0427-134 r3 — PR #1457 execution (round 3)

## Status

ACTIVE — executing the fix recipe from `act-1457-review.md` (r2 review; points 2-4, OWNERSHIP/ANCESTRY, CLEANUP-WITNESS already PASS).

## PLAN

- Read mission + `act-1457-review.md` fully; verify live refs
- Create worktree, cut branch from candidate, confirm ancestry + single commit
- (1) Fix `cmd/baha/operator_auth.go`: capture `--no-browser` into `TrustOptions.NoBrowser` and pass to `Login`; keep env alias
- (2) `internal/operatorauth`: combine the CA-discovery + headless PKCE fixtures into one combined production-path `Login` test over managed-CA-only TLS; fixed callback-port case; flag>env>default
- (3) Regenerate `docs/cli/command-index.md` (+ DE) from command tree; add `--no-browser` CLI regression; run full suites + docs audit
- (4) Push, watch required CI to terminal, ls-remote, drift-merge develop, publish evidence

## Reality witnesses

- `git ls-remote origin refs/heads/develop refs/heads/wip/0427-134-ca-pkce-integrate` -> `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` and `09030b370c607a818a77cc128322c7b06fffd4f7 refs/heads/wip/0427-134-ca-pkce-integrate`
- `git ls-remote origin refs/heads/main` -> `988c35a28d0cdd4ab352040f133fc37cc2217631 refs/heads/main`
- PR #1457 head `09030b370c607a818a77cc128322c7b06fffd4f7`, base `develop`, OPEN, MERGEABLE
- `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 09030b370c607a818a77cc128322c7b06fffd4f7` -> exit 0 (develop is ancestor of candidate)
- Candidate-only log: single commit `09030b37 wip(ca-pkce): ...`
- Branch cut from `09030b370c607a818a77cc128322c7b06fffd4f7` (candidate head)
- Hosted run `42455848388` -> conclusion failure on exact head `09030b37` (`go-unit-tests` failed on `human_documentation_test.go:101` command-index.md drift)
- develop moved during the round: `07ae6c3e` -> `48d6f10a` (commits 1452, 1454, 1456, 1461, 1462). Merged origin/develop into 134-r3-ca-pkce (drift-merge, recipe point 4); merge commit clean, no conflicts; command-index login row still carries `[--ca FILE] [--auth-code-file FILE] [--no-browser]`; TestHumanCommandIndexTracksExactCommandMetadata passes on the merged tree
- My branch's only delta vs the candidate head is the r3 fix (8 files, +440/-18)

## Repo-rule compliance

- Single integration candidate per chain; branch `134-r3-ca-pkce` cut from the named PR head, no second branch
- No subagents (4.8); every step run inside this session
- `.github/**` not edited, no workflow_dispatch/rerun
- Evidence file lives in baseharbor-plan only, not in the product repo
- Workspace fixed layout: worktree under `/tmp/opencode/134-r3-ca-pkce`

## END

PENDING.
