# Independent read-only review — PR #1693 / 0428-123

Reviewed 2026-11-19.

- Head `97987af6954aca0318a16aef99b19c27dbee231a`; base `7ee6f817dbff5a238bbc651315d6d76b3819fc91`; current develop `558dc42d0c8c9d798fcdf5938be2ea14e432b754`.
- Exact-head run `44578337221` passed PR Selected Checks, all six Go unit shards, build/vet, focused Python, source format, workflow policy and Trusted Plan; runtime/native jobs skipped. This run is stale relative to current develop.
- No edits/comments/merge by this review.

## Finding

**`Verification=none` can leave an old scrape target behind.** In `internal/metrics/prometheus_files.go:113-117`, `appKeep` includes every app source regardless of Verification, while the write loop skips `Verification==none` at lines 139-141. If an existing source with the same ID/name changes from verified to none, the previous `application--...json` is still treated as current and continues to be scraped. Build `appKeep` only from currently exportable sources. Add a regression that first writes a verified target, then syncs the same ID as `VerificationNone`, and asserts the old file is deleted.

The two target filename globs overlap in rendering (`prometheus_files.go:198-199`), but whether Prometheus de-duplicates matching paths was not established; treat it as a coverage question rather than a confirmed duplicate-scrape defect. The stale-file finding is related to the blocked 0428-143 `Verification=none` contract card; do not take that blocked card without the required contract decision.
