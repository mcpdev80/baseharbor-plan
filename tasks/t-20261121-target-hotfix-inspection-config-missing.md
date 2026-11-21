---
id: t-20261121-target-hotfix-inspection-config-missing
card_number: "0428-220"
card_short_title: "0428-220 hotfix inspect"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: 0428-220-hottarget
kanban_status: active
kanban_lane: active
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
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/target-hotfix-inspection/round-1.md"]
  - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md
created: "2026-11-21T06:52:00Z"
updated: "2026-11-21T06:52:00Z"
superseded_by: t-20261120-cli-operator-entrypoints

---

- [ ] t-20261121-target-hotfix-inspection-config-missing · 0428-220 target hotfix inspection reports the target as unconfigured in CI #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-220-hottarget · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/target-hotfix-inspection/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-all-targets-config-loss](t-20261121-all-targets-config-loss.md)  
**Owner:** 0428-220-hottarget  
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

diagnose-lane (a1df027f, akte round-1.md plan cba364a2) und VON MIR NACHGEPRUEFT: der gemeldete fall ist an der AKTUELLEN basis nicht mehr rot; die korrektur 46017060d ('test(0428-198): register target before selecting', owner, 21.11 05:43) ist im head von PR #1726 enthalten - mein nachweis: merge-base --is-ancestor 46017060d #1726-head = 0, gemessen. KEINE gemeinsame ursache mit 0428-210: deren fix (#1739, 79d962a063be) toleriert deployment.ErrConfigMissing im arm '--all-targets' von cmd/baha/app_commands.go, der hotfix-pfad war eine andere stelle. Karte superseded durch 0428-204/#1726; kein eigener PR, keine duplicate.

Diagnosis: reported failure not reproducible on current base. Commit 46017060d 'register target before selecting it' (present in PR#1726 head e45430f2f1b7) fixes the test ordering; the error was a ResolveTarget miss, not deployment.ErrConfigMissing. No product change or second PR needed. Card closed as already-resolved in base.

zurueckgezogen: mein supersede-zeuge '46017060d' ist NICHT in develop. PR #1726 ist CLOSED ohne merge (closedAt 2026-11-21T09:09:20Z, mergedAt null, mergeable CONFLICTING); 'merge-base --is-ancestor' liefert fuer alle acht geprobten commits der basis-lane NEIN. inhaltlicher beleg: develop traegt 0 Vorkommen von 'withoutOperatorAuthTestContext' in cmd/baha/app_init_wizard.go, die basis-lane traegt zwei. Die hotfix-aenderung lebt also weiter.owner-entscheidung: basis-inhalt neu landen oder karte erneut schneiden

superseded_by 0428-204 ist UNWIRKSAM: PR #1726 ist geschlossen ohne merge (refs/pull/1726/head = e45430f2f1b = lane-0428-198-cli-shard-operator-env), und 'git merge-base --is-ancestor 46017060d develop' = NEIN. Der fix existiert nur auf dem 198-branch. Portierung auf develop ist jetzt die arbeit der lane. Der verlust selbst ist ein fund fuer karte 0428-221.
