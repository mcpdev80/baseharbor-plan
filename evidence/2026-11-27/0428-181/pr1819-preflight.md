# ROLLE: REVIEW — PR #1819 preflight

**Read-only disposition, 2026-11-27. No product edit, rerun, review action, or merge was performed.**

## Current witnesses

- Core PR #1819 is OPEN, non-draft, base `develop`, head `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` (`w54-0428-181-export`), `MERGEABLE` but `BEHIND`. The live develop tip observed was `ea5218d72e263f21e79853b679af50074dab8c25`; the PR head is 40 commits behind and 11 ahead. `refs/pull/1819/head` matched the API head.
- The latest Hosted run on that exact head is pull_request run `45699760220`, completed SUCCESS. `PR · Trusted Plan`, Go unit packages and CLI shards, the selected Docker data-capabilities runtime job, and `PR Selected Checks` succeeded. The other native matrix jobs were skipped in this run. Thus this is **not a Trusted Plan failure class**: Trusted Plan passed on that historical exact head. It is **chain-blocked and stale-base evidence**, not current qualification: #1812 remains OPEN at `6ab5310d17358bc0f4c86ef09bea476b82517e3e`, and #1819 is behind live develop. The prior success cannot qualify a post-#1812 head.
- Core PR #1812 is OPEN, base `develop`, head `6ab5310d17358bc0f4c86ef09bea476b82517e3e`, `BLOCKED`; it has not landed. The sequence remains #1812 first, then #1819. Disjoint preparation may continue, but #1819 qualification and merge must wait for #1812's landing.

## Forward-only worker recipe after #1812 lands

1. Verify the #1812 landing on live `develop` from GitHub's mergedAt/mergeCommit and the landed content; do not rely on the PR's current `MERGEABLE` field. Fetch current `origin/develop` after that landing.
2. On the owning #1819 branch, merge `origin/develop` once as an ordinary forward merge under the executing lane's canonical identity, then push normally. No rebase, force-push, or history rewrite.
3. The present #1812/#1819 file sets overlap at `.github/workflows/pre-release-runtime-suite.yml`; the other current #1819 files (`internal/application/runtime_postgres.go` and the two `internal/metrics/perses_dashboard_provision*` files) do not overlap #1812's current file list. A read-only `git merge-tree` of today's two heads reports no textual conflict. Still inspect the workflow result after the real absorb and preserve both changes; stop for a worker conflict resolution if a later base produces a conflict.
4. On the resulting frozen exact head, obtain fresh Hosted pull_request qualification: Trusted Plan, applicable Go/unit checks, and all card-required selected Docker and rootless-Podman runtime gates (including the relevant data-capabilities/observability surfaces) must be executed-success or have valid exact-head reusable evidence; skipped required gates do not qualify. Obtain the required distinct exact-head pull_request run IDs sequentially if that pair rule is in force. Review/merge only after that evidence and the #1812-first chain condition are satisfied.

## Planning-field check

Card `0428-181` is `wait`, links product PR #1819, and its owner field `w54-0428-181-export` matches the PR branch's historical lane. Its wait reason correctly records that the lane was released and work awaits the #1812 chain gate; there is no active execution session to infer from that owner value. The card's `depends_on` currently names only `t-20261114-r28-perses-datasources`; it does **not** encode the separately mandated #1812 prerequisite. The prose wait reason records the order, but the dependency field is incomplete relative to the current serial chain. Record/add the #1812 governing task dependency before the next lifecycle transition; do not change it as part of this preflight.

The separate baseline card `0428-273` is `wait`, has no owner or PR, and records that the #1819 source catalog rows already landed through #1822. It is baseline evidence, not a replacement for #1819's product card or its #1812 ordering gate.
