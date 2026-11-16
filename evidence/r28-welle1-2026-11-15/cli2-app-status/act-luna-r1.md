# CODEX-REVIEW — PR #1614

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-cli2-app-status`  
**Candidate:** `03e280800b53b43cd08d6c468c0be7b55d45b1a8`  
**Base:** `lane-0428-059-cli2-source-model` @ `818d572b982a69e2caebd5474a4ba270ed21fd41`  
**Exact-head CI:** run `43815584499`, event `pull_request`, created `2026-11-16T06:16:03Z`, COMPLETED SUCCESS, exact head. `git diff --check` clean.

## Verdict: REQUEST CHANGES

The retained-placement helper added in `cmd/baha/app_versions_view.go` is not connected to production. `viewPlacementServices` is referenced only by tests; production `collectSourceModelComponents` and `componentRowsForRecord` call `declaredVersionServices` directly. That helper classifies shared PostgreSQL/Valkey using ambient application placement (`application.UsesSharedPostgreSQL/Valkey`), so production status and versions can report rows from ambient config instead of the per-deployment retained placement. The helper itself mutates process-global environment with `os.Setenv`, which would also make a future production call unsafe under concurrent CLI/MCP requests.

## Recipe / stop

- **Files/change:** thread the record's retained per-provider placement through the production row builders (`cmd/baha/app_versions_view.go` and `cmd/baha/app_versions_command.go`) and make service enumeration a pure function of manifest plus placement. Remove the global environment mutation helper.
- **Required tests:** exercise the actual production builders/command with two records whose retained PostgreSQL/Valkey placement differs from ambient organization/environment config; assert correct ownership rows and consistent CLI, JSON, and MCP output. Include concurrent calls to demonstrate no cross-request placement leakage.
- **Checks:** retain the exact-head green run as evidence for the reviewed head only; correction requires a new exact-head PR `pull_request` SUCCESS covering changed packages and tests.
- **Stop:** if a record lacks retained placement, preserve the documented unavailable/ambient fallback semantics; do not infer shared-resource ownership from unrelated ambient state.

Read-only SHA-exact review; no product files changed; no merge.
