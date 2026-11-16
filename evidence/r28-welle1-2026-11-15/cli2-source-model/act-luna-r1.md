# CODEX-REVIEW — PR #1595

**ROLLE: REVIEW**
**Task:** t-20261114-r28-cli2-source-model
**Candidate:** 0963d08d022ccd671333512fec501bd9d2ab6ed2
**Base:** PR base lane-0428-uid-target at 3a91e2a8362bc8028c8f4a7ef278f8c9d96df823. The head adds a merge of develop 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95; the SHA-exact tree diff includes that develop-sync content plus the source-model slice. I separated the merge parent from the lane-authored source-model commit for the task review.
**Exact-head CI:** run 43794259476, pull_request, COMPLETED SUCCESS, exact SHA; Draft source/routing, CLI shards 0–3, and packages jobs succeeded. Remaining native/release checks were skipped under draft selection. git diff --check clean.

## Verdict: APPROVE CONTENT

The authored source-model slice supports optional unique components, multiple component mappings per source, local-directory sources, incremental source/component edits, and ownership-safe detach without deleting user files or checkouts. Validation rejects unsupported source types, duplicate IDs/components, invalid source fields, path escapes, and removal of the last source. Local path handling checks the specified directory and Git status inspects the declared source rather than neighboring directories. The exact-head hosted test jobs are green, covering the changed cmd/baha and internal/development packages.

## Recipe / dependency gate

- **File/change:** no content correction required by this review.
- **Checks:** exact-head pull_request CI passed for the changed packages; preserve the recorded test-to-CI mapping.
- **Stop:** the task depends on t-20261114-r28-cli2-uid-app, which remains unaccepted. This content verdict does not accept that dependency or authorize merge. Recheck the stack after uid-app is accepted and retarget/rebase as required by the lane contract.

Read-only review; no merge performed.
