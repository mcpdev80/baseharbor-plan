---
id: t-20261118-app-env-recovery-flags-claim
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w1-lane-494cd839 (0428-117)
kanban_status: active
card_number: 0428-117
card_short_title: align app env recovery-flag
kanban_title: 0428-117 · align app env recovery-flag
---
# t-20261118-app-env-recovery-flags-claim · app-env recovery-flag claim vs actual command contract

- [ ] t-20261118-app-env-recovery-flags-claim · align app env recovery-flag docs with the real command contract #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w1-lane-494cd839 (0428-117)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w1-lane-494cd839 (0428-117)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal
Hunt 915 B1 (mittel, CLI-vertrag): the generic recovery text promises `--uuid`/`-e/--environment` for EVERY `baha app <command>`, but `baha app env` rejects these flags itself (cmd/baha/app_env.go:21 defines only NAME/format/reveal). Align the documentation claim with the actual per-command contract: state explicitly which `baha app` subcommands accept the recovery selectors and note that `app env` is selected BY NAME, not by uuid/environment. Keep the observed read-command Port nuance documented truthfully.

## Scope
- docs only (the recovery-flag passage + app env command reference lines). NO behavior change; wiring flags into `app env` is out of scope (would need its own contract decision).

## Required checks
- docs build/link check; machine-docs consistency job if it exists in the affected group.

## Dependencies and file ownership
- Source: hunt 915 Befund B1, evidence/r28-welle4-2026-11-18/hunt-cli2merged/befund-1.md (origin/main 49323cde).
