# Restart inventory 2026-10-27 (coordinator, per CODEMAN-START section 7)

- Frozen base: product develop `3431b22c94b068f15f9bd7b31b9f87e846200f0f`; planning base `052e5c9`.
- W1 `w1-lane`: fresh lane session `0909d47b-3852-469c-994c-924e809e7d96` (ornith); checkpoint worktree `worktrees/pr3a` -> branch reservation `work/r27-w1-discovery`; 3 unpublished files listed on the W1 card.
- W2 `w2-lane`: fresh lane session `b074bf85-94a8-4430-aca4-2c925729e8da` (qwen); no prior checkpoint; branch reservation `work/r27-w2-publication`.
- W3 `w3-lane`: fresh lane session `619b8e7c-deb9-4380-9801-7a5841541f31` (flash); basis = merged PR #1107 head `b83e4faa` (branch `work/r27-pr3-approve-contract`, worktree `worktrees/pr3b`); branch reservation `work/r27-w3-verification` (ordinary forward from b83e4faa).
- External config: `PLANNING_RECEIPT_WRITE_TOKEN` NOT present (only RENOVATE_TOKEN). One-time Owner request issued 2026-10-27; code preparation proceeds regardless.
- CI-only main registration: prepared later by coordinator after candidate qualification (distinct default-branch step).

## END RESTART-INVENTORY
