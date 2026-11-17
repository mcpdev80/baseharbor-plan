END_CHANGES_REQUESTED — 0428-100 / PR #1676 — role CODEX-REVIEW

Exact candidate `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c`, base `develop@8db0d9bdf8d9ae77db94c9ddce9c209001c4da54` included in merge parent. Own exact-head `pull_request` run 44018836577 completed SUCCESS; PR Selected Checks SUCCESS. PR remained OPEN, mergeable, CLEAN at review time.

Blocking R3 point (4): the source uses `runtime://<project>/workload` with `VerificationNone`; provider file_sd/network generation excludes it and the verifier skips it. `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy` explicitly asserts that no scrape target is generated. This proves a logical snapshot entry, not a scrapeable metrics target or an `up=1` verification. The current user acceptance says the target must be scrapeable without weakening verification. Verdict CHANGES REQUESTED; no GitHub APPROVE attempt and no merge.

Review akte: `evidence/r28-welle3-2026-11-16/workload-only-registration/review-1.md`. Recipe: resolve the runtime identity to a real workload endpoint under an existing product contract and prove positive scrape verification; if no endpoint/port contract exists, stop and obtain explicit owner approval to revise the card to non-scraped logical registration. New exact head/run and fresh review are required after any correction.
