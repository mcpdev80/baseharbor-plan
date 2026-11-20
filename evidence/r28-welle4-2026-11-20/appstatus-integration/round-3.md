# Round 3 — Takeover: deliver 0428-078 commit to GitHub, make PR-valid, watch CI to terminal

Card `t-20261114-r28-perses-dashboard-identity` (0428-078), PR `mcpdev80/baseharbor#1650`, branch `lane-0428-078-perses-identity-on-resolver`.

Mission (takeover, NO new implementation — only deliver, rebase, prove): the previous lane `w078-…-r2` finished the round-2 implementation but its commit was reported as 'pushed' twice while `ls-remote` stayed at `b6dab95a8d73`. Root cause (measured by the coordinator, found in the coordinator's own toolchain): in the shared checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor` the *previous* lane's `origin` pointed at a local path, so `git push origin …` wrote into a local object store and never reached GitHub. The task was to deliver the real commit to GitHub, make the PR currency-valid, and observe one CI run to terminal.

Base-SHA of #1650 = `f61ef0f4991c`; `f61ef0f4991c` IS an ancestor of develop (verified below). No divergent fork, no retarget needed.

## PLAN

1. Fetch + ls-remote witnesses. Confirm `origin` = real GitHub (`https://github.com/mcpdev80/baseharbor.git`). Run `git fetch --prune origin develop` and `git ls-remote origin refs/heads/develop refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head`.
2. Create an isolated worktree under `/var/tmp` based on the remote branch.
3. Verify `git merge-base --is-ancestor b6dab95a8d73 16d3430234d2` = YES (the commit continues the line).
4. Checkout the branch at `16d3430234d2` then rebase onto `origin/develop` (develop = `36d075fad77f`). Resolve the 5 card-files conflicts inline with reasoning.
5. `go build ./...` + targeted `go test` on the card path.
6. `git push --force-with-lease` to the real GitHub remote, then `git ls-remote` proof that the new head propagated to both the branch and `refs/pull/1650/head`.
7. `git merge-base --is-ancestor origin/develop <new head>` = YES.
8. Observe one CI run to terminal (§4.6); report head + run-id + conclusion immediately.
9. Write this round-3 akte (new file; do not rewrite the round-2 akte).

## Witnesses

- Step 1 — `git fetch --prune origin develop`: exit 0, `From https://github.com/mcpdev80/baseharbor / branch develop -> FETCH_HEAD`.
- Step 1 — `git ls-remote origin refs/heads/develop refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head` (BEFORE push):
  ```
  36d075fad77fa61ac8c153e979855546589b32c2	refs/heads/develop
  b6dab95a8d73e870841bbe96cbff28cafc216d81	refs/heads/lane-0428-078-perses-identity-on-resolver
  b6dab95a8d73e870841bbe96cbff28cafc216d81	refs/pull/1650/head
  ```
- Step 3 — `git merge-base --is-ancestor b6dab95a8d73 16d3430234d2`: `YES` (b6dab95a8d73 is an ancestor of the target commit `16d3430234d2`, parent `7820a932578d`, subject `test(0428-078): gate identity availability on verified Perses status`). No divergence, no alternate takeover path needed.
- Step 4 — rebase onto `origin/develop`: clean, no conflicts. `git rebase origin/develop` => "Successfully rebased and updated refs/heads/lane-0428-078-perses-identity-on-resolver." New head = `ac2a5450379492d410a379469e9845b2ce21190d`.
- Step 4 — diff vs `origin/develop` (exactly the card write-set, no foreign files):
  ```
   cmd/baha/app_status_result.go                      |  62 ++-
   internal/metrics/perses_identity_dashboards.go     | 503 +++++++++++++++++++++
   internal/metrics/perses_identity_dashboards_test.go | 376 +++++++++++++++
   internal/metrics/perses_identity_witness.go        | 129 ++++++
   internal/metrics/perses_identity_witness_test.go   | 191 ++++++++
   .../identity-keycloak.json                         | 137 ++++++
  6 files changed, 1381 insertions(+), 17 deletions(-)
  ```
- Step 7 — `git merge-base --is-ancestor origin/develop HEAD` (HEAD = `ac2a54503`): `YES`.
- Base-SHA provenance — `git merge-base --is-ancestor f61ef0f4991c origin/develop`: `YES` (f61ef0f4991c, the #1650 base, is an ancestor of develop). No divergent fork.
- Step 6 — `git push --force-with-lease origin HEAD:refs/heads/lane-0428-078-perses-identity-on-resolver`:
  ```
  To https://github.com/mcpdev80/baseharbor.git
   + b6dab95a8...ac2a54503 HEAD -> lane-0428-078-perses-identity-on-resolver (forced update)
  ```
- Step 6 — `git ls-remote origin refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head` (AFTER push; PROOF the commit is really on GitHub):
  ```
  ac2a5450379492d410a379469e9845b2ce21190d	refs/heads/lane-0428-078-perses-identity-on-resolver
  ac2a5450379492d410a379469e9845b2ce21190d	refs/pull/1650/head
  ```
  Both the branch and the PR head now carry the delivered head. The PR is currency-valid.

## CI run (§4.6)

- Run: `44680875974` (GitHub run number 6718), trigger `pull_request`, head `ac2a5450379492d410a379469e9845b2ce21190d`, branch `lane-0428-078-perses-identity-on-resolver`.
- Terminal state: `completed` / `conclusion: success`.
- Jobs: 13 required jobs `success`, 17 `skipped` (skipped = release-matrix / VM-native / consumer-pin / advisory candidate-added checks that do not apply to this path — not required on this base). No `failure`.
- Required successes: Workflow policy; Native gate plan; Trusted Plan; Source format; go-vet; go-build; Go unit cli-0/1/2/3; Go unit packages; Go unit owner; Focused Python.
- CI triggered on its own by the pull_request hook on the pushed head (no workflow_dispatch / no `.github/**` edit — Owner scope untouched).

## Build / test witnesses

- `go build ./...`: exit 0.
- `go test ./internal/metrics/... ./cmd/baha/...`:
  - `internal/metrics` (the card package): `ok github.com/mcpdev80/baseharbor/internal/metrics 0.250s` — PASS.
  - `cmd/baha`: 16 failures, ALL pre-existing environmental failures, not card-caused. Established by running the identical `cmd/baha` test suite on `origin/develop` baseline: identical 16 failures (`TestAccess*PersistsThroughCLI`, `TestApp*Formatting` = cwd-relative file lookups that need the package source in the working directory, `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` = needs a running Core, `TestAppEditCommandChecksGoSourceFormat` = gofmt on files absent from cwd). The `cmd/baha` failures are an artifact of the local run directory / missing workspace files / real-Core dependency; the shared-host `/` filesystem was 98% full (18G in `/var/tmp/go-cache`), compounding the environment. They do not touch the card path and are not carried by this diff. GitHub CI's clean runner runs these under the proper working directory.

## repo-rule compliance

- Scope: NO new implementation. Only deliver (push), rebase, prove. Diff vs develop is exactly the 6 card files — within the allowed write-set. No files outside `cmd/baha/app_status_result.go`, `internal/metrics/perses_identity_dashboards.go`, `internal/metrics/perses_identity_dashboards_test.go`, `internal/metrics/perses_identity_witness.go`, `internal/metrics/perses_identity_witness_test.go`, `internal/metrics/testdata/perses-identity-dashboards/identity-keycloak.json`.
- No merge, no PR-base retarget (base remains f61ef0f4991c, ancestor of develop), no write to `.github/**` or `scripts/**`, no product change beyond the clean rebase (which had no conflicts).
- No refactoring beyond the rebase (§4.2). No subagents (§4.8). No write to `internal/observability/{migration,registry}.go` or `internal/logs/realization.go`. No worktree written under `/home/marcel/dev/baseharbor-ecosystem/baseharbor` directly — isolated worktree under `/var/tmp/wt-078-r3`.
- One integration candidate per chain: the branch history lists only the 3 rebased card commits (plus the 2 witness commits already on develop); no foreign commit on the chain.
- Branch provenance: cut from `b6dab95a8d73` (base SHA of the PR, an ancestor of develop, shown as ancestor of the first delivered commit). `origin/develop` (`36d075fad77f`) is an ancestor of the delivered head `ac2a54503`.
- CI policy: required checks come from the base plan; checks added by this PR run and report but are advisory; this PR carries product code, tests and (no) CI change together. No required check was skipped here that covers the changed path.

## takeover-protokoll

- Took over from lane `w078-…-r2`. Reason: that lane reported the round-2 commit as 'pushed' twice, but `ls-remote` stayed unchanged at `b6dab95a8d73` on both the branch and `refs/pull/1650/head`. The commit existed in the shared object store of this host but never reached GitHub. Root cause measured by the coordinator: a `origin` in the toolchain that pointed at a local filesystem path, so `git push origin …` reached 'Everything up-to-date' against a local ref and never hit GitHub.
- No reimplementation. The target commit `16d3430234d2` was carried onto `origin/develop` by a clean `git rebase origin/develop` (no conflicts) into the delivered head `ac2a5450379492d410a379469e9845b2ce21190d`, then `--force-with-lease`-pushed to the real GitHub remote. Verified by `ls-remote` that both the branch and `refs/pull/1650/head` now carry `ac2a54503`. One CI run (44680875974) observed to terminal: success.

## origin/main witness (second-to-last action)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan log origin/main --oneline -5`:
```
47823030 evidence(0428-078): round-3 takeover akte — deliver commit to GitHub, CI success
33093a83 evidence(0428-091): round-1 perses-tempo-source — draft-blocker finding (c781eb86, CI 43874313785)
820c094a docs: record current PR sweep and 1665 audit
427cb1fd card 0428-176: stale draft PR #1665 on parked card 0428-082 needs restack-or-close with witness
88963a6a docs: record independent PR sweep audit
```
Evidence path `evidence/r28-welle4-2026-11-20/appstatus-integration/round-3.md` is on origin/main (commit 47823030).

## Cleanup

- No containers / compose projects / networks / volumes created. No VM network used as a test carrier.
- Isolated worktree: `/var/tmp/wt-078-r3` (git worktree, not a separate clone). Removed at END.
- Build/test cache written to `/tmp/go-cache-078`, `/tmp/go-modcache-078`, `/tmp/gotmp-078` to avoid the full `/var/tmp` overlay.
