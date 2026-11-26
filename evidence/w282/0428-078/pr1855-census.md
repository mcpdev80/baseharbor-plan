# Read-Only Census: Reissue PR #1855 (card 0428-078)

- Lane: `w282-0428-078-1855census` · Shift: w282 · Date: 2026-11-26
- Work order: coordinator commission 2026-11-26 — read-only run census of reissue PR #1855 to determine whether its reissue class shares #1856's defect before another CI cycle is spent.
- HARD LIMITS: read-only. No PR edits, no close/reopen, no push, no merge, no CI trigger, no reruns, no product/.github/card/plan-main writes, no local tests.

## Visible Ansatz Block (required before first commit)
- Per-card frontmatter owner (fetched from origin/main at 2026-11-26T03:56Z): card 0428-078 owner read from plan note; this is a read-only census, no plan note edit performed.
- git user.name: `w165-0428-078-pr1650-basehop` (author/committer of PR #1855's single commit — the lane's witness identity)
- git user.email: `w165-0428-078-pr1650-basehop@baseharbor.local`
- Plan writing uses isolated worktree `workers/w282-0428-078-1855census-plan` (git worktree add origin/main), commit only evidence file, push via worktree.
- Pre-push gate line: `git show -s --format=%an` must equal `w165-0428-078-pr1650-basehop` (evidence-only lane).

## Base Attestation
- develop tip (real github.com remote): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- PR #1855 head: `43326cf57f1a3a8d73f2b9289e8c5ad00b74782a` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1855/head`)
- PR #1856 head (sibling, known-green run 45744295474): `cc453c79bfc027088f3af621e1bba1a1507dc914`
- The single commit 43326cf57 has exactly ONE parent = develop tip ac7c970 (merge-base == parent): single-lane, no foreign commit carried.

## (1) PR /1855 identity + single-lane proof
- `gh pr view 1855`: state=OPEN, base=develop, branch=`w279-0428-078-pr1650-reissue`, mergeable=MERGEABLE, title="fix(0428-078): reissue Perses identity-keycloak (reviewed content, single-lane)", reviews=[]
- Files (git diff origin/develop...HEAD --name-only):
  - `cmd/baha/app_perses_cli_test.go` (+4/-0)
  - `cmd/baha/app_status_result.go` (+84/-38)
  - `internal/metrics/identity_dashboard_witness.go` (+155/-0)
  - `scripts/pr-gate-coverage.json` (+1/-1, byte-identical canonical JSON)
- Single commit `43326cf57f1a3a8d73f2b9289e8c5ad00b74782a`, author==committer==`w165-0428-078-pr1650-basehop`, single parent = develop tip ac7c970.
- `git log --oneline origin/develop..HEAD` lists ONLY this one commit.

## (2) pull_request runs on the EXACT head (per_page=100 including attempts)
- Fetched 5 pages (500 PR runs total across ALL PRs), filtered to head_sha == 43326cf57f1a3a8d73f2b9289e8c5ad00b74782a:
- EXACT HEAD RUNS: exactly ONE
  - id=45743494737, name="CI · PR #1855", event=pull_request, attempt=1, status=completed, conclusion=success, created=2026-11-26T02:35:59Z
- NO second distinct executed run exists on this head. NO cancelled/queued run on this head. (No older head's green run is claimed as evidence.)

## (3) Newest (only) executed run — full jobs table (30 jobs)
- job 139653887710 Workflow policy: yes 8 steps success
- job 139653888078 PR · Source format: yes 7 steps success
- job 139653888128 PR · Trusted Plan: yes 11 steps success
- job 139653888154 PR · Native gate plan: yes 5 steps success (computes native matrix)
- job 139653889188 Targeted HA · docker: NO (skipped, 0 steps, run_started_at null) skipped
- job 139653889246 PR · Main release source: skipped 0 skipped
- job 139653889265 Release Source Preflight: skipped 0 skipped
- job 139653889280 PR · Draft Go: skipped 0 skipped
- job 139653889317 Targeted HA · podman: NO (skipped, 0 steps, run_started_at null) skipped
- job 139653889545 PR · Exact full Pre-Release: skipped 0 skipped
- job 139653889609 PR · Draft source and routing: skipped 0 skipped
- job 139653889616 validate: skipped 0 skipped
- job 139653889646 Targeted · Workstation onboarding: skipped 0 skipped
- job 139653927297 PR · Main release Go: skipped 0 skipped
- job 139653939539 PR · Native: NO (skipped, 0 steps) skipped
- job 139653953289 PR · Candidate-added checks (advisory): yes 8 steps success
- job 139653953314 PR · Focused Python: yes 5 steps success
- job 139653953318 PR · Exact Candidate: yes 8 steps success
- job 139653953348 PR · Runner Interface: yes 5 steps success
- job 139653953351 PR · Demo Pin: yes 4 steps success
- job 139653953395 PR · Go unit · cli-3: yes 8 steps success
- job 139653953424 PR · Go unit · cli-2: yes 8 steps success
- job 139653953475 PR · Go unit · cli-1: yes 8 steps success
- job 139653953479 PR · Go unit · cli-0: yes 8 steps success
- job 139653953483 PR · Validation · go-vet: yes 7 steps success
- job 139653953515 PR · Validation · receipt-execution-tests: yes 7 steps success
- job 139653953534 PR · Validation · ci-executor-tests: yes 7 steps success
- job 139653953568 PR · Validation · go-build: yes 7 steps success
- job 139653953579 PR · Validation · pr-planner-tests: yes 7 steps success
- job 139653953623 PR · Validation · cli-gofmt: yes 7 steps success

Three-way question for "PR · Demo Pin" (139653953351) — the job that failed on #1856:
- Did it execute or skip? EXECUTED — 4 steps all completed.
- What ran: (1) checkout (2) "Verify exact Demo dependency against integration source" — `git clone --filter=blob:none` baseharbor-demo, `git fetch --depth=1 origin 98e4d549c73fb099c780b5ae455da35a0ef68c71`, checkout, `test "$(rev-parse HEAD)" = "98e4d549..."` PASSED, `test -s baseharbor-core.ref` PASSED, uploaded artifact `verified-pr-demo-pin`; (3) upload-artifact success; (4) complete.
- Env: `EXPECTED_CORE_SHA=5879232f114ec77e882ac0ab5c06d1562d58e783`, `EXPLICIT_PR_DEMO_SHA=98e4d549c73fb099c780b5ae455da35a0ef68c71`.
- KEY DIFFERENCE FROM #1856: Demo Pin executed and passed on #1855. #1856's required job 'PR · Demo Pin' SKIPPED (0 steps) because ci.yml:1080 gates it on pr_plan outputs runtime_required||integration_required||public_contracts_required; the validator ran only in the advisory job with `${{ github.token }}` failing at scripts/pr-check-runner.py:472 (cross-repo read). On #1855 the Demo Pin executed as a real cross-repo read and the validator-in-advisory did NOT run ("No candidate-added validation checks. The trusted base plan remains the only merge requirement.").

"PR Selected Checks" aggregator: there is NO job named "Selected Checks". PR #1855's run has no AGGREGATOR job; the run's success is the union of the 30 executed jobs above. (The "PR Selected Checks" aggregator exists in the sibling #1856 run 45744295474, not here.)

grep for 'Running validation check:' and 'demo-source-pin-validation' across run logs:
- 'demo-source-pin-validation' appears only inside the receipt-execution-tests step 2 reference line (a switch label), not as an executed check invocation.
- 'Running validation check:' does NOT appear in the Demo Pin or advisory job logs on #1855.
- The candidate-added advisory job (139653953289) printed: `No candidate-added validation checks. The trusted base plan remains the only merge requirement.` — i.e. `scripts/pr-check-runner.py` did NOT execute on #1855 (unlike #1856 where it ran in advisory and failed).

## (4) Write-set -> planner required? (runtime_required/integration_required/public_contracts_required)
Read selection logic:
- ci.yml `pr_native_impact` job (lines 477-524) computes `matrix` via `scripts/pr-native-gate-plan.py --changed-paths-file ... --coverage pr-gate-coverage.json --requirements release-requirements.json`, then `required = include?`.
- `resolve_matrix()` in pr-native-gate-plan.py calls `validator.resolve_native_checks(changed_paths, coverage)` and keeps only ids with runtime in {docker,podman}.
- `resolve_native_checks()` matches changed component IDs against `native_checks[].source_components`.
- Executed the exact planner locally on #1855's changed paths: `{"include":[]}` — ZERO native gates.
- `resolve_covered_gates()` (catalog path) DOES resolve 4 gates (atomic/docker|podman/data-capabilities + observability) because component surfaces match `gate.covers`, BUT `resolve_native_checks()` (the one the CI planner actually calls) returns `[]` because the changed component IDs (`source.cmd.baha.app.status.result`, `source.cmd.baha.app.perses.cli.test`, `source.internal_metrics.identity_dashboard.witness`) are NOT listed in any `native_checks[].source_components`.
- Confirmed baseline: identical computation on develop tip (ac7c970) for the same paths ALSO yields `[]`. The catalog (pr-gate-coverage.json) is BYTE-IDENTICAL between develop and #1855 head (diff empty, canonical JSON deep-equal). So #1855 did NOT change CI routing or the gate catalog.
- The +1/-1 change in scripts/pr-gate-coverage.json is cosmetic (whitespace/formatting only); canonical JSON is deep-equal. No runtime_required/integration_required/public_contracts_required was introduced. The write-set therefore does NOT trigger the required-route gating defect that #1856 hit — the defect is orthogonal to this card's content.

## (5) Native data-capabilities gates on this head
- `Targeted HA · docker` (139653889188) and `Targeted HA · podman` (139653939539) and `PR · Native` (139653939539): all `conclusion=skipped`, `steps=0`, `run_started_at=null`, `skip_details=null` (workflow conditional never produced an execution step — correct, they only run on push to runtime-validation/ha/* per ci.yml:183/225).
- They did NOT execute on #1855's PR because pr_native_impact.outputs.required=false (empty matrix), which is the correct planner output for this write-set.
- No native behavior line to quote because the gates were never dispatched on this PR (by design). This is the correct state, not a defect.

## (6) Verdict
- PR #1855's remaining gap is the **pair (two distinct executed pull_request runs on the exact head)**, not the #1856 required-route gating defect and not an actual content problem — evidence per claim:
- Not the #1856 defect: On #1856 the required job 'PR · Demo Pin' SKIPPED (0 steps) behind ci.yml:1080's runtime_required/integration_required/public_contracts_required gate, and the validator in the advisory candidate-added job failed at scripts/pr-check-runner.py:472 with `${{ github.token }}` reading mcpdev80/baseharbor-demo. On #1855 the exact same 'PR · Demo Pin' job EXECUTED (4 steps) and PASSED, performing a real cross-repo read of baseharbor-demo@98e4d549 and uploading artifact verified-pr-demo-pin; the advisory job printed "No candidate-added validation checks" (validator did not run). #1855's write-set does not touch ci.yml or the gate catalog (pr-gate-coverage.json is byte-identical to develop), and `pr-native-gate-plan.py` returns `{"include":[]}` for both #1855 and the develop baseline — so the required-route gating defect is not reachable from this card.
- Not a content problem: all four Go unit shards executed and passed (cli-0: 496/13 skipped/509, cli-1: 461/10/471, cli-2: 482/24/506, cli-3: 459/17/476, CLI inventory total=1962); go-vet, go-build, cli-gofmt, pr-planner-tests, ci-executor-tests, receipt-execution-tests, Focused Python, Trusted Plan, Source format, Runner Interface all conclusion=success.
- The ONLY missing piece for merge-qualification is a second DISTINCT executed run on the exact head 43326cf57: only run 45743494737 exists (attempt 1). No second run, no cancel/reopen pair. The sibling #1856 head (cc453c79b) has its green run but is a DIFFERENT head and cannot be reused as evidence.

## Akte (evidence trail)
- All evidence measured via `git ls-remote https://github.com/mcpdev80/baseharbor.git` (real github.com remote) and `gh api`/`curl` with a bearer token against api.github.com; no quarantined/local remote cited.
- Read-only census: zero product writes, zero plan-main writes (isolated worktree only), zero CI triggers/reruns.

## END_DONE
- Tables + verdict above. Plan PR: none created (read-only census does not open a plan PR).
- Zero-mutation proof: ls-remote before == ls-remote after (PR1855 head 43326cf57f1a3a8d73f2b9289e8c5ad00b74782a; develop ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee) — identical, no mutation.
- CLEANLINESS: `docker ps -a` — no containers started (read-only census, zero docker/podman launches); no compose projects; no orphaned networks/volumes; host untouched.

END_DONE w282-0428-078-1855census
