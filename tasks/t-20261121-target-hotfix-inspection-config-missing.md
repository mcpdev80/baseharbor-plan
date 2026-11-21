---
id: t-20261121-target-hotfix-inspection-config-missing
card_number: "0428-220"
card_short_title: "0428-220 hotfix inspect"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: planned
kanban_lane: planned
kanban_summary: "collectTargetInspection after the hotfix command path returns the configured target instead of failing with target \"edge-a\" is…"
kanban_title: 0428-220 · 0428-220 hotfix inspect
priority: normal
depends_on: [t-20261121-all-targets-config-loss]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md
created: "2026-11-21T06:52:00Z"
updated: "2026-11-21T06:52:00Z"
---

- [ ] t-20261121-target-hotfix-inspection-config-missing · 0428-220 target hotfix inspection reports the target as unconfigured in CI #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261121-all-targets-config-loss](t-20261121-all-targets-config-loss.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-all-targets-config-loss](t-20261121-all-targets-config-loss.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: CODEX-REVIEW `evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md` (P2, logged failure lines).

## Goal

`collectTargetInspection` after the hotfix command path returns the configured target instead of failing with
`target "edge-a" is not configured`, so `cmd/baha/target_hotfix_test.go` passes in the hosted `PR · Go unit · cli-3` shard.

## Why

The review counted exactly three first-level FAIL lines in run 44867319394 and states the inherited gate text is absent for all
three, so none is an "inherited class" case. The third line is `target_hotfix_test.go:201`. Measured context: the test builds a
target through the command tree (`edge-a`, `--runtime-provider docker`, `--access node-a`, `--access-provider
baseharbor-node-connector`, `--reference node-a`), then calls `collectTargetInspection(context.Background())` at
`cmd/baha/target_hotfix_test.go:203-205`, which is the same inspection path that 0428-210 (#1739) changed for `--all-targets`
in `cmd/baha/app_commands.go`. 0428-210's fix tolerates the config-missing error inside the command path only; this caller still
sees the raw error.

## Scope

Allowed write-set:

  - `cmd/baha/app_commands.go` (the inspection helper shared with 0428-210 - coordinate, do not fork the tolerance)
  - `cmd/baha/target_hotfix_test.go` (assertions unchanged: guard setup, not expectation)

Forbidden:

  - `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**` (Owner rails)
  - `.github/**` and `scripts/**` workflow selection (Owner scope - report file:line instead)
  - weakening the "not configured" error for genuinely unknown targets: that message is the product's fail-closed behaviour

## Acceptance criteria

  - One diagnostic step first: state in the evidence file whether this and 0428-210 (#1739) share one root cause
    (`deployment.ErrConfigMissing` on the inspection read path). If yes, recommend ONE PR (extend 0428-210's change to this
    caller, this card closes as `superseded_by 0428-210`); if no, deliver the fix here.
  - Red-first proof on a named SHA (§5.6), with the failure line quoted.
  - Hosted run at the candidate head shows `TestTargetHotfix…` in `PR · Go unit · cli-3` passing, run-id + per-cell conclusion.
  - A negative case keeps failing: a target that was never configured must still produce "is not configured".

## Stop criteria

  - The fix requires changing what `collectTargetInspection` reports for unknown targets: STOP and report (fail-closed rule).
  - 0428-210 is already merged when this lane starts: re-check against develop first, the failure may be gone.
  - Hosted logs unavailable: report the three commands with byte counts, do not substitute a local run.

## Handoff

Evidence: `evidence/r28-welle4-2026-11-21/target-hotfix-inspection/round-1.md`. Base: develop if this card fixes it, or
`lane-0428-198-cli-shard-operator-env` if it stacks behind 0428-204 - the lane states its choice with a `merge-base` witness.
Counting law from H-V26: distinct first-level `--- FAIL: Test` names (plan `571364e4`).
