# 0428-208 / #1746 — unfreeze final candidate (run to terminal)

## Candidate status: implementation + local validation COMPLETE; one base-policy gate blocker reported to coordinator (Owner scope)

Candidate head: `fde3468d42dde3e52f4627c38a501b0cf5305dff`
Parents: `c09ad378` (hop) -> `f0f38b5c` (commit 1) -> `fde3468d` (commit 2)
PR #1746 head (witnessed): `fde3468d42dde3e52f4627c38a501b0cf5305dff`
develop base: `e8acf740553f7218b259f4855f5b79f83f21ab6b` (= `15c652136` + `test(metrics) #1789`)

## What was delivered (2 commits, 5 files, 0 .github, 0 Go)

Commit 1 `f6d62ca1a` — ci(0428-208): move ci-fast-check requirement to v0.4.28 + release-only catalog + narrow validator future-coverage fix
Commit 2 `fde3468d4` — test(0428-208): align v0.4.28 release-selection test with single-gate move

Files changed by my commits only (verified `git diff f0f38b5c HEAD --name-only`):
- scripts/release-requirements.json: ci-fast-check required_for moved to [v0.4.28]; releases list gains v0.4.28 (only list-change); no other gate/release touched; requirement NOT deleted.
- scripts/pr-gate-coverage.json: release field stays v0.4.27; added release-only atomic/static/ci-fast-check catalog object (covers source.gate.atomic.static.ci.fast.check); dropped that surface from focused shell-ux; 63 catalog gates total; no blanket-adds.
- scripts/validate-pr-gate-coverage.py:249-250 (releases_prefix at line 124; future-coverage exclusion at 252-263): currently-required v0.4.27 gates stay mandatory (missing rule unchanged); catalog gates whose required_for lists only newer releases allowed as future coverage (no extra-fail); owner authorization cited in comment.
- scripts/test_pr_gate_coverage.py: 4 regression tests (future-only passes / missing-current fails / release field hard / missing-current-with-future-gate).
- scripts/test_pre_release_check_plan.py: renamed/aligned test_v0428 assertion to v0428 == {ci-fast-check} (was the blanket-add invariant).

## Local validation (all green)
- validate-pr-gate-coverage.py: "PR gate coverage catalog is valid"
- test_pr_gate_coverage.py: 45 passed, 55 subtests (includes my 4 new regression tests)
- test_pre_release_check_plan.py: 5 passed, 11 subtests
- test_ci_v0427_gate_catalog.py: 7 passed, 68 subtests
- test_pr_native_gate_plan.py: 13 passed; test_pr_stage_boundary.py: 10 passed; test_pr_gate_dependencies.py: 5 passed
- targeted validator/coverage subset in test_pr_gate_plan.py: 30 passed
- ci-fast-check.sh: PASS
- 0 Go files changed (Python/JSON only)

## Hosted CI run 45102450630 (head fde3468d) — TERMINAL STATE + blocker

Run: 45102450630 | conclusion: failure | event: pull_request
Jobs: 34 success, 72 skipped, 1 failure. Every executed job succeeded.

Failing job: `PR · Selected Checks` (aggregate, job 137460950188) — completed failure
Root-cause log line (ci-executor / aggregate):
  BLOCKED: selected gate has no workflow executor: atomic/static/shell-ux

Diagnosis:
- The `atomic/static/shell-ux` gate is a pre-existing, PR-scoped focused gate present in the base
  develop coverage unchanged (verified `git show origin/develop:scripts/pr-gate-coverage.json`).
- Base policy `scripts/pr-required-final.py` lines 76-84 maps only
  `atomic/{docker,podman}/*`, `integration/static/public-contracts`, and
  CORELESS_LIFECYCLE_GATES to workflow executors. Every other `atomic/static/*` gate (including
  shell-ux) falls through to `else: errors.append('selected gate has no workflow executor')`.
- This is a SHARED BASE-POLICY file (scripts/pr-required-final.py) OUTSIDE card 0428-208's
  write-set. The same "no workflow executor: shell-ux" failure appeared in the earlier run
  45099897243 on a different base, confirming it is a base-develop-wide condition, not a
  defect introduced by this candidate.
- My candidate's product changes (cmd/baha/*) resolve to atomic/docker/data-capabilities and
  atomic/podman/data-capabilities gates — both have executors. The shell-ux selection is a
  base-policy/aggregate matter, not caused by my domain change.

