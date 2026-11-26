# w259-0428-284-pinroute review akte

## Visible commit identity gate

Card frontmatter owner VERBATIM, fetched from origin/main at runtime from `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`: `owner: w198-0428-284-demo-parser`.
Canonical author `git user.name`: `w198-0428-284-demo-parser`.
Canonical `git user.email`: `w198-0428-284-demo-parser@baseharbor.local`.
Literal invocation: `git -c user.name=w198-0428-284-demo-parser -c user.email=w198-0428-284-demo-parser@baseharbor.local commit -m "..."`.
Pre-push author gate line: `git show -s --format=%an HEAD`; required output exactly `w198-0428-284-demo-parser`.

## PLAN

1. DONE Read required policy and mission, card owner from origin/main, current #1842 diff, and established routing evidence.
2. DONE Inspect the exact failed run and correlate failure details with the planner, runner, mapping, and workflow sources at the tested head.
3. DONE Write a correction prescription that preserves every selector and fallback requirement and adds the same-PR required execution route.
4. DONE Publish the akte through isolated plan branch and PR #67; merge only after exact-base ancestry, green Hosted Plan validation on the final head, and my own content review.
5. DONE Record the post-merge witnesses in the final handoff and post END_DONE with the evidence commit SHA.

## Source and scope witnesses

