# 0428-179 exact acceptance — 2026-11-21

- PR: [#1731](https://github.com/mcpdev80/baseharbor/pull/1731), merged normally as `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046`.
- Exact source SHA: `db3f6927fee1a1831de9820a51f5e0264e59f184`.
- Test inventory entry: `cmd/baha/context_terminal_test.go::TestEndToEndInstalledZshAndFishWrappers`.
- Deterministic shard mapping: `scripts/pr-go-unit-shard.py::selected_tests` hashes the test name with SHA-256 and assigns `first_8_bytes % 4`; computed result is `cli-3`.
- Mapped gate: `PR · Go unit · cli-3`, job `136793350734`, PASS. The workflow installs zsh and fish before running this shard; the test fails loudly if either shell is missing.
- Exact run: [44886665489](https://github.com/mcpdev80/baseharbor/actions/runs/44886665489), terminal SUCCESS. Required aggregate `PR Selected Checks`, job `136794441684`, PASS. Workflow policy, source format and other selected required checks are also green.
