# Restart inventory 2026-10-27 (coordinator, per CODEMAN-START section 7)

- Frozen base: product develop `3431b22c94b068f15f9bd7b31b9f87e846200f0f`; planning base `052e5c9`.
- W1 `w1-lane`: fresh lane; checkpoint worktree `worktrees/pr3a` -> branch reservation `work/r27-w1-discovery`; 3 unpublished files listed on the W1 card.
- W2 `w2-lane`: fresh lane; no prior checkpoint; branch reservation `work/r27-w2-publication`.
- W3 `w3-lane`: fresh lane; basis = merged PR #1107 head `b83e4faa` (branch `work/r27-pr3-approve-contract`, worktree `worktrees/pr3b`); branch reservation `work/r27-w3-verification` (ordinary forward from b83e4faa).
- External config: `PLANNING_RECEIPT_WRITE_TOKEN` NOT present (only RENOVATE_TOKEN). One-time Owner request issued 2026-10-27; code preparation proceeds regardless.
- CI-only main registration: prepared later by coordinator after candidate qualification (distinct default-branch step).

## END RESTART-INVENTORY
