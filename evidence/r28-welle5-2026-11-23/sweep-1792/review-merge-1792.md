# PR #1792 review and merge record

## PLAN — PR #1792
- 295. Read the #1792 review/merge contract and create the numbered plan in the live board and Planning evidence.
- 296. Verify the GitHub remote, exact PR head/base/current develop refs, ancestry, merge state, and immutable diff.
- 297. Confirm the catalog delta is exactly nine intended source-pull rows, 62 insertions and zero deletions, with no duplicate IDs or paths and release unchanged.
- 298. Verify exact-head run 45103750422 through terminal state and inspect required job conclusions; treat 45101821205 as diagnostics only.
- 299. Confirm the hosted validator job reports the catalog valid and that no content, workflow, or unrelated file changed.
- 300. Record the forward-row coverage caveat and exact review verdict; merge normally only if every gate passes.
- 301. Verify merge SHA/develop refs or record a repair recipe, then validate and publish the Planning evidence.
- 302. Update the board and post the final END status with candidate SHA.


## ROLLE: REVIEW

Session: codex-rev-1747 (Codex / GPT-6-Luna); backend identifier not exposed. Review time: 2026-11-23 03:13 UTC.

### Candidate identity and scope

The product remote names `origin` and `lane-origin` resolve to `https://github.com/mcpdev80/baseharbor.git`. Planning remote, checked before the evidence commit:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Live product refs before review decision:

```text
1b7598aef8c4cae33b77c8523872637090d0f2bf	refs/heads/develop
a2bbeaefb34583f0a5d6c1b8483e8350169d516e	refs/pull/1792/head
```

PR #1792 is open, ready, mergeable/clean; base SHA is `1b7598aef8c4cae33b77c8523872637090d0f2bf`, head is `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`. GitHub compare reports merge base equal to the exact develop base, `ahead_by: 2`, `behind_by: 0`. Its only changed file is `scripts/pr-gate-coverage.json`, with 62 additions and zero deletions. There are no content files, `.github/**` files, or release field edits.

The two commits after the base are the task's catalog commit `59b5960694d5945583675ec1efb104325199edfa` (`ci(0428-061): catalog source-pull paths...`) and a merge commit `a2bbeaef...` whose second parent is the exact develop base. The latter has no additional file delta; no foreign product change is carried in the compare.

### Catalog inspection

I fetched the JSON at exact base and head through GitHub Contents API and compared the `components` arrays. Base: 219 rows, 219 unique IDs and paths. Candidate: 228 rows, 228 unique IDs and paths. The delta is exactly nine additions, zero deletions, zero modified rows; duplicate candidate IDs and paths: none. `release` remains `v0.4.27` at both refs.

The nine paths are `cmd/baha/app_pull.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/app_pull_options_test.go`, `cmd/baha/app_pull_mcp_approval_regression_test.go`, `cmd/baha/mcp_lifecycle_extra.go`, `internal/development/source.go`, `internal/development/source_pull.go`, `internal/development/source_pull_test.go`, and `internal/machine/contract.go`. Their surfaces match the requested groups: the four app-pull paths have both Docker and Podman data-capabilities; `mcp_lifecycle_extra.go` has `gate.mcp`; the three development source paths and machine contract have both Docker and Podman observability. These are intentional forward rows admitting #1752 after the ingress PR merges, as the mission specifies.

### Exact-head CI

Run `45103750422` is terminal `completed/success` for exact head `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`; the earlier diagnostic run `45101821205` was not used. Direct job results include:

- `PR Selected Checks` 137460729501: success.
- `PR · Trusted Plan` 137460226708: success.
- `PR · Native gate plan` 137460226892: success.
- `PR · Source format` 137460226811: success.
- `PR · Focused Python` 137460293022: success.
- Validation jobs `ci-executor-tests` 137460293142, `ci-policy` 137460293173, `receipt-execution-tests` 137460293185, and `pr-planner-tests` 137460293222: success.
- `PR · Candidate-added checks (advisory)` 137460293078: success, but it reports: `No candidate-added validation checks. The trusted base plan remains the only merge requirement.`

Skipped unrelated release, Go-unit, and runtime cells are not counted as passes. The exact-head required aggregate is green, but it does not satisfy the mission's additional candidate-catalog validator requirement.

### Blocking acceptance gap and Owner-scope finding

The mission requires the hosted job to validate the candidate catalog and emit the catalog-valid result. No such output appears in run `45103750422`. In the hosted `PR · Native gate plan` log, the selector loads `scripts/validate-pr-gate-coverage.py` and `scripts/pr-gate-coverage.json` from `$BASE_SHA` (`.github/workflows/ci.yml:503-510`), not the candidate. The trusted-plan path also takes policy inputs from its trusted controller (`.github/workflows/ci.yml:865-869`). The successful advisory log explicitly says that no candidate-added validation checks ran. Therefore the nine new rows were not semantically validated by the hosted run, even though I confirmed their JSON shape, uniqueness, release field and intended surfaces by read-only inspection.

Finding for the Owner: add a step to the existing hosted plan/validation job in `.github/workflows/ci.yml:503-510` that invokes the trusted base version of `validate-pr-gate-coverage.py` against the PR head's `scripts/pr-gate-coverage.json` and the trusted base release requirements, and require its `PR gate coverage catalog is valid` result. Keep the validator trusted from base; use the candidate file only as input. This workflow change is Owner scope, so I did not edit it, trigger a rerun, or dispatch a workflow.

VERDICT: BLOCKED — do not merge PR #1792 until the exact-head hosted candidate-catalog validation is present and successful. No product fix or content change is requested; the required repair is the Owner-scope hosted validation route above, followed by a terminal run on the exact candidate head.

## cleanliness

- Before: `docker ps -a --no-trunc`, shell PID 3512274; header only, no containers.
- After: `docker ps -a --no-trunc`, shell PID 3519760; header only, no containers.
- No Docker or Podman containers or compose projects were started.

END_BLOCKED codex-rev-1747: #1792 exact head `a2bbeaefb34583f0a5d6c1b8483e8350169d516e` is blocked pending hosted candidate-catalog validation; no merge attempted.

## origin/main evidence-path witness

Exact output of evidence/r28-welle5-2026-11-23/sweep-1792/review-merge-1792.md before publishing this review:

```text
evidence/r28-welle5-2026-11-23/sweep-1792/review-merge-1792.md
```
