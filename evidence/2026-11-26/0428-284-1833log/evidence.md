# w263-0428-284-1833log — Failure-log diagnosis for PR #1833

ROLE: read-only failure-log diagnosis (card of chain, supports Codex disposition in w252)
STATUS: END_DONE
CANDIDATE SHA (read-only): a7b0a48048c11d20234160eede941532ddc33156
DATE: 2026-11-26

## PLAN
- ls-remote develop tip; gh pr view 1833 (head a7b0a48-era, state, base)
- runs API per_page=100 on that head: every pull_request run ID with status/conclusion/created_at; for the failing ones FULL jobs table (executed vs skipped) and exact FAILING STEP LOG LINES verbatim
- Map each failure to its deciding config/code line (file:line); classify as (i) ancestry artifact, (ii) trigger-context classification, (iii) real defect
- Answer which failures remain after #1842 lands and #1833 absorbs the tip
- END_DONE: table + one-line answer + akte via plan-PR branch path (no plan-PR merge; direct-main forbidden)

## Reality witnesses
- plan repo remote (git -C baseharbor-plan remote -v): origin=https://github.com/mcpdev80/baseharbor-plan.git
- develop tip (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee
- PR #1833 (gh pr view -R github.com/mcpdev80/baseharbor 1833): number 1833, state OPEN, base develop, base sha f7540e591609e0db6453e9b690fbb5d6686448a2, headRef lane-0428-288-compose-ids, headOid a7b0a48048c11d20234160eede941532ddc33156, title "fix(0428-288): preserve Compose service IDs through workload preflight"
- baseharbor product remote resolved: origin=https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80)

## (1) Runs on failing head a7b0a48 (gh api .../actions/runs?pull_request=1, per_page=100) — 30 runs total
run id | event | status | conclusion | attempt | title | created_at
- 45731000555 | pull_request | completed | failure | 1 | CI · PR #1842 | 2026-11-26T00:45:25Z
- 45728113999 | push | completed | failure | 1 | fix(release): resolve demo pin via releases[] semver + gate-coverage… | 2026-11-26T00:21:08Z
- 45725208272 | push | completed | success | 1 | Runtime · Docker Core · develop | 2026-11-25T23:57:26Z
- 45725208242 | push | completed | success | 1 | Runtime · Podman Core · develop | 2026-11-25T23:57:26Z
- 45717496553 | pull_request | completed | success | 1 | CI · PR #1853 | 2026-11-25T22:57:20Z
- 45717487430 | pull_request | completed | cancelled | 1 | CI · PR #1853 | 2026-11-25T22:57:15Z
- 45717078703 | pull_request | completed | success | 1 | CI · PR #1842 | 2026-11-25T22:54:09Z
- 45716254159 | pull_request | completed | cancelled | 2 | CI · PR #1853 | 2026-11-25T22:47:56Z
- 45716226824 | pull_request | completed | success | 1 | CI · PR #1842 | 2026-11-25T22:47:44Z
- 45715757627 | pull_request | completed | success | 1 | CI · PR #1853 | 2026-11-25T22:44:18Z
- 45713698195 | push | completed | success | 1 | Runtime · Podman Core · develop | 2026-11-25T22:29:47Z
- 45713698146 | push | completed | success | 1 | Runtime · Docker Core · develop | 2026-11-25T22:29:47Z
- 45713494016 | pull_request | completed | success | 1 | CI · PR #1842 | 2026-11-25T22:28:17Z
- 45712217182 | pull_request | completed | success | 1 | CI · PR #1842 | 2026-11-25T22:19:22Z
- 45711869496 | pull_request | completed | success | 1 | CI · PR #1850 | 2026-11-25T22:16:56Z
- 45710380590 | pull_request | completed | success | 1 | CI · PR #1820 | 2026-11-25T22:06:42Z
- 45709369458 | pull_request | completed | success | 1 | CI · PR #1850 | 2026-11-25T22:00:01Z
- 45709363023 | pull_request | completed | cancelled | 1 | CI · PR #1850 | 2026-11-25T21:59:58Z
- 45709326054 | pull_request | completed | success | 1 | CI · PR #1812 | 2026-11-25T21:59:41Z
- 45707682812 | pull_request | completed | success | 1 | CI · PR #1850 | 2026-11-25T21:48:25Z
- 45707680053 | pull_request | completed | cancelled | 1 | CI · PR #1850 | 2026-11-25T21:48:24Z
- 45707597763 | pull_request | completed | cancelled | 1 | CI · PR #1850 | 2026-11-25T21:47:51Z
- 45703956650 | push | completed | success | 1 | Runtime · Podman Core · develop | 2026-11-25T21:23:51Z
- (schedule Repository GC runs: success, omitted from failure analysis)

