# Round 2 — 0428-207 app-edit-core-activation (CODEX-REVIEW fix)

## PLAN

- Read mission + review-1.md akte; record numbered plan (board file, todos json, this PLAN). Verify GitHub remote, base `develop` ancestor of PR head, changed files.
- Fix finding 1 (blocking): pass `os.ErrNotExist` wrapped sentinel into the missing-inventory test so `core_network_binding.go:70` `errors.Is(err, os.ErrNotExist)` is exercised; assert the unique `:70-72` wording.
- Fix finding 2 (acceptance criterion 2): add a regression test that exercises `inspectCoreDefaultNetworkBinding` / the real App-Edit activation path (not just the renderer) and asserts the actionable missing-owner message.
- Mutation test: confirm both tests fail under a mutation that removes/reverses `errors.Is(err, os.ErrNotExist)`, then pass in the `cmd/baha` Go unit shard.
- Push to same branch (PR #1735) with `git push --force-with-lease lane-origin`; prove delivery with `git ls-remote`; watch `gh pr checks 1735` to terminal; record run-id.
- Write round-2.md evidence with merge-base witness, before/after file line counts, PR-check table, `## repo-rule compliance` + `## cleanliness`; commit evidence to plan main; publish to origin/main; END_DONE to coordinator.

## Scope

Mission r28-welle4-2026-11-21 (pending-mission-207fix.txt): fix EXACTLY the two CODEX-REVIEW findings, nothing else. Write-set is `cmd/baha/core_network_binding_actionability_test.go` and, where the task requires, `cmd/baha/core_network_binding.go`. Forbidden: `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`, and owner-stack #1615/#1625/#1623 (branch `cli2-identity-secrets-head`); `#1615` touches `app_edit_apply_test.go` and `core_network_binding_native_test.go` which stay untouched. No `.github/**` edits, no reruns/dispatch, no subagents. Same branch only, PR #1735 stays.

## Candidate and proof (read-only)

- Session: Worker (ornith) session for lane `lane-0428-207-appedit-core-activation`.
- Model/backend: worker-ornith1.5 via AgentGateway.
- PR #1735: open, ready for review, not merged. PR head `09cf55bbaa41c921f72681ef4ee4500d9083f807`; base `develop` at `40cb28c758b02960356434b630086a341ebe1738`.
- GitHub remote (verified, first git action): `lane-origin` = `https://github.com/mcpdev80/baseharbor.git` (also `origin`, `upstream`). Used only `lane-origin`/`origin`/`upstream` whose URL contains github.com/mcpdev80.
- `git ls-remote origin refs/heads/develop refs/heads/lane-0428-207-appedit-core-activation refs/pull/1735/head` before any edit returned:
  ```
  40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
  09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/heads/lane-0428-207-appedit-core-activation
  09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/pull/1735/head
  ```
- `git merge-base --is-ancestor origin/develop origin/lane-0428-207-appedit-core-activation; echo $?` => `ancestor_exit=0` (develop IS an ancestor of the PR head).
- `git diff --name-status origin/develop...origin/lane-0428-207-appedit-core-activation` returned exactly:
  ```
  M cmd/baha/core_network_binding.go
  A cmd/baha/core_network_binding_actionability_test.go
  ```
- `git log --oneline origin/develop..origin/lane-0428-207-appedit-core-activation` returned only:
  ```
  09cf55b fix(0428-207): make Core default-network binding guard actionable
  ```

## Findings being fixed (from review-1.md)

- Finding 1 (blocking): `core_network_binding.go:70` selects the missing-inventory wording only when `errors.Is(err, os.ErrNotExist)`. The test `Test0428207CoreNetworkBindingGuardNamesMissingPreconditions` passes `errors.New("lstat ... : no such file or directory")` — a plain error that does NOT satisfy `errors.Is(..., os.ErrNotExist)`, so the ENOENT branch is never taken. Recipe: pass `os.ErrNotExist` or a wrapped sentinel `fmt.Errorf("…: %w", os.ErrNotExist)`; assert a phrase unique to the `:70-72` branch such as `runtime inventory is missing`. Keep the noncanonical test on a non-ENOENT error.
- Finding 2 (acceptance criterion 2): the new tests only call `coreDefaultNetworkBindingMissingOwnerMessage` directly, never `inspectCoreDefaultNetworkBinding` or the real App-Edit activation path. Recipe: add/reshape an allowed `cmd/baha/*0428-207*` test that exercises `inspectCoreDefaultNetworkBinding` or the real activation path and asserts the actionable message; keep auto-discovery in a `cmd/baha` CLI shard.

## Mutation rubric (per mission)

A truthful assertion must check the MESSAGE CONTENT, not just `err != nil`. An content test on an unreachable path is also wrong — verify the asserted line exists in the produced branch.

## Repo-rule compliance

- Write-set strictly limited to `cmd/baha/core_network_binding_actionability_test.go` and, where required, `cmd/baha/core_network_binding.go`. No other file touched.
- No `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`.
- `app_edit_apply_test.go` and `core_network_binding_native_test.go` (owner-stack #1615) untouched.
- No `.github/**` file edited; no `workflow_dispatch` / rerun issued.
- No subagents (AGENTS 4.8); every step run in this own session.
- Same branch / same PR #1735; no second candidate.

## Cleanliness

- No lifecycle test run on this host (mission forbids it; requires a daemon on the coordinator host). Skipped the daemon lifecycle witness by design.
- No containers/networks/volumes created on this host.
