# evidence/ p1242q — PR #1242 Observability Acceptance Test: Consent Guard plan→apply Flow

## PLAN (Plain-Bullets)

- Step 1: Worktree vom Branch work/fix-observ-consent rebase auf origin/develop-TIPP, push — DONE (head 2a561ff9)
- Step 2: PRSC beobachten — DONE (run 41340862268 completed/failure)
- Step 3: Nativer Nachweis: Ref runtime-validation/ci/observ-consent-1242 auf NEUEN head — DONE (Probe-Run-ID 41340862268 gruen/rot: FAILURE)
- Step 4: PR-Kommentar mit neuem head + Probe-Run-ID — BLOCKED (no auth token, no PR comment possible)
- Step 5: Karte via plan.py zeigen, Status auf review — BLOCKED (no auth token for plan.py)

## PRSC Probe-Run-ID: 41340862268

### Run Status
- **Status:** completed
- **Conclusion:** failure
- **URL:** https://github.com/mcpdev80/baseharbor/actions/runs/41340862268

### Check Suite Failure
The PRSC workflow run 41340862268 completed at "PR Selected Checks: failure" with the step "Enforce every required check (unqualified runtime remains blocked)".

### Job Detail
- Workflow policy: completed / success
- PR · Trusted Plan: completed / success
- Targeted HA · docker: completed / skipped
- Targeted HA · podman: completed / skipped
- validate: completed / skipped
- Release Source Preflight: completed / skipped
- PR · Focused Python: completed / success
- PR · Validation · cli-guided-tests: completed / success
- PR · Validation · source-contracts: completed / success
- PR · Validation · cli-build: completed / success
- PR · Validation · cli-vet: completed / success
- PR · Exact Candidate: completed / skipped
- Runner Interface: completed / skipped
- Consumer Pins: completed / skipped
- PR · Public Contracts: completed / skipped
- PR · Demo Pin: completed / skipped
- PR · Selected Runtime: completed / skipped
- **PR Selected Checks: completed / failure** ← failure point

## Evidence Summary

### Head SHA: 2a561ff9
Commit message: "fix(observability-acceptance): follow plan→apply flow to satisfy consent guard"

### Test File Changes
cmd/baha/app_observability_acceptance_test.go:
- Added plan→apply consent flow (resolveApplication → buildResolvedApplicationPlan → two-stage consent → withProviderChangeConsent(ctx, consent) → app apply)
- Renamed `resolved` to `statusResolved` to avoid variable shadowing in status/read phase
- No product code changes (TEST-FEHLER, decision A)

### Runtime Validation Result
The PRSC run 41340862268 concluded FAILURE at "PR Selected Checks". The enforcement step "Enforce every required check (unqualified runtime remains blocked)" failed — meaning the runtime validation checks did not pass. This blocks the merge.

## ACCEPTANCE VERDICT

### Status: BLOCKED
- PRSC run 41340862268: failure
- The runtime validation at "PR Selected Checks" blocks the merge
- No auth token available for PR comment or plan.py status update
- The acceptance test follows the correct plan→apply consent flow

### Candidate SHA
2a561ff974b3e60c37b558df04810adac96d1085

### END Lane
END_BLOCKED p1242q: head=2a561ff9 probe-run=41340862268 | PRSC run 41340862268 completed/failure at runtime enforcement check (unqualified runtime blocked), no auth for PR-comment/plan.py
