# ROUND 3 — r27 profile-codec (PR #1363 / card t-20261018-r27-profile-codec)

- Lane: w123-codec-r3 (Worker). Coordinator: f49a3303.
- Repo: baseharbor (core), contract package `contracts/managementaccess/v1`.
- Mission: coordinator/missions/w123-codec-r3.txt; archive reviewed fully: baseharbor-plan/evidence/r27-night-2026-11-02/review-1363b.md.
- Branch: work/r27-profile-codec-w123, isolated worktree /tmp/opencode/w123-wt.
- Base: develop ecbb8854 (parent of head). Head under review: e45e85ed5f22ca7ff51b811174fc0161ffbba701.
- Self-run duty: every local check done inside this session, no subagents.

## PLAN

1. Read mission + review-1363b; confirm scope, branch, head.
2. Work on isolated branch work/r27-profile-codec-w123 off origin/work/r27-profile-codec (e45e85ed).
3. Fix finding 1 (secret scan over every serialized field) in store.go.
4. Fix finding 2 (atomic import commit) in store.go.
5. Fix finding 3 (mandatory trust binding) in store.go + spec.
6. Fix finding 4 (full canonical round-trip + golden re-encoding) in store_test.go.
7. Add canary-in-every-field-category test proving export rejection before bytes; short-write/commit-failure injection test proving no partial file / no temp artifact; replacement leaves exactly one record.
8. build, vet, gofmt, package test (self-run).
9. Commit + push; record ls-remote == head verbatim.
10. Report hosted gate STATE if red; never edit .github/workflows; post END to coordinator.

## Repo-rule compliance

- No edit to any .github/** workflow file (owner/ci field). No workflow rerun/dispatch.
- No deleted tests. No changes to cmd/baha or internal/delivery. No subagents (AGENTS §4.8 / mission).
- All changes confined to contracts/managementaccess/v1/store.go and store_test.go (plus test seams in store_testseams_test.go only if needed).
- No scratch/cache/stray files under ecosystem root; worktree under /tmp/opencode/w123-wt.

## Evidence

(To be filled per finding with witness lines: command output, Run-IDs, SHAs.)

## END

END_BLOCKED w123-codec-r3: <one line + candidate SHA>
