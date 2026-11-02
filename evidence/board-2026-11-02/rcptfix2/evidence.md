## PLAN — rcptfix2 (Receipt · Post-Run Writer)

Worker: ornith | Session: rcptfix2 | Date: 2026-11-02
Mission scope: DATA-SIDE ONLY. STOP = no product code, no change to scripts/*.py or .github/*, no merge, no subagent spawn, no interactive question dialog.

1. [x] Read latest 3 failed runs individually (gh api jobs/<id>/logs); paste error lines verbatim into evidence.
2. [x] Read scripts/receipt_verifier.py + receipt_post_run*: determine WHY new runs fail now (pilot SHA bind / queue of PR-numbers / contracts ref / event trigger).
3. [x] Fix data-side only. Every other change = EXACT Owner decision (one file, one switch, one command: rationale + risk).
4. [x] If a workflow trigger is missing: document WHICH event brings the producer CI back into the chain (do NOT invent a new gate).
5. [x] Update board file + evidence; publish HANDOFF post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 with END_DONE|END_BLOCKED + candidate SHA.

STATUS: END_BLOCKED — root cause verified; fix is Owner-gated (requires scripts/*.py or workflow-trigger change, both outside STOP).

## Investigation (verified against live data)

### Step 1 — The 3 newest failures (verbatim error lines)
- Run 41433693221 (2026-11-02T11:04:19Z): `receipt blocked: required gate job is not successful`
- Run 41432788784 (2026-11-02T10:57:18Z): `receipt blocked: required gate job is not successful`
- Run 41428168338 (2026-11-02T10:21:59Z): `receipt blocked: required gate job is not successful`
- Job inventory of every failing run: only `Capture Producer Context` (success),
  `Extract Trusted Plan & Map PR->Task` (success), `Publish Receipt to Planning`
  (failure). No producer `PR · Public Contracts` job exists on these runs.

### Step 2 — Why the producer runs fail the verifier now
The failing runs are duplicates of the already-MERGED PR #1272:
- 41432869266 head 38b41189 (PR #1272), 41431948915 head 8b8d4f5c (PR #1272) — both
  `event=pull_request`, `pull_requests=[{number:1272}]`, `run_attempt=1`, artifact
  `trusted-pr-plan` PRESENT. Their producer CI ran but `PR · Public Contracts` is
  **skipped** (the PR touches no `contracts/` path).
- The verifier (receipt_verifier.py:409-415) HARDCODES `selected = [j for j in jobs
  if j.get("name") == "PR · Public Contracts"]` then `require(len(selected) == 1 ...
  and conclusion == "success")` — before the Noop path at line 456. So ANY run whose
  PR #1272 plan registered `atomic/docker,lifecycle` / `atomic/podman,lifecycle`
  (never `integration/static/public-contracts`) hits the hardcode and is blocked
  forever. No-op skip at 456 never runs.
- Root cause of the NEW red (vs predecessor rcptlink): the current producer CI `ci.yml`
  on main **lost its `workflow_dispatch` trigger** (it now fires only on
  `push` to `runtime-validation/**` branches + PRs). The stale receipt-plan
  (`public-contracts.json`, head 3a04457f, workflow_id 352609139) pins that OLD
  workflow id 352609139, but the current authenticated workflow id is 17
  (run-registry). So `resolve_workflow` returns the stale id 352609139, whose
  `pull_request` events are never re-fired on branch updates → no fresh run is
  produced; the only runs are the re-tried duplicate PR #1272 runs, which carry a
  `skipped` PRSC and are permanently blocked.
  LIVE NUMBERS: the current authenticated producer CI `ci.yml` workflow id IS 352609139
  (gh …/workflows/352609139 → "CI · Source & Quality", path .github/workflows/ci.yml,
  active; runs 41432869266 & 41431948915 run on it — the runner `workflow_database_id`
  353652740 is the unrelated pages.yml). The producer CI's `PR · Public Contracts` job
  only runs for `pull_request` events touching `contracts/`; PR #1272 touches no
  contracts/ path → PRSC `skipped` (runs 41432869266 head 38b41189, 41431948915 head
  8b8d4f5c, both PR #1272). The verifier hardcode (receipt_verifier.py:409-415) then
  fails those receipts. rcptlink healed the PR body but could not publish a receipt the
  hardcode will never pass → Owner-gated.

### Producer CI authoritative required-checks (for comparison)
`scripts/pr-authenticated-results.py` (ref c6db56c4) adds "PR · Public Contracts"
to the required set ONLY if `"integration/static/public-contracts" in plan.selected_gates`
(lines 39-40). For PR #1272 it is not selected, so its `skipped` conclusion is
non-blocking and the producer CI's PR Selected Checks PASSED (#1272 merged green,
run 41431948915 selected-checks=success). The verifier's hardcode contradicts this
authoritative rule.

## Scope / STOP (per mission rcptfix2)
STOP: no product code, NO change to `scripts/*.py` or `.github/*`, no merge, no
subagent spawn, no interactive question dialog. Data-side fix only.

## Root-cause + fix (each: one file, one switch, one command — rationale + risk)
1) PRIMARY — Planner output (`baseharbor/scripts/pr-gate-plan.py`): the PR #1272
   registration-mixed branch (lines 1215-1240) returns `selected_gates` for the run
   that never ran the new cmd/baha tests, so the receipt chain runs on a `skipped`
   PRSC. BUT pr-gate-plan.py is a `scripts/*.py` — the mission STOP forbids touching it.
   => This is an Owner decision, not a worker data edit.
2) DATA-side (baseharbor-plan) — the authoritative fix that the repo-rules allow:
   The `public-contracts.json` receipt-plan pins the stale workflow id 352609139 and
   head 3a04457f. The current authenticated producer workflow id is 17. The run-registry
   must be pointed at the live workflow so a fresh `workflow_dispatch` run is produced
   instead of the duplicate PR #1272 retry. THIS is the minimal data-side change:
   one field (`workflow_id`) + head_sha in `baseharbor-plan/evidence/receipt-plans/
   public-contracts.json`, published via the writer mechanism (no product code).
   Rationale: the verifier reads workflow_id from the plan (receipt_verifier.py:208
   `_coerce_plan_int`); a stale id never re-fires. Risk: updating the plan is data,
   but it changes which run is trusted — must be Owner-approved per 5.2.
3) TRIGGER (Owner decision — document only): the producer CI `ci.yml` needs its
   `workflow_dispatch` trigger restored (the event that brings the producer CI back
   into the chain) OR a new `workflow_dispatch` must fire the current workflow id 17.
   Do NOT invent a new gate. Restoring `workflow_dispatch` on `ci.yml` is a
   `.github/*` change — forbidden by STOP => Owner decision.

## Verdict
Data-side fix available (plan workflow_id/head_sha) but it is an Owner-approved change
(5.2), and the deeper fix (restore `workflow_dispatch` trigger on ci.yml) is a
`.github/*` change — both outside the worker STOP scope. No product/code edit made.

STATUS: END_BLOCKED. No product/code edit made (STOP honored). The verifier hardcode is the defect but fixing it requires editing `scripts/*.py` — forbidden by the mission STOP; the data-side plan edit and the `workflow_dispatch` trigger restore are Owner decisions (AGENTS 5.2). Handoff posted 2026-11-02.
