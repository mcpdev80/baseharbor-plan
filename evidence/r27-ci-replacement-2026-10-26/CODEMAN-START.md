# Codeman: v0.4.27 CI replacement — current work order

**Owner restart, 2026-10-29:** Codeman is authorized to work autonomously with multiple workers in small parallel iterations until the new CI is implemented, verified and enforced. There is no timebox or legacy-check fallback for feature development. This order supersedes older pause, deadline, fallback and fixed worker-count instructions. Preserve historical evidence and claims. This is not authorization to tag or publish a release.

## Owner clarification — 2026-11-02

The current Owner instruction supersedes older receipt-specific approval and proof requirements below: the receipt is a small commit record (the actual merged commit SHA and PR reference), not a claim that CI passed. The receipt writer checks the commit binding; it does not re-query or re-judge GitHub Actions runs or jobs. GitHub Required Checks enforce actual CI outcomes before merge; the Owner makes the merge decision, with no separate receipt approval dispatch. Preserve existing V1 receipts and their readers as historical data. Never fabricate a PASS or weaken required checks, source authentication or SHA binding.

As of this clarification, the change is not deployed or accepted. Core drafts [#1335](https://github.com/mcpdev80/baseharbor/pull/1335) (commit-only receipt) and [#1336](https://github.com/mcpdev80/baseharbor/pull/1336) (advanced-base CI repair) require review and actual GitHub-hosted qualification. Workflow and Planning write-source protection, token scope, GitHub event policy, missed-event recovery and an actual end-to-end proof remain open. Required rulesets are disabled; do not claim GitHub enforces them yet. No release or tag is authorized.

The older sections below describe the prior V1 pilot and its history; wherever they demand a separate Owner receipt approval, job/run re-verification by the receipt writer, or an approved-pilot receipt as a new required check, this clarification takes precedence. Continue to preserve the proven CI checks and their fail-closed behavior.

## Goal
Complete the automatic producer → plan/receipt → Owner decision → approved publication → retained verification chain and replace the old required CI path for current development. Regular product feature work waits for verified new CI cutover. A bounded real profile-contract producer is permitted as an explicit pilot slice; select and reserve its exact files after checking current startup state. Existing test implementations and valid evidence may be reused in the new execution path; do not call legacy enforcement the completed replacement.

## Coordination and small iterations
Refresh remote heads, running jobs, claims, unpublished work and runner capacity first; preserve others' work. Coordinator publishes task claims and exact disjoint file reservations before dispatch; integrate small coherent results, reassign free workers to executable work and update board after each handoff. Worker count is based on real independent work and available resources, not a fixed limit. No competing edits to shared files or invented interfaces. Read product rules, use targeted checks and existing valid evidence; no repeated full matrices or synthetic passes. Owner-authorized maintainer acceptance is allowed, do not label it independent review unless independently performed.

## First parallel slices
- [Coverage inventory](../../tasks/t-20261029-r27-ci-coverage-inventory.md): inventory current required contexts, tests, runners, source and mapping; read-only.
- [Approval pins](../../tasks/t-20261029-r27-ci-approval-pin.md): resolve empty TRUSTED_SOURCE and shadow pin with targeted checks. Coordinate verifier edits with existing owner.
- [Producer](../../tasks/t-20261029-r27-ci-producer.md): select and qualify one real public-contracts producer; reserve product paths and check planner.
- [Cutover design](../../tasks/t-20261029-r27-ci-cutover-design.md): identify asynchronous exact-candidate check, app and ruleset transition; read-only before implementation.
- Existing [publisher](../../tasks/t-20261022-r27-evidence-publisher.md) and [verifier](../../tasks/t-20261022-r27-evidence-verifier.md) cards remain integration/acceptance parents. Coordinator splits only concrete residual gaps into bounded tasks; avoid duplicating work and confirm live state before editing.

## Proof and cutover
Verify default-branch workflow registration, immutable pins and publication rights without exposing secrets. On one real successful producer prove automatic plan, receipt and task link; Owner selects the PR for the actual approval, then automatic publication and retained-only shadow run. Verify wrong candidate, genuinely missing run and edited receipt/history fail for their intended reasons, and retained positive works without origin API. Keep exact commits/runs and honest results. Only then accept shadow and chain. Do not infer success from a skipped job.

Map all current required checks to new selected execution, enforce correct candidate-bound completion, verify success and missing/failed/mismatched behavior and ruleset transition before retiring old required contexts. Implement only actual coverage gaps; preserve required security and isolation. Activation follows the accepted chain and verified replacement; retain a documented rollback for operational failure, not a planned legacy development fallback. The Owner has authorized this cutover within this task. Check actual GitHub permissions and required checks; never bypass failed checks.

The four domain cards distinguish baseline CI capability from later product-specific tests; do not require future unimplemented product interfaces to prove current CI readiness. Coordinator updates the real dependency graph, generated views and evidence after each accepted slice, without marking unproven work accepted. Close the CI integration card only with coverage map, actual enforcement and proof; then allow ordinary feature work.
