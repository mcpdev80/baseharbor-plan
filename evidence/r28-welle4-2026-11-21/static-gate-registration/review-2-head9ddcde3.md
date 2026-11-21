# CODEX-REVIEW evidence: PR #1746 round 2

## PLAN

1. Finish the active #1702 exact-head review and publish its terminal evidence.
2. Complete the intervening #1625 r2 review and publish its terminal evidence.
3. Recheck PR #1746 and its pre-release gate run at the exact assigned head; abort or wait if the head differs or the gate is nonterminal.
4. Review pre-release workflow scope, static release suite preservation, fail-closed proof, and required follow-up/identity data.
5. Publish the exact-head #1746 review evidence with terminal run states, render/check, and origin/main witnesses.

## STATE — stop on failed required gate

The two assigned runs are terminal on the exact PR head, but the second run failed. Per the workflow-scope rule, I am recording the failing check state and stopping before the remaining code verdict review.

- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1746/head`:

  ```text
  d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3	refs/heads/develop
  9ddcde356e9ed452ddbf00440ab8189add586d3e	refs/pull/1746/head
  ```

- PR #1746 remains at exact head `9ddcde356e9ed452ddbf00440ab8189add586d3e`; assigned develop base is `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`.
- Run `44943804395` (`workflow_dispatch`, Release - Pre-Release Validation): completed/success on the exact head. 39 jobs total: 17 success, 22 skipped, 0 failure. Successful named cells include `Source · Candidate and Gate Plan`, `Source · Format and Readability`, `Docs · Workflow and Release Validation`, `Source · Go Tests · cli-0`, `Source · Go Tests · cli-1`, `Source · Go Tests · cli-2`, `Source · Go Tests · cli-3`, `Source · Go Tests · packages`, `Source · Go Vet`, `Static · ci-fast-check / Executed static · ci-fast-check`, `HA groups · All runtime results`, `runtime heavy gates · All runtime results`, `runtime light gates · All runtime results`, and terminal `Pre-Release Checks` job `136968438679` success.
- Run `44944570763` (`workflow_dispatch`, Release - Pre-Release Validation): completed/failure on the same exact head. 44 jobs total: 17 success, 5 failure, 22 skipped. Successful precondition cells included `Source · Candidate and Gate Plan` job `136968932542`, `Source · Format and Readability` job `136969074184`, `Static · agent / Executed static · agent` job `136970241298`, and `Static · ci-fast-check / Reused static · ci-fast-check` job `136970291142`. Runtime result aggregates `HA groups · All runtime results`, `runtime light gates · All runtime results`, and `runtime heavy gates · All runtime results` also succeeded.
- Failing required cells: `Static · shell-ux / Executed static · shell-ux` job `136970241182`; `Static · init / Executed static · init` job `136970241191`; `Static · config-matrix / Executed static · config-matrix` job `136970241203`; `Static · mcp / Executed static · mcp` job `136970241277`; and `Pre-Release Checks` job `136970326775`.
- Failing log line from `Pre-Release Checks` step `Require selected checks to succeed` at 2026-11-21T20:12:24Z: `AssertionError: static_gates: expected success, got failure`. The aggregate’s preceding summary lists `ONLY_GATES: atomic/static/config-matrix,atomic/static/init,atomic/static/mcp,atomic/static/agent,atomic/static/shell-ux,atomic/static/ci-fast-check`. The individual static job log endpoints returned no lines in `gh run view --log`; no further cause is inferred.

## Finding: release workflow coverage scope

The addendum records six zsh/fish installation lines in `.github/workflows/pre-release.yml`, including lines 37 and 39, that are not covered by `scripts/ci-fast-check.sh`; the script has no zsh/fish references and actionlint runs with `-shellcheck=`. These workflow lines are Owner scope and were not changed. Required follow-up: Owner must supply the explicit scope release or add the six lines to an allowed, effective static validation route; then rerun the assigned release validation. No workflow rerun or dispatch was triggered by this review.

## Repo-rule compliance

- Reviewer-only: no product files changed, no local product tests run, no workflow dispatch/rerun, no product push, and no subagents used.
- Planning remote identity before the evidence commit: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Planning evidence path: `evidence/r28-welle4-2026-11-21/static-gate-registration/review-2-head9ddcde3.md`.
- `python3 scripts/plan.py render`: completed successfully.
- `python3 scripts/plan.py check`: 663 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 11 dependency warnings.
- Evidence checkbox scan: clear.
- Planning main ls-remote after first evidence push: `75a7eda7e5b638447a21b4fafa038f1ccf54d56a\trefs/heads/main`.
- Planning main ls-remote after path-witness push: `29d2d12da462ed63edd033a5c73db3b340210e4e\trefs/heads/main`; the same check confirmed this evidence path in fetched `origin/main`.
- Required `git fetch origin main && git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/static-gate-registration/review-2-head9ddcde3.md'` output before the final evidence push:

  ```text
  evidence/r28-welle4-2026-11-21/static-gate-registration/review-2-head9ddcde3.md
  ```

## cleanliness

- Before review: pid 3480580; `docker ps -a` showed eight pre-existing `bh-itest-*` containers, all exited. No containers were started by this review.
- After review: pid 3483253; `docker ps -a` listed the same eight pre-existing containers, all exited. No container state changed.

## END BLOCKED

END codex-rev-1747 BLOCKED — STATE: run 44944570763 failed required static gates and Pre-Release Checks on exact head `9ddcde356e9ed452ddbf00440ab8189add586d3e`; no code verdict issued.
