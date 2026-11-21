# 0428-215 — cli runtime tests, round 2 (native coverage gap: CI-bedarf)

Lane: `0428-215-cli215` · Host: laptop · Task: `t-20261121-cli-shard-runtime-tests`
Evidence lives in baseharbor-plan ONLY (never in the product repo). No markdown checkboxes anywhere in this file.

## PLAN (three places)

Board file `workers/todos/0428-215-cli215.json`:

- Step 1: reality check — planning remote `baseharbor-plan.git` (github.com/mcpdev80), sanctioned worktree `workers/0428-215-cli215-wt` on base head `e45430f2f1b7` (verified remote = github.com/mcpdev80). DONE.
- Step 2: write-set confirmation with file:line (four cmd/baha/ test files + shared runtime helper). DONE.
- Step 3: red-first named-form run on base head. DONE (two pure tests pass, two runtime tests CI-healed).
- Step 4: coordinator scope decision received (ans215.txt). DONE — see below.
- Step 5: investigate `core_network_binding.go:55-57` ENOENT ast, confirm missing testable statement + the native cell that must cover it. DONE.
- Step 6: write CI-bedarf section in akte. DONE (this file).
- Step 7: commit akte to baseharbor-plan, push origin/main, verify evidence path on origin/main, END to coordinator with plan SHA + PR number, cleanliness. PENDING.

## Reality witnesses

- Planning remote (verified before any evidence commit): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Sanctioned worktree `workers/0428-215-cli215-wt`: `origin https://github.com/mcpdev80/baseharbor.git` (resolved to github.com/mcpdev80 per remote-guard), HEAD `e45430f2f test(0428-204): authenticate secure export command path` = base head.
- Base head (ls-remote): `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4  refs/heads/lane-0428-198-cli-shard-operator-env`.
- PR #1740 head: `0ffe093357d9f7fb52f5e7542f4ade41e48fab1b`, base `lane-0428-198-cli-shard-operator-env` @ `e45430f2f1b7`.

## Red-first results on base head `e45430f2f1b7` (named runner form, GOTMPDIR=/home/marcel/.gotmp GOCACHE=/home/marcel/.gocache)

- `TestRuntimeUpRequiresORASBeforeCoreBootstrap` — PASS (pure negative-path, no runtime).
- `TestSharedBackendReconcileRejectsSecondProcess` — PASS (in-process second-process emulation).
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` — FAIL locally (no runtime / OOM); PASS on CI.
- `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` — FAIL locally (host OOM); PASS on CI.

## CI evidence (run 44868911131, CI #1740, head 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b)

- `PR · Go unit · cli-1` = success, `cli-2` = success, `cli-3` = success, `cli-0` = failure.
- Exactly ONE first-level `--- FAIL:` test name in the whole protocol = `TestAppListAllTargetsWorksAfterInstallationDestroy` (card 0428-210 / PR #1739, still open). Counting by unique test names (H-V26), not gate lines: 1.
- The two runtime-pflichtige tests are assigned to **cli-2** by `scripts/pr-go-unit-shard.py`; `cli-2` SUCCESS therefore proves they PASSED on the CI runner (real runtime). Healed at the base — not my work to skip or restructure.
- `PR · Native Keycloak/Core · docker` = success, `PR · Native Keycloak/Core · podman` = success.

## Coordinator scope decision (ans215.txt, within card)

1. The two runtime-pflichtige tests are already healed at the base — do NOT skip, do NOT restructure, keep assertions untouched. Evidence is CI-only: cite cell + run-id. If a case were never selected in any cell, report the selection-rule with file:line — no own skip. (Not the case here: cli-2 is green.)
2. `core_network_binding.go:55-57` ENOENT ast is owner-scope (would live in `scripts/**` / `.github/**`); I do NOT edit those. I write a `CI-bedarf` section: ast (file:line), the missing testable statement, and which native cell must cover it. Coordinator carries the workflow change to the owner.
3. Use the named runner form `go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run <name>`, never bare `go test ./cmd/baha/`. `## cleanliness` with my own pid line.

## CI-bedarf: the uncovered native coverage gap

- AST: `cmd/baha/core_network_binding.go:55-57`, inside `inspectCoreDefaultNetworkBinding` (file `cmd/baha/core_network_binding.go`, function `prepareCoreDefaultNetworkBinding` at line 62 is the caller seam; production callers `cmd/baha/runtime_start.go:164`, `cmd/baha/target.go:682`).
- The branch: when a Core-owned default network already exists on the runtime (`len(actual) != 0`) but it is not the independent shared-backend owner, the code refuses to adopt it and verifies native ownership via `bhruntime.ExistingControlPlaneRuntimeInventory(...)` (a daemon call). With no daemon it returns ENOENT → "existing native network lacks a protected Core or shared backend owner".
- Missing testable statement: *When a Core-owned default network already exists on the runtime and is not the independent shared backend owner, `inspectCoreDefaultNetworkBinding` rejects the binding and refuses to adopt the foreign network (and does not fall back to `BindControlPlaneToExistingDefaultNetwork`).*
- Why no local route: the precondition (a pre-existing Core-owned default network that is not a shared owner) requires a real Core lifecycle; the mission bans local lifecycle containers. `internal/runtime/compose_resources.go:102` `InspectProjectResources` calls `c.directOutput(...)` which ENOENTs without a daemon.
- Existing test `cmd/baha/core_network_binding_native_test.go:23` (`TestCoreBootstrapRetainsApplicationSharedNetworkAndSQL`, skips unless `BASEHARBOR_CORE_SHARED_NETWORK_ACCEPTANCE=1`) covers the **shared-backend-owner** branch (lines 38-52) but NOT the line-55-57 branch.
- Cell that must cover it: `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` (both green at #1740 head, run 44868911131). This is the native path the card means.
- Route to wire: a native-runtime-cell test in `cmd/baha/core_network_binding_native_test.go` that seeds an independent Core-owned default network and asserts `inspectCoreDefaultNetworkBinding` rejects it — gated behind an acceptance env var like the existing sibling (e.g. `BASEHARBOR_CORE_FOREIGN_NETWORK_ACCEPTANCE=1`), selected by the Runtime workflows. This is a CI/selection change: owner-scope, carried to the owner by the coordinator. No own skip guard.

## GRENZEN honored

- No `.github/**`, no `scripts/**` selection change, no `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go`.
- Assertions untouched on all four runtime tests; no local skip guard added.
- No bare `go test ./cmd/baha/`; no lifecycle containers started; no subagents; no second PR.

## END status

END_BLOCKED — CI-bedarf documented; the actual coverage-gap implementation + CI route is owner-scope (workflow change), carried by coordinator. No product commit, no PR this round. Candidate SHA: none.

## cleanliness

- No docker/podman compose project started. `docker ps -a` BEFORE (own pid `<pid>`): read-only `docker network ls` (only pre-existing `baseharbor-*` projects). No containers created. After: none.
