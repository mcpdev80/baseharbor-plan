# Fix akte: card t-20261118-ownership-stale-consent-hardening (0428-119), PR #1690

**Lane:** lane-0428-119-consent-hard
**Owner takeover on fresh seat:** session 80aa0bf4 (w119-0428-119-consenthop), replacing vanished session 'w99-0428-119 r3' (codeman f5dabf03)
**Date:** 2026-11-19

## PLAN

- Step 1 — Remote reality check (re-measured witnesses per §4.1)
- Step 2 — Old-claim check, then publish claim from my own /var/tmp clone
- Step 3 — Monotone merge-hopf onto develop (no rebase/reset/force) with witnesses
- Step 4 — Base-distance diff (deeeb6477 vs origin/develop)
- Step 5 — Focused local checks (go build / vet / consent + oscillation + auth suites / ci-fast-check)
- Step 6 — Push (draft=false) and one exact-head run to terminal
- Step 7 — Contract points with test-id -> packet -> gate -> run-url
- Step 8 — Card state update (blocked on owner wire 114(a) if runtime stays open)

## repo-rule compliance

- No .github/** or scripts/** edits.
- No merges performed by me.
- No subagents.
- Evidence lives only in baseharbor-plan, never in the product repo.
- Exactly one candidate branch (lane-0428-119-consent-hard).
