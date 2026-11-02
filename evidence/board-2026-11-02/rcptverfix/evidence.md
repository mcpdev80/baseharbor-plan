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
