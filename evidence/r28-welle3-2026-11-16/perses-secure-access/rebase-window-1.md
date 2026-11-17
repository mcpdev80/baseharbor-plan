# mission-1599-hopf — rebase window 1 (card 0428-089 / PR #1599)

Lane: hopf (flash). Mission: /var/tmp/missions/mission-1599-hopf.md

## PLAN

1. ls-remote witnesses (origin/develop + PR #1599 head branch via `gh pr view 1599 --json headRefName`) — DONE: develop=0ec4706b12c8fa869a2c23db18b6cab4f91f2178, head branch=lane-welle2-089-perses-secure-access=85b01f0ff6df9f45179a7754f6cf4a5daa224d1a
2. Set up /tmp/opencode/w1599-hopf-wt on the exact PR head branch; BASE attestation + provenance checks — DONE (see witnesses below)
3. `git merge origin/develop` (normal, no force; sweeper collisions per 078/1602 rule: develop structure wins, port own additions; unportable = STOP with marker-block)
4. go build / go vet / gofmt + secure-access tests green
5. Refspec push to PR head branch + ls-remote witness + git show HEAD completeness
6. Monitor exact-head CI run to terminal state; record run id / status / failure lines
7. This evidence act committed and pushed to baseharbor-plan origin/main; verify path present
8. Cleanup (VM compose projects: none expected) + END post to coordinator

## Reality witnesses

(being filled)
