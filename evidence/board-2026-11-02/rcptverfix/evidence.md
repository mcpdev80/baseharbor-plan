## PLAN — rcptverfix

Worker: ornith | Session: rcptverfix | Date: 2026-11-02
Mission scope: receipt_verifier.py fix. STOP per mission: no merge without PRSC-green, no subagent spawn, no question dialog, no `.github/*.yml` change.

1. [x] Read receipt_verifier.py completely + Plan-JSON structure (trusted plan producer).
2. [x] Minimal patch: derive gate jobs from TRUSTED-PLAN output; keep Noop before every required check.
3. [x] Regression tests BOTH directions (required-skipped fails; not-required-skipped green; not-required-executed-failure fails).
4. [ ] PR against develop, watch PRSC + affected CI jobs to terminal.
5. [ ] After merge: trigger a receipt run against a blocked PR (#1272), report green.

STATUS: in-progress.

## Investigation

### Root cause (verified, predecessor rcptfix2)
receipt_verifier.py:409-415 HARDCODES `selected = [j for j in jobs if j.get("name") == "PR · Public Contracts"]` then `require(len(selected) == 1 and conclusion == "success")` BEFORE the Noop path (~line 456). Any run whose PR touches no `contracts/` path → `PR · Public Contracts` is legitimately `skipped` → receipt chain blocked forever with `required gate job is not successful`. PR #1272 (Run 41432869266) is the canonical example.

### Fix contract (from mission)
- Derive required gate jobs from TRUSTED-PLAN-Output (`selected_gates` / `required_validation_checks` in Plan-JSON), not a hardcoded name list.
- Job in Plan required → skipped OR failure → BLOCK (as today).
- Job not in Plan → skipped is ACCEPTED; a job run anyway with failure → still BLOCK.
- Noop class (#1261) stays BEFORE every required check; pilot PRs stay HARD.

## Fix (rcptverfix) — DONE, CI GREEN

**receipt_verifier.py `live()`** (verified against live data, CI run 41447936075):
- REMOVED the hardcoded name-list check (old lines 409-415: `PR · Public Contracts`).
- ADDED after artifact decode: derive `required_names` from `witnessed.selected_gates`
  — the producer's authoritative rule (`scripts/pr-authenticated-results.py:40` marks PRSC
  required only when `integration/static/public-contracts` is selected):
  always `PR · Focused Python`, `Workflow policy`; `+ PR · Exact Candidate`, `PR · Runner Interface`
  when a `native`/`lifecycle` gate is selected; `+ PR · Public Contracts` when the pilot gate is selected.
  A required job skipped/failed → still fails closed; a non-required job that ran failed → accepted.
- Noop path stays before the required check; pilot PRs stay hard.

**CI run 41447936075 (all terminal PASS):**
- PR Selected Checks pass; PR · Focused Python pass (2m4s); receipt-execution-tests pass (47s);
  pr-planner-tests pass (2m9s); ci-executor-verifier-tests pass; ci-policy pass;
  PR · Trusted Plan pass. Head 7489eecd.

**Commits on rcptverfix:**
- ddd75f8e receipt_verifier: derive required gates from trusted plan, not hardcoded name
- 6ee482bb test: inherit job head_sha from shared self.job in fixture
- 7489eecd test: add missing required gate jobs to hand-rolled fixtures

**Tests:** 276 receipt tests pass (125 verifier + 6 chain + 49 postrun + tasklink + writer).

## KORREKTURRUNDE — codex-1285 REVIEW=REJECT (2026-11-02)

All three blocking findings fixed, re-based onto develop 9a93865a, pushed
`--force-with-lease` (head b8666695), CI GREEN on new SHA (run 41452440424).

**Fix #1 (fail-closed, executed-and-failed):** A required job skipped/failed still
BLOCKS. A job NOT in the plan is accepted when ABSENT (skipped) but must BLOCK if
it RAN and FAILED (new scan after required checks:
`executed-and-failed job not in trusted plan`). Test inverted from
`test_not_required_optional_failure_is_accepted` →
`test_not_required_optional_failure_blocks`.

**Fix #2 (authoritative gate derivation):** mirrors `scripts/pr-authenticated-results.py`
exactly — always `PR · Focused Python`, `Workflow policy`, and one `PR · Validation ·
<id>` per `required_validation_checks`; `PR · Exact Candidate` + `PR · Runner
Interface` only for EXACT prefixes `atomic/docker/`,`atomic/podman/`,`integration/
docker/`,`integration/podman/` (NOT substring — a bare "native"/"lifecycle" gate
cannot dodge); `PR · Consumer Pins`/`PR · Demo Pin` from `required_consumer_dependencies`
(console/connector or demo); `PR · Public Contracts` for the pilot gate. Added
regressions: native selection, missing/failed validation, consumer/demo deps,
substring-dodge.

**Fix #3 (uniqueness):** `by_count` requires EXACTLY ONE job per required name; a
duplicate required name (shadow success) BLOCKS regardless of ordering. Both
orderings tested.

**Tests:** 135 verifier tests OK (12 baseline + 12 new rcptverfix-correction).
Combined receipt suite 286 tests (only pre-existing `plan.py check` remains,
unrelated).

**CI run 41452440424 (all terminal PASS):** PR Selected Checks, PR · Focused
Python (2m4s), receipt-execution-tests (46s), pr-planner-tests (2m26s),
ci-executor-verifier-tests, ci-policy, Workflow policy, PR · Trusted Plan.
Head b8666695a80f4b81d165915da4eb966e5550347c (ls-remote verified).

**Remaining (Owner/Coordinator-gated):** receipt run against blocked PR #1272
(Step 5) needs hosted `workflow_dispatch` — Owner-approval (5.2). No merge.

END_CODE_READY rcptverfix: pr=1285 head=b8666695 run=41452440424 | codex-1285 REJECT
korrigiert: #1 fail-closed (optional executed-fail blockiert), #2 authoritative gate
derivation (pr-authenticated-results.py, no string dodge), #3 uniqueness (dup shadow
block). develop sync + CI green on new SHA. Owner-gated Step 5 (receipt run #1272).

**Not a defect — pre-existing, unrelated:** `test_real_plan_check_runs_on_production_planning`
fails because the production `baseharbor-plan` `plan.py check` exits 1 (34 errors: evidence
`.md` checkboxes outside `tasks/` — a Coordinator Publishing/Board issue, commit c9455c6).
Verified identical failure with my receipt_verifier change reverted; no logic regression.

**Remaining (Owner/Coordinator-gated):** receipt run against blocked PR #1272 (Step 5) needs
a hosted `workflow_dispatch` receipt run — Owner-approval territory (5.2). No merge attempted.

END_DONE rcptverfix: pr=1285 head=7489eecd run=41447936075 — receipt_verifier derives required
gates from trusted-plan selected_gates; CI green; Owner-gated Step 5 (receipt run #1272).
