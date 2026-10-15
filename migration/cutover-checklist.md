# Coordinated planning cutover

The Maintainer authorized completion on 2026-10-15. This is one coordinated operation, not a separate approval request per step. Until the activation commit reaches `main`, GitHub issues remain authoritative. Following the explicit 2026-10-15 merge instruction, real UI acceptance is deferred; it is not claimed as passed. Technical validation remains required.

## Preparation

1. Review the candidate, [coverage](coverage.md) and [migration decisions](conflicts.md). Remaining product work stays open in the plan and does not block the migration.
2. Reconcile live issues/comments and PR heads. Run `snapshot.py diff`; examine each change before refreshing the snapshot. Run unit tests, `plan.py render` and `plan.py check`.
3. Prepare the [product entry-point updates](entry-point-updates.md) as small dedicated PRs. Their wording must explicitly honor the activation record so a prepared link never silently changes authority.
4. The Maintainer authorized merging despite the disclosed missing native UI. Defer [real Obsidian UI acceptance](ui-acceptance.md) to a real installation; record actual OS/versions/results there later. No fabricated pass and no additional approval request.
5. Preserve active sessions' branches, PRs, ownership and remaining acceptance. Briefly freeze only planning edits while taking the final inventory. No product-code freeze or task reassignment is required.

## Switch in one coordinated window

6. Reconcile the final live diff. Change the planning-authority decision and short entry-point notices from candidate to active. Merge the qualified planning PR; record the actual activation commit as the cutover SHA. Conditional product entry points must be available at this time; land any remaining links within this window before retiring old sources.
7. Preserve each original issue body. Add a migration notice and `planning/moved`, then close migrated planning issues as `not_planned` with the explicit explanation **migrated, not implemented or cancelled**. Link every destination of a split. Do not close Renovate #889, PRs or new external reports outside the migration manifest. Re-read each issue just before changing it; reconcile concurrent changes first.
8. Retire only BaseHarbor Project #4. ai-coding-system #1 stays untouched. If the connector cannot close Project #4, report that exact outstanding UI action; do not claim it was performed. The activation record remains the sole authority even if a stale board still exists.
9. Validate planning and migration notices. Do not run pre-cutover `snapshot.py diff` as if intentional issue closures were missing work. Preserve the cutover snapshot and per-issue operation record; compare expected closures against the manifest and verify their notice, label, destination and state. New issues follow the documented intake process.
10. Record activation SHA, entry-point PRs, migrated issue outcomes, UI result and remaining external actions. Only then report cutover complete.

## Current execution status

- Candidate verified at `df8e31233916ba66ede39212215adb243404c948`: 24 tests passed; validator 0 errors, 4 existing dependency warnings.
- All 87 open source issues remain present and unchanged at the live recheck. PR heads are refreshed separately; source issue inventory is not silently recaptured after closure.
- UI acceptance: **not executed, explicitly deferred by the merge instruction**. Product work remains intact. Authority switches when this accepted decision reaches `main`.

## Rollback

Stop planning edits, retain the failed cutover SHA and reconcile post-cutover task changes before restoring old authority. Reopen only issues actually closed by the migration operation record, restore entry-point authority notices, and reverse the activation decision. Never blindly reopen every issue carrying a label or discard intervening task changes. Product code, PRs, CI and releases are unaffected.

## Prepared entry points

BaseHarbor #937, Console #5, Demo #114 and Node Connector #6 are separate documentation draft PRs. No active task PR, original issue or product protected branch has been changed. Their conditional authority notices can be reviewed independently; merge and final cleanup follow the coordinated window above.
