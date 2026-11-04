# Review 1354h — journal B1 completion

- Role: CODEX-REVIEW; no merge.
- PR: [#1354](https://github.com/mcpdev80/baseharbor/pull/1354), task `t-20261022-r27-ci-authority`.
- Exact reviewed head: `5a5f1b38f5151ef5d0beabfd0f5343f1b58f72e9`; base `develop` = `f8ef4255592fcb1502fa54187c0965b9d00f118c`, confirmed ancestor.
- PR: OPEN, READY, mergeable. `ls-remote` matched PR head and develop both before and after review; `git diff --check` clean.
- Gate run `41820069131`: completed/success on exact head. PR Selected Checks passed; 18 reported applicable jobs passed, 0 failed, with only conditional/inapplicable jobs skipped.
- Owner B1 decision verified in the CI-authority task and w99 handoff: Option 1, fixed 16 MiB budget, older large test entries made terminal.

## Six counter-probes from review-1354g

1. **Active ID retention / B1 — PASS.** `TestRound7ActiveIDSurvivesManyBigEntriesReopen` passes with older large entries transitioned to terminal and the newest active entry retained after reopening. Independent reviewer-only mutation kept all eight ~2.4 MB entries running: `start` rejected at entry index 3 with `total-cap set cannot retain active execution ids within segment slots`. The failed transition remained `pending` both in memory and after reopening; the failed start was not partially persisted.
2. **Torn final record — PASS.** Besides the package suite’s interrupted-fragment case, an independent disposable probe wrote syntactically complete `pending` JSON without a final newline; reopen rejected it as an unterminated final record.
3. **Durability failure / event ordering — PASS.** An independent disposable FIFO probe forced `File.Sync` to fail. `start` returned the fsync error, the in-memory state rolled back to `pending`, and no event was published. Production append explicitly checks Write, Sync and Close errors.
4. **Production root guard — PASS.** An independent disposable probe exercised `registerOperatorAPI`: empty operations root returned `ErrMissingOperationsDir`, a valid directory registered successfully, and a file-valued root failed construction.
5. **Retention limits — PASS.** Full package suite passed `TestRound3BoundedRetentionAndNoPayloads` (6,000 entries, total journal <=16 MiB, all newest terminal records retained and no result/progress/error payloads) and `TestRound3RotationProducesNumberedBackups` (bounded numbered backups). Round 7 also checks each segment <=4 MiB. Product constants remain `4 MiB` per segment, `3` backups and `16 MiB` total. The B1 delta from the prior candidate is test-only; `store.go` and `store_retention.go` are unchanged across that delta.
6. **No production test hook — PASS.** The retention implementation adds no callback or injectable test instrumentation. `currentJournalDir` is a read-only accessor; it cannot alter production behavior. The option-1 mutation is an ordinary test case, not a production hook.

## Verification

- `GOCACHE=/tmp/review-1354h2-gocache go test ./internal/machinehttp -count=1 -timeout 8m` — PASS, 28.541s.
- Separate `TestRound7B1MutationCapRejectionRed` — PASS; exact fail-closed cap error at entry 3.
- `go vet ./internal/machinehttp` — PASS.
- `gofmt -l internal/machinehttp` — empty.
- `git diff --check` against the assigned base — PASS.
- Disposable reviewer probe tests and the detached SHA worktree were removed after execution. The original working tree was left untouched; unrelated uncommitted work observed there was preserved.

## Verdict: ACCEPT

B1 follows the Owner-approved Option 1 without changing the production budget: the active-under-cap case survives reopen, while the all-active mutation fails closed at the cap without persisting the rejected transition. The prior journal counter-probes and exact-head hosted gates are green. No merge performed.
