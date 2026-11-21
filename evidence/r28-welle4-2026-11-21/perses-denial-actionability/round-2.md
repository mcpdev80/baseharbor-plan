# 0428-211 / PR #1733 — exact-head closeout

- Exact head: `3aec8701e497e583861babc227b509ddbd86398c`.
- Exact hosted run: [44889694969](https://github.com/mcpdev80/baseharbor/actions/runs/44889694969), SUCCESS.
- Test: `internal/application.TestEvaluatePersesAnonymousDenialNamesNextCommand`.
- Mapped gate: package-level Go unit suite in job `PR · Go unit · packages` (`136802680814`), SUCCESS; task test binding is auto-discovery in the Go package suite. Aggregate `PR Selected Checks` job `136803684844`, SUCCESS.
- The exact run also passed all four CLI shards, owner, go-build, go-vet, source format, Trusted Plan, Workflow policy, and required selected runtime checks.
- PR #1733 merged normally at `2026-11-21T09:34:10Z`; merge commit `44b55ea4bc66e0139dc147df10f925079ab1b27d`.
- The denial now includes both the missing verified operator identity and the next command (`baha login`) while preserving the existing machine-readable error code.
