# CODEX-REVIEW: PR 1772 / 0428-245

## PLAN

1. Read the review contract and capture exact-head scope, acceptance criteria, evidence path, and read-only boundaries.
2. Verify live PR/base refs and exact-head changed-file list.
3. Inspect presenter code and default-mode regression for Unused-ID parity with JSON.
4. Verify exact-head run 45025731965 and required job terminal results.
5. Record verdict and merge witness, validate and publish this evidence on Planning origin/main, then post END.

## Review target and scope

PR #1772 is merged. GitHub reports base `develop` at `64eab13e23fba8bca07a1d68c687fa36afedb64e`, exact reviewed head `232ded21d6ab51cbd8e7b5a1214fd1877c4b551f`, and merge commit `62784eff7befadfaa8a08fc21eaffbd4e3cc8962`. The live product remote was verified as `https://github.com/mcpdev80/baseharbor.git`; all configured names observed (`origin`, `lane-origin`, `upstream`) resolved to that GitHub URL. Remote truth was checked with the direct GitHub URL. The exact head is the PR head and the base is the PR's recorded base SHA.

Exact base-to-head diff (`git diff 64eab13e23fba8bca07a1d68c687fa36afedb64e...232ded21d6ab51cbd8e7b5a1214fd1877c4b551f --name-only`):

- `cmd/baha/app_footprint_presenter.go`
- `cmd/baha/app_footprint_show_test.go`

Only the presenter and its regression test changed. There are no contract, data-model, guard, broker, unrelated card, script, or `.github/**` changes.

## Source and regression review

In `cmd/baha/app_footprint_presenter.go:51-58`, `renderAppFootprint` prints each `fp.Unused` instance ID and the count before the `!options.Details` early-return at line 59. The default human mode therefore retains the per-instance IDs rather than showing only a count. JSON/MCP parity is preserved because the human presenter emits those same `Footprint.Unused` IDs.

`cmd/baha/app_footprint_show_test.go:261-315` adds `TestAppFootprintShowHumanAndJSONAgreeOnUnused`. Its default human call at lines 276-279 omits `Details`; the test also renders details and JSON. With `Unused` set to `orphaned-cache` and `stale-queue`, it requires both IDs and the matching count in default human, details, and JSON output, and asserts private context metadata does not leak. This covers the default-mode regression and the same expected Unused IDs across both output surfaces.

## Exact-head CI evidence

Run `45025731965` is terminal `completed / success`, event `pull_request`, on exact head `232ded21d6ab51cbd8e7b5a1214fd1877c4b551f` ([run](https://github.com/mcpdev80/baseharbor/actions/runs/45025731965)). Selected required jobs are terminal success: `PR · Source format`, `PR · Native gate plan`, `PR · Trusted Plan`, `PR · Validation · source-contracts`, `PR · Validation · wizard-footprint-command-tests`, `PR · Validation · wizard-footprint-presenter-tests`, `PR · Validation · cli-vet`, `PR · Validation · cli-build`, and `PR · Validation · cli-gofmt`. The new regression is picked up by `PR · Validation · wizard-footprint-presenter-tests` on the `pull_request` trigger; the same run also executes the command tests and source-contract validation. Unselected matrices report skipped and are not claimed as passes.

## Verdict

APPROVE for exact head `232ded21d6ab51cbd8e7b5a1214fd1877c4b551f`: the two-file display-only scope is respected, default human mode renders the Unused IDs before its early return, the regression covers default human and JSON output, and all named exact-head required jobs completed successfully.

## CODEX-MERGE

The requested merge state is already present: GitHub reports PR #1772 `merged: true` with merge commit `62784eff7befadfaa8a08fc21eaffbd4e3cc8962`; a fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` returned the same SHA. No second merge action was issued.

## Repo-rule compliance

Read-only independent review. No product source changes, local tests, PR comment, close action, workflow rerun, or subagent action was performed. The review used exact-head GitHub diff/source, exact-head hosted CI jobs, and direct remote-ref witnesses.

## cleanliness

Before review, `docker ps -a --no-trunc` with shell PID 117984 showed only the header and no containers. This review started no container or compose project. After review, `docker ps -a --no-trunc` with shell PID 118745 also showed only the header and no containers.

## END_DONE

END_DONE: APPROVE; PR #1772 is already merged at `62784eff7befadfaa8a08fc21eaffbd4e3cc8962`, which is also the current `develop` head.
