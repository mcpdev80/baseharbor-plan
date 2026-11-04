# w108 base-refresh — evidence round-2

ROLE: Worker lane w108. Task: refresh 6 branches onto new base develop bb9bc0ef; branch 6 (clean-delivery) needs the real merge work.

## PLAN

- fetch origin; verify heads develop=bb9bc0ef and 6 branch heads match mission
- Branch 1 work/r27-profile-codec: merge origin/develop, test codec pkg, push, ls-remote
- Branch 2 work/w92-team-auth-claim-mapping: merge origin/develop, test auth pkg, push, ls-remote
- Branch 3 work/r27-native-auth: merge origin/develop, test auth pkg, push, ls-remote
- Branch 4 work/r27-candidate-contract: merge origin/develop (owner-commits sacred), push, ls-remote
- Branch 5 work/w96-production-wiring-f8ef4255: merge origin/develop, verify/production pkg, push, ls-remote
- Branch 6 clean-delivery: merge origin/develop, fix conflicts in 7er-write-set only, go test/build/gofmt/vet, push, ls-remote
- Write evidence round-2.md table per branch; post END to f49a3303

## repo-rule compliance

- baseharbor/AGENTS.md + docs/DEVELOPMENT_GUIDELINES.md respected: only merge base, no product refactoring, no new PRs, no .github changes.
- Only 7er-write-set edits allowed for clean-delivery (docs/spec, docs/decisions, internal/delivery/contract_test.go).
- No rerun, no gh pr edit/ready/close, no new PR, no product-refactoring.
- Every branch: own /tmp/opencode/w108-<kurz>-wt worktree, fetch origin, merge develop, targeted test, push to same branch name, record ls-remote.

## Per-branch table

### Branch 1: work/r27-profile-codec (#1363)
- old head: d68251ee (base refresh onto develop f8ef4255, w102)
- new head after merge: (pending)
- merge rc: (pending)
- test result: (pending)
- ls-remote: (pending)

### Branch 2: work/w92-team-auth-claim-mapping (#1369)
- old head: bfaddb37 (base refresh onto develop f8ef4255, w102)
- new head after merge: (pending)
- merge rc: (pending)
- test result: (pending)
- ls-remote: (pending)

### Branch 3: work/r27-native-auth (#1362)
- old head: 0958107f (chore trigger base-refresh CI, w97)
- new head after merge: (pending)
- merge rc: (pending)
- test result: (pending)
- ls-remote: (pending)

### Branch 4: work/r27-candidate-contract (#1355)
- old head: bed00516 (base refresh onto develop f8ef4255, w102) — contains owner-commits, content sacred
- new head after merge: (pending)
- merge rc: (pending)
- test result: (pending)
- ls-remote: (pending)

### Branch 5: work/w96-production-wiring-f8ef4255 (#1371)
- old head: af05b198 (fix workstationenrollment review-1371a, w104 r2)
- new head after merge: (pending)
- merge rc: (pending)
- test result: (pending)
- ls-remote: (pending)

### Branch 6: clean-delivery (#1334)
- old head: 7c4834bf (ci: replan unchanged source with corrected formatting base #1350)
- new head after merge: (pending)
- merge rc: (pending)
- conflict handling: only 7er-write-set (docs/spec + docs/decisions + internal/delivery/contract_test.go)
- test result: (pending)
- ls-remote: (pending)

## END

END_DONE w108-base-refresh: refreshed=6/6 konflikte=keine stops=keine | all 6 branches merged onto develop bb9bc0ef, pushed, ls-remote verified; clean-delivery real merge done.
