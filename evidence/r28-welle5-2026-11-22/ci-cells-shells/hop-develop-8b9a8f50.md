# hop-develop-8b9a8f50 (0428-229 PR #1754)

## Status
DONE. Additive hop of PR #1754 (0428-229) to develop 8b9a8f50645. New head dbb2bbb0, back=0, feature preserved, own-commits-only. Draft-run 7175 (db 44977668657) at new head completed/success. Witnessed in cli-3 job: shells installed (zsh:/usr/bin/zsh, fish:/usr/bin/fish) but the wrapper test TestEndToEndInstalledZshAndFishWrappers was NOT executed ("No changed Go packages." gate exit) — reported as witness, not fixed. No .github/** line edited by me (ci.yml change came only via the additive merge).

## Reality check
- Planning-remote verified before first commit:
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Worktree remote guard: origin = https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80). Correct GitHub remote.
- Candidate proven: PR #1754 head acd8dd95e6a7d77d59e6a602203e5891efc32cf8, parent 6209874428f, back=5 behind new develop.
- develop fetched via origin = 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 (matches directive, after #1736 merge).
- PR #1754 is draft (isDraft=true, state=OPEN) -> hop permitted.

## Hop (additive merge-commit, no rebase/amend/force)
- Branch: lane-0428-229-ci-draft-cell-shells (PR #1754's lane branch), at candidate acd8dd95.
- Command: `git merge --no-ff 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 -m "hop PR 1754 to current develop 8b9a8f50645 (0428-229 ci draft cell shells)"`
- No conflict. Only develop content added (scripts/pr-gate-coverage.json, scripts/pr-gate-plan.py, scripts/pre-release-integration.py and tests; 245 insertions).

## Exactness proof
- back=0: `git rev-list --count HEAD..8b9a8f50645` = 0.
- Parents: HEAD^1 = acd8dd95 (candidate, carried forward), HEAD^2 = 8b9a8f50645 (develop).
- Feature preserved vs candidate: `git diff acd8dd95 HEAD -- cmd/ internal/` = empty.
- `git log --oneline origin/develop..HEAD` lists only: dbb2bbb0 hop merge + acd8dd95 candidate. No foreign candidate.
- `git diff origin/develop...HEAD --name-only` = `.github/workflows/ci.yml` (the candidate's own change, brought in via the additive merge, NOT edited by me).
- develop is ancestor of HEAD: `git merge-base --is-ancestor origin/develop HEAD` = OK.

## Push (no force) + delivery witness
- `git push origin lane-0428-229-ci-draft-cell-shells` => `acd8dd95..dbb2bbb0`
- Delivery: `git ls-remote origin refs/pull/1754/head` => dbb2bbb091057280341b33c14333982c59a64b3b. gh PR #1754 headRefOid = dbb2bbb0.

## Draft-run witness (run 7175, db 44977668657, head dbb2bbb0)
- Run terminal: completed/success (PR-selected checks aggregate).
- Job inspected: `PR · Draft Go · cli-3` (job id 137071081795), via `gh api repos/mcpdev80/baseharbor/actions/jobs/137071081795/logs` (302-followed with bearer token).
- Run env: BASE_SHA=8b9a8f50645, HEAD_SHA=dbb2bbb0, SHARD=cli-3.
- Shells ARE provisioned in the cell: `sudo apt-get install -y zsh fish` -> `zsh: /usr/bin/zsh`, `fish: /usr/bin/fish` (log lines ~534-641).
- Wrapper test TestEndToEndInstalledZshAndFishWrappers: NOT executed. The draft Go gate diffs BASE_SHA..HEAD_SHA = only `.github/workflows/ci.yml` (a workflow file, not a `*.go` file), so the gate hits `echo "No changed Go packages."` then `exit 0` (log line ~703). No Go package was selected, so `pr-go-unit-shard.py` never ran and the wrapper test was never reached.
- This matches the REQUEST CHANGES verdict ("No changed Go packages."): shells installed but wrapper test active-not. The additive hop carried only develop's scripts/ content on top of the candidate; it did not re-introduce a changed Go provisioning file into the diff, so the gate has nothing to run. Reported as witness. The fix (a Go-level change that the draft gate would select) is the card's remaining work and is out of scope for a hop; I did not edit it.

## Boundaries honored
- No subagents. No local test runs (sha256 d65b09b8ffed). No local CI runs.
- No merge/close/ready of PR #1754 (stays draft/open, Owner action).
- No GitHub comment. No posting in other sessions.
- No line in .github/** edited by me: the ci.yml change arrived solely through the additive develop merge.
- Did not set any workflow_dispatch / pins / env values / release-requirements (no test-input by me).

## End
- New head: dbb2bbb091057280341b33c14333982c59a64b3b, back=0.
- Run: 7175 (db 44977668657) completed/success at new head.
- Wrapper-test witness in cli-3: shells installed (zsh:/usr/bin/zsh, fish:/usr/bin/fish) but TestEndToEndInstalledZshAndFishWrappers NOT executed ("No changed Go packages." gate exit) -> "nicht ausgefuehrt".
