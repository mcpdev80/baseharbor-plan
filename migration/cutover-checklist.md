# Cutover checklist (requires Maintainer approval)

Nothing below has been executed. Each step needs explicit approval; steps are ordered. Until step 7, the GitHub issues stay authoritative.

## Before approval

1. **Review this candidate:** the PR in baseharbor-plan, [coverage.md](coverage.md) (all 87 open issues mapped), [conflicts.md](conflicts.md).
2. **Answer the Maintainer decisions** in [conflicts.md](conflicts.md): C2 (Core definition), C3 (interface SHA), C4 (#862 release), triage items (console-1, console-2, nc-3, demo-24), stale PRs (M3), branch deletion record (M1), Docker Desktop licensing (M7).
3. **GitHub Projects:** run `gh auth refresh -s read:project` and list Projects of `mcpdev80`; decide whether any must be archived (M4).
4. **Manual Obsidian acceptance** (see [ui-acceptance.md](ui-acceptance.md)) on a real Obsidian installation.
5. **Recheck live state immediately before cutover:** `python3 scripts/snapshot.py diff`. Reconcile every NEW / UPDATED / NO LONGER OPEN / PR change in the notes (for example core-900 after PR #931 was merged; core-893/896/895 PR heads), then `snapshot.py capture`, `plan.py render`, `plan.py check`, commit.

## Transition for running sessions

6. Announce a short freeze of planning edits on GitHub issues. Active sessions (at the snapshot: session 1 on core-893/core-896 with PRs #930/#932, session 2 on core-900 with PR #931, core-895 PR #933, core-910 read-only preparation) **keep their branches, PRs and ownership**; nothing is reassigned. Their owners are already recorded in the task notes. From the switch on, they record handoffs in the task note instead of issue comments. No session is interrupted mid-change and no one else's PR is edited or merged.

## Switch (one sitting)

7. Merge the baseharbor-plan PR to `main`. From this commit on, baseharbor-plan is authoritative ([decision](../decisions/2026-10-15-planning-authority.md) → `status: accepted`).
8. Post the [notices](notices.md) on every migrated issue (script over `manifest.json`), then apply the chosen option:
   - **Option A (recommended):** add label `planning/moved` and close as "not planned" — no competing authority remains; discussion stays readable.
   - **Option B:** add label `planning/moved`, keep open, and stop editing bodies.
   Do not touch baseharbor#889 (Renovate) or triage items before their decision.
9. Land the [entry-point updates](entry-point-updates.md) as small PRs in the product repositories (EN/DE parity for public docs).
10. Retire or archive GitHub Projects if any exist (from step 3).
11. Re-run `snapshot.py diff` and `plan.py check` and record the final cutover commit SHA in this file.

## Rollback

- Before step 8: revert the merge in baseharbor-plan; GitHub issues were never changed.
- After step 8: reopen the closed issues (filter by label `planning/moved`), remove the label, post a short "planning moved back" comment, and revert the entry-point PRs. The source snapshot lets you restore any issue text that was edited afterwards. Changes made in task notes after the cutover must be copied back to the issues manually (list them with `git log` since the cutover commit).
