# Evidence — t-20261123-planner-deleted-source-advisory (0428-253, lane w205-0428-253)

## Ansatz block (owner directive 2026-11-28, written before first commit)

- Card frontmatter owner VERBATIM (fetched from origin/main at runtime):
  `owner: ""` in `tasks/t-20261123-planner-deleted-source-advisory.md` at origin/main
  `be9495d4d9c40a48427092d5b52d5b4ada4384fb` (unassigned at claim time). The claim, published
  as plan commit `201fb31ab` on origin/main, set `owner: w205 (lane w205-0428-253)`; that is
  the owning-lane identity for candidate commits.
- git identity for every candidate commit: `user.name=w205`, `user.email=w205@baseharbor.local`.
- Literal commit invocation:
  `git -c user.name=w205 -c user.email=w205@baseharbor.local commit -m "..."`
- Pre-push identity gate (run before EVERY push; output under Delivery witnesses):
  `git show -s --format=%an HEAD` — printed `w205` for 90c8017b2 and for the
  base-refresh merge 3c1ebc6fc.
- Identity incident (reported, not hidden): the FIRST `git merge lane-origin/develop` in the
  shared-checkout-derived worktree inherited a FOREIGN worktree config identity
  (w198-0428-284-demo-parser) into the merge commit cc723b9b4. Per the admission rule I did
  NOT amend: `git reset --hard 90c8017b2` (my own commits only; cc723b9b4 was created by this
  lane seconds earlier), set `git config user.name w205` in the worktree, and re-merged →
  3c1ebc6fc authored `w205`. No foreign commit content entered the branch; the discarded
  merge object exists only as dangling local history.

## PLAN

- Read mission + full card contract (plan.py show + task file).
- Claim via scripts/plan.py claim in an isolated plan worktree; push only my claim rows (landed: plan commit 201fb31ab on origin/main).
- Fresh worktree off baseharbor origin/develop tip; cite cut-from SHA (99d9ddebc).
- Visible Ansatz block in board file + this akte before first commit (this section).
- Implement smallest sufficient scope: classify deleted sources before the uncataloged-source demand in scripts/pr-gate-plan.py (deletion_exemption helper) + statuses parameter in scripts/validate-pr-gate-coverage.py resolve_covered_gates; required Trusted Plan semantics untouched; no auth/consent change.
- Regression tests (package-discovered, CI-routed in this same PR): test_pr_ci_fallback.py, test_pr_gate_plan.py MappingTests, test_pr_gate_coverage.py, route-parity in test_ci_check_routes.py; registration in CI_CHECKS pr-planner-tests command, ci.yml route line, pr-check-runner.py CI_EXECUTION_SUITES.
- Prove branch provenance; draft PR to develop; push; watch own runs to terminal; two distinct green run IDs on exact final head.
- Evidence on origin/main before END post; END_DONE with head SHA + run IDs + PR number.

## Contract (tasks/t-20261123-planner-deleted-source-advisory.md, origin/main)

- Goal: the candidate-added validation lane treats a DELETED product source with a removed
  catalog row as resolved-by-deletion, not as an uncataloged change, so #1789-shaped PRs
  (advisory job 137410039120 red) no longer surface a red advisory while required Trusted
  Plan stays green.
- In scope: scripts/pr-gate-plan.py candidate-planner path resolving changed/deleted source
  rows (classify deletion before demanding an owner); one regression proving a deleted-source
  PR yields green advisory.
- Out of scope: required Trusted Plan semantics; .github workflows; catalog content of other
  PRs. Base-precedence policy stays.

## Reality witnesses

Plan repo remote (git action before first evidence commit):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Product checkout remotes (first git action; only github.com/mcpdev80 URLs used):

```
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` at cut time
  → `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82 refs/heads/develop`.
- Branch `lane-0428-253-planner-deleted-source` (worktree `workers/w205-0428-253-wt`) cut from
  exactly that ref (`git worktree add ... lane-origin/develop`, HEAD at cut 99d9ddebc).
- Ancestor proof: `git merge-base --is-ancestor 99d9ddebcfb6... HEAD` → true (before and
  after the base refresh to d766e49c2; `git merge --no-edit lane-origin/develop` transport,
  no force, no cherry-pick).

## Root cause (measured on develop 99d9ddebc)

- #1789 (merge e8acf7405) deleted `internal/metrics/perses_dashboards_promql_test.go` and
  removed its row from `scripts/pr-gate-coverage.json` plus its tuple from
  `scripts/test_pr_native_gate_plan.py`; it also touched comments in
  `internal/metrics/perses_dashboards_test.go`.
- ci.yml `pr_plan` sets `candidate_advisory_required=true` when any diff path starts with
  `.github/workflows/` or `scripts/`; `pr-candidate-advisory.py` re-plans the exact verified
  diff with candidate scripts. The candidate planner hit the 0428-242 fail-loud guard in
  `plan()`: `resolve_covered_gates` is path-only, so a deleted file whose catalog row was
  already removed has no owner row left and looks like a NEW uncataloged source. It raised
  `uncataloged source change, no declared runtime gate owner:
  internal/metrics/perses_dashboards_promql_test.go` — the red advisory job 137410039120.
