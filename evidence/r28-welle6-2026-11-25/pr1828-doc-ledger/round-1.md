# PR #1828 evidence ledger (docs-only AGENTS.md test-routing correction)

## PLAN
- record merge state and exact-head witnesses
- attempt second distinct exact-head witness
- document applicability verdict for the two-run-ID rule

## Findings
- PR #1828 baseharbor: state MERGED, merged by mcpdev80 at 2026-11-24 17:41Z, merge commit 08274e67dfd61d65834a5c4bdb4bf6640fa11576, PR head 6769600e40dfbd3651669444cd0b5fc8b9805db9, single file AGENTS.md (docs-only).
- Qualifying Hosted run on EXACT PR head 6769600e: 45450752785 (CI · Source & Quality) SUCCESS. 45450737046 was CANCELLED and is NOT a witness.
- Second distinct exact-head witness attempted: gh run rerun 45450752785 -> refused ("cannot be rerun; its workflow file may be broken" = closed-PR rerun block). A PR-event run cannot be produced again for a merged PR head; therefore the two-run-ID rule is NOT APPLICABLE to this exact head.
- Content witnesses instead (post-merge, develop): 45451382356 Runtime · Docker Core SUCCESS and 45451382283 Runtime · Podman Core SUCCESS, both at merge commit 08274e67 which contains the exact PR-head content.
- Honest summary: one green exact-head PR run + two green post-merge develop runs on the merge commit; no claim of two green PR-head runs.