## (2) Failing jobs: FULL jobs table (executed vs skipped)

### Run 45731000555 (pull_request "CI · PR #1842", head dfd3495858501fe49d9c331c056a4289b780e0f8)
Job | status | conclusion
- PR · Native gate plan | completed | success
- Workflow policy | completed | success
- PR · Source format | completed | success
- PR · Trusted Plan | completed | success
- validate | completed | skipped
- PR · Main release Go | completed | skipped
- PR · Draft Go | completed | skipped
- Targeted HA · docker | completed | skipped
- Targeted HA · podman | completed | skipped
- Release Source Preflight | completed | skipped
- PR · Main release source | completed | skipped
- PR · Exact full Pre-Release | completed | skipped
- PR · Native | completed | skipped
- PR · Draft source and routing | completed | skipped
- Targeted · Workstation onboarding | completed | skipped
- PR · Focused Python | completed | FAILURE
- PR · Candidate-added checks (advisory) | completed | FAILURE
- PR · Validation · pr-planner-tests | completed | FAILURE
- PR · Validation · go-vet | completed | success
- PR · Go unit · owner | completed | success
- PR · Validation · receipt-execution-tests | completed | success
- PR · Go unit · cli-2 | completed | success
- PR · Go unit · packages | completed | success
- PR · Go unit · cli-0 | completed | success
- PR · Go unit · cli-1 | completed | success
- PR · Go unit · cli-3 | completed | success
- PR · Validation · ci-executor-tests | completed | FAILURE
- PR · Validation · ci-policy | completed | success
- PR · Validation · go-build | completed | success
- PR · Runner Interface | completed | skipped

18 of the 30 listed jobs executed (completed success or failure); 12 were skipped. The six listed Go-unit shards (`owner`, `cli-2`, `packages`, `cli-0`, `cli-1`, `cli-3`) completed successfully. The release, HA, native, and pre-release jobs marked skipped did not run, so this PR run does not qualify those runtime gates.

### Run 45728113999 (push) — 0 jobs / 0 steps (workflow never dispatched; conclusion=failure, start_failure=none)

## (3) Exact FAILING STEP LOG LINES verbatim

### PR · Focused Python (job 139612747191, run 45731000555) — FAILED (failures=1, skipped=1); exit code 1
FAIL: test_v0427_demo_pin_uses_only_exact_source_validation (test_pr_ci_fallback.ConservativeFallbackTests)
  File ".../scripts/test_pr_ci_fallback.py", line 176
    self.assertNotIn('fallback_used', result)
  AssertionError: 'fallback_used' unexpectedly found in {… 'coverage_status': 'resolved', 'selected_gates': [], 'required_validation_checks': [{'id': 'go-build', …},{'id': 'go-unit-tests', …},{'id': 'go-vet', …}], 'reasons': ['docs/releases/v0.4.27.demo-ref: unresolved', 'No declared runtime gate owner for: docs/releases/v0.4.27.demo-ref', 'Unknown narrow coverage selects normal broad unit/vet/build checks; runtime gates require declared coverage.'], 'fallback_used': True, 'fallback_reasons': ['unknown impact for docs/releases/v0.4.27.demo-ref']}