- Reproduced before any change (develop 99d9ddebc): planning the deleted-source diff raises
  exactly the ValueError above.

## Implementation (exact writes, smallest sufficient)

- scripts/validate-pr-gate-coverage.py — `resolve_covered_gates(changed_paths, coverage,
  statuses=None)`: a path with status `deleted` is resolved by its deletion alone (neither
  demands a catalog owner nor selects gates). All other statuses behave exactly as before;
  the parameter is optional, existing callers unchanged.
- scripts/pr-gate-plan.py — helpers `_catalog_roots`, `_covered_by_catalog`,
  `deletion_exemption(diff, coverage)` and `_base_catalog_document`; in `plan()` the exemption
  map is computed before the fail-loud guard: (a) exempt when the checkout catalog owns the
  deleted path (exact row or package root); (b) deleted paths the checkout catalog no longer
  lists (row removed in the same PR — the #1789 case) are exempted only from the base catalog
  at the pr-diff-base-VERIFIED `target_base_sha`, read via `git show` from the trusted base
  checkout, and only under authenticated runner context
  (GITHUB_REPOSITORY=mcpdev80/baseharbor + supported target branch + 40-hex SHA); a failed
  lookup exempts nothing. A stale legacy `unknown impact for <exempted path>` marker is
  dropped from unresolved_coverage so the advisory replan resolves. Renames/copies keep their
  old_path owner demand; a source neither catalog view ever owned still aborts — never a
  deletion blanket. The pr-planner-tests CI_CHECKS command now names
  scripts/test_pr_ci_fallback.py (the suites carrying the regressions).
- Registration (same PR, GATE RULE): ci.yml `pr-planner-tests)` route line extended to the
  planner command's suite set (the route must equal the planner check — precedent job
  14144947258: a registered suite that misses its route silently never runs);
  pr-check-runner.py CI_EXECUTION_SUITES now includes test_pr_gate_coverage; the new
  route-parity test in test_ci_check_routes.py pins both sides. The ci.yml edit touches only
  that one route line — no trigger, job graph or required-plan change.
- scripts/release-requirements.json: NOT touched (no new gate id). No product Go code, no
  runtime, no auth/consent behavior changed.

## Tests added/changed (exact IDs)

- scripts/test_pr_ci_fallback.py (ConservativeFallbackTests):
  - test_deleted_source_with_base_cataloged_sibling_resolves_planner_green — #1789-shaped
    replay incl. the real base-catalog read at e8acf7405^ (skip-guarded if the object is
    absent) + unknown-context fail-loud case.
  - test_lone_deleted_uncataloged_source_still_fails_loud — deletion-only uncataloged change
    sets still abort.
- scripts/test_pr_gate_coverage.py (CoverageCatalogTests):
  - test_deleted_source_without_catalog_row_resolves_by_deletion
  - test_deleted_source_selects_nothing_even_with_remaining_catalog_row
  - test_status_map_never_exempts_non_deletion_statuses
  - test_planner_deletion_exemption_contract (unit: rule a exact row / package root,
    never-owned, non-deleted statuses)
- scripts/test_pr_gate_plan.py (MappingTests):
  - test_deleted_source_with_removed_catalog_row_resolves_planner_green (end-to-end green
    on the trusted base-catalog read + fail-loud for never-owned deletions)
- scripts/test_ci_check_routes.py (CheckRoutingTests):
  - test_planner_validation_route_includes_planner_and_coverage_suites (pr-planner-tests
    command contains the suites; ci.yml route line == planner command file set)

## CI mapping (which job runs each test, under which trigger)

- `pr_validations` check `pr-planner-tests` (pull_request, non-draft, develop/lane-*/cli2-*/w0*):
  `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pr_gate_coverage.py
  scripts/test_pr_ci_fallback.py scripts/test_pre_release_runtime_reuse.py` (command from
  pr-gate-plan.py CI_CHECKS, executed via the ci.yml route line, both updated in this PR).
- `pr_validations` check `ci-executor-tests` (same trigger): trusted-runner roster
  CI_EXECUTION_SUITES — includes test_pr_gate_coverage (added here) and test_pr_ci_fallback.
- `source_format` job "Run all discovered Python validation tests"
  (`find scripts -maxdepth 1 -name 'test_*.py'`): discovers and runs all touched test files
  on every non-draft PR — the package-discovery route the card demands.
