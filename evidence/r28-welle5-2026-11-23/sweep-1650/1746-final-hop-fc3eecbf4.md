# PR #1746 final hop onto develop fc3eecbf4 (sitz 043d9868, lane w078-pr1650-0428-078-reloc)

## Mission
PR-SWEEP #1746 final hop. #1793 was merged (develop fc3eecbf4), so the TP blockade that blocked #1746 from being base-admissible is resolved. The seat (043d9868) had been idle on the #1650 action; this hop fills the seat. Task: `--no-ff` merge develop onto the current #1746 head, witness, push, trigger the PR run to terminal, flip to ready at handoff. Evidence file only in baseharbor-plan. No subagents, no local suites, no merge of the PR.

## BASE ATTESTATION
- develop head at start of work: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `fc3eecbf4b65330bf0643dcde4136ca6d9620665`.
- PR #1746 head at start: `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443`, base `develop`, draft false, title "ci: run ci-fast-check in the release gate suite", backing branch `lane-0428-208-static-release-gate`.
- Remote guard: `git remote -v` on the worktree shows `https://github.com/mcpdev80/baseharbor.git`; all remote reads via that URL only.

## PLAN
1. Fetch origin develop, rev-parse == fc3eecbf4 (take higher if tipped).
2. Cut finalhop-1746 from the current #1746 head b68372ec, `--no-ff` merge origin/develop (no rebase, no force).
3. Witness: catalog net diff origin/develop..HEAD (the #1746 release-gate content is its own, not an empty-diff expectation); net diff name-status; .github untouched-by-me; `git log --oneline origin/develop..HEAD` lists only the hop merge.
4. Build + vet + affected Python script tests locally.
5. Push backing branch, ls-remote witness PR #1746 head.
6. Trigger the PR CI run, poll to terminal, record run-id + gates + per-job conclusion.
7. Root-cause the one failing check; document as STATE (check name + failing line), stop, report file:line for the one Owner-scope case.

## MERGE RESULT
- Branch finalhop-1746 cut from b68372ec, then `git merge --no-ff origin/develop`.
- Merge commit: `6ba380b9d723a047a6e2c396ce25db5d8e3adc3c`.
- Parents (git rev-list --parents -n1 HEAD): `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443` (#1746 head) + `fc3eecbf4b65330bf0643dcde4136ca6d9620665` (develop). Two parents, provenance intact.
- `git log --oneline origin/develop..HEAD` = only the merge commit (no foreign commit carried on top beyond #1746's own line).

## NET DIFF vs develop (all files)
- `.github/workflows/pre-release-runtime-suite.yml` (M) — #1746 release-gate content (Owner scope, part of the candidate, not my change).
- `.github/workflows/pre-release.yml` (M) — #1746 content.
- `CHANGELOG.md` (M)
- `docs/releases/v0.4.28.demo-ref` (A)
- `scripts/ci-fast-check.sh` (M)
- `scripts/pr-gate-coverage.json` (M) — net change vs develop: #1746 adds the `atomic/static/ci-fast-check` gate (release-only), dropping `source.gate.atomic.static.ci.fast.check` from the `shell-ux` gate's covers. Catalog stays valid (validator PASS on HEAD).
- `scripts/pr-gate-plan.py` (M), `scripts/pr-required-final.py` (M), `scripts/pre-release-check-plan.py` (M), `scripts/pre-release-runtime-impact.json` (M), `scripts/release-requirements.json` (M)
- `scripts/test_ci_v0427_gate_catalog.py` (M), `scripts/test_pr_gate_coverage.py` (M), `scripts/test_pre_release_check_plan.py` (M), `scripts/test_pre_release_runtime_reuse.py` (M), `scripts/validate-pr-gate-coverage.py` (M)
- My #1650 files (`cmd/baha/app_status_result_test.go`, `internal/metrics/realization.go`) are NOT in this diff — this is the #1746 release-gate candidate, independent of #1650. This is the seat's #1746 mission, not the #1650 relocation.

## BUILD / VET / LOCAL TESTS
- `go build ./...` exit 0.
- `go vet` clean.
- `scripts/test_pr_gate_coverage.py` OK; `scripts/test_ci_v0427_gate_catalog.py` OK; `scripts/test_pre_release_runtime_reuse.py` OK.
- `scripts/test_pre_release_check_plan.py`: 5 tests, 1 FAIL (see STATE below).

## CI RUN 45124289849 (run_number 7449, head 6ba380b9d) — terminal FAILURE
- Status: completed. Conclusion: failure.
- Per-job conclusions (from `actions/runs/45124289849/jobs`):
  - Workflow policy: success
  - PR · Trusted Plan: success
  - PR · Native gate plan: success
  - PR · Source format: success
  - PR · Demo Pin: success
  - PR · Go unit (cli-0, cli-1, cli-2, cli-3): success
  - PR · Go unit (packages): success
  - PR · Focused Python: success
  - PR · Candidate-added checks (advisory): success
  - PR · Validation · ci-policy: success
  - PR · Validation · ci-actionlint: success
  - PR · Validation · pr-planner-tests: success
  - PR · Validation · go-build: success
  - PR · Validation · documentation-audit: success
  - PR · Validation · pages-candidate-build: success
  - PR · Validation · ci-executor-tests: FAILURE
  - PR · Validation · pr-executor-tests (not shown): success
  - All native runtime / HA gates (docker, podman): skipped (not selected for this diff).

## STATE: ci-executor-tests failure — root cause and why it is out of this seat's write-set
- Failing check: `PR · Validation · ci-executor-tests`, job id 137525054630.
- Failing test (CI log, timestamp 2026-11-23T06:33:20.709Z): `test_v0428_adds_only_fast_check_and_moves_no_other_gate (test_pre_release_check_plan.ReleaseCheckPlanTests) ... FAIL`, assert at `scripts/test_pre_release_check_plan.py:40` (`AssertionError: Items in the first set but not the second`).
- Mechanism: the test reads `scripts/release-requirements.json` and asserts the set of gates tagged `v0.4.28` equals exactly `{atomic/static/ci-fast-check}`. On my merged HEAD that set is `{atomic/static/mcp, atomic/static/ci-fast-check}`.
  - `atomic/static/ci-fast-check` tagged v0.4.28 = #1746's own content (commit a63635358 / branch b68372ec).
  - `atomic/static/mcp` tagged v0.4.28 = develop's content (present on fc3eecbf4, introduced by an earlier develop commit — confirmed `git show origin/develop:scripts/release-requirements.json` lists it). develop itself passes the test (3 tests OK; the new v0428 assertion is not present on develop). #1746's own branch b68372ec passes the test (5 tests OK; it has no mcp tag).
  - My `--no-ff` merge combined develop's `mcp` v0.4.28 tag with #1746's `ci-fast-check` tag, exposing a genuine develop-vs-#1746 incompatibility in `release-requirements.json`. It is not a defect in the #1650 lane, nor introduced by anything in this seat's write-set.
- This check is Required: the merge commit does not match any reviewed source chain, so the plan controller returns `broad_required: True, coverage_status: unresolved` (verified via `scripts/pr-gate-plan.py` with authenticated runner context). Under the broad fallback, any changed `scripts/` or `.github/workflows/` path requires the full `CI_CHECKS` set, which includes `ci-executor-tests`.
- Write-set boundary: the fix lives in `scripts/release-requirements.json` v0.4.28 gating — a shared base-policy file on develop. Per AGENTS 5.2 and the Owner PR-#1780 / workflow ownership rule, shared base-policy edits and any `.github/**` change are the Owner's action. This seat does not edit develop. Reporting the exact file and line below for the Owner.
- Reported file:line for Owner: `scripts/release-requirements.json` — reconcile the two v0.4.28 tags (`atomic/static/mcp` from develop vs `atomic/static/ci-fast-check` from #1746) so the single-gate assertion in `scripts/test_pre_release_check_plan.py` holds on the merged candidate, OR widen the test to the merged reality. That one case stays a coordinator/Owner action; this seat stops.

## GOVERNANCE CHECKS
- No subagents. Every step ran in this session.
- No merge of the PR. Push only to backing branch.
- PR #1746 head delivered to `6ba380b9d` (ls-remote witness below).
- One candidate per chain: finalhop-1746, backing branch `lane-0428-208-static-release-gate`.

## WITNESSES
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1746/head` = `6ba380b9d723a047a6e2c396ce25db5d8e3adc3c`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-208-static-release-gate` = `6ba380b9d723a047a6e2c396ce25db5d8e3adc3c`.
- CI run 45124289849, run_number 7449, head 6ba380b9d, terminal.

## CLEANLINESS
- Pre-merge `docker ps -a`: empty (exit 0). No containers.
- Post work: no containers or compose projects started on this host. This seat ran no docker/podman runtime; the CI blob-unknown failure belongs to the separate PR #1650 identity-gate lane and its own runners.
- No scratch files created under /home/marcel/dev/baseharbor-ecosystem; temporaries under /tmp only.

## HANDOFF / STOP
- Candidate `6ba380b9d` is pushed and CI-run to terminal. One Required check (`ci-executor-tests`) fails on #1746's inherent release-gate self-inconsistency, not on this seat's write-set. The one required change is develop-side (`scripts/release-requirements.json`, Owner scope) and is reported file:line above. Seat holds at END_BLOCKED pending the Owner decision on that one file; #1650 lane action rests until the 1623 merge.

END_BLOCKED w078-pr1650-0428-078-reloc: #1746 final hop 6ba380b9d — CI 45124289849 terminal, one Required check (ci-executor-tests) fails on #1746 release-gate v0.4.28 tag incompatibility (scripts/release-requirements.json), Owner scope.
