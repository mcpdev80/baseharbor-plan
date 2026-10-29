## promotion-pr

- ✔ 0. Read main-reg-evidence-route.md and codex-rv1204.
- ✔ 1. git -C baseharbor fetch origin; confirm origin/main at 7a417d37, origin/develop at f95b3446.
- ✔ 2. Verify the six-file main->develop diff: .github/workflows/receipt-approval.yml, .github/workflows/receipt-post-run.yml, contracts/contracts_test.go, scripts/receipt_writer.py, scripts/test_receipt_postrun.py, scripts/test_receipt_verifier.py — all CI-chain-only, zero product features.
- ✔ 3. Create worktree worktrees/promote-ci, branch work/r27-promote-ci-registration from origin/develop (f95b3446), NO merges performed.
- ✔ 4. Push branch and open PR #1205 against main with title "ci: promote develop f95b3446 to main (R27 registration lineage)".
- ✔ 5. Report PR details and evidence.

### Branch details

- **Branch**: work/r27-promote-ci-registration
- **Base**: origin/develop (f95b3446)
- **Created from**: origin/develop f95b3446
- **No merges performed** — the branch is a clean development promotion.

### PR details

- **PR #1205**: https://github.com/mcpdev80/baseharbor/pull/1205
- **Base**: main
- **Head**: work/r27-promote-ci-registration
- **Head SHA**: f95b3446ed9a007a31fcc692396d6dfaf3b38c36
- **State**: OPEN

### PR body cites

- Precedents 364db5d4/df451e0d/e13f1570
- Six-file main->develop diff (confirmed CI-chain-only: workflow files, receipt scripts, contract tests)
- Task cards t-20261029-r27-postrun-token-mapping and t-20261027-r27-cutover-pr3
- Merge execution belongs to CODEX-MERGE after review

### CI status on PR #1205

No checks reported on the branch — expected for a promotion PR that carries already-qualified lineage from develop. The qualified lineage for this exact change exists on develop via PR #1202 (head 7a417d37), which has green PR Selected Checks. The promotion PR adopts that lineage to main via a release/promotion merge pattern (364db5d4/df451e0d/e13f1570).

### Six-file CI-chain-only diff confirmed

```
.github/workflows/receipt-approval.yml
.github/workflows/receipt-post-run.yml
contracts/contracts_test.go
scripts/receipt_writer.py
scripts/test_receipt_verifier.py
scripts/test_receipt_postrun.py
```

All 6 files are CI-chain-only: workflow definitions, receipt writer/test scripts, and contract tests. Zero product features.

### Route (a) selection

Per main-reg-evidence-route.md, Route (a) is selected: qualify the exact change on develop (green PR Selected Checks via PR #1202), then adopt onto main via the release/promotion merge. The promotion PR #1205 carries this already-qualified lineage.

END q206-DONE
