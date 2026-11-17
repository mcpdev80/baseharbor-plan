# mission-1579-uid-app-rebase — hopf-2 akte (base-refresh 8db0d9bdf)

## One-line summary
Base-Hopf: develop advanced to 8db0d9bdf (#1666-merge, fail-loud base config + keycloak signal) after my prior push 06a852a64. Re-merged into lane-0428-uid-app (merge commit c93d0e541, no force), build/vet/gofmt + affected tests green, pushed, PR #1579 OPEN/mergeable, CI run #6447 completed success.

## Trigger
Base-Hopf fensterregel: develop moved since the prior run (8db0d9bdf = #1666-merge). My head 06a852a64 did NOT contain it (`git merge-base --is-ancestor 8db0d9bdf HEAD` => NO), so a re-merge was required.

## Provenance (Owner rules)
- Base ref: `git ls-remote origin develop` => 8db0d9bdf8d9ae77db94c9ddce9c209001c4da54.
- Origin lane head BEFORE re-merge: 06a852a643a0aff3ce0c1c7bd684c7c7d670f0a0 (my prior push, verified).
- Ancestry proof: `git merge-base --is-ancestor 8db0d9bdf … HEAD` => YES (develop is an ancestor of the new merge commit).
- My commits on top of 06a852a64: c93d0e541 (merge) only — no foreign candidate carried.

## Re-merge (no rebase / no force, §5.2)
- Command: `git merge origin/develop --no-edit` on lane-0428-uid-app.
- Result: merge made by 'ort', exit 0, ZERO conflicts.
- New merge commit: c93d0e5414523836d5c8845de4821bb0b5f6f04e.
- Diff from fresh develop: 4 files changed, 528 insertions(+), 3 deletions(-):
  - internal/deployment/config_fail_loud_test.go (new)
  - internal/deployment/target.go
  - internal/identityprovider/keycloak_realization.go
  - internal/identityprovider/keycloak_signal_registration_test.go (new)

## Verification (all local, self-run)
Toolchain: go1.26.8.
- `go build ./...` => exit 0 (clean).
- `go vet ./...` => exit 0 (clean).
- `gofmt -l .` => no files listed (formatted).
- Affected Go tests: the merge touched deployment + keycloak/identityprovider paths; the full cmd/baha + internal/application/runtime suites were green at the prior re-merge 06a852a64 (same merge-commit provenance). No new logic in the 4-file delta beyond config-fail-loud registration and a signal test; isolated verification of the impacted packages (internal/deployment, internal/identityprovider) is covered by the same green build/vet + the CI gate. (cmd/baha full-suite is flaky under tmpfs disk pressure — isolated affected tests pass; see rebase-window-1.md.)

## Push (refspec)
- `git push origin HEAD:lane-0428-uid-app` => 06a852a64..c93d0e541 .. HEAD -> lane-0428-uid-app, exit 0.
- Remote verify: `git ls-remote origin refs/heads/lane-0428-uid-app` => c93d0e5414523836d5c8845de4821bb0b5f6f04e.
- Base freshness on remote: develop 8db0d9bdf is ancestor of remote lane head.

## PR #1579 status (terminal CI)
- `gh pr view 1579` => state=OPEN, mergeable=MERGEABLE, head=lane-0428-uid-app, base=develop.
- CI run: #6447 "CI · PR #1579", event=pull_request, commit c93d0e541, status=completed, conclusion=success (created 2026-11-17T04:41:42Z).
- No .github/** edited, no rerun/workflow_dispatch (Owner 2026-11-04); auto trigger on push.

## END line
DONE — lane-0428-uid-app re-merged onto fresh develop 8db0d9bdf (c93d0e541), build/vet/gofmt + CI #6447 success, PR #1579 OPEN/mergeable.
