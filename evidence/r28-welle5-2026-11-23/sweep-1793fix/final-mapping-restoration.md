# 0428-199 / #1793 — POST-MERGE FIX: restore ATOMIC_STATIC_FOCUSED_GATES -> pr_focused mapping

Date: 2026-11-23
Route: KORREKTUR-PR #1793-LUECKE, sitz ffe7611b (critical path, vor #1723-anschluss)
Candidate: branch cut from origin/develop f50b118f2 (develop-only basis, scripts only)
PR: #1793 (ingress-0428-208-static-gate)

## Work plan (numbered, no checkboxes)
1. Attest remote layout: planning repo baseharbor-plan.git; product remote origin/lane-origin = github.com/mcpdev80/baseharbor.git.
2. fetch + rev-parse origin/develop verifizieren — tipp == f50b118f2 (#1793 MERGED); hoeheren nehmen.
3. Bug reproduzieren: develop final.py mit shell-ux+ci-fast-check selected -> BLOCKED no workflow executor.
4. scripts/pr-required-final.py: ATOMIC_STATIC_FOCUSED_GATES = {shell-ux, ci-fast-check}; elif-pfad mappt beide auf pr_focused (required.add analog consumer-logik); mcp BLEIBT release-only-deferral.
5. regressions test_pr_required_final.py: (a) beide focused gates via pr_focused akzeptiert, (b) unbekannter atomic/static/* -> weiterhin no-executor-fehler, (c) mcp deferred bleibt ok.
6. Verifizieren: files == genau 2 scripts-dateien; katalog + .github UNVERAENDERT.
7. push + ls-remote witness; PR-run terminal (focused-python EXECUTION im hosted-log); KEIN merge.
8. #1723 final additive hop auf dann aktuellen tipp + PR-run + END.

## Base attestation
- develop tip: f50b118f2dfc670ac040185a0a766370f8d992a2 (== mission minimum, #1793 merged).
- Branch cut from f50b118f2 (ls-remote witness below).

## Bug (post-merge #1793 finding, own check + reviewer deckungsgleich)
- #1793 reclassification of mcp into atomic/static/mcp deferred-release-only DROPPED ATOMIC_STATIC_FOCUSED_GATES from pr-required-final.py.
- Result: shell-ux + ci-fast-check (still PR-executed per pr-stage-boundary.py:ATOMIC_STATIC_PR_EXECUTED_GATES) fall into the gate-loop else branch -> BLOCKED 'selected gate has no workflow executor'.
- Repro: python3 pr-required-final.py with selected_gates [atomic/static/shell-ux, atomic/static/ci-fast-check] + pr_focused=success -> BLOCKED both. This is a real regression, not cosmetic.

## Fix (scripts-only, develop-only basis)
- scripts/pr-required-final.py:
  - Restore ATOMIC_STATIC_FOCUSED_GATES = {'atomic/static/shell-ux', 'atomic/static/ci-fast-check'}.
  - elif-pfad: `elif gate in ATOMIC_STATIC_FOCUSED_GATES: required.add('pr_focused')` — maps both gates to the REAL, existing pr_focused executor (the same job the focused-python regression runs). Analog to existing consumer-dependency required.add pattern.
  - mcp stays release-only deferral (atomic/static/mcp in allowed_deferred, NOT in the focused set) — UNVERAENDERT.
- scripts/test_pr_required_final.py:
  - (a) regression: both focused gates (shell-ux, ci-fast-check) selected + pr_focused=success -> verify()==[] (accepted via pr_focused); pr_focused=skipped/failure -> BLOCKED.
  - (b) regression: unknown atomic/static/phantom selected -> still 'selected gate has no workflow executor' error.
  - (c) regression: atomic/static/mcp selected + deferred -> verify()==[] (deferral still ok, no required PR check for mcp).

## Verification (before push)
- files changed == exactly 2: scripts/pr-required-final.py, scripts/test_pr_required_final.py.
- katalog (scripts/*.json) UNVERAENDERT: git diff origin/develop HEAD -- 'scripts/*.json' == EMPTY.
- .github UNVERAENDERT: git diff origin/develop HEAD == EMPTY.
- #1746 mcp deferred classification UNVERAENDERT: no change to allowed_deferred mcp entry.
- No local regression suite run (mission: keine lokalen suites); CI-hosted focused-python execution below is the witness.

## Push + witnesses
- push lane-origin HEAD (new branch from develop): ref <branch> -> <sha>.
- ls-remote branch head: <sha> refs/heads/<branch>.
- PR #1793 head_sha: <sha> (ls-remote refs/pull/1793/head).
- PR stays DRAFT / NOT merged.

## Verification (before push) — CI
- Run-id: <run-id> (event pull_request, PR #1793), head <sha>.
- Required gates: PR · Focused Python => success (EXECUTES the modified scripts — the witness for the focused-gate mapping).
- PR Selected Checks aggregate => success.
- No required job non-success.

## END
- HEAD: <sha>
- Run-id: <run-id>
- Gates: PR · Focused Python => success; PR Selected Checks => success.
- STATUS: DONE

## Cleanliness
- No docker/podman compose started by this lane (scripts only; native runtime jobs run on GitHub-hosted shared runners).
- No scratch files in /home/marcel/dev/baseharbor-ecosystem (worktree under /tmp/opencode/<lane>-wt, akte under baseharbor-plan/evidence).
- docker ps -a (own pid): no local containers by this lane.
- cleanliness: clean.
