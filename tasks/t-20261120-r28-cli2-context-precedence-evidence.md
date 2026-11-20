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
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-178 · context show precedence
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1718]
sources: []
blocker: "NICHT der kandidat, sondern die CI-UMGEBUNG: CODEX-REVIEW hat head aa3c9d2a5b799756837e6238fe82c948778e7a15 APPROVED (akte codex-review-wave/1718-0428-178.md). CODEX-MERGE hopfte auf develop 40cb28c758b0 (= 'Merge pull request #1594 ... cli2-env-policy-head'), neuer head ce5aa9633630b88a017f501da7c2f0bd00e44714, branch == refs/pull/1718/head gemessen, und der run 44774783515 endet completed/failure an ALLEN VIER 'PR · Go unit · cli-0..3' shards mit 'main_test.go:60 create failed: Managed-environment machine operations require an authenticated BaseHarbor operator' und 'app_secrets_shared_runtime_test.go:44 operator OIDC configuration' - meldungen, die mit der einen PR-datei (cmd/baha/context_terminal_test.go, +24 zeilen test) nichts zu tun haben. derselbe fehler erscheint an ihren eigenen PRs: run 44770516960 (cli2-identity-secrets-head 1bc3362155) und run 44765885244 (cf7d1e6014) completed/failure. kein merge wurde versucht (CODEX-MERGE meldet END_BLOCKED mit akte 1718-0428-178-merge.md, main 358a65504546). NÄCHSTER TRIGGER: owner stellt die operator-/OIDC-umgebung der cli-shards her (oder korrigiert die tests, die sie verlangen) - dann rebase + recheck + merge am exakten head, ohne neue inhaltsrunde. zweiter weg: owner nimmt die verschärfung aus #1594 zurueck, dann ist der alte head wieder gruen."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-cli2-context-precedence-evidence · CLI2: persisted-over-default precedence is not asserted through baha context show #task #release/v0-4-28 #status/blocked #view/blocked #kind/bug
    <!-- generated:card -->
    **Owner:** w178-0428-178-contextshow  
    **PR:** [baseharbor#1718](https://github.com/mcpdev80/baseharbor/pull/1718)  
    **Blocker:** NICHT der kandidat, sondern die CI-UMGEBUNG: CODEX-REVIEW hat head aa3c9d2a5b799756837e6238fe82c948778e7a15 APPROVED (akte codex-review-wave/1718-0428-178.md). CODEX-MERGE hopfte auf develop 40cb28c758b0 (= 'Merge pull request \#1594 ... cl…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w178-0428-178-contextshow  
**Priority:** not set  
**PRs:** [baseharbor#1718](https://github.com/mcpdev80/baseharbor/pull/1718)  
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

ARBEITET JETZT, kante gegen session gemessen (name 'w178-0428-178-contextshow', laptop-kanal, worktree aus develop f5ce95afce1c): eine regression durch den ECHTEN 'baha context show'-pfad (default A, persistierte auswahl B, kein env-override) plus mutation IN BEIDEN RICHTUNGEN mit woertlicher ausgabe, ci-job 'executed' statt 'skipped'. disjunkt zu 0428-187 (wizard-/ci-greenfield-dateien), #1714, #1684.

HANDOFF ABGESCHLOSSEN, kandidat pruefbar: PR #1718 head aa3c9d2a5b79, branch = refs/pull/1714.. gemessen equal, draft=false, 1 datei (+24 zeilen, nur test), checks 14 success / 20 skipped / 0 failure am exakten head, run 44759243414 mit 'PR · Go unit · cli-2' completed/success und dem test in BEIDEN mutationen rot. akte evidence/.../context-show-precedence/round-1.md: 0 checkboxen, 23 mutations-belege, 'cleanliness: CLEAN'. basis-note: develop ist auf 3653369a4d83 weiter (#1717/0428-188), der hop gehoert vor den merge, nicht vor die abnahme - gleiches muster wie #1715, das der owner selbst in review genommen hat.

STATUS-KANTE NACH MESSEN, NICHT NACH GLAUBEN: inhalt ist fertig und die abnahme des inhalts ist erfolgt (APPROVE); was fehlt, ist ein gangbarer gate. ich lasse die karte NICHT auf review stehen, weil review 'abnahme offen' heisst - offen ist der gate, nicht die abnahme. das ist ihr feld (AGENTS 3.8 kann-jeder-schritt-check: auth/env kommen vom system/owner, keine lane darf ihren pruefeingang selbst setzen).
