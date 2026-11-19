# 0428-144 · Documentation selector mapping

## Change

PR [#1705](https://github.com/mcpdev80/baseharbor/pull/1705) maps `docs/internal/**/*.json` and `docs/example/**/*.{yml,yaml}` to the existing `DOC_CHECKS` selection in `scripts/pr-gate-plan.py`. It adds positive selector tests for internal JSON (including nested files), `.yml`, and `.yaml`, plus negative checks for unrelated JSON/YAML paths. No workflow or new gate was added.

## Exact candidate and integration

- Exact PR head: `0b5dd34713fe778aaf4d79dfa0b2a0600fc50e6a`
- PR base: `ab77e29d7c1cf981777e1069e51dfff82ffcf654`
- Hosted run: [44619193702](https://github.com/mcpdev80/baseharbor/actions/runs/44619193702)
- Merge commit: [28fb427f057499efca705c1b7459e7653bd532a8](https://github.com/mcpdev80/baseharbor/commit/28fb427f057499efca705c1b7459e7653bd532a8)

## Test → check → trigger → result

- `MappingTests` in `scripts/test_pr_gate_plan.py`, run via `scripts/ci-fast-check.sh` → local check → exact worktree at PR head → 286 tests passed.
- `scripts/test_pr_gate_plan.py` → `PR · Validation · pr-planner-tests` → pull request on `develop` → SUCCESS in run `44619193702`.
- `PR Selected Checks` → trusted target-base selection → pull request on `develop` → SUCCESS in run `44619193702`.
- `scripts/ci-workflow-policy.sh` / source formatting → `PR · Validation · ci-policy`, `Workflow policy`, `PR · Source format` → pull request on `develop` → SUCCESS in run `44619193702`.
- `PR · Native gate plan`, `PR · Trusted Plan`, `PR · Focused Python`, `PR · Validation · ci-executor-tests`, `PR · Validation · receipt-execution-tests`, and candidate-added advisory checks → same exact-head PR event → SUCCESS in run `44619193702`.

No full release, Docker/Podman native runtime, or unrelated service matrix is claimed; those jobs were skipped because the change only affects path selection and its unit coverage.

## Remaining acceptance witness

A local trusted-base simulation after merge used develop `28fb427f057499efca705c1b7459e7653bd532a8`, target head `708f5c5c8acee5133e480d151544cb139bb3ded`, and the three `docs/internal/*.json` changes. `scripts/pr-diff-base.py` plus the trusted planner returned `coverage_status=resolved` and selected `documentation-audit`, `mkdocs-de-strict`, `mkdocs-en-strict`, and `pages-candidate-build`. This confirms the mapping now routes the paths; it is not hosted execution evidence.

This fix enables the existing docs audit selection. Dependent PR [#1697](https://github.com/mcpdev80/baseharbor/pull/1697) was still based on `1019190d8dc0ecac7693f3461153e76be0e2cb8a` at this evidence snapshot. Its old run `44559589447` did not execute `documentation-audit`, so it cannot witness the mapping. After #1705 merged, #1697 must hop to the new `develop` and a fresh exact-head run must show `documentation-audit` executed successfully for its `docs/internal/*.json` changes. Until that proof is recorded, 0428-144 remains active and is not accepted.
