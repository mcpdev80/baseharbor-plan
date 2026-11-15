# PR #1582 Review R2 — BF-03

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base/ancestry, ls-remote refs, and specified pull_request run witness.
2. Review diff c678cdd0..fa3190eb for one-time legacy /tmp migration and prove no later /tmp write path.
3. Verify foreign-target symlink rejection and new-location 0700/0600 mode assertions; check for BF-01 drift.
4. Write APPROVE or REJECT with correction recipe and exact witnesses; validate and publish evidence on origin/main.
