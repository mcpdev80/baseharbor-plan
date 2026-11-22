# hop-develop-82825e95 (0428-061 PR #1752, w27)

## Status
DONE. Hop of PR #1752 (0428-061 sourcepull) from 0045bdcc7438 to develop 82825e95a6f. New head b61c5350, back=0, feature preserved, own-commits-only, no .github/** or scripts/** own-change. First green PR-run for #1752: run 7196 (db 44984775584) completed/success, 0 failed jobs. cli-3 (job 137092835690) now ran and is green: 'Install interactive shells for the shell-wrapper path' succeeded (zsh:/usr/bin/zsh, fish:/usr/bin/fish) and TestEndToEndInstalledZshAndFishWrappers executed --- PASS (10.35s). This is the only rose that fell for this PR (the old 'zsh: executable file not found' failure, job 137077374467 at base 44979724623) is resolved by the #1754 merge.

## Reality check
- Planning-remote verified before first commit:
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Worktree remote guard: origin = https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80). Correct GitHub remote.
- Candidate proven: PR #1752 head 0045bdcc743854164f54adecf0cb2c17e3e49c8d, parent 7b3c658800a, back=1 behind new develop.
- develop fetched via origin = 82825e95a6f6083702d0ba5401d97f356085c722 (directive: #1754 merged, zsh-lücke in Draft-Go-cell closed).
- PR #1752 is draft=true, state=OPEN, headRefName=lane-0428-061-sourcepull -> hop permitted; stays draft.

## Hop (additive merge-commit, no rebase/amend/force)
- Branch: lane-0428-061-sourcepull (PR #1752's lane branch), at candidate 0045bdcc7438.
- Command: `git merge --no-ff 82825e95a6f6083702d0ba5401d97f356085c722 -m "hop PR 1752 to current develop 82825e95a6f (0428-061 sourcepull)"`
- No conflict. Only develop ci.yml change arrived (14 insertions) via the merge — the #1754 shell provisioning that is now part of base; NOT my hand-edit.

## Exactness proof
- back=0: `git rev-list --count HEAD..82825e95a6f` = 0.
- Parents: HEAD^1 = 0045bdcc7438 (candidate, carried forward), HEAD^2 = 82825e95a6f (develop).
- Feature preserved vs candidate: `git diff 0045bdcc7438 HEAD -- cmd/ internal/` = empty.
- `git log --oneline origin/develop..HEAD` lists only: hop merge b61c5350 + candidate 0045bdcc + prior 0428-061 commits. No foreign candidate.
- `git diff origin/develop...HEAD --name-only` = only 0428-061 sourcepull files (cmd/baha/*, contracts/machine/v1/control.golden.json, docs/*, internal/development/*). NO .github/** and NO scripts/** in my diff.
- ci.yml count in develop...HEAD diff = 0 (ci.yml change came from develop via the merge, not my edit).
- develop is ancestor of HEAD: `git merge-base --is-ancestor origin/develop HEAD` = OK.

## Push (no force) + delivery witness
- `git push origin lane-0428-061-sourcepull` => `0045bdcc..b61c5350`
- Delivery: `git ls-remote origin refs/pull/1752/head` => b61c5350cbcb75eacdcd2ef07e0f19b2dd26b817. gh PR #1752 headRefOid = b61c5350, isDraft=true, state=OPEN.

## Run witness (new head vs baseline)
- New head PR-run: run 7196, db 44984775584, head b61c5350, event pull_request, terminal **completed/success**. Job tally: 6 success / 27 skipped / **0 failure**.
- Baseline run: run 7183, db 44979724623, event pull_request, completed/**failure**. Failed job: `PR · Draft Go · cli-3` (id 137077374467), reason 'zsh: executable file not found'. This reason no longer exists at the new base.
- Comparison: the new head carries **0 failed jobs**; the single previously-failing cli-3 job is now green.

## cli-3 witness (job id 137092835690, conclusion success)
- Logs fetched via `curl ... /actions/jobs/137092835690/logs`.
- Shells provisioned in the cell: 'Install interactive shells for the shell-wrapper path' -> `zsh: /usr/bin/zsh`, `fish: /usr/bin/fish`.
- Wrapper test executed and PASSED: `go test ./cmd/baha -run TestEndToEndInstalledZshAndFishWrappers -count=1 -v` -> `=== RUN   TestEndToEndInstalledZshAndFishWrappers` -> `--- PASS: TestEndToEndInstalledZshAndFishWrappers (10.35s)`. No `--- FAIL`, no old 'zsh: executable file not found'.
- Verdict: **cli-3 ausgefuehrt + groen**. This is the only rose that has fallen for PR #1752; it is now resolved by the develop #1754 merge.

## End
- New head: b61c5350cbcb75eacdcd2ef07e0f19b2dd26b817, back=0.
- Run: 7196 (db 44984775584) completed/success at new head.
- Failed jobs at new head: 0.
- cli-3 (job 137092835690): SHELLS installed + TestEndToEndInstalledZshAndFishWrappers --- PASS (10.35s) => 'cli-3 ausgefuehrt + groen'.
- Cleanliness: nothing started (no containers/compose/docker/podman launched). No .github/** or scripts/** edited by me.
