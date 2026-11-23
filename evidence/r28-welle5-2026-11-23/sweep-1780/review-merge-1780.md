# Mission m_rev_1780 — PR #1780

## PLAN

1. Read the mission and verify scope, candidate, required checks, and evidence path.
2. Refresh GitHub and Planning state; verify the exact PR head, base, and branch provenance.
3. Inspect the candidate diff, task write-set, catalog neutrality, workflow scope, and targeted test execution evidence.
4. Verify every required exact-head check and run the authorized merge only if all acceptance gates pass.
5. Publish evidence, update the board, verify remote witnesses, and post the final status.

## Review scope and candidate

- Mission: `/tmp/opencode/m_rev_1780.md.g`, PR #1780, card 0428-241, candidate `lane-0428-241-footprint-consent`.
- Product remote verified by `git -C baseharbor remote -v`: `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `(push)`; all remote reads below use that GitHub URL.
- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- PR API: open, not draft, head `5a05da37c8c0ec6813f398bae1fb5f542c06cc2e`, base ref `develop` at `7880a8f6bcfaabd8fd254ef987522abc1770c52e`, mergeable, merge state `behind` at review time.
- Initial live witness for the mission base: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1780/head` returned `7880a8f6bcfaabd8fd254ef987522abc1770c52e refs/heads/develop` and `5a05da37c8c0ec6813f398bae1fb5f542c06cc2e refs/pull/1780/head`.
- Later fresh remote witness: develop advanced to `0c1b8ca2ff4a057853432a7a565040be57cade06`; PR head remains `5a05da37c8c0ec6813f398bae1fb5f542c06cc2e`.
- `git merge-base --is-ancestor 7880a8f6bcfaabd8fd254ef987522abc1770c52e lane-origin/pr/1780` passed. Against fresh `lane-origin/develop` (`0c1b8ca2ff4a057853432a7a565040be57cade06`), the same ancestry check failed (exit 1).
- `git log --oneline 7880a8f6bcfaabd8fd254ef987522abc1770c52e..lane-origin/pr/1780` listed only the 0428-241 changes and its develop-hop/merge commits: `5a05da37c`, `87ba9bac2`, `92ba5d810`, `ef6de8504`, `56b1571ea`, `36c679823`, `c95c2377c`, `78171ae9d`.

## Diff and acceptance review

- Fresh comparison against current develop lists exactly `cmd/baha/app_capability_runtime_test.go`, `scripts/ci-native-pr-gate.sh`, `scripts/pre-release-integration.py`, and `scripts/test_pre_release_integration.py`.
- Current-develop numstat: `163 0` for `cmd/baha/app_capability_runtime_test.go`, `4 0` for `scripts/ci-native-pr-gate.sh`, `7 0` for `scripts/pre-release-integration.py`, and `3 0` for `scripts/test_pre_release_integration.py`. All are test/harness routing and registration; there is no product implementation change.
- `git diff lane-origin/develop...lane-origin/pr/1780 -- .github/` produced no paths. `git diff --quiet lane-origin/develop lane-origin/pr/1780 -- scripts/pr-gate-coverage.json` passed, so the catalog is byte-identical to current develop.
- The 0428-241 task contract is `tasks/t-20261122-guided-fixture-footprint-contract-divergence.md`, closed/accepted, and lists PR #1780. The separate 0428-251 demo adaptation is blocked by its owner finding that no demo change is needed; this review does not treat that distinct card as the #1780 write-set.
- Test review: `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` at candidate lines 363-485 exercises pre-apply footprint show, fail-closed apply without consent, extracts the 64-hex digest from the refusal, re-applies through the existing `coreBootstrapFixtureConsent` helper, then confirms read-only footprint show succeeds. The helper recomputes consent from the unchanged resolved submission; a mismatch would leave apply rejected. No product consent boundary is edited.
- Gate routing is in the same PR: the test is selected by native Docker/Podman `data-capabilities` and `coreless-lifecycle` paths in `scripts/ci-native-pr-gate.sh`, and by the `core-capability` shard in `scripts/pre-release-integration.py` with a corresponding registration assertion in `scripts/test_pre_release_integration.py`.

## Hosted checks and execution witnesses

- Run `45113316321`: `completed`, `success`, event `pull_request`, exact head `5a05da37c8c0ec6813f398bae1fb5f542c06cc2e`, updated `2026-11-23T05:04:52Z`.
- Terminal required aggregate: job `137497390395`, `PR Selected Checks: PASS` at `2026-11-23T05:04:49Z`; integration id 15368. The run summary reports 30/30 checks successful for its selected plan.
- Trusted Plan job `137490367624` succeeded with exact `BASE_SHA: 7880a8f6bcfaabd8fd254ef987522abc1770c52e`; the plan selected Go scope `cli`. No “No narrow mapping” fallback warning was emitted.
- Exact targeted test execution was verified in the owning jobs, not inferred from the aggregate: Docker core-capability job `137490462004` logged `TestApplicationCapabilityLifecycleFootprintShowDigestConsent` running and `PASS` at `2026-11-23T04:54:05Z` (89.36s); its summary names `go test -race -count=1 -json ./cmd/baha -run ^TestApplicationCapabilityLifecycleFootprintShowDigestConsent$ -timeout 30m`. Podman core-capability job `137490461623` logged the same exact test and `PASS` at `2026-11-23T05:00:32Z` (112.76s), with the same test command.
- Advisory checks are reported separately: `PR · Candidate-added checks (advisory)` job `137490419835` succeeded; these checks are not represented as required base-plan gates. Unselected release/HA/other shards were skipped by the selected plan and are not claimed as passes.
- Active ruleset `develop - required checks` (id `25223521`) requires `PR Selected Checks` from integration 15368 and has strict up-to-date status enabled. Therefore the previously green exact-head run on base `7880a8f6…` does not authorize merging after develop advanced to `0c1b8ca2…`.

## Verdict and handoff

- ROLLE: REVIEW — source scope, test routing, catalog neutrality, `.github` neutrality, and exact-head execution pass for the mission’s stated base and SHA.
- VERDICT: BLOCKED — do not merge this stale-base head. GitHub currently reports the PR `behind`, and the active strict required-check ruleset means the candidate is not current with develop. No PR update, rerun, workflow dispatch, or merge was performed in this review.
- Recipe: refresh the same candidate branch `lane-0428-241-footprint-consent` onto the current develop head `0c1b8ca2ff4a057853432a7a565040be57cade06`; before any candidate push run `bash scripts/ci-fast-check.sh`, then observe the terminal `PR Selected Checks` aggregate and exact Docker/Podman core-capability test jobs for the resulting head. Re-review and normal expected-head squash merge only after those required checks pass on the current base.
- ROLLE: MERGE — not executed because the exact current-base acceptance gate is not met.

## repo-rule compliance

- Review-only work; no product files changed, no workflow files edited, no workflow rerun/dispatch, no product push, no test added or run locally, and no container/compose project started.
- No subagents used. The one planning evidence file is in the planning repository, not a product repository.

## cleanliness

- Session PID `3898554`; `docker ps -a` before review work: empty (header only).
- Session PID `3898554`; `docker ps -a` after review work: empty (header only).
- No test-owned containers, networks, volumes, or state directories were created by this session.

END_BLOCKED codex-rev2-1736: #1780 reviewed; current develop is ahead of the tested base; no merge. Candidate `5a05da37c8c0ec6813f398bae1fb5f542c06cc2e`.
