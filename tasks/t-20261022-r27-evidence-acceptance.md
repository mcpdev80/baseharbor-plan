---
id: t-20261022-r27-evidence-acceptance
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: flash-coordinator + o145 (W5 independent)
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-verifier]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-acceptance · evidence acceptance #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** flash-coordinator + o145 (W5 independent) · **Priority:** critical  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Owner:** flash-coordinator + o145 (W5 independent)  
**Priority:** critical  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090)  
**Source:** 
<!-- /generated:links -->


# Receipt acceptance: one ordinary contributor PR end to end

## Acceptance fixed before implementation
- Exactly one gate: runner -> trusted post-run writer -> Receipt commit -> live verifier -> authenticated Owner approval commit -> final-check consumption.
- One genuine successful GitHub path plus three rejected cases: wrong candidate SHA, nonexistent run ID, edited receipt. Unit fixtures alone do not accept the skeleton.
- An ordinary contributor PR generates, verifies and links its receipt without anyone writing a run number, manifest or evidence URL by hand. The explicit Owner approval remains a decision, not evidence bookkeeping.
- After approval, retained verification succeeds with GitHub API access disabled; edited receipts still fail.
- Developer summary is at most three lines: checked / validly reused / not required with reason. Not-required belongs to the plan, never a PASS receipt.
- Existing required legacy checks remain authoritative during the pilot. Only a subsequent cutover PR may replace the relevant check.
- No additional gates, cross-domain matrix or reuse machinery before this acceptance. No release or product-task acceptance is implied.

## Sequence and fallback
PR 1: contract + two scripts + three negatives + EN/DE docs. PR 2: one real shadow skeleton and automatic task link. PR 3: accepted final-check cutover. Each PR qualifies through the existing accepted path.
If the one-gate pilot is blocked by missing administrative configuration, publish that concrete blocker and continue eligible product work using already adequate trusted legacy checks; do not add infrastructure scope while waiting. Product interfaces and necessary coverage remain required.

## Superseded scope
Earlier signature, artifact-archive, expiry simulation and recovery-system requirements are superseded by Marcel's explicit 2026-10-26 receipt decision. No existing implementation is marked accepted by this rewrite.

Source assignment: <https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md> (three concurrent worker packages; coordinator owns integration).