- Current reviewed PR #1842 head/run candidate: `dfd3495858501fe49d9c331c056a4289b780e0f8`.
- Hosted PR run `45731000555` on that exact head is terminal FAILURE. Both `pr-planner-tests` and `ci-executor-tests` report 11 `ReleaseDemoPinSelection` failures: enumerated parameterized failures are v0.4.22 through v0.4.27, with unresolved fixture mappings where resolved is expected; the mixed-pin and mapping-release mismatch negative cases also fail. No failing v0.4.28 parameter case was confirmed.
- Focused Python failure `test_v0427_demo_pin_uses_only_exact_source_validation` reports `AssertionError: 'fallback_used' unexpectedly found` in a `pr-gate-plan/v1` result whose `target_base_sha` is all `a`s. The v0.4.27 pin incorrectly takes broad fallback.
- Candidate-added advisory job says `No candidate-added validation checks.` Finding A remains covered by existing planner and CI-executor test routes; do not duplicate them. This is a live selection regression and a separate execution-route gap.
- The planning remote was verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Plan `origin/main` branch tip at initial isolated branch cut: `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`.
- Fresh plan remote advanced through `9e9e53cf775699b4ea80bd8e72e776e3bce61ad` (w254 PR #1822) to `08b1f66bb733d4c1422135429e5bc29fbd67cd57` (w256 evidence), where the original evidence commit was based. While PR #67 was open, live `origin/main` advanced to `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf` (w258 preflight), a descendant of 08b. Integrate this current tip by normal merge before updating the PR and re-prove ancestry.

## Correction prescription: selection contract

At `scripts/pr-gate-plan.py:840-842`, `release = mapping['release']` is the validated target release; the checked-in `scripts/pr-gate-map-v1.json` currently names `v0.4.27`. At `scripts/pr-gate-plan.py:1184-1205`, the candidate imports the runner and replaces that mapping release with `_current_release(repository)`. `scripts/pr-check-runner.py:402-433` selects the highest semantic-version entry in `release-requirements.json['releases']` (v0.4.28). That conflates mapping target with catalog maximum: it rejects otherwise valid mappings for v0.4.22-v0.4.27 and lets a v0.4.28 path resolve when the mapping says v0.4.27.

Prescription:

- At `scripts/pr-gate-plan.py:1184-1205`, remove the import/call to `_current_release` from planner selection. Match `docs/releases/<tag>.demo-ref` against the validated `release` already taken from the mapping at line 840. Require the tag to be in `requirements['releases']` and equal the mapping release. Do not swallow catalog errors and fall back to another release. This recognizes each v0.4.22-v0.4.28 pin when the map names that release, and leaves mismatched path/mapping pairs unresolved.
- Preserve the existing standalone, modified-file rule at lines 1202-1205. A pin mixed with another changed path remains unresolved in targeted planning. Preserve the normal conservative fallback behavior and all broad checks; do not convert an unresolved/mixed diff into exact targeted coverage or suppress `fallback_used`.
- For execution, carry the selected release on the validation row at `scripts/pr-gate-plan.py:792-798`, preserve it in `scripts/pr-check-runner.py:295-303` matrix entries, and accept/validate that explicit supported release in `scripts/pr-check-runner.py:436-479`. `_current_release` may remain a default for callers without an explicit release; it must not override the mapped/selected release. Thus planner selection and immutable pin validation use the same release.
- Keep regressions for each active release v0.4.22-v0.4.28 with mapping release equal to the path release; keep mismatch-negative, mixed-change unresolved, standalone-modified-only, and v0.4.27 no-fallback assertions. Do not delete tests or change expectations. The provided hosted failure list confirms v0.4.22-v0.4.27 failures only; do not claim a v0.4.28 parameter failure absent evidence.

## Same-PR required execution route

The `pull_request` workflow loads the planner and runner from the trusted controller at `.github/workflows/ci.yml:865-876`, so candidate selection code does not route this same run. The executor case at `.github/workflows/ci.yml:1323-1327` also loads the trusted base runner, and the candidate advisory job is non-required and says `No candidate-added validation checks.`

Prescription for the route:

- In `.github/workflows/ci.yml:869-876`, after generating the trusted plan from the verified `pr-diff.json` and before emitting the matrix, detect the changed `docs/releases/v0.4.28.demo-ref` path, validate its tag against the trusted release catalog, and add a `demo-source-pin-validation` row carrying `release=v0.4.28` if the ID is not already present. This is an additive required validation. Preserve targeted unresolved reasons and existing conservative fallback semantics: when the mixed diff takes fallback, it must retain `fallback_used=true` and every broad check while the pin validator also runs.
- In `.github/workflows/ci.yml:1323-1327`, pass the matrix release to the corrected validator and run the candidate's corrected release-scoped runner for this one ID; keep other checks on the trusted base runner and retain read-only permissions. Log an explicit start line before invocation. Do not rely on the advisory candidate-added job.
- The `pr-gate-plan.py` mapping correction is effective for later runs once trusted. The workflow's additive route is still needed for this exact event because its planner is pinned to trusted base/controller code.

## Delegation classification

This is purpose-bound test routing/mapping, which the 25-Nov delegation classifies as Codex-decided. The mission explicitly assigns the owner-authorized gate-route scope for this exact validation ID and PR. This review recommends the narrow workflow route above; it makes no product or workflow edits itself.

## Completion criterion

On the corrected absorbed head, an executed `pull_request` validation job must log the exact line `Running validation check: demo-source-pin-validation`, followed by validator output `{"check":"demo-source-pin-validation","matched_tests":["5ca92a7cd2f746934890cfd7096a48068bdf218e"]}`. The matrix job and `PR Selected Checks` must both succeed for that exact head, and existing broad fallback checks must remain selected whenever overall coverage is unresolved. A source selector, skipped job, advisory-only execution, or aggregate success without this validator output is not completion evidence.

## Worker pair instruction

For the corrected absorbed head, require two distinct GitHub `pull_request` event run IDs, each with `PR Selected Checks` success and the validator execution log above. Use a `per_page=100` job census for each run and retain run ID, head SHA, event, aggregate result, validator job ID, and matched pin output. A rerun/attempt on one run ID is not the second run; the second qualifying event is a separate PR event via the authorized close-and-reopen trigger. No VM or local test is needed for this route.

## Publication witnesses

This is planning evidence only. Plan PR #67 is the sole PR in this lane. It was based on live plan `main`; before its next update, current `origin/main` `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf` must be integrated without rewriting history. Merge only after Hosted Plan validation on the final head and my content review. The post-merge `git show` and `gh api contents` witnesses will be included in the handoff. Product PR #1842 remains untouched and unmerged; no product CI was triggered by this review.

END w259-0428-284-pinroute BLOCKED: the correction prescription is complete; plan PR #67 needs current-base integration, Hosted Plan validation on the final head, and authorized plan-only merge before completion.
