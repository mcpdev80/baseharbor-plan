# PR #1763 delta review and merge record

## PLAN — PR #1763b

- 343. Read the #1763b delta-review contract and record the numbered plan in the board and evidence.
- 344. Resolve remotes and verify current PR head, base, develop, ancestry, additive-hop delta and exact changed files.
- 345. Inspect the build-identity diagnostic and regression evidence on the exact candidate.
- 346. Verify exact-head Trusted Plan, required jobs, terminal PR Selected Checks and native runtime jobs.
- 347. Squash-merge normally only if every delta and acceptance check passes; otherwise record a repair recipe.
- 348. Verify post-merge PR/develop refs and merge SHA; record docker cleanliness.
- 349. Validate and publish the delta evidence in baseharbor-plan, including the origin/main path witness.
- 350. Update the live board and post the final END with the verdict and candidate or merge SHA.

## Role and relation to the first review

- ROLLE: REVIEW; MERGE conditionally authorized by the mission.
- Mission: `/tmp/opencode/m_rev_1763b.md.g`.
- First review record: `evidence/r28-welle5-2026-11-23/sweep-1763/review-merge.md`.
- The first record was REQUEST CHANGES on the older comparison/base. This delta review evaluates the new candidate and its exact new base independently; it does not rewrite the earlier verdict.
- The old review's changed-file expectation is superseded by this delta contract: `app_broker_compat_test.go` is already present at base `b517b279c9533669c104dc6429c0a1934c508716`, so the PR diff against that base should contain only the two broker files.

## Remote and commit witnesses

- Product remote resolution: `origin` and `lane-origin` both resolve to `https://github.com/mcpdev80/baseharbor.git`; only the GitHub URL was used for remote truth.
- Planning remote verification before first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Mission candidate head: `b1b49890586f662b873eff0e6fac8d0d4a255fa3`.
- Mission base: `b517b279c9533669c104dc6429c0a1934c508716`.
- Candidate merge-hop parents: first parent `60844a770a67dd6c4a86e85ed2292933e64a88da` (the earlier content head), second parent `b517b279c9533669c104dc6429c0a1934c508716` (the develop hop).
- The two broker-file blob SHAs are identical between the earlier content head and the delta candidate:
  - `cmd/baha/app_broker.go`: `3da1b717465be86a8f05d7227546a66f728d8457` at both heads.
  - `cmd/baha/app_broker_diagnostics_test.go`: `8cdb6f4066183ac9700c4511a3a90d9583a85d64` at both heads.
- GitHub compare from mission base to candidate reports `ahead_by=16`, `behind_by=0`, merge base `b517b279c9533669c104dc6429c0a1934c508716`, and exactly:
  - `cmd/baha/app_broker.go`
  - `cmd/baha/app_broker_diagnostics_test.go`
- The candidate is a merge commit with precisely the prior content head and develop-hop parents; the current-base compare contains only those two broker files. No additional candidate-authored content change was found.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1763/head` before and after review (identical output):

```text
a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d refs/heads/develop
b1b49890586f662b873eff0e6fac8d0d4a255fa3 refs/pull/1763/head
```

- GitHub PR API reports #1763 closed and merged at `2026-11-23T09:05:28Z`; merge commit `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`; base was `b517b279c9533669c104dc6429c0a1934c508716`; source head was `b1b49890586f662b873eff0e6fac8d0d4a255fa3`.
- Squash commit `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d` has sole parent `b517b279c9533669c104dc6429c0a1934c508716` and exactly the two broker files. Live develop equals the squash SHA.
- The authorized normal squash merge was already completed remotely before this delta review finished. No second merge attempt was made.

## Broker mismatch diagnostic and hosted regression

- At candidate `b1b49890586f662b873eff0e6fac8d0d4a255fa3`, `cmd/baha/app_broker.go:663` formats the mismatch as `runtime version %s incompatible with CLI version %s`, passing `actualVersion` followed by `expectedVersion`. The observed runtime value is reported truthfully.
- `cmd/baha/app_broker_diagnostics_test.go:142-169` defines `TestRuntimeBrokerBuildIdentityMismatchReportsTrueRuntimeVersion`. It asserts actual `0.4.14`, expected `0.4.15`, and exactly one occurrence of the observed runtime value.
- The test has no skip. CI's `scripts/pr-go-unit-shard.py:28-40,64-81,101-115` discovers every top-level `cmd/baha` test, deterministically assigns this name to `cli-3` (SHA-256 first eight bytes modulo four), executes selected tests, and fails if any selected test is missing or neither passed nor intentionally skipped.
- Hosted run log for `PR · Go unit · cli-3`, job `137578349441`, reports: `PASS cli-3: 437 passed / 16 intentionally skipped / 453 discovered; CLI inventory total=1871`. The log summarizes the shard rather than printing each passing test name; the runner's JSON-event completeness checks cover the assigned test, and this test contains no `t.Skip` path.
- This is durable GitHub-hosted evidence for the regression; no local product test was run.

## Exact-head hosted checks

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/45140871554
- Run `45140871554`: pull_request event, exact head `b1b49890586f662b873eff0e6fac8d0d4a255fa3`, terminal `completed / success`.
- `PR · Trusted Plan`: job `137578262258`, completed / success.
- `PR · Go unit · cli-3`: job `137578349441`, completed / success.
- `PR · Native · native/docker/data-capabilities`: job `137578354602`, completed / success.
- `PR · Native · native/podman/data-capabilities`: job `137578354642`, completed / success.
- Selected runtime Docker job `137579032056` and Podman job `137579031997`: completed / success.
- `PR Selected Checks`: job `137587962693`, completed / success, GitHub Actions integration app ID `15368`.
- The exact-head run's selected jobs executed and passed. Skipped unrelated release/draft jobs were not treated as passes. Candidate-added checks were skipped/advisory and do not affect this acceptance.
- No rerun or workflow dispatch was triggered.

## Cleanliness

- Before review, `docker ps -a` returned only the header; PID `1516071`.
- After review, `docker ps -a` returned only the header; PID `1532807`. No containers or compose projects were started.

## Repo-rule compliance

- Review used GitHub API and `git ls-remote` against the resolved GitHub URL; no quarantined stale-ref checkout was used.
- No product files, workflows, PR metadata, or branch refs were changed by this review. No local product tests were run.
- Planning task status was not changed by this review.
- Evidence is kept only in `baseharbor-plan/evidence/r28-welle5-2026-11-23/sweep-1763/review-merge-delta.md`; no Markdown checkboxes are present.

## Literal verdict and END

- VERDICT: PASS — accept the #1763 delta. The broker content is unchanged from the earlier content head, the develop hop is the only candidate-history change, the exact new-base diff has the two expected broker files, and exact-head hosted checks passed. The authorized squash merge is already confirmed remotely as `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`.
- END DONE codex-rev-1747: #1763 delta review PASS; squash merge already verified. Merge SHA `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`.
