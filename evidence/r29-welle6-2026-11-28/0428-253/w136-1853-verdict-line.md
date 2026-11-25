# #1853 Hosted route verdict

## PLAN

1. Inspect Hosted pull_request run job lists for this repository and era (per_page=100); identify a run showing planner and executor semantics.
2. Verify whether the two-suite planner command and CI_EXECUTION_SUITES execute test_pr_gate_coverage.py and test_pr_ci_fallback.py; capture exact job names and output evidence.
3. Record a GO/NO-GO one-line verdict with job citations in planning evidence and deliver it to the coordinator; no repository changes.

## Scope

Read-only review of Hosted job evidence for #1853. No product or workflow repository changes.

## Hosted evidence and verdict

- #1853 PR run `45699482849` was a `pull_request` run on head `030e58489389b12f1684eb1c50cebc86a276cf9d`. Job `PR · Validation · ci-executor-tests` (`139505586492`) executed 225 tests, including `test_pr_ci_fallback.py` cases, but failed `test_planner_validation_route_includes_planner_and_coverage_suites` because the workflow command contained only `test_pr_gate_plan.py` and `test_pre_release_runtime_reuse.py`, while the expectation included four suites.
- Green same-era PR run `45711869496` on #1850: `PR · Validation · ci-executor-tests` (`139548148860`) succeeded and its `matched_tests` included `test_pr_ci_fallback.py` but not `test_pr_gate_coverage.py`; `PR · Validation · pr-planner-tests` (`139548148916`) succeeded with the actual command `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py`, a two-suite route. `PR · Focused Python` also executed `python3 scripts/test_pr_ci_fallback.py`.
- Hosted logs for these runs do not show execution of `test_pr_gate_coverage.py`; the route regression in 45699482849 is explicitly red. Therefore the combined claim that both named files execute through the current two-suite planner route plus `CI_EXECUTION_SUITES` is not proven.

**NO-GO —** #1853 Hosted evidence does not prove both files execute: `PR · Validation · ci-executor-tests` ran `test_pr_ci_fallback.py` but its matched list omits `test_pr_gate_coverage.py`; `PR · Validation · pr-planner-tests` ran only the two-suite command.

END_DONE w136-pr1836-rowsreview: #1853 route verdict delivered as NO-GO on candidate `030e58489389b12f1684eb1c50cebc86a276cf9d`.

## Publication identity and base

- Current card owner VERBATIM from plan `origin/main` (`c66cab2e1e513255aa1990721b7275a51c0ce45d`): `w205 (lane w205-0428-253)`.
- Planning remote verified: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Evidence commit identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record #1853 hosted route verdict'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- The evidence update is on a branch cut from plan `main` at `c66cab2e1e513255aa1990721b7275a51c0ce45d`; ancestry must be verified before commit.

## Correction round: identity classification and current integration gate

### PLAN

1. Re-read the exact seven-commit PR census, current 0428-253 owner field and owner note on live plan main.
2. Classify every commit author variant separately without broadening the owner's two-commit exception or rewriting history.
3. Verify the actual lane-dispatch source and distinguish session-name resolution from Git identity configuration.
4. Refresh PR head, develop tip, diff and exact-head Hosted run census; state whether this head can merge now.
5. Record the disposition to the PR and planning evidence.

### Ownership and evidence identity block

- Card owner VERBATIM from live plan main `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`: `w205 (lane w205-0428-253)`.
- Git user.name for this evidence commit: `w136-pr1836-rowsreview`.
- Git user.email for this evidence commit: `w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): classify #1853 author variants'`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- Planning remote witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Plan branch base: `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`; this exact base is the current origin/main fetched before this evidence branch.

### Commit-by-commit identity classification

