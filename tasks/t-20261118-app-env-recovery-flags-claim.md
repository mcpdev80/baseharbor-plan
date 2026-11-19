---
id: t-20261118-app-env-recovery-flags-claim
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w01-0428-117 (codeman 27c5ae85)
kanban_status: review
card_number: 0428-117
card_short_title: align app env recovery-flag
kanban_title: 0428-117 · align app env recovery-flag
prs: [mcpdev80/baseharbor#1687]
wait_reason: ""
blocker: ""

---
# t-20261118-app-env-recovery-flags-claim · app-env recovery-flag claim vs actual command contract

- [ ] t-20261118-app-env-recovery-flags-claim · align app env recovery-flag docs with the real command contract #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w01-0428-117 (codeman 27c5ae85)  
    **PR:** [baseharbor#1687](https://github.com/mcpdev80/baseharbor/pull/1687)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w01-0428-117 (codeman 27c5ae85)  
**Priority:** not set  
**PRs:** [baseharbor#1687](https://github.com/mcpdev80/baseharbor/pull/1687)  
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

docs-only, exact-head CI SUCCESS auf 7aa8b01e9, DE-mirror mitgezogen

CODEX-REVIEW comment #6994874926 im thread (formale change-request durch self-author-block nicht moeglich — Konvention): REQUEST CHANGES — 'NAME vor --uuid' falsch (uuid-strip vorher; regression status nur --uuid+ID). r2 ueber neue lane, PR bleibt 7aa8b01e9, kein merge

r2b END akzeptiert: head da7a2ace9 (force-with-lease linear rebase auf 9a37b4bc, lane-exklusiver branch — akzeptierte variante statt mission-kraft; history-pruefung ergab keine fremd-commits), exact-run 44427162228 SUCCESS, akte r2.md mit r2b-revision-label + superseded-vermerk fuer 7aa8b01e9 am band. Doku je subcommand nach wirklichkeit (uuid NAME-frei bei show/status/destroy, plan verweigert --uuid remote, env ablehnt beide) — genau das geforderte realitaetsprofil. Routing an CODEX-REVIEW
