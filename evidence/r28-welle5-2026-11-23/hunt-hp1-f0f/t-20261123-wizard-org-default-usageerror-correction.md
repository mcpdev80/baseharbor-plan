# TASK EVIDENCE: t-20261123-wizard-org-default-usageerror — CI receipt-omission root-cause (correction round)

- lane: w081-pr1802-wizard-org-default-usageerror-correction (branch hijacked by coordinator, see BLOCKER)
- card: 0428-258 · wizard-org-default usageError (correction round, coordinator/fecb akte af50fee57 + 673a30a32)
- PR: #1804 https://github.com/mcpdev80/baseharbor/pull/1804 (base develop f3d847874)
- owner: w081
- real github remote confirmed: origin = https://github.com/mcpdev80/baseharbor.git

## PLAN

1. Reproduce prior receipt-omission: run #7511 at head c67ea34e6 showed matched_tests with 17 TestAppNewWizard* tests and NONE of the three org-default tests.
2. Trace the actual CI execution path of the wizard-app-new-tests gate end to end.
3. Locate the exact layer that drops the three functions.
4. Verify the minimal fix at that layer names all three tests.
5. Push the fix to the reachable target; END with head + run-id + BASE_SHA + log witness.

## ROOT CAUSE (definitive, source-verified)

CI's pr_validations job (.github/workflows/ci.yml:1267) runs the wizard-*-tests case at ci.yml:1332-1336:

    git fetch --no-tags origin "$BASE_SHA"
    git show "$BASE_SHA:scripts/pr-check-runner.py" > "$RUNNER_TEMP/pr-check-runner.py"
    python3 "$RUNNER_TEMP/pr-check-runner.py" execute --check "$VALIDATION" --repository "$GITHUB_WORKSPACE"

BASE_SHA for this job = needs.pr_plan.outputs.controller_sha (ci.yml:1289). The pr_plan job resolves controller_sha = effective_base (ci.yml:839-864), and for a develop-base PR effective_base = develop tip. The migration controller 85965486 is an ancestor of develop, so controller = develop (f3d847874), NOT the candidate head.

CONFIRMED with git merge-base --is-ancestor 85965486 origin/develop -> YES.

So the gate runs the checker FROM develop. Develop's selector (scripts/pr-check-runner.py:26) is:
    'wizard-app-new-tests': (r'^TestAppNewWizard',),
which does NOT match TestGuidedStackProfileOrgDefaultMissingStackUsageError, TestGuidedStackProfileOrgDefaultPresentStackResolves, TestOrgDefaultStackNotInCatalog.

Also develop's scripts/pr-gate-plan.py has NO row for cmd/baha/app_new_wizard_org_default_test.go.

Local proof (ci.yml step simulation, BASE_SHA=f3d847874, repo=candidate checkout):
    grep 'wizard-app-new-tests' (develop copy) -> (r'^TestAppNewWizard',)
    python3 pr-check-runner.py execute --check wizard-app-new-tests --repository <candidate>
    -> matched_tests count: 17, org tests: []  <-- receipt-omission reproduced

## FIX AT THE FOUND LAYER (verified)

Edit develop's scripts/pr-check-runner.py:26 to:
    'wizard-app-new-tests': (r'^TestAppNewWizard', r'^TestGuidedStackProfile', r'^TestOrgDefault'),
Edit develop's scripts/pr-gate-plan.py to add the org-default test mapping:
    'cmd/baha/app_new_wizard_org_default_test.go': ('wizard-app-new-tests', ('atomic/docker/lifecycle', 'atomic/podman/lifecycle')),

VERIFY (full ci.yml step simulation with fixed develop checker + candidate repo):
    matched_tests count: 20, org tests: ['TestGuidedStackProfileOrgDefaultMissingStackUsageError', 'TestGuidedStackProfileOrgDefaultPresentStackResolves', 'TestOrgDefaultStackNotInCatalog']
    exit 0, stderr empty.

This is the minimal fix ON THE GATE SCRIPTS (scripts/), at exactly the layer that drops the three functions: the selector regex (pr-check-runner.py:26) and the per-file gate-plan mapping (pr-gate-plan.py). No test rename, no .github change, no product code change.

## BLOCKER / SCOPE DECISION REQUIRED (POSTED AS QUESTION)

The gate scripts run from develop, but develop cannot be advanced by a direct push (repo rule rejects push to develop; requires a merged PR). The develop-side fix therefore needs a PR — but:
- AGENTS.md: a change to a shared/base script (pr-check-runner.py, pr-gate-plan.py) outside this card's write-set is a COORDINATOR/Owner action, not a lane fix.
- One PR per card (#1804 is this card's PR). A second PR for the develop-side shared-script fix collides with single-PR discipline.
- The branch w081-pr1802-... that PR #1804 is pinned to was FORCE-MOVED by a coordinator process to b9a487209 (a develop merge carrying ~21 foreign files: logs/exec/urls, machine-coverage, docs, contracts, operator-auth) — violating the one-candidate-per-chain rule (AGENTS 3.8).

CLEAN CANDIDATE PRESERVED: branch w081-pr1804-receipt-final at c67ea34e6 (my two clean commits: 854c7ceff usageError fix+test, c67ea34e6 selector+mapping fix), pushed to origin. Commit-content diff vs parent = exactly the 2 files at the tip.

## repo-rule compliance

- Root-cause traced against actual ci.yml and scripts source, not assumption.
- Fix is the minimal change at the exact drop layer (selector regex + gate-plan mapping).
- No product code touched this round.
- No subagents; every step in this session.
- No docker/podman containers started (Go unit + python gate simulation only).

## CLEANLINESS

- No docker/podman containers or compose projects started. docker ps -a: (none started this lane).
- Worktrees created under /tmp/opencode/w081-pr1804-receipt-wt and /tmp/opencode/w081-pr1804-develop-wt (safe zones); candidate worktree at workers/baseharbor.
- Temporary branch w081-pr1804-receipt-final (clean) pushed.

## END

END_BLOCKED w081-pr1802-wizard-org-default-usageerror-correction: root cause of CI receipt-omission FOUND and FIX VERIFIED locally — the gate runs pr-check-runner.py from develop, whose selector (r'^TestAppNewWizard',) and missing gate-plan mapping drop the three org-default tests. Fix (widen selector to include r'^TestGuidedStackProfile' and r'^TestOrgDefault', add org-default mapping) verified to name all three tests (matched_tests 17->20, exit 0). BUT BLOCKED on a scope decision: the fix must land on develop, which cannot be direct-pushed (repo rule), and a develop-side shared-script change is a coordinator/Owner action under a single-PR-per-card constraint. Branch hijacked by coordinator (b9a487209, foreign files). Clean candidate preserved on w081-pr1804-receipt-final@c67ea34e6.
