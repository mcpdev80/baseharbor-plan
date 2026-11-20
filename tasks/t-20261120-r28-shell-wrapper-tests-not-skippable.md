---
id: t-20261120-r28-shell-wrapper-tests-not-skippable
card_number: "0428-179"
card_short_title: "shell wrapper cells must run"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w179-0428-179-shells
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-179 · shell wrapper cells must run
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "ECHTER EXTERNER BLOCKER, OWNER-ENTSCHEID NÖTIG: der Kandidat 0eeda344 (base 3653369a4d83, 2 dateien: cmd/baha/context_terminal_test.go fail-loud + .github/workflows/ci.yml +18 zeilen 'Install interactive shells' in der ci-shard) lässt sich nicht pushen - das einzige verfügbare GitHub-Token hat scopes gist/read:org/repo, NICHT 'workflow', und GitHub's OAuth-App workflow-scope protection lehnt pushes ab, die .github/** ändern. Die lane hat korrekt NICHT erzwungen und NICHT umgangen (AGENTS 3.8 letzter absatz: tokens kommen vom system/owner, nie von der lane; 5.6). Arbeit ist nicht verloren: format-patch + akte landen in evidence/r28-welle4-2026-11-20/shell-wrapper-cells/ auf plan main. NÄCHSTER TRIGGER (einer davon): (a) owner vergibt ein workflow-scope token bzw. ergänzt 'workflow' an der OAuth-App, dann push + PR (base develop) + hosted run in derselben lane; (b) owner legt den patch selbst auf einen branch und nennt die PR-nummer; (c) owner entscheidet, dass die gate-route NICHT in diesem PR gehören darf (widerspricht dann ihrer anweisung 51d95b99 - bitte ausdruecklich)."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-shell-wrapper-tests-not-skippable · CI intake: zsh/fish wrapper tests skip silently when the shell is not installed #task #release/v0-4-28 #status/blocked #view/blocked #kind/bug
    <!-- generated:card -->
    **Owner:** w179-0428-179-shells  
    **Blocker:** ECHTER EXTERNER BLOCKER, OWNER-ENTSCHEID NÖTIG: der Kandidat 0eeda344 (base 3653369a4d83, 2 dateien: cmd/baha/context\_terminal\_test.go fail-loud + .github/workflows/ci.yml +18 zeilen 'Install interactive shells' in der ci-shard) lässt sich…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w179-0428-179-shells  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this card exists (finding -> card duty, AGENTS 3.3.5 / 5.3)

Same CODEX post-merge review (post-merge-068-166-develop-96f2ae11.md, B2): TestEndToEndInstalledZshAndFishWrappers
(cmd/baha/context_terminal_test.go:434-439 and :491-505) drives zsh/fish ONLY if the binary is present and continues
otherwise. On a runner without those shells the gate reports success without executing either path, which is not durable
evidence for the fish recursion guard (completion_setup.go:64-67, :78-80).

## Acceptance

1. The test must fail loudly (or be reported as skipped by the CI aggregate, not as passed) when the shell under test is
   absent, so the gap is visible.
2. Either install the shells in the cell that owns this path, or split a dedicated cell with a name that shows it runs.
   Where this needs a change in .github/workflows/ci.yml or its trigger rule, the card owner reports the needed change to
   the coordinator with file:line (Owner scope, AGENTS 5.3) instead of editing it.
3. Evidence: one hosted run id at the exact head showing the cells as executed (not skipped) or failing loudly.

## Boundaries

Test code plus the guard that detects a missing shell. No silent taint of unrelated cells, no gate deletion.


ARBEITET JETZT, kante gegen session gemessen (name w179-0428-179-shells, ornith-kanal, worktree aus develop 3653369a4d83): der stille erfolg der zsh/fish-pfade in cmd/baha/context_terminal_test.go:434-439 und :491-505 wird zu fail-loud oder sichtbarem skip, und die gate-route kommt in DENSELBEN PR (owner-anweisung 51d95b99). konfliktfrei geworden, weil 0428-178 soeben #1718 abgeliefert hat (nur test-datei, keine funktionsaenderung).

ARBEIT ruht am exakten kandidat 0eeda344; lokal belegt: test FAILT laut ohne shells und BESTEHT mit ihnen, gofmt/vet leer. ke kein PR, kein remote-branch (gemessen: ls-remote refs/heads/lane-0428-179* = leer).