### PR · Candidate-added checks (advisory) (job 139612747241) — exit code 1
2026-11-26T00:45:55.0476315Z - `demo-source-pin-validation`: FAIL; candidate command: `python3 scripts/pr-check-runner.py execute --check demo-source-pin-validation --repository .`
2026-11-26T00:45:55.0486390Z RuntimeError: v0.4.28 Demo source commit does not resolve in the pinned repository
(called from pr-check-runner.py:478 main -> 459 validate_demo_source_pin -> 399)

### PR · Validation · pr-planner-tests (job 139612747265) — FAILED (failures=12, skipped=2); exit code 1
FAIL: test_v0427_demo_pin_uses_only_exact_source_validation (test_pr_ci_fallback) — same AssertionError: 'fallback_used' unexpectedly found (docs/releases/v0.4.27.demo-ref: unresolved, fallback_used:True)

### PR · Validation · ci-executor-tests (job 139612747392) — FAILED (failures=11); exit code 1
FAIL: test_v0427_demo_pin_uses_only_exact_source_validation (test_pr_ci_fallback) line 176 -> 'fallback_used' unexpectedly found
FAIL: test_demo_pin_mixed_with_other_change_is_unresolved (test_pr_gate_coverage) line 681 -> AssertionError: False is not true
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.22') line 691 -> 'resolved' != 'unresolved'
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.23') line 704 -> 'resolved' != 'unresolved'
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.24') line 717 -> 'resolved' != 'unresolved'
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.25') line 730 -> 'resolved' != 'unresolved'
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.26') line 743 -> 'resolved' != 'unresolved'
FAIL: test_each_active_release_demo_ref_resolves_to_source_validation (release='v0.4.27') line 756 -> 'resolved' != 'unresolved'
FAIL: test_v0427_demo_pin_is_resolved (test_pr_gate_coverage) line 769 -> 'resolved' != 'unresolved'
FAIL: test_demo_ref_release_must_match_mapping_release (test_pr_gate_coverage) line 782 -> 'unresolved' != 'resolved'
FAIL: test_v0427_demo_ref_still_selects_exact_pin_validator (test_pr_gate_coverage) line 795 -> 'resolved' != 'unresolved'

## (4) Root-cause mapping (each failure -> deciding config/code line; classification)

### Focused Python / pr-planner-tests: demo-ref catalog missing -> broad fallback (the core defect)
- Deciding code: scripts/pr-gate-plan.py:1706 `unresolved.append('unknown impact for ' + path)` + scripts/pr-gate-plan.py:1910-1911 sets fallback_used=True and adds the broad go-build/go-unit-tests/go-vet checks.
- The failing test test_pr_ci_fallback.py:176 (and test_pr_gate_coverage.py) assert docs/releases/v0.4.27.demo-ref resolves via the docs/release path to `demo-source-pin-validation` (a single targeted required_validation_check), NOT the broad fallback.
- Verdict on the catalog: docs/releases/v0.4.27.demo-ref is NOT a cataloged component row in scripts/pr-gate-coverage.json on BOTH develop (301 components) AND the failing head (293 components). develop lists 0 demo-ref component rows; the failing head lists 0 too. The failing head REMOVED additional catalog rows (see below).
- Classification: (iii) real product defect — the docs/release demo-ref path is not wired into the coverage catalog, so the fail-loud planner treats it as unknown impact and falls back to the broad Go checks (which the test forbids). This is NOT an ancestry artifact: it exists on develop identically.

