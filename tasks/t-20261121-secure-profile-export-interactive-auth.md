---
id: t-20261121-secure-profile-export-interactive-auth
card_number: "0428-219"
card_short_title: "0428-219 secure-profile export auth"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: planned
kanban_lane: planned
kanban_summary: "TestSecureProfileExportCommandPathAssemblesProductionWiring passes in the hosted PR · Go unit · cli-0 shard, so the command tree…"
kanban_title: 0428-219 · 0428-219 secure-profile export auth
priority: normal
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md
created: "2026-11-21T06:50:00Z"
updated: "2026-11-21T06:50:00Z"
---

- [ ] t-20261121-secure-profile-export-interactive-auth · 0428-219 secure-profile export command path refuses with interactive setup in CI #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    **Evidence:** [proof 1](evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: CODEX-REVIEW `evidence/r28-welle4-2026-11-21/destroy-authority-stamp/review-1.md` (P2, logged failure lines).

## Goal

`TestSecureProfileExportCommandPathAssemblesProductionWiring` passes in the hosted `PR · Go unit · cli-0` shard, so the command
tree wiring it asserts is actually exercised on the runner instead of stopping at a usage error.

## Why

CODEX-REVIEW of PR #1738 counted exactly three first-level FAIL lines in run 44867319394 (903158 bytes of log) and states that
none of them carries the inherited gate text `Managed-environment machine operations require an authenticated BaseHarbor
operator`. One of the three is this test: `cmd/baha/secure_profile_export_command_test.go:125` reports
`baha app secure-profile export through the command tree failed: operator authentication needs interactive setup`, raised in
`cmd/baha/operator_auth_boundary.go:117` as a `usageError`. So the assertion never reaches the wiring it names. No card covers
this file: `grep -l secure_profile_export baseharbor-plan/tasks/*.md` returns only `t-20261114-r28-cli2-app-export.md`
(0428-065), whose PR #1625 is a draft on the Owner-held `cli2-identity-secrets-head` stack - a different scope and a different
base.

## Scope

Allowed write-set:

  - `cmd/baha/secure_profile_export_command_test.go`
  - the command-path test support needed to give that call a non-interactive operator context
    (`cmd/baha/app_init_wizard.go` helpers, `cmd/baha/runtime_integration_test_support_test.go`) - reported with file:line
    before the first edit

Forbidden:

  - `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**` (Owner rails)
  - `.github/**` and `scripts/**` workflow selection (Owner scope - report the need as a file:line finding)
  - any change to the refusal in `cmd/baha/operator_auth_boundary.go:117`: the interactive-setup message is product behaviour

## Acceptance criteria

  - Hosted run at the candidate head shows `TestSecureProfileExportCommandPathAssemblesProductionWiring` selected in
    `PR · Go unit · cli-0` and passing, with run-id and per-cell conclusion in the evidence file.
  - Red-first proof (§5.6): the same test fails on a named SHA before the change, with the failure line quoted.
  - The refusal path stays reachable for the interactive case: a second case asserts the usage error when no operator context
    exists, so the fix does not silence the refusal.
  - `git diff develop -- internal/operatorauth/ cmd/baha/operator_auth_boundary.go` is empty at the candidate head.

## Stop criteria

  - The only way to pass is to alter `operator_auth_boundary.go`: STOP and report - Owner rail.
  - The test is not selected by any shard at the candidate head: STOP and report the selection rule with file:line (CI intake
    duty, §5.3), do not add a local skip.
  - Hosted logs unavailable: report the three commands (`--log`, `--log-failed`, `--job <id> --log`) with byte counts.

## Handoff

Evidence: `evidence/r28-welle4-2026-11-21/secure-profile-export-interactive-auth/round-1.md`. Base: stacked on
`lane-0428-198-cli-shard-operator-env` (card 0428-204) per the stacking rule - content dependency, not merge dependency. Count
by distinct first-level `--- FAIL: Test` names, not gate lines (H-V26 law, plan `571364e4`).
