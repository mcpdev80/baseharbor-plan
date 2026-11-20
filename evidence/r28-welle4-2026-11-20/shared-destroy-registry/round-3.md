# 0428-184 closeout — shared destroy registry retry safety

- PR: [#1715](https://github.com/mcpdev80/baseharbor/pull/1715), merged 2026-11-20 15:43:19 UTC.
- Exact PR head: `5666a6c5a8db4d6c9dde0ed59199d1b15923e534`.
- Merge commit and current `develop`: `2f81fa21dc77543a0583be4a485e9088605b5fc8`.
- Exact CI run: [44761809861](https://github.com/mcpdev80/baseharbor/actions/runs/44761809861), conclusion `success`, head `5666a6c5a8db4d6c9dde0ed59199d1b15923e534`.
- Required package check: `PR · Go unit · packages` passed. The planner-selected runtime check `PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities` passed on the same exact head. Source format, workflow policy, trusted plan, runner interface, exact candidate, focused Python, Go build and Go vet passed; other unselected matrices were skipped by plan.
- Local verification on the final implementation: `go test ./internal/application -run 'TestSharedDestroy(RemovesOwnedPlatformSources|PreservesForeignPlatformSources|KeepsEnvironmentForRegistryPruneRetry)$' -count=1`; `go test ./internal/application ./internal/observability -count=1`; `go vet ./internal/application ./internal/observability`; `git diff --check` — all passed.
- The new retry regression commits the real PostgreSQL prune, injects failure for Valkey, verifies that the environment identity remains and only the Valkey row remains, then retries through the production entry point and confirms both provider rows are removed. Independent read-only review found the injected seam limited to the unexported helper and no further blocker.
- Acceptance: owned Postgres and Valkey platform rows are cleaned, foreign environment rows are preserved, re-registration succeeds, and partial prune progress remains retryable. Card accepted after exact-head CI and merge verification.
