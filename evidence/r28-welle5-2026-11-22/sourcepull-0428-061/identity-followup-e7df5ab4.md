# #1752 commit identity follow-up — exact head e7df5ab4a6c3219404de26846198d4f6e1b8fed0

## PLAN

1. Read `/var/tmp/rev1754c.g.md` and identify its additional #1752 identity question.
2. Read the live PR commit metadata for the reported exact head and compare it with the earlier task-identity commits.
3. Record what the metadata establishes and what it does not establish; do not issue a #1752 code verdict.
4. Publish this read-only note to Planning and report both current holds to the Coordinator.

## Verified metadata

- Planning remote verified before commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).

- Live PR #1752 is OPEN and Draft, base `develop`, head `e7df5ab4a6c3219404de26846198d4f6e1b8fed0`.
- PR commit listing shows the first ten commits through `a4adc29a5844266cf4009bb12b9b68ae26a4a99a` authored as `0428-061-sourcepull` with email `0428-061@baseharbor.local`.
- The next commit `b010dabcbbd853d8ee7eaf8d28fb3869b025dec3` and current head commit `e7df5ab4a6c3219404de26846198d4f6e1b8fed0` both show author and committer name `BaseHarbor Worker`, email `worker@example.invalid`, no associated GitHub author/committer login, and signature verification `verified=false`, reason `unsigned`.
- The prior #1714 review precedent records its hop commit author and committer as `mcpdev80` in `evidence/r28-welle5-2026-11-22/mcp-perses-tool-drift/review-2-head89253bd2.md:20`; the metadata differs here.

## Assessment and scope

The two new commits have a materially different, unlinked and unsigned Git commit identity from the task-attributed commits. Git metadata alone cannot establish who created them or why that identity was used; no attribution or owner authorization is present in the reviewed metadata. This is a provenance discrepancy to resolve before treating the change as task-owner-authored. It is not by itself a finding about code correctness.

Any earlier #1752 verdict at `a4adc29a5844266cf4009bb12b9b68ae26a4a99a` is exact-head-specific and does not cover commits `b010dabc...` and `e7df5ab4...`; the current candidate requires a fresh exact-head review after its hosted run is terminal, with identity attribution addressed. No #1752 verdict is issued here.

## repo-rule compliance

Read-only GitHub metadata inspection. No local tests, source changes, branch changes, comments, approval, merge, close, or PR-state changes.

## END codex-rev-1747 BLOCKED

#1752 identity attribution and exact-head CI/review remain unresolved; #1754 remains REQUEST CHANGES pending an executed hosted wrapper test; #1753 remains held separately.

Exact remote Planning tree output after fetch:

```text
evidence/r28-welle5-2026-11-22/ci-cells-shells/review-1754-headacd8dd95.md
evidence/r28-welle5-2026-11-22/sourcepull-0428-061/identity-followup-e7df5ab4.md
```
