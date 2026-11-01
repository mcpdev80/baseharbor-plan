# PLAN — Review-B (read-only review of #1242 and #1243)

ROLE: REVIEW (read-only). No product code changes. No merge.

## Steps
1. [ ] Open #1242: get gen-accurate diff (gh diff/files). Assess whether the *_test.go change correctly encodes the §2.7 consent rule and is NOT a circumvention (no `---`-on-force over an real deletion).
2. [ ] Open #1243: get gen-accurate diff (gh diff/files). Assess whether the native broker+s3 gates are real (no permanent SKIP covering coverage) on GitHub-hosted runners.
3. [ ] Repo-rule check for both PRs.
4. [ ] Write REVIEW.md: per PR verdict {APPROVE-WARTEND-GREEN | CHANGES:…} + ROLE:REVIEW + session/model/time + witnesses (commit SHAs, GH run IDs, diff hunks).
5. [ ] Post handoff: `codeman agent post 8c0f41e1-21b3-4d3e-9537-ec733a3c2d60 "END_DONE review-B: #1242=<v> #1243=<v>"`.

## repo-rule compliance
- Read-only review lane. No product edits. No merge.

## END
END_DONE review-B: #1242=<v> #1243=<v>
