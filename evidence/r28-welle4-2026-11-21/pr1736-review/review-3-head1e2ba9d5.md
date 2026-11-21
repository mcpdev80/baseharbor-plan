# CODEX-REVIEW — PR #1736, card 0428-055

## PLAN
1. Verify both GitHub refs for PR #1736 match the mission's exact head; stop if either differs.
2. Verify head ancestry from the prior approved candidate and inspect the stat parity against it.
3. Recheck the three prior spot-check claims on the hopped head: Docker and Podman coreless lifecycle coverage for environment destroy, full-bundle gate behavior with registration-only paths remaining open, and native test uniqueness in exactly one application shard.
4. Hold the #1736 verdict as directed because #1627 is still open and behind develop; do not issue a fresh approval or prepare evidence that could advance a merge.
5. Verify author/committer identity and that the hop added no authors.
6. Publish exact-head review evidence from the lane-owned Planning worktree only; no product edits, comments, merges, closes, or local suite tests.
7. Review #1625 then #1749; #1751 was already reviewed at its exact head. Await w21’s #1627 documentation-audit correction and exact terminal run; keep #1736 last until #1627 registration plus Docker and Podman gates pass.

## Planning remote
`origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). Raw `git remote -v` output:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```, verified in the lane-owned Planning worktree before evidence publication.

## Sequence correction

The follow-up mission `/var/tmp/seq2.g.md` explicitly pauses the #1736 verdict because dependency #1627 (card 0428-055, branch `cli2-env-delete`) is open and behind develop. #1627 requires shard registration and both Docker and Podman runtime gate executions. No new #1736 verdict will be issued until that dependency is accepted. Run 44952497719 had already been inspected before this sequence correction arrived; it is a terminal success for the exact head, but does not satisfy the missing dependency.


## Sequencing update

Owner sequence correction `/var/tmp/revorder2.g.md` confirms the order: #1625, #1749, #1751 (already reviewed), then #1627 after w21 corrects its documentation-audit failure; #1736 remains held until #1627 acceptance. This file is a hold record only, not a #1736 verdict.
## Live dependency hold — revorder2 sequence

- Current GitHub API state for prerequisite PR #1627: OPEN, non-draft, base `develop`, head `5dd34a3752aa861f0be1b0b5dd81acbea17708d6`, merge state BLOCKED. The owner mission reports documentation-audit job 136999832459 failed because two literals were lost in `docs/en/reference/cli-machine-coverage.md`; w21 is correcting it. The task still requires named test registration and successful Docker plus Podman gates.
- Therefore #1736 remains HELD at `1e2ba9d57868778d7c74ef68882f61bd1b01bb33`; this is not a new approval or a finding that its implementation is defective. Its earlier exact-head CI result does not satisfy the open prerequisite.
- Docker inventory before and after this review, shell PID 578947: the same eight pre-existing `bh-itest-*` containers were already exited; no container or compose project was started by this review.
- Verdict state: HOLD pending #1627 acceptance. No merge, PR comment, or close was performed.


END_BLOCKED codex-rev-1747: #1736 remains held pending #1627 acceptance at observed head 5dd34a3752aa861f0be1b0b5dd81acbea17708d6; candidate under hold 1e2ba9d57868778d7c74ef68882f61bd1b01bb33.