### Candidate-added (advisory): demo-source-pin-validation fails on missing gh auth
- Deciding code: scripts/pr-check-runner.py:384-400 validate_demo_source_pin -> :395 calls `gh api repos/mcpdev80/baseharbor-demo/commits/<sha>` -> :398-399 raises RuntimeError 'v0.4.28 Demo source commit does not resolve in the pinned repository' when the SHA cannot be authenticated.
- Run 45731000555 GITHUB_TOKEN permissions: Contents: read, Metadata: read (from the runner log). No read access to mcpdev80/baseharbor-demo (a separate repo) -> the gh api 404s -> RuntimeError.
- The run head dfd3495858501fe49d9c331c056a4289b780e0f8 pins demo commit 6591a7235370683704d98986b0311b4588d51345; the failing advisory uses release v0.4.28 pin (b14d391e3605659205f914f15f231f2575420735) which cannot be resolved by this token.
- Classification: (ii) trigger-context classification — the advisory demo-source-pin-validation requires Owner/CI auth for the separate demo repo; without it it always fails. Not a code defect; an auth-context gap.

### Push run 45728113999 (0 steps) — never dispatched
- gh api runs/45728113999: event=push, steps=0, jobs=0, start_failure=none. The push gate job never created steps; no FAILING STEP LOG LINES exist to quote.
- Classification: (i)/(ii) environmental — a push-run that failed at dispatch/setup, not attributable to a product code line visible here.

### Test-method presence note (evidence integrity)
- CI executed classes/methods ReleaseDemoPinSelectionTests / ReleaseDemoPinSelectionRegression / test_v0427_demo_ref_still_selects_exact_pin_validator that are NOT present in either the failing head tree (a7b0a48) or develop for scripts/test_pr_gate_coverage.py. The CI-run head was dfd3495858501fe49d9c331c056a4289b780e0f8 (run_number=7824). The tree at a7b0a48048c11d20234160eede941532ddc33156 has only CoverageCatalogTests. So CI ran a test file that differs from the current PR head — a head drift between run head and PR head. This must be resolved before any acceptance of #1833.

## (5) Answer: which failures remain after #1842 lands and #1833 absorbs the tip?

ONE failure remains after absorption: the demo-ref catalog gap (Focused Python + pr-planner-tests), classified (iii) real product defect. It is an ancestry artifact for NOTHING — it exists identically on develop, so absorbing the tip does not change it. The catalog simply lacks a docs/release demo-ref component row that routes docs/releases/v0.4.N.demo-ref to the `demo-source-pin-validation` targeted check; the failing planner hits pr-gate-plan.py:1706 unknown-impact and falls back to the broad Go unit/vet/build checks the test forbids.

The other two failure clusters do NOT remain:
- The advisory demo-source-pin-validation failure (ii) is an auth-context artifact of the pull_request run's Contents:read/Metadata:read token lacking access to the separate baseharbor-demo repo; it is not a product defect and is orthogonal to absorption.
- The push run 45728113999 (i) never dispatched (0 steps) and is environmental, not attributable to any product line.

One-line answer: Only the demo-ref catalog gap survives absorption — the docs/release demo-ref path is not wired into scripts/pr-gate-coverage.json, so the fail-loud planner (scripts/pr-gate-plan.py:1706) marks docs/releases/v0.4.27.demo-ref unresolved and falls back to the broad Go checks (scripts/pr-gate-plan.py:1910-1911); this defect is present on develop identically and cannot disappear by absorbing the tip. Everything else (advisory gh-auth, the un-dispatched push run) is trigger-context/environmental.

## Repo-rule compliance
- Read-only: no writes, no commits, no pushes, no merges, no CI triggers, no reruns. All facts measured via `gh api` and `git show`/`git ls-tree` against github.com/mcpdev80/baseharbor and the plan repo origin.
- No .github/** edits, no workflow_dispatch/rerun.
- No subagents.
- Evidence written only to baseharbor-plan evidence path (plan-PR branch), never a product repo.

## Cleanliness
- No containers/compose projects started. No docker/podman state touched.
- No scratch files created in the ecosystem root; temp files under /tmp only.

## Handoff
- This akte is prepared for Codex publication via a baseharbor-plan PR (no direct-main writes, no plan-PR merge by this lane).