- `pr_focused` job explicitly runs test_pr_ci_fallback.py + test_ci_check_routes.py.
- Positive selection: this PR touches scripts/** so pr-planner-tests + ci-executor-tests are
  selected for it; negative/non-selection behavior is pinned by the existing suite that
  stayed green (test_unknown_never_auto_selects_full_release_catalog).
- Mapping-selection proof: required checks come from the BASE plan (unchanged); the checks
  this PR (re)registers run on this candidate and are the card's own acceptance gate.

## Provenance

- `git merge-base --is-ancestor origin/develop(=d766e49c2 fetched) HEAD` → true (see above).
- `git log --oneline lane-origin/develop..HEAD` → exactly:
  `3c1ebc6fc Merge remote-tracking branch 'lane-origin/develop' into lane-0428-253-planner-deleted-source`
  and `90c8017b2 ci(planner): resolve deleted source rows by deletion...` — both authored by
  w205 (merge = transport of my own base refresh; no foreign commits on top).
- `git diff origin/develop...HEAD --name-only` → the eight files listed under Implementation
  + tests; equals `git diff-tree -r --name-only 90c8017b2`.

## Delivery witnesses

- Pre-push gate: `git show -s --format=%an HEAD` → `w205` (both commits, recorded above).
- Push delivery:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-253-planner-deleted-source`
  → `3c1ebc6fcb71334a85a32601939de1d128de56ba refs/heads/lane-0428-253-planner-deleted-source`
- PR #1853 (draft at push): gh pr view → `headRefOid=3c1ebc6fc... draft=true state=OPEN`.

## Hosted CI runs

- Run 45685219382, event pull_request, head 3c1ebc6fcb71334a85a32601939de1d128de56ba,
  triggered while the PR was DRAFT (draft-route jobs: Draft source and routing + Draft Go
  shards all success). Per the PROOF RULE this run is NOT the qualifying receipt; recorded
  honestly as the required second distinct run ID on the exact final head.
- Run 45690887363, event pull_request, head 3c1ebc6fcb71334a85a32601939de1d128de56ba,
  QUALIFYING (PR ready, draft=false; gh api pulls/1853 .draft==false verified after toggle).
  Watched to terminal: conclusion=success, zero failed/cancelled jobs. Key jobs:
  PR · Trusted Plan SUCCESS, PR Selected Checks SUCCESS (12s, job 139476883461),
  PR · Validation · pr-planner-tests / ci-executor-tests / ci-policy / ci-actionlint /
  receipt-execution-tests all SUCCESS, PR · Focused Python SUCCESS,
  PR · Candidate-added checks (advisory) SUCCESS (job 139475830545 — the card's goal: the
  deleted-source advisory lane replans green on this very candidate).
  Heavyweight runtime/HA/journey jobs correctly SKIPPED (this PR's base plan selects no
  native runtime gates; scripts-only change set).
- Aggregate terminal observed by this lane: `gh run view 45690887363` → completed success;
  `gh pr checks 1853` → "PR Selected Checks pass".
- ci-fast-check.sh before the final push: exit=0 (324 tests OK; log retained at
  /tmp/opencode/w205-fast2.log).

## repo-rule compliance

- One candidate branch (named in mission lineage: lane-0428-253-planner-deleted-source), one
  PR (#1853), draft until gate complete. No subagents. No containers or VMs (docker not
  installed on this coordinator host; `docker ps -a` → command not found).
- Test execution is Hosted CI only; local `python3 -m unittest` runs were development-time
  precheck diagnostics with named modules/classes (no bare package tests, no lifecycle
  triggers).
- Evidence lives only in baseharbor-plan (this file); nothing planning-related in the product
  branch; no main-branch writes in the product repo.
- Stop-Kriterien checked: NO merge conflict with w198 chain files — scripts/pr-check-runner.py
  touched only in the CI_EXECUTION_SUITES tuple; scripts/release-requirements.json untouched;
  scripts/pr-gate-plan.py edited per this card's own scope (this IS the card's file).
- Base refresh transport: `git merge origin/develop` + normal push (rule of 2026-11-25);
  no force, no cherry-pick.

## Handoff

- Branch: lane-0428-253-planner-deleted-source (worktree workers/w205-0428-253-wt)
- PR: https://github.com/mcpdev80/baseharbor/pull/1853 · head 3c1ebc6fcb71334a85a32601939de1d128de56ba
- Review queue: w200/w136.
- Card state: the mission's claim step covered claim→active; review-column movement and prs
  rows are coordinator publishing (card-status.py), noted here as handoff state, not edited
  by this lane.

## cleanliness

- pid witness: coordinator-host shell pid recorded in the lane transcript.
- `docker ps -a` before/after on this coordinator host: docker CLI not installed →
  "command not found" (empty before and after); this lane started NO containers, NO compose
  projects, NO VM/SSH.
- Untracked residue `internal/application/prune-*`, `trace-*` directories in the worktree
  predates this lane (other lanes' test fixtures; reported, untouched, never committed).

## END

END w205-0428-253 DONE — candidate 3c1ebc6fcb71334a85a32601939de1d128de56ba, PR #1853
(ready), qualifying run 45690887363 success (PR Selected Checks pass), second run on exact
head 45685219382 success (draft-route, non-qualifying, recorded). Handoff to w200/w136
review queue.
