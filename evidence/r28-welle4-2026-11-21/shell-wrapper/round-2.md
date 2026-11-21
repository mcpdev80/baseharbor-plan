# 0428-179 / PR #1731 — exact-head CI round 2

- PR: https://github.com/mcpdev80/baseharbor/pull/1731
- Source SHA: `b67c3427dd8106d15082fff34187b9761161a10a`
- Exact run: https://github.com/mcpdev80/baseharbor/actions/runs/44881683635 (terminal failure)
- Test: `cmd/baha/context_terminal_test.go::TestEndToEndInstalledZshAndFishWrappers`
- Gate: `PR · Go unit · cli-3`, selected by `scripts/pr-go-unit-shard.py`; SHA-256 shard index for the test name is 3 (`cli-3`). Workflow step installs zsh and fish in cli-3 before `scripts/pr-unit-database.sh cli-3` runs the selected Go tests.
- Hosted evidence: job `136778526985` completed with failure; its log shows `zsh: /usr/bin/zsh`, `fish: /usr/bin/fish`, and the selected Go test step ran. The test cell was not skipped. The wrapper test is not in the shard's failure list, but the runner only emits failing test details when the shard fails, so this run does not claim a per-test hosted PASS.
- Blocking failures: all four CLI Go shards fail managed-operator authentication fixtures; `PR · Validation · pr-planner-tests` fails `TestMCPRegistrationCIInProcessDiscoverAndInvoke` at the same authentication boundary. `PR Selected Checks` is red. The shared prerequisite is card 0428-057 / PR #1615; that PR remains owned by the other session and was not inspected or changed.
- Result: the shell wrapper path now executes on hosted CI and cannot silently pass when shells are missing. Card remains Wait because the exact required aggregate checks are red on the external authentication prerequisite.
