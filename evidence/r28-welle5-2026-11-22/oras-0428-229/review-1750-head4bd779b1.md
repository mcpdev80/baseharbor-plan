# PR #1750 independent read-only review — 4bd779b1501d

## PLAN

1. Verify the product GitHub remote, PR #1750 live head, develop base and exact run identities.
2. Compare the test-side ORAS provisioning path with scripts/ci-install-oras.sh, including pin and checksum verification; determine whether the test-side path preserves fail-closed behavior.
3. Inspect logs via GitHub API for the six named app-repository integration tests in exact runs 44972447675 and 44972454590; count only actually executed tests, never skipped tests.
4. Withhold verdict/publication until both runs are terminal; then record the decision, evidence and exact job IDs.
5. Preserve #1753 hold, avoid repeating #1752 review, and make no product changes, local test runs, merges, closes, comments or reruns.

## Exact refs

- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Product remote was resolved to `https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote` witness: `4bd779b1501db00049c353b3865bd3ba75704aef refs/pull/1750/head` and `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`.
- The PR API reported #1750 OPEN/DRAFT, base `develop`, exact head `4bd779b1501db00049c353b3865bd3ba75704aef`.
- Diff against the exact base covers eight test files under `cmd/baha/`: `app_init_source_neutral_test.go`, `app_init_wizard_test.go`, `app_perses_host_containers_cli_test.go`, `app_perses_infra_dashboards_cli_test.go`, `application_lifecycle_lock_test.go`, `repository_up_init_test.go`, `runtime_integration_test_support_test.go`, and `test_operator_context_test.go`.

## Review findings

The test-side helper `runtime_integration_test_support_test.go:1426-1443` returns immediately for any `oras` found by `exec.LookPath`, and also reuses any user-local executable. When missing, it delegates to production `installORAS`; errors are retained by `ensureRuntimeIntegrationTrustPlane` at `:740-742` and become `t.Fatalf` at `:936-940`. Therefore the missing-tool error path is fail-closed and does not skip, but a preinstalled binary is not checked against the pinned version.

The production installer pins `orasSetupVersion = "1.3.6"` at `oras_setup.go:24`, downloads the official archive and checksum file, and verifies SHA-256 before installation at `:62-83`. The CI script also pins version 1.3.6 and checksum-verifies at `scripts/ci-install-oras.sh:7,17-21`; unlike the helper, it installs that pin unconditionally into `~/.local/bin` and adds it to `GITHUB_PATH` at `:24-27`. The fallback download implementation shares the pin/checksum mechanism; the overall test-side behavior is not identical because it accepts whatever executable is already on PATH.

Card 0428-229 (`tasks/t-20261122-ci-cells-missing-runner-prerequisites.md`) explicitly scopes the prerequisite fix to `.github/workflows/ci.yml` and requires the verified ORAS step before `validate` runtime integration tests, plus zsh/fish in `PR · Draft Go · cli-3`. It points to the existing ORAS step at workflow lines 288-289 / 551-552 and asks for the validate insertion before lines 400-404. Thus item 1: a workflow step is required by the task contract; the test-side fallback is useful defense-in-depth but does not satisfy that acceptance or guarantee a pinned binary when one is already present. This review did not edit workflow files.

## Hosted-run results

- Run `44972447675`, exact head `4bd779b1501db00049c353b3865bd3ba75704aef`: terminal FAILURE. Job `137054968702` (`PR · Draft Go · cli-3`) failed with the log line `context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh" executable file not found in $PATH`. `PR Selected Checks` job `137054970611` was SKIPPED. This is a STATE finding; no workflow changes or reruns were made.
- Run `44972454590`, same exact head: terminal CANCELLED. `validate` job `137054992447` was cancelled during step 16, `Run runtime integration tests serially`; `PR Selected Checks` job `137055085429` and `Targeted HA · docker` job `137055017658` were SKIPPED.
- The serial hosted log listed six native tests. Actually executed terminal PASS: `TestRepositoryWorkflowRealLifecycle`, `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`, and `TestRepositoryComposeWorkloadOnlyLifecycleInCI`. `TestRepositoryComposePinnedWorkloadLifecycleInCI` had started but the operation was cancelled before a PASS. `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` and `TestMultiInstanceComposeLifecycleInCI` did not start. Therefore the six-test requirement is incomplete; a started/cancelled test is not a pass.
- The first lifecycle test did complete, establishing that the test-side setup reached the production ORAS gate, but the hosted log does not show that it installed the pin (the helper can no-op for any existing ORAS). No skipped or absent test was counted as a pass.

## Review outcome

NOT APPROVED. The fail-closed error path is sound, but item 1 requires the workflow install step and the exact hosted evidence is incomplete: run 44972447675 failed for missing zsh and run 44972454590 was cancelled with three of six native tests unproven. No product changes, local tests, merge, close, comment or rerun occurred.

## repo-rule compliance

Read-only inspection used the exact GitHub head and hosted API logs. No product checkout changes, workflow edits, local tests, local containers, PR comments, merge, close, rerun or subagents were used.

## cleanliness

Before: command `docker ps -a`, shell pid 1625899. Output:

```text
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                      PORTS     NAMES
268b7d8b4612   alpine:3.22             "sleep 300"              6 hours ago    Exited (0) 6 hours ago                bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1
34cf9576dc2b   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-1
e88b00795b5c   openbao/openbao:2.7.1   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-member-1-1
1451a7b5b3c6   postgres:18-alpine      "docker-entrypoint.sh"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-init-1
d7ba821c0e08   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-1
957a80e73b57   postgres:18-alpine      "/bin/sh -ec 'cp /ru…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-member-1-1
45bddf32278e   postgres:18-alpine      "/bin/sh -ec 'trap :…"   10 hours ago   Exited (130) 10 hours ago             bh-itest-7daed22f-28345-shared-postgres-admin-1
9d3f1a2b1e0e   openbao/openbao:2.7.1   "/bin/sh -ec 'trap :…"   10 hours ago   Exited (143) 10 hours ago             bh-itest-7daed22f-28345-shared-openbao-admin-1
```

After: command `docker ps -a`, shell pid 1633232. The output was identical to the before snapshot; no containers were started by this review.

## END codex-rev-1747 BLOCKED

Reason: workflow prerequisite is not satisfied and required hosted coverage failed/cancelled; awaiting correction and a complete exact-head run.