| Commit | `.commit.author.name` | Classification |
| --- | --- | --- |
| `90c8017b2363aef0f75aea481cd147883b312a22` | `w205` | Same-lane shortened author; admitted by the owner ruling, limited to this commit. |
| `3c1ebc6fcb71334a85a32601939de1d128de56ba` | `w205` | Same-lane shortened author; admitted by the owner ruling, limited to this commit. |
| `4ca3f46508b4b006c1fffbe7766fbe4c386e9e27` | `w205 (lane w205-0428-253)` | Codex ruling: same-lane formatting variant; the literal author contains the full canonical lane ID. This is not covered by the owner's two-commit exception. |
| `030e58489389b12f1684eb1c50cebc86a276cf9d` | `w205 (lane w205-0428-253)` | Codex ruling: same-lane formatting variant; the literal author contains the full canonical lane ID. This is not covered by the owner's two-commit exception. |
| `b69fc54d728b44fc98481b5769f0590bc2956bf3` | `w205-0428-253` | Canonical lane author. |
| `0ba631deb15025b0ce0479f831ffdee8b07a14f1` | `w205-0428-253` | Canonical lane author. |
| `228ecc5bab28e5e6158ccc63160f442a6afc9ed3` | `w205-0428-253` | Canonical lane author. |

No foreign-lane author was found. The first two shortened authors are the only commits covered by the owner's written exception. The two parenthetical forms are accepted solely by this Codex same-lane formatting judgment; no history was rewritten.

### Dispatch-source proof and limitation

- `coordinator/scripts/dispatch-lane.sh:28-33` resolves the lane by calling `lane-name.py` with the Codeman session ID; `lane-name.py:16-21` queries `codeman agent list --json`, matches the ID and prints the session's `name`.
- These lines do not extract parentheses and do not set `git config user.name`. `dispatch-lane.sh:45` is prompt text describing the admission rule, not executable identity configuration.
- Current workspace check returned `file:.git/config<TAB>w205-0428-253`; that is only the current workspace configuration and does not prove the Git identity of a newly started lane. A fresh lane identity needs an explicit worktree-level configuration or per-commit `git -c` and a measured `%an` before push. No new lane was started for this proof.

### Current-head review and merge disposition

- Exact PR head: `228ecc5bab28e5e6158ccc63160f442a6afc9ed3`; card owner is the string above; head author and committer are both canonical `w205-0428-253`.
- Distinct exact-head `pull_request` successes: run `45716254159` attempt 1 and run `45717496553` attempt 1. Run `45716254159` attempt 2 and `45717487430` were cancelled and do not count.
- Current develop: `ae70964d7b80b779822b76107b70ea76782f998e`. Compare reports the candidate seven commits ahead of develop and zero behind; the PR changes `.github/workflows/ci.yml`, `scripts/pr-gate-plan.py`, and CI test definitions. The PR base equals current develop, and compare reports the candidate seven commits ahead, zero behind, with merge base equal to develop. No develop hop is required now; the two exact-head successes remain usable. Later develop movement that changes these workflow/planner/test inputs will require a hop and fresh qualification.
- GitHub PR comment recording this identity decision and hold: https://github.com/mcpdev80/baseharbor/pull/1853#issuecomment-7178056642.
- Disposition: identity is accepted; final merge remains held until the candidate absorbs current develop and obtains fresh exact-head Hosted qualification. No merge was executed.

### Live card-note verification discrepancy

- Live plan `origin/main` is `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`; GitHub contents API reports card blob `dca634c9139a413dc1873a1069433484d9ad4001` and frontmatter owner `w205 (lane w205-0428-253)`.
- A fresh `rg -n 'Erste zwei|owner:'` over that live card returned only `10:owner: w205 (lane w205-0428-253)`; the owner-ruling sentence is absent from this current blob despite the earlier PR #43 merge witness. This is recorded as a plan-main content discrepancy, not as a reason to expand the ruling.

END_DONE w136-pr1836-rowsreview: #1853 identity accepted by owner-specific and Codex same-lane rulings; final merge held pending current-base hop and fresh Hosted pair at `228ecc5bab28e5e6158ccc63160f442a6afc9ed3`.


### Forward restoration of the owner ruling after live-main drift

- Despite prior merge witness PR #43 / `549fc5de`, a fresh read of current plan main `76ab859144661e7fdabdc10e36b9cee5f3ce99ad` found the sentence absent from card blob `dca634c9139a413dc1873a1069433484d9ad4001` and the owner-ruling evidence path absent. This forward PR restores exactly the requested sentence and the historical ruling evidence; it does not extend the owner ruling to the two parenthetical-format commits.
- The sentence is inserted without changing card metadata or status.
