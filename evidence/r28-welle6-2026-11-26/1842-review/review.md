# #1842 exact-head CODEX review — CHANGES

## PLAN

1. Read the assigned final-review mission and bind the review to the exact current PR head.
2. Verify the pull request base, five-file diff, commit authorship, required Hosted runs, and terminal selected-check results.
3. Inspect the real release catalog shape, the changed release resolver, the test fixture, and the workflows that execute or skip the relevant checks.
4. Record two separate actionable findings: the unexecuted coverage suite and the runtime resolver defect, including exact minimal corrections and Hosted proof required.
5. Post a formal review verdict, publish this akte through the planning PR path, and leave #1842 unmerged until both findings are resolved.

## Visible commit ansatz

Card frontmatter read from current planning `origin/main` at runtime: `owner: w198-0428-284-demo-parser` for `t-20261125-0428-284-1812-postretry-gate-failure`. This file records a reviewer disposition only; it does not update that card or the product candidate. Reviewer lane identity: `w200-1842-final-review`. Git user.name: `w200-1842-final-review`; git user.email: `w200-1842-final-review@baseharbor.local`. Literal commit invocation: `git -c user.name=w200-1842-final-review -c user.email=w200-1842-final-review@baseharbor.local commit -m "review(w200-1842-final-review): record #1842 CHANGES findings"`. Pre-push gate: `test "$(git show -s --format=%an HEAD)" = w200-1842-final-review`.

Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`. The branch was created from freshly fetched `origin/main` `132ee736b0fabfb55a2f8488ae25b677be5f35f1` with no candidate commits, then fast-forwarded before the first commit to current `origin/main` `ea9f7ab6583542ab3bd1b782e7652585ca567d04`.

## Candidate and integration evidence

PR: [mcpdev80/baseharbor#1842](https://github.com/mcpdev80/baseharbor/pull/1842). Reviewed head: `5d9965944ff6cd265cbd5d042d59cf522b38b76d`. Current develop base: `ae70964d7b80b779822b76107b70ea76782f998e`. Remote witness:

```text
ae70964d7b80b779822b76107b70ea76782f998e refs/heads/develop
5d9965944ff6cd265cbd5d042d59cf522b38b76d refs/pull/1842/head
```

GitHub compare `develop...head` is `ahead`, `ahead_by=7`, `behind_by=0`, merge base `ae70964d7b80b779822b76107b70ea76782f998e`. The changed paths are exactly:

- `docs/releases/v0.4.28.demo-ref`
- `scripts/pr-check-runner.py`
- `scripts/pr-gate-plan.py`
- `scripts/test_pr_check_runner.py`
- `scripts/test_pr_gate_coverage.py`

Head commit author and committer are both `w198-0428-284-demo-parser <w198-0428-284-demo-parser@baseharbor.local>`. The merge-hop parents are `996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52` and current develop `ae70964d7b80b779822b76107b70ea76782f998e`.

The pin file contains `5ca92a7cd2f746934890cfd7096a48068bdf218e`; the Demo Contents API resolves that exact SHA. PR body pin and reviewed source paths match the mission contract.

## Hosted run census

Runs [45716226824](https://github.com/mcpdev80/baseharbor/actions/runs/45716226824) and [45717078703](https://github.com/mcpdev80/baseharbor/actions/runs/45717078703) are distinct `pull_request` runs, each `completed/success` on exact head `5d9965944ff6cd265cbd5d042d59cf522b38b76d`, with 39 jobs and zero failed jobs. `PR Selected Checks` succeeded in both runs under GitHub Actions integration `15368`.

Run `45717078703` executed `PR · Focused Python`, `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Validation · pr-planner-tests`, and `PR Selected Checks`. It skipped `PR · Demo Pin` and `PR · Selected Runtime`. Its `PR · Focused Python` script list includes `scripts/test_pr_check_runner.py` but not `scripts/test_pr_gate_coverage.py`. The `PR · Validation · pr-planner-tests` log runs `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py` only; it does not run `scripts/test_pr_gate_coverage.py`. The `PR · Candidate-added checks (advisory)` log states `No candidate-added validation checks.` No `PR · Validation · demo-source-pin-validation` job appears in the 39-job run.

The `PR · Demo Pin` workflow job is not the release-pin validator: it validates the paired Demo source used for PR runtime testing and is conditionally selected for runtime/integration/public-contract gates. Its skip does not prove or execute `demo-source-pin-validation`.

## Finding A — changed gate-coverage suite was not executed

The PR changes `scripts/test_pr_gate_coverage.py`, including the v0.4.28 selector regression. Neither exact-head Hosted run executed that file. The `pr-planner-tests` Hosted branch at `.github/workflows/ci.yml:1362-1363` invokes only `scripts/test_pr_gate_plan.py` and `scripts/test_pre_release_runtime_reuse.py`. The Focused Python job also omitted `scripts/test_pr_gate_coverage.py`.

Disposition: this is purpose-bound test-path completion for #1842, so the route can be included in this PR under the standing delegation for test-environment and classification/mapping corrections. The minimal change is to extend the `pr-planner-tests` unittest command at `.github/workflows/ci.yml:1363` to include `scripts/test_pr_gate_coverage.py` alongside the two current modules. Requalification must show that module actually executing on the repaired exact head; a green aggregate without it is insufficient.

## Finding B — runtime resolver fails against the real catalog, and no Hosted job executed it

At `scripts/pr-check-runner.py:383-399`, `_current_release()` reads `requirements.get('release')` from `scripts/release-requirements.json`. The actual file at both develop `ae70964d7b80b779822b76107b70ea76782f998e` and candidate `5d9965944ff6cd265cbd5d042d59cf522b38b76d` has only top-level keys `gates`, `releases`, and `schema`; it has no `release` field. The candidate's `releases[]` includes `v0.4.28`. Consequently every execution of the new resolver raises `RuntimeError('release-requirements.json missing a release tag')` before checking the pin.

The alternative `scripts/pr-gate-map-v1.json['release']` is also the wrong source for this card: it is `v0.4.27` at this head and would select the old pin, not the v0.4.28 regression target.

Minimal in-scope correction: make `release-requirements.json['releases']` the authoritative supported-release set, derive the highest/current tag deterministically by semantic version (which is `v0.4.28` here), and validate that chosen tag belongs to the catalog before resolving `docs/releases/<tag>.demo-ref`. Do not read a nonexistent top-level `release`, and do not use the map's v0.4.27 label for this v0.4.28 pin. If a future schema adds an explicit active tag, it must be defined and tested as such rather than assumed.

Correct the fixture at `scripts/test_pr_check_runner.py:24-28`: use the real catalog shape (`schema`, `releases`, `gates`) with a v0.4.28 entry and assert that the validator reads the v0.4.28 pin. Add a negative case for an empty or malformed release catalog. The current fixture invents `{'release': 'v0.4.27'}` and masks the production-schema failure.

Hosted proof required: the exact repaired PR head must execute `PR · Validation · demo-source-pin-validation` through the `pr_validations` matrix and pass against the candidate's v0.4.28 pin. The corresponding dispatch implementation is `.github/workflows/ci.yml:1323-1326`; the matrix is consumed at `:1267-1273`. Neither exact-head run included that job. Under the same purpose-bound test-path completion authority, the worker should add a trusted diff-selection route for `docs/releases/v0.4.28.demo-ref` so the named validation enters the matrix and executes. Do not repurpose `PR · Demo Pin` at `.github/workflows/ci.yml:1075-1098`; it checks a different Demo/Core runtime pairing. This is an actionable CI routing change within #1842's release-pin validation purpose, not an escalation finding.

## Verdict and merge state

Verdict: **CHANGES**. Finding A and Finding B are independent acceptance blockers. Neither exact-head green aggregate is sufficient because A's changed suite did not execute and B's validator both has an input-schema defect and lacks Hosted execution. No approve review was submitted and no product merge was performed. The complete Codex CHANGES review is GitHub review `6066258782` (`COMMENTED`, commit-bound to the reviewed head); an earlier comment `6066220597` covered Finding A only. The PR author and authenticated reviewer login are both `mcpdev80`, so GitHub records a comment review rather than a self-approval. The akte is the durable review rationale, not a substitute for CI.

#1842 remains open at the reviewed head until the worker correction and the purpose-bound CI routing changes above are complete, followed by exact-head Hosted evidence. No merge SHA exists. #1812 re-hop remains sequenced after a later #1842 merge and is not started here. #1853 remains untouched while this prescription is published.

## Publication / provenance

This evidence is being published through one planning PR branch with current base `origin/main` `ea9f7ab6583542ab3bd1b782e7652585ca567d04` after a fast-forward from the branch-cut SHA recorded above. Before opening or updating a PR, prove `git merge-base --is-ancestor origin/main HEAD` and record `git diff origin/main...HEAD --name-only`; the diff must contain only this evidence path. Push delivery and final origin/main tree membership will be recorded after the plan PR is opened and merged.

## END w200-1842-final-review BLOCKED

Pre-PR provenance command: `git merge-base --is-ancestor origin/main HEAD` -> exit 0.

Exact `git diff origin/main...HEAD --name-only` output before recording this witness:

```text
evidence/r28-welle6-2026-11-26/1842-review/review.md
```

Planning validation: `python3 scripts/plan.py check` reported `776 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`. The ten warnings are existing accepted-task dependency warnings; this evidence-only change updates no task metadata.

## Routing authority addendum

Owner scope correction: the standing delegation permits Codex to decide test-environment and classification/mapping corrections; the prior Batch-Baseline workflow restriction does not govern this PR. I rule option (i): add the minimal routes within #1842's purpose-bound release-pin test completion. At `.github/workflows/ci.yml:1363`, add `scripts/test_pr_gate_coverage.py` to the `pr-planner-tests` unittest command. Add a trusted selector mapping for `docs/releases/v0.4.28.demo-ref` into the `pr_validations` matrix so `PR · Validation · demo-source-pin-validation` executes; the workflow dispatch implementation is `.github/workflows/ci.yml:1323-1326` and the matrix consumer is `:1267-1273`. Keep the separate runtime `PR · Demo Pin` job unchanged. The worker may make these CI changes inside #1842; no owner escalation is needed.

The resolver source and fixture prescription remains as Finding B above: use the real `release-requirements.json['releases']` catalog, derive the current/highest semantic release (`v0.4.28` here), update the fixture to the actual `schema`/`releases`/`gates` shape, and test the v0.4.28 pin. Exact-head Hosted qualification requires both the `pr-planner-tests` command to execute `scripts/test_pr_gate_coverage.py` and `PR · Validation · demo-source-pin-validation` to execute and pass. Aggregate green without either execution is not qualifying.

The plan evidence branch was rebased only over its own commits onto current `origin/main` `ea9f7ab6583542ab3bd1b782e7652585ca567d04`. Current `git merge-base --is-ancestor origin/main HEAD` succeeded. `git log --oneline origin/main..HEAD` lists only this lane's commits. `git diff origin/main...HEAD --name-only` lists only `evidence/r28-welle6-2026-11-26/1842-review/review.md`. The current tip author gate passed: `git show -s --format=%an HEAD` equals `w200-1842-final-review`.
