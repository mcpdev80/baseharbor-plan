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
- clean-delivery: conflicts resolved ONLY in 7er-write-set (docs/spec + docs/decisions + EN/DE). No edits to internal/delivery/contract_test.go (no conflict there).
- No rerun, no gh pr edit/ready/close, no new PR, no product-refactoring.
- Every branch: own /tmp/opencode/w108-<kurz>-wt worktree, fetch origin, merge --no-ff develop, targeted test, push to same branch name, record ls-remote.
- clean-delivery STOP condition checked: develop's ADR-0022/spec content is identical to canonical delivery-boundary 1c921c47; my branch blob was a broken placeholder ("exists on disk, but not in HEAD"), NOT a content dispute. Resolved to canonical develop content, not silently reworded.

## Per-branch table

### Branch 1: work/r27-profile-codec (#1363)
- old head: d68251ee (base refresh onto develop f8ef4255, w102)
- new head: 0eb8f2316b602fe707f0d111c19429c1aac03e7a
- merge rc: 0 (auto-merge, no conflicts)
- test: go test ./contracts/managementaccess/v1/ -> ok (0.093s)
- ancestry: old-head + develop both ancestors of new head (rc=0)
- ls-remote: 0eb8f231... work/r27-profile-codec

### Branch 2: work/w92-team-auth-claim-mapping (#1369)
- old head: bfaddb37 (base refresh onto develop f8ef4255, w102)
- new head: 689689e3abdaf1bc14ef81aa601d69f40595e185
- merge rc: 0 (auto-merge, no conflicts)
- test: go test ./internal/auth/... ./internal/identity/... ./internal/operatorauth/... -> all ok (0.337/0.002/0.111s)
- ancestry: old-head + develop both ancestors (rc=0)
- ls-remote: 689689e3... work/w92-team-auth-claim-mapping

### Branch 3: work/r27-native-auth (#1362)
- old head: 0958107f (chore trigger base-refresh CI, w97)
- new head: a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c
- merge rc: 0 (auto-merge, no conflicts)
- test: go test ./internal/credential/native/... -> ok; go vet ./cmd/baha/... -> rc=0; go test ./cmd/baha/ -run Native|Credential|Auth -> PASS (32.9s)
- ancestry: old-head + develop both ancestors (rc=0)
- ls-remote: a3eee132... work/r27-native-auth

### Branch 4: work/r27-candidate-contract (#1355)
- old head: bed00516 (base refresh onto develop f8ef4255, w102) — contains owner-commits
- new head: ffe27712f25b75418a356ac37caec0bb9ae1fbdd
- merge rc: 0 (auto-merge, no conflicts)
- owner-commit ancestry: bed00516 ancestor rc=0; c25340f5 (owner work r27 delivery-boundary) ancestor rc=0 — content sacred preserved
- test: go test ./internal/machinehttp/ -> ok (25.868s)
- ancestry: old-head + develop both ancestors (rc=0)
- ls-remote: ffe27712... work/r27-candidate-contract

### Branch 5: work/w96-production-wiring-f8ef4255 (#1371)
- old head: af05b198 (fix workstationenrollment review-1371a, w104 r2)
- new head: 589baf0e84e63c7eb351b6a11accf9c95200976a
- merge rc: 0 (auto-merge, no conflicts)
- test: go test ./internal/workstationenrollment/... -> all ok (0.006/0.012s)
- ancestry: old-head + develop both ancestors (rc=0)
- ls-remote: 589baf0e... work/w96-production-wiring-f8ef4255

### Branch 6: clean-delivery (#1334)
- old head: 7c4834bf (ci: replan unchanged source with corrected formatting base #1350)
- new head: 4a4e322ea39f94497f5ce5fb7f5a7e903592f917
- merge rc: 1 (add/add conflicts) -> resolved in 7er-write-set ONLY
- conflict files (all in authorized scope):
  - docs/spec/delivery-provider-v1.md (EN)
  - docs/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md (EN)
  - docs/decisions/index.md (EN)
  - docs/de/spec/delivery-provider-v1.md (DE)
  - docs/de/decisions/0022-one-reconciliation-owner-and-delegated-delivery.md (DE)
  - docs/de/decisions/index.md (DE)
  - (internal/delivery/contract_test.go: no conflict)
- STOP-condition check: develop's ADR-0022 + delivery-provider-v1 EN content is byte-identical to canonical delivery-boundary 1c921c47 (git diff rc=0). Branch blob at 7c4834bf was a broken placeholder ("exists on disk, but not in HEAD"), NOT a different ADR-0022 text. Resolved to canonical develop content (verified diff against 1c921c47 rc=0 for both EN files) — NOT silently reworded.
- go test ./internal/delivery/ -> ok; ./internal/delivery/... ./internal/deployment/ -> ok; go build ./... -> rc=0; gofmt -l ./internal/delivery/ -> clean; go vet ./internal/delivery/ -> rc=0
- ancestry: old-head (7c4834bf) + develop (bb9bc0ef) both ancestors of new head (rc=0)
- ls-remote: 4a4e322e... clean-delivery

## END

END_DONE w108-base-refresh: refreshed=6/6 konflikte=keine-stopp stops=keine | all 6 branches merged onto develop bb9bc0ef, pushed to same branch names, ls-remote + ancestry verified; clean-delivery real merge done (6 doc conflicts in 7er-write-set resolved to canonical develop content, ADR-0022 not a content dispute, go build/test/gofmt/vet clean).