## Action taken (per rules)
- STOPPED at the base-policy blocker. Did NOT edit scripts/pr-required-final.py (shared base
  policy, outside write-set) and did NOT touch .github/** (Owner scope).
- Reported file:line + diagnosis to the coordinator for an Owner decision (single shared-policy
  fix to register the static shell-ux executor, or a documented non-blocking exemption).
- All in-scope work, local validation, and the real CI checks (Focused Python, go-vet, go-build,
  pr-planner-tests, documentation-audit, demo-pin, trusted-plan, native-gate-plan, source-format)
  passed.

## Still pending
- Owner decision on the shell-ux executor registration in scripts/pr-required-final.py (or a
  documented non-blocking exemption) before the candidate can go green and move to review.
- Post END_DONE / QUESTION to coordinator 9142ab1f.

## RUN-TO-TERMINAL — candidate built, two blockers identified (updated run)

Candidate head (clean rebuild): `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443`
PR #1746 head (witnessed): `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443`
develop base: `cd9cc4836a69815a6cdcf7079902bafe5be1e000`

### Root cause 1 (FIXED locally): deep-hop history polluted the branch with foreign merges
- The branch carried the frozen base's long hop history (foreign merge commits such as
  `Merge remote-tracking branch 'origin/develop' into codex/1746-zsh-only`).
- The CI `pr_plan` base-detection (`ci.yml:586-590`, `source_parents[2]` / merge-base)
  resolved the controller/effective_base to a FOREIGN branch merge (`c456505d`, a merge of a
  different lane), not my head — so the aggregate ran a foreign `pr-required-final.py`.
- REBUILT the branch clean: fresh frozen `208ee7607` hop onto current develop, then
  cherry-pick the 3 substantive commits (release-scope move, test alignment, executor mapping).
  Parent chain is now linear and clean; `git diff develop..HEAD` includes ONLY the 6 script
  files I own (0 .github, 0 Go).

### Root cause 2 (still open): the aggregate reads the CONTROLLER's pr-required-final.py
- `ci.yml:780-781` sets `controller_sha` from `steps.plan`; `ci.yml:855-864`:
  `controller=$effective_base` (== develop tip `cd9cc483` for this PR).
- The aggregate (`PR · Selected Checks`) runs `git show "$CONTROLLER_SHA:scripts/pr-required-final.py"`.
- My fix lives in my branch `b68372ec`, which the aggregate does NOT read for this script.
- The mapping must land in **develop** (`cd9cc483`, base policy) — an Owner/coordinator action,
  outside this lane's write-set.

### CI evidence (4 runs, same shell-ux failure across bases)
- Run 45102450630 (head fde3468d) + earlier 45099897243: `BLOCKED: selected gate has no
  workflow executor: atomic/static/shell-ux`.
- Run 45108377482 (clean head b68372ec): same error; aggregate resolved `controller_sha` to
  `cd9cc483` (confirming the base-detection is now correct, but the controller's policy still
  lacks the mapping).
- All executed CI checks passed in every run (Focused Python, go-vet, go-build, pr-planner-tests,
  documentation-audit, demo-pin, trusted-plan, native-gate-plan, source-format). Only the
  shell-ux executor mapping blocks the aggregate.

### Fix verified correct (against develop's policy file)
- Copied develop `cd9cc483:scripts/pr-required-final.py`, applied the 1-line
  `atomic/static/*` -> `pr_focused` mapping (mirroring the `atomic/{docker,podman}` precedent at
  lines 62-63), and `verify()` with `atomic/static/shell-ux` selected returns `[]` (passes).
- The exact diff to apply in develop (scripts/pr-required-final.py, lines 66-69):
  insert before the final `else:`:
  ```python
  elif len(parts) == 3 and parts[0] == 'atomic' and parts[1] == 'static':
      # atomic/static/* focused gates (e.g. atomic/static/shell-ux) execute through the
      # PR · Focused Python job; without this they fell through to
      # 'selected gate has no workflow executor' and blocked the run.
      required.add('pr_focused')
  ```

## ACTION TO OWNER / COORDINATOR
The candidate implementation + local validation + all real CI checks are complete and green.
The single remaining blocker is a base-develop policy gap in scripts/pr-required-final.py
(executor registration for atomic/static/* focused gates). Authorized as a lane action by
coordinator scope-bug修正 2026-11-23, but the aggregate reads the controller (develop) copy,
so the mapping must be applied to develop (base policy) by the Owner/coordinator — OR the
MIGRATION_CONTROLLER / effective_base must be repointed so the aggregate reads the candidate.
Once develop carries the mapping, re-push is a no-op re-hop and CI goes green.
