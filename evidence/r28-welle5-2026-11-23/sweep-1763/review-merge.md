# PR #1763 review and merge record

## PLAN — PR #1763

- 327. Read the #1763 review/merge contract and create this numbered plan in the live board and Planning evidence.
- 328. Verify GitHub remotes, exact PR/base/head/develop refs, ancestry, mergeability, current check runs, and candidate immutability.
- 329. Confirm the exact changed files and develop catalog byte parity; verify .github is untouched.
- 330. Inspect the broker build identity mismatch message and regression assertion for truthful actual-version reporting.
- 331. Verify sentinel removal did not alter caller retry behavior.
- 332. Verify exact-head run 45131580969 through selected aggregate and required jobs; classify advisory and prior-run state.
- 333. Merge normally only if all acceptance points pass; otherwise record a repair recipe and stop.
- 334. Verify merge/develop refs or candidate immutability, record cleanliness, validate/publish evidence, update board, and post END.

## Session and scope

- ROLLE: REVIEW; merge withheld because acceptance fails.
- Mission: `/tmp/opencode/m_rev_1763.md.g`.
- Candidate PR: https://github.com/mcpdev80/baseharbor/pull/1763
- Candidate head: `60844a770a67dd6c4a86e85ed2292933e64a88da`.
- Session identity: codex-rev-1747; review time: 2026-11-23.
- Product remote resolution: `origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)`; only the GitHub URL was used for remote truth.
- Planning remote verification before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Live ref and ancestry witnesses

- Initial live refs: `b3df96348a9c56de00d67a060c9a5f0ddf6593d5 refs/heads/develop`; `60844a770a67dd6c4a86e85ed2292933e64a88da refs/pull/1763/head`.
- Final live refs: `826d498fc1ae9524112d07477a8809798d8272a7 refs/heads/develop`; `60844a770a67dd6c4a86e85ed2292933e64a88da refs/pull/1763/head`.
- PR API reports base `develop` at `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, candidate head unchanged at `60844a770a67dd6c4a86e85ed2292933e64a88da`, state OPEN, mergeable true, not merged.
- Candidate commit parents: `c62808054253dca4d0a0016ffe0b2bee10a8cf6d` and `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`; it contains the PR base as a parent.
- The base advanced after the tested run: live `develop` is now `826d498fc1ae9524112d07477a8809798d8272a7`; comparison against the current develop reports `ahead_by=15`, `behind_by=1`, `status=diverged`, merge base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`.
- No PR head changes were made. Merge was not attempted.

## Exact diff and contract review

- `git diff origin/develop...HEAD --name-only` equivalent from GitHub compare at base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`:
  - `cmd/baha/app_broker.go`
  - `cmd/baha/app_broker_diagnostics_test.go`
- Required `cmd/baha/app_broker_compat_test.go` is absent. The compare API and PR files API both report only two changed files. This fails the contract requiring exactly three paths; the diagnostics test file is not a substitute for the required compatibility test path.
- No catalog path and no `.github/**` path appears in the compare file list, so candidate changes do not alter catalog bytes or workflow files.
- The mismatch message in `cmd/baha/app_broker.go` includes `actualVersion` and `expectedVersion`: `runtime version %s incompatible with CLI version %s`. `TestRuntimeBrokerBuildIdentityMismatchReportsTrueRuntimeVersion` in `cmd/baha/app_broker_diagnostics_test.go` checks the observed value, the expected value, and that the observed value occurs once.
- Sentinel removal retains retry behavior: the readiness loop retries all errors except `errRuntimeBrokerIncompatible`; `waitRuntimeBrokerReady` also loops after non-nil errors until readiness or timeout. The new ordinary “healthcheck is not ready” error therefore remains retryable.
- Contract result: FAIL. The required compatibility test file is missing, and the tested PR base is no longer the live develop tip.

## Hosted checks

- Exact-head run: https://github.com/mcpdev80/baseharbor/actions/runs/45131580969
- Run `45131580969`: event `pull_request`, head `60844a770a67dd6c4a86e85ed2292933e64a88da`, base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, terminal `completed / success`.
- `PR · Trusted Plan` job `137548069033`: completed / success.
- `PR · Exact Candidate` job `137548146669`: completed / success.
- `PR Selected Checks` aggregate job `137556999798`: completed / success.
- Selected native Docker job `137548120926` and selected native Podman job `137548120939`: completed / success. Selected Go unit shards, `go-build`, `go-vet`, and `cli-gofmt` also completed / success.
- Candidate-added checks were skipped/advisory; skipped jobs were not counted as passes. Selected aggregate success is valid for the exact tested head and tested base only. It does not satisfy the contract after develop advanced.
- No workflow rerun or dispatch was triggered.

## Repair recipe

- Update the existing PR candidate so its base is the current `develop` tip; preserve the same PR/branch chain.
- Add the required `cmd/baha/app_broker_compat_test.go` regression to the same PR, asserting truthful actual runtime version reporting. Keep the existing regression only if it remains appropriately scoped and avoid duplicating assertions unnecessarily.
- Run a new CI evaluation on the resulting exact head and current base, then verify `PR · Trusted Plan`, selected required jobs, and terminal `PR Selected Checks` before requesting another review. Keep the PR unmerged until all three exact paths and the current-base proof pass.

## Cleanliness

- PID: `439462`.
- Before review: `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were started.
- After review: no test stack was started, so no compose cleanup was needed.

## repo-rule compliance

- Review used GitHub API/CLI remote witnesses and did not use the quarantined stale-ref checkout.
- No product repository files, workflow files, branches, or PR metadata were changed. No tests were run locally and no container was started.
- Evidence is stored only in the planning repository. Evidence contains no Markdown checkbox syntax.

## Verdict and handoff

- VERDICT: REQUEST CHANGES; do not merge PR #1763.
- Blocking findings: required `cmd/baha/app_broker_compat_test.go` is absent from the two-file diff; current develop is `826d498fc1ae9524112d07477a8809798d8272a7` while the PR and successful run still target base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`.
- END BLOCKED codex-rev-1747: review complete; repair the same PR candidate and obtain current-base exact-head CI proof. Candidate SHA `60844a770a67dd6c4a86e85ed2292933e64a88da`.

## Planning publication witness

Exact output from the required origin/main tree check:

`evidence/r28-welle5-2026-11-23/sweep-1763/review-merge.md`
- After review `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were started. Post-review command PID: `447167`.
- Planning `origin/main` delivery witness after evidence publication: `faf2e02cfc0b833289328d056700ad80e316622f refs/heads/main`.
