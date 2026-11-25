# Independent exact-head review — BaseHarbor PR #1842

Date: 2026-11-27
Reviewer: Codex review lane (authenticated GitHub actor `mcpdev80`; formal request-changes review API refused because the actor authored the PR)
Card: 0428-284 / `t-20261125-0428-284-1812-postretry-gate-failure`
PR: https://github.com/mcpdev80/baseharbor/pull/1842
Reviewed head: `50c6d84e6e4a91fe71b385c68abf0bd531a2b173`
Base at review: `develop` `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`
Commit author: `w177-0428-284-demo-pin-1812` (historical candidate; card's current owner is w198 per transfer record)
Verdict: **CHANGES; not merge-authorized.** No merge performed.

## Diff and scope

The exact diff contains three files only:

- `docs/releases/v0.4.28.demo-ref`: pin value changed to `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`.
- `scripts/pr-gate-plan.py`: a release pin path matcher now selects `demo-source-pin-validation` for v0.4.27 and v0.4.28.
- `scripts/test_pr_gate_coverage.py`: regression cases for v0.4.27 and v0.4.28.

No `.github` workflow, product authentication, authorization, or consent files changed.

## Exact-head CI evidence

Three `pull_request` workflow runs on the same head completed successfully: [45626853905](https://github.com/mcpdev80/baseharbor/actions/runs/45626853905), [45630630092](https://github.com/mcpdev80/baseharbor/actions/runs/45630630092), and [45631228584](https://github.com/mcpdev80/baseharbor/actions/runs/45631228584). Run 45631228584 has `PR Selected Checks` success (job 139267523487; required integration 15368), plus successful Focused Python, planner tests, CI executor tests, source format, Go checks, and trusted plan. However, that run's `PR · Demo Pin` job 139264792505 was **SKIPPED**. The planner test is not execution proof for the selected validator.

The separate pre-release `workflow_dispatch` run [45627034676](https://github.com/mcpdev80/baseharbor/actions/runs/45627034676) used the same Core head and completed with top-level **FAILURE**. Candidate/gate-plan and source qualification/artifact/docs checks passed, but eight of fourteen Light runtime gates failed. Six Light jobs executed and passed: Docker guided, lifecycle, failure; Podman guided, lifecycle, failure. The other eight failed in the consented post-retry Demo acceptance path. The dispatch run is distinct evidence and does not replace PR CI. These downstream Light results remain binding for #1812 requalification; they are not, by themselves, a reason to withhold a pin-only PR merge.

## Findings

1. **Trusted executor does not validate the new pin.** On the reviewed base, `scripts/pr-check-runner.py:383-392` hardcodes `docs/releases/v0.4.27.demo-ref` for `demo-source-pin-validation`. The candidate selector now routes v0.4.28 to that check, but the trusted executor still reads v0.4.27. This exact-head PR run skipped `PR · Demo Pin`, so the mismatch was not exercised.

2. **Selector contradicts its new test's stated contract.** Candidate `scripts/pr-gate-plan.py:1182` uses `re.fullmatch(r'docs/releases/v0\.4\.2[78]\.demo-ref', path)`. The new test comment says changed pins of “ANY active release” must select this validator. Active `scripts/release-requirements.json` lists v0.4.22 through v0.4.28, and standalone `.demo-ref` files exist for v0.4.22, v0.4.23, v0.4.27, and v0.4.28. The new matcher excludes two active pin files.

## Required fix and acceptance rule

Make planner selection and trusted execution agree for every active release with a standalone `.demo-ref` pin. Prefer deriving eligible pin paths from the active release catalog; an explicit exhaustive set is acceptable if tests prove it stays aligned. Pass the exact selected pin path into the executor and validate that path's single immutable SHA against the Demo repository; remove the v0.4.27 hardcode. Add planner and executor regressions for v0.4.22, v0.4.23, v0.4.27, v0.4.28, and a non-active/non-pin path. Re-run exact-head PR CI so `PR · Demo Pin` executes and passes, then preserve a separate explicit-`demo_ref` dispatch with the relevant executed pin-validation slices green. The 14 Light gates remain required for the later #1812 requalification, not as a blanket precondition for merging a correctly validated data-only pin.

GitHub PR comment with this verdict and recipe: https://github.com/mcpdev80/baseharbor/pull/1842#issuecomment-7166661667

Formal review API result: `GraphQL: Review Can not request changes on your own pull request`; therefore the PR comment is the recorded GitHub verdict. Merge was withheld because the pin-specific validation route is incomplete.

3. **Merge identity gate fails.** The verified candidate commit author name is `w177-0428-284-demo-pin-1812`; the current authoritative card owner is `w198-0428-284-demo-parser`. Under the owner's exact author-name equality rule, this head is not merge-qualified until an admission rail is recorded. Fix-forward only; do not rewrite history. This is independently sufficient to withhold merge even after the pin-validator code is corrected.
