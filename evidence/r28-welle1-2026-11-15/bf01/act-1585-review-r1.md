# PR #1585 Review R1 — BF-01 state-dir honoring

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1585 head/base refs, ancestry and single-candidate log, metadata, prior PR #1584 closure, and exact-head run 43684179345.
2. Compare the access/init test diff with `develop` to ensure green results come from correct state-dir honoring, not weakened expectations.
3. Verify positive two-state-dir isolation, no temp-write regression per BF-03, and no duplicate registration.
4. Write verdict and actionable recipe with exact witnesses and cherry-pick SHA if approved, validate and publish evidence on `origin/main`, then post END.
