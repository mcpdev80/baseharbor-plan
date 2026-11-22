# hop-develop-8b9a8f50 (0428-208 PR #1746, re-hop)

## Status
DONE. Re-hop of PR #1746 (0428-208) from 48f0cb1e to develop 8b9a8f50645. New head fec44963, back=0, feature preserved, own-commits-only. ci.yml stays UNCHANGED vs candidate (promise honored; diff empty). PR-triggered CI run 7178 (db 44978841587) at new head completed/success (35 success / 72 skipped / 0 failure). Candidate carries no new failures; the four static failures live only in the dispatch-gated pre-release runtime suite (baseline db 317 at old head), which remains Owner-dispatch-gated and does not execute under PR CI.

## Reality check
- Planning-remote verified before first commit:
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Worktree remote guard: origin = https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80). Correct GitHub remote.
- Candidate proven: PR #1746 head 48f0cb1e44d5014ea1fc65015fe1c1b312aed47f, parent 9ddcde356e9, back=5 behind new develop.
- develop fetched via origin = 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 (directive: #1736 merged 02:36:09Z).
- PR #1746 is draft=false, state=OPEN -> re-hop permitted.
- Promise check: ci.yml identical between 48f0cb1e and 8b9a8f50645 (`git diff 48f0cb1e 8b9a8f50645 -- .github/workflows/ci.yml` = empty), so the additive hop cannot touch ci.yml.

## Re-hop (additive merge-commit, no rebase/amend/force)
- Branch: lane-0428-208-static-release-gate (PR #1746's lane branch), at candidate 48f0cb1e.
- Command: `git merge --no-ff 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 -m "hop PR 1746 to current develop 8b9a8f50645 (0428-208 static release gate, ci.yml unchanged)"`
- No conflict. Only develop scripts/ content added (6 files, 245 insertions).

## Exactness proof
- back=0: `git rev-list --count HEAD..8b9a8f50645` = 0.
- Parents: HEAD^1 = 48f0cb1e (candidate, carried forward), HEAD^2 = 8b9a8f50645 (develop).
- ci.yml UNCHANGED vs candidate: `git diff 48f0cb1e HEAD -- .github/workflows/ci.yml` = empty (promise kept).
- Feature preserved vs candidate: `git diff 48f0cb1e HEAD -- cmd/ internal/` = empty.
- `git log --oneline origin/develop..HEAD` lists only: hop merge fec44963 + pre-hop 48f0cb1e + 9ddcde35 + ab7e45be + b79ead79 + 8bc9011b. No foreign candidate commit.
- `git diff origin/develop...HEAD --name-only`: does NOT include .github/workflows/ci.yml (ci.yml absent from the changed set).
- develop is ancestor of HEAD: `git merge-base --is-ancestor origin/develop HEAD` = OK.

## Push (no force) + delivery witness
- `git push origin lane-0428-208-static-release-gate` => `48f0cb1e..fec44963`
- Delivery: `git ls-remote origin refs/pull/1746/head` => fec44963fc71b8ab6d0f53169cbf0cb892344b0c. gh PR #1746 headRefOid = fec44963.

## Run witness (new head vs baseline)
- New head PR-run: run 7178, db 44978841587, head fec44963, event pull_request, terminal completed/success. Job tally: 35 success / 72 skipped / **0 failure**.
- Baseline pre-release-run: run 317, db 44976686495, head **48f0cb1e** (the OLD head), event workflow_dispatch (Pre-Release), completed/failure. Failed jobs: Static·init, Static·mcp, Static·config-matrix, Static·shell-ux (+ Pre-Release Checks aggregator) = 4 static failures.
- Comparison: the candidate at the NEW head carries NO new failures and zero failures in the PR-triggered CI run. The four static failures are confined to the dispatch-gated pre-release runtime suite (db 317), which does not execute under PR CI and requires an Owner workflow_dispatch with required inputs (ref, demo_ref, runtime, gate). Reported as witness; not fixed. No .github/** or scripts/** edited by me; no local test runs; no merge/close; no GitHub comment.

## End
- New head: fec44963fc71b8ab6d0f53169cbf0cb892344b0c, back=0.
- Run: 7178 (db 44978841587) completed/success at new head.
- Failed jobs at new head PR-run: 0. The four static failures (init/mcp/config-matrix/shell-ux) remain only in the dispatch-gated pre-release run 317 at the old head 48f0cb1e (Owner dispatch-gated).
- ci.yml unchanged vs candidate (promise honored).
