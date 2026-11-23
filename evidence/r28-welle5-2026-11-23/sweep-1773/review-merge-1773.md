# PR #1773 review and merge record

## PLAN — PR #1773
- 303. Read the #1773 review/merge contract and create the numbered plan in the live board and Planning evidence.
- 304. Verify the GitHub remote, current PR/base/head refs, ancestry, mergeability, changed paths, and candidate immutability.
- 305. Check the card-specific product/documentation diff and confirm catalog delta is empty with no .github or go.mod changes.
- 306. Verify exact-head run 45106857935 and all required job conclusions.
- 307. Inspect owning-shard logs for each card-named test and confirm actual execution by test-name lines.
- 308. Separate advisory results from required checks and record any exact failing log line.
- 309. Merge normally only if every acceptance point passes; otherwise record a repair recipe and stop.
- 310. Verify merge/develop refs or candidate immutability, validate and publish Planning evidence, update board, and post END.

## REVIEW — PR #1773

- Role: CODEX-REVIEW. Merge role not entered because an acceptance boundary fails.
- Session: codex-rev-1747. Model: GPT-6.2. Backend/session UUID: not exposed in this shell transcript.
- Review time: 2026-11-23 04:07 UTC.
- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Product remote was resolved before remote reads: `lane-origin https://github.com/mcpdev80/baseharbor.git`; all product refs below were read from that real GitHub URL or GitHub API.

### Live candidate and provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-246-footprint-human-doc refs/pull/1773/head` returned:
  - `cd9cc4836a69815a6cdcf7079902bafe5be1e000 refs/heads/develop`
  - `a014d35380bc6e0c3430710e94e587b82a1755a3 refs/heads/lane-0428-246-footprint-human-doc`
  - `a014d35380bc6e0c3430710e94e587b82a1755a3 refs/pull/1773/head`
- GitHub PR API: open, unmerged, base `develop` at `cd9cc4836a69815a6cdcf7079902bafe5be1e000`, head `a014d35380bc6e0c3430710e94e587b82a1755a3`, mergeable true, mergeable state `clean`.
- GitHub compare API for exact base...head reports merge base `cd9cc4836a69815a6cdcf7079902bafe5be1e000`, ahead 5, behind 0. This is the remote ancestry witness; the candidate did not carry a foreign base.
- Changed paths (eight): `cmd/baha/app_env_test.go`, `cmd/baha/app_export_command_test.go`, `cmd/baha/app_footprint_presenter.go`, `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `cmd/baha/installation_destroy_native_test.go`, `cmd/baha/target_definition_change_test.go`, `cmd/baha/test_operator_context_test.go`.
- No `.github/**`, `go.mod`, or `scripts/pr-gate-coverage.json` path changed. Catalog delta against develop is empty. Candidate remains at the same exact head; no product checkout changes were made by this review.

### Contract inspection and finding

Card `0428-246` (`tasks/t-20261122-footprint-human-surface-doc-gaps.md`) permits presenter comments/help and an existing test only when a string is asserted. It requires documenting the human-vs-machine status label mapping and noting that scope/ownership fields remain available through JSON/MCP. Its acceptance explicitly says: “No behavioral change to the JSON/MCP contract.”

The candidate violates that boundary in `cmd/baha/app_status_result.go`: it removes the `DatabaseDashboards` field with JSON tag `database_dashboards`, removes its collection, and removes its JSON output assignment. In `cmd/baha/app_perses_cli_test.go`, it deletes `TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases` and `TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed`, which covered that JSON surface. This is an externally observable JSON contract change, unrelated to explaining the human-readable curated subset. A clean mergeability state and green CI do not waive the card contract.

Review verdict: REQUEST CHANGES. Do not merge this candidate.

Repair recipe:
- In `cmd/baha/app_status_result.go`, restore the `database_dashboards` JSON field and its prior collection/output behavior.
- In `cmd/baha/app_perses_cli_test.go`, restore the two status JSON regression tests for unavailable databases and unverified targets.
- Keep the card implementation to the human presenter documentation/label mapping (and any test that asserts the new help/comment text); do not alter JSON/MCP behavior.
- Push a corrected candidate through the normal process, then run and observe the newly selected exact-head required CI and the owning validation shard. Stop before merge if the JSON regression reappears or the owning test shard is skipped/queued.

### Exact-head CI and test execution

- Run `45106857935`: `completed`, `success`, event `pull_request`, exact head `a014d35380bc6e0c3430710e94e587b82a1755a3`.
- Check-run census: 26 successful, 16 skipped. Selected aggregate `PR Selected Checks` succeeded. Successful required/selected checks included Trusted Plan, Native gate plan, Source format, Workflow policy, Focused Python, Exact Candidate, Runner Interface, Go unit cli-0/1/2/3/owner/packages, go-build, go-vet, cli-gofmt, presenter validation, and selected Docker/Podman data-capabilities and observability validations.
- Owning execution evidence: successful job `PR · Validation · wizard-footprint-presenter-tests`, job id `137470100349`. Its log at `2026-11-23T03:37:35.9340977Z` records `matched_tests` containing `TestAppFootprintPresenterEmptyAndCoreless`, `TestAppFootprintPresenterStatesAndDetails`, `TestAppFootprintPresenterMeasuredEstimatedUnknown`, `TestAppFootprintPresenterTransitiveAndIncomplete`, and `TestAppFootprintPresenterContextAuthorityAndNoSecrets`.
- Advisory classification: `PR · Candidate-added checks (advisory)` was skipped. This is not a pass or failure result and is not counted as a required check. The other skipped release/targeted groups likewise are not passes; the run's relevant selected required gates did execute and succeed.
- CI verdict: required selected checks and the named owning test shard passed for this exact head. CI does not resolve the contract violation above.

## repo-rule compliance

- Review was read-only against the product repository. No product files, workflow files, branches, PR metadata, or CI runs were changed or triggered.
- The existing product working tree has unrelated modified/untracked paths (`scripts/pr-gate-coverage.json`, `scripts/pre-release-check-plan.py`, `scripts/release-requirements.json`, `.last-owner-report`, `0428-211-hopdevelop-wt/`, and `QUEUE.md`); they were left untouched.
- Planning changes are limited to this review evidence and the requested live board plan.

## cleanliness

- Before review, `docker ps -a --no-trunc` under PID 3512274 printed only the header; no containers were present.
- After review, PID 3682196 ran `docker ps -a --no-trunc`; output was only `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES`. No containers were started.

## END codex-rev-1747 BLOCKED

PR #1773 remains open and unmerged at candidate `a014d35380bc6e0c3430710e94e587b82a1755a3`. Review is blocked by removal of the `database_dashboards` JSON/MCP surface contrary to card 0428-246. Required exact-head CI succeeded, but the contract repair above is required before merge.

## origin/main evidence-path witness

Exact output from `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle5-2026-11-23/sweep-1773/review-merge-1773.md` after fetching origin/main and before this evidence update was:

```text
evidence/r28-welle5-2026-11-23/sweep-1773/review-merge-1773.md
```
