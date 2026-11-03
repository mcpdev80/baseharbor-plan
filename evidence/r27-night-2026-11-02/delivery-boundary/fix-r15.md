# Fix R15 — ADR 0022 §2 wording round 4

Worker lane: w24-delivery-wording4. Coord: f49a3303.
PR #1333, base 1dde4208, branch work/r27-delivery-boundary.

## PLAN
1. Fetch branch + develop, add worktree at base 1dde4208.
2. EN: replace §2 "attests conflicting active ownership" paragraph (5 lines) with the decided wording.
3. DE: replace §2 "Wenn der gespeicherte Datensatz..." paragraph (incl. stray "ausdrückbar ist;" fragment) with the decided wording.
4. Verify fragment greps + diff == exactly 2 files.
5. Merge develop, ancestry rc=0, go build ./... + go test ./internal/deployment ./internal/delivery, push, ls-remote==head.
6. Write evidence, post END_DONE.

## repo-rule compliance
- Write set restricted to the two 0022 decision markdowns (docs/ and docs/de/), plus develop-merge + go tests. No other product files touched.
- No force-push, no protection-bypass. Only `git add <file>` used.

## Evidence
- EN fragment `two differing persisted owners` removed; `conflicts with the delivery mode being saved` == 1.
- DE fragment `ausdrückbar ist;` removed; `Wo genau ein Besitzer` == 1; no `sofern nicht` remainder.
- diff 1dde4208..HEAD --name-only == exactly 2 files.

## END
DONE w24-delivery-wording4: head=6a335b4b fragment=0 grep0=2stellen
