---
id: t-20261120-r28-cli2-context-precedence-evidence
card_number: "0428-178"
card_short_title: "context show precedence"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w178-0428-178-contextshow
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-178 · context show precedence
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-cli2-context-precedence-evidence · CLI2: persisted-over-default precedence is not asserted through baha context show #task #release/v0-4-28 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** w178-0428-178-contextshow  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w178-0428-178-contextshow  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this card exists (finding -> card duty, AGENTS 3.3.5)

CODEX post-merge review of develop 96f2ae11a25a (evidence/r28-welle4-2026-11-20/codex-review-wave/post-merge-068-166-develop-96f2ae11.md)
returned BEFUND MIT REZEPT for card 0428-068: production precedence is implemented (cmd/baha/context_terminal.go:187-190
override, :195-205 shell env, :206-210 persisted selection, then configured default), but no test proves persisted-wins-over-default
through the CLI path. Existing tests miss it: TestContextPrecedenceDefaultFallback calls the internal effectiveContextOrigin
directly (cmd/baha/context_terminal_test.go:122-135) and TestContextShowReportsWinningStage only exercises the
configured-default stage (context_terminal_test.go:156-163).

## Acceptance

1. One regression in cmd/baha/context_terminal_test.go: configured default A, persisted selection B, invoke the actual
   baha context show path and assert the printed target is B (not A, not the helper result).
2. Mutation proof both directions: reverting the persisted stage (:206-210) must turn THIS test red; the failure output is
   archived verbatim.
3. The test is picked up by an existing GitHub CI job (name it in the evidence); a locally-only test is not durable evidence
   (AGENTS 5.3).

## Boundaries

Tests plus, if unavoidable, the precedence function in cmd/baha/context_terminal.go. No .github/** (report a needed
workflow change to the coordinator instead). One PR for this card.


ARBEITET JETZT: session , worktree aus develop f5ce95afce1c. auftrag: EINE regression, die die echte 'baha context show'-kette durchfaehrt (default A, persistierte auswahl B, kein env) und MUTATION IN BEIDEN RICHTUNGEN beweist; ci-jobname in der akte; Write-Set disjunkt zu 0428-187 (app_edit_apply_result.go / ci-greenfield-apply.py), 0428-184 (#1715), 0428-183 (#1714), 0428-083 (#1684).

NICHT GESTARTET (korrektur meiner eigenen statuskante von vor zwei minuten): ich hatte die karte auf active gesetzt, obwohl der spawn mit 'ADMISSION-HOLD [POOL-FULL ornith 2/2]' ABGELEHNT war und es keine session gibt. bewiesen: 'codeman agent list' fuehrt keien w178-lane, pool 5/5 mit offenen sitzen = []. mission liegt bereit (/var/tmp/mission-178.md, gate exit 0) und wird auf dem ersten freien sitz dispatcht - naechster Kandidat ist der sitz von 0428-184 (session e5840c51), sobald deren END gemessen ist. inhalt der karte bleibt: eine regression durch den ECHTEN 'baha context show'-pfad (default A, persistierte auswahl B, kein env) plus mutation in beide richtungen.
