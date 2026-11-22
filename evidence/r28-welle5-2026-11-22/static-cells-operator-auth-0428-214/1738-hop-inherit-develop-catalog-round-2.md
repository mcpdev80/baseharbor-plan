# 0428-214: re-hop #1738 onto develop 78f75c907 WITH correct catalog handling (inherit develop 1:1) + exact hosted

- karte 0428-214, sitz f0f6c8b4. #1738 additive hop onto develop 78f75c907 WITH CORRECT catalog handling. git-only, NO content-edit.
- #1738 does NOT change scripts/pr-gate-coverage.json itself (own catalog diff = 0). A hop on develop inherits develop's catalog (develop = superset base) -> CORRECT and WANTED, not a regression or Owner decision.
- Previous STOP (round-1) was a FALSE-POSITIVE: the 6 imported rows (mcp.go/target.go/opauth tests) are develop's own.
- NO subagent, NO content-edit, NO .github/catalog/product touch (NO #1738 catalog edit), NO merge.

## PLAN

1. Reality: git remote guard. develop HEAD 78f75c907 (ls-remote). #1738 head 1a1e5db4.
2. Additive: git merge --no-ff origin/develop 78f75c907 (NO force/rebase/amend). Diff = only #1738 1-file content. KEY CHECK: after merge, git diff origin/develop HEAD -- scripts/pr-gate-coverage.json MUST BE EMPTY (develop catalog inherited 1:1). STOP only if: (a) that diff NOT empty (#1738 changes develop catalog), OR (b) .github/** touched, OR (c) Trusted Plan fails on un-catalogued #1738 product-source.
3. Push NEW head + ls-remote pull/1738/head witness. PR open/ready. NO merge.
4. EXACT hosted: native + selected data-caps + Trusted Plan + Go/static GREEN expected. Report head + run-id + catalog-diff-empty + gates.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop, fresh): 78f75c90780c12f44062c562470285413f16a047
- PR #1738 head (git ls-remote origin refs/pull/1738/head): 1a1e5db480637dee8ccfd6f106dd043f684c210f
- PR #1738 branch: lane-0428-214-destroystamp
- #1738 content: 1 file (cmd/baha/core_installation_runtime_test.go), own catalog diff = 0

## Catalog-handling rule (authoritative, per mission round-2)

- STOP criterion is NOT the branch-vs-develop delta (that is inherited develop catalog, always non-empty in the merge).
- STOP criterion is: `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` == EMPTY.
  - EMPTY means #1738 changed nothing in the catalog and develop's catalog is inherited 1:1 -> OK, continue.
  - NON-empty means #1738 would be changing/regressing develop's catalog -> STOP + file:line.
- Also STOP if: .github/** touched, OR Trusted Plan fails on an un-catalogued #1738 product-source (fail-loud guardian -> surface line missing -> STOP + file:line).

## END

END_DONE|END_BLOCKED w27-pr1627-0428-061-pull: 0428-214 re-hop #1738. new head, run-id, 'katalog diff vs develop == leer', gates, 'cleanliness:'
