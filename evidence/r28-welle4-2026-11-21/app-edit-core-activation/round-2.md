# Round 2 — 0428-207 app-edit-core-activation (CODEX-REVIEW fix)

## END

END DONE then END_BLOCKED 0428-207-appedit-fix2: round-2 fix delivered (51c6ccc90 + gofmt 213331217), PR #1735 head 213331217024 (develop-ancestor), CI 44859099909 at exact head shows only inherited operator-auth failures (pre-existing on clean base 09cf55b), 0428-207 tests pass; then STOPped per owner (stop207.txt) + publish hold (holdpub.txt) during owner's active 4-path rebase; committed nothing / pushed nothing more to plan repo; card owned by owner now. Awaiting release to commit this END_BLOCKED line.

## Scope

Mission `pending-mission-207fix.txt` + operator update `n207.txt`: fix EXACTLY the two CODEX-REVIEW REQUEST CHANGES findings (finding 1 blocking ENOENT branch, finding 2 acceptance-criterion-2 activation regression), nothing else. Write-set strictly `cmd/baha/core_network_binding_actionability_test.go` and, where required, `cmd/baha/core_network_binding.go`. Forbidden: `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`, owner-stack #1615/#1625/#1623 (`cli2-identity-secrets-head`); `app_edit_apply_test.go` and `core_network_binding_native_test.go`. No `.github/**` edits, no reruns/dispatch, no subagents, same PR #1735 only.

## PLAN

- Read mission + review-1.md akte; record numbered plan (board file `workers/todos/0428-207-appedit-fix2.json`, this PLAN). Verify GitHub remote, base `develop` ancestor of PR head, changed files.
- Fix finding 1 (blocking): pass `os.ErrNotExist` wrapped sentinel into the missing-inventory test so `core_network_binding.go:70` `errors.Is(err, os.ErrNotExist)` is exercised; assert the unique `:70-72` wording `runtime inventory is missing`.
- Fix finding 2 (acceptance criterion 2): add a regression test that exercises `inspectCoreDefaultNetworkBinding` (not just the renderer) and asserts the actionable missing-owner message; gofmt the test.
- Local unit checks: build, vet, all 4 Test0428207* pass; confirm inherited shard failures are pre-existing on clean base.
- Push evidence to plan main; push code to same branch via --force-with-lease; prove delivery; watch hosted CI to terminal (4.6); record run-id + conclusion.
- Write this round-2.md, publish to origin/main, END_DONE to coordinator.

## Candidate and proof (read-only)

- Session: Worker (ornith) session for lane `lane-0428-207-appedit-core-activation`.
- Model/backend: worker-ornith1.5 via AgentGateway.
- PR #1735: open, ready for review, not merged. Base `develop` `40cb28c758b02960356434b630086a341ebe1738`; PR head after fix `2133312170247bdc340d3be8fa11b3e299ae0e6d` (two commits on top of original `09cf55bbaa41c921f72681ef4ee4500d9083f807`).
- GitHub remote (first git action, resolved to github.com/mcpdev80): `lane-origin` = `https://github.com/mcpdev80/baseharbor.git` (also `origin`, `upstream` — same URL). Used only remotes whose URL contains github.com/mcpdev80.
- `git ls-remote origin refs/heads/develop refs/heads/lane-0428-207-appedit-core-activation refs/pull/1735/head` before any edit returned:
  ```
  40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
  09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/heads/lane-0428-207-appedit-core-activation
  09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/pull/1735/head
  ```
- develop IS an ancestor of the original PR head: `git merge-base --is-ancestor origin/develop origin/lane-0428-207-appedit-core-activation` => `ancestor_exit=0`.
- Base attestation: cut from `09cf55bbaa41c921f72681ef4ee4500d9083f807` (`git ls-remote origin refs/heads/lane-0428-207-appedit-core-activation`); that SHA is the parent of both my commits.
- `git log --oneline origin/develop..HEAD` lists ONLY my own commits (plus the single original 0428-207 commit):
  ```
  213331217 fix(0428-207): gofmt import ordering in actionability test (round 2)
  51c6ccc90 fix(0428-207): make missing-inventory ENOENT branch actionable + guard activation regression (round 2)
  09cf55bba fix(0428-207): make Core default-network binding guard actionable
  ```
- `git diff origin/develop...HEAD --name-status` (final pushed branch):
  ```
  M cmd/baha/core_network_binding.go
  A cmd/baha/core_network_binding_actionability_test.go
  ```

## The two findings fixed

### Finding 1 (blocking) — ENOENT branch now reachable

Before, `Test0428207CoreNetworkBindingGuardNamesMissingPreconditions` passed `errors.New("lstat ... : no such file or directory")`, a plain error that never satisfies `errors.Is(err, os.ErrNotExist)` at `core_network_binding.go:70`, so the missing-inventory branch was never taken. Now the test passes a wrapped sentinel that the production check matches:

```go
missingErr := fmt.Errorf("lstat \"/state/runtime\": no such file or directory: %w", os.ErrNotExist)
msg := coreDefaultNetworkBindingMissingOwnerMessage(missingErr).Error()
```

and asserts the phrase that exists ONLY on the `:70-72` branch:

```go
if !strings.Contains(msg, "runtime inventory is missing") {
    t.Fatalf("0428-207: ENOENT missing-inventory message must name the missing runtime inventory, got %q", msg)
}
```

### Finding 2 (acceptance criterion 2) — real activation path regression

Added `Test0428207CoreNetworkBindingGuardActivationPathReturnsGuardedError`, which drives the actual production function `inspectCoreDefaultNetworkBinding(context.Background(), target, files)` (not the renderer) with a real `deployment.ResolvedTarget` and `bhruntime.Files`. The fixture builds the canonical shared-backend owner directory under `dataRoot = deployment.TargetStateRoot(target.Name)` = `<BASEHARBOR_STATE_DIR>/targets/<name>/providers/shared-backends/core` with an unprotected `state.json` (0777), so the guard's non-ENOENT shared-owner check at `core_network_binding.go:24-26` fires WITHOUT a daemon, and the test asserts `inspectCoreDefaultNetworkBinding` returns a non-nil error carrying the guarded `"verify existing shared network owner"` refusal. This proves the production guard is wired end-to-end on App Edit activation, not only that the renderer returns text.

The daemon-gated ENOENT branch (`ExistingControlPlaneRuntimeInventory` at `core_network_binding.go:55-57`) is intentionally out of scope here (requires a runtime daemon; forbidden on this host) — the renderer ENOENT wording there is pinned by Test0428207CoreNetworkBindingGuardNamesMissingPreconditions.

### Abweichung vom Rezept (deviation from recipe, per n207.txt)

Finding 2 was solved by driving the REAL `inspectCoreDefaultNetworkBinding` function with a filesystem fixture — exactly the recipe's primary option ("exercise `inspectCoreDefaultNetworkBinding` ... and assert the actionable message"). No helper/stub was substituted; the assertion checks the real production function's return value. The only non-renderer path exercised without a daemon is `core_network_binding.go:24-26` (shared-owner refusal), because the `:55-57` ENOENT branch requires a runtime daemon that is forbidden on this coordinator host.

## Local unit checks

- Build: `go build ./cmd/baha/` => exit 0.
- Vet: `go vet ./cmd/baha/` => exit 0.
- The 4 Test0428207* tests:
  ```
  --- PASS: Test0428207CoreNetworkBindingGuardNamesMissingPreconditions (0.00s)
  --- PASS: Test0428207CoreNetworkBindingGuardNoncanonicalShape (0.00s)
  --- PASS: Test0428207CoreNetworkBindingGuardFailClosedNeverSilent (0.00s)
  --- PASS: Test0428207CoreNetworkBindingGuardActivationPathReturnsGuardedError (0.00s)
  ```
- gofmt: `gofmt -l cmd/baha/core_network_binding_actionability_test.go` is empty after import-ordering fix.
- Inherited shard failures verified pre-existing: `TestAppCreateListShowPlan` and `TestMCPRegistrationCIInProcessDiscoverAndInvoke` fail with `Managed-environment machine operations require an authenticated BaseHarbor operator` on the clean base `09cf55bbaa41` (checked via `git stash`/`git checkout 09cf55b`), and `TestW154*` retire tests fail with `operator authentication needs interactive setup but input is not a terminal` on the clean base. None touch either changed file.

## Hosted CI (self-run, 4.6)

- Run-id: `44859099909`, event `pull_request`, triggered by the branch push (no `.github` edit, no `workflow_dispatch`, no rerun of another lane).
- Watched to terminal with `gh run watch 44859099909 --exit-status`; run status `completed`, conclusion `failure`.
- Per-job conclusions:

| Job | Conclusion |
| --- | --- |
| PR · Trusted Plan | success |
| PR · Native gate plan | success |
| Workflow policy | success |
| PR · Source format | success |
| PR · Validation · cli-gofmt | success |
| PR · Validation · go-vet | success |
| PR · Validation · go-build | success |
| PR · Focused Python | success |
| PR · Go unit · owner | success |
| PR · Go unit · cli-0 | failure (inherited) |
| PR · Go unit · cli-1 | failure (inherited) |
| PR · Go unit · cli-2 | failure (inherited) |
| PR · Go unit · cli-3 | failure (inherited) |
| PR · Go unit · packages | failure (inherited) |
| PR Selected Checks | failure (inherited) |
| All other gates (docker/podman/pre-release/contracts/pins/release) | skipped |

- Failing shards fail with the inherited operator-auth failure, e.g. `TestAppCreateListShowPlan: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.` (cli-0 log line, `main_test.go:60`). These are the `#1717`/`0428-204` class; they do NOT touch `core_network_binding.go` or `core_network_binding_actionability_test.go`. My `Test0428207*` tests pass (absent from the failure list).
- The only format failures in run 44858435428 (previous run) were `cli-gofmt`/`Source format` from my un-gofmt'd import order; corrected in 213331217 and now `PR · Source format` and `PR · Validation · cli-gofmt` succeed.

## Repo-rule compliance

- Write-set strictly the two authorized files: `cmd/baha/core_network_binding_actionability_test.go` and `cmd/baha/core_network_binding.go`. No other file touched.
- No `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`.
- `app_edit_apply_test.go` and `core_network_binding_native_test.go` (owner-stack #1615) untouched.
- No `.github/**` file edited; no `workflow_dispatch` / rerun issued.
- No subagents (AGENTS 4.8); every step run in this own session.
- Same branch / same PR #1735; no second candidate. Branch cut from base `09cf55b` (develop ancestor), delivered to `lane-0428-207-appedit-core-activation` via `git push --force-with-lease lane-origin HEAD:lane-0428-207-appedit-core-activation`. Delivery proved with `git ls-remote origin refs/heads/lane-0428-207-appedit-core-activation refs/pull/1735/head` = `2133312170247bdc340d3be8fa11b3e299ae0e6d`.

## Cleanliness

- No lifecycle/daemon test run on this host (mission forbids it). My Go unit tests create no containers/networks/volumes.
- `docker ps -a` before and after: only `bh-docker-dev-edit-runtime-integration-dev-api-1` (another lane's ambient stack, not mine) — unchanged count (1), no orphan created.

## Publication

- Evidence repo: `baseharbor-plan` (`https://github.com/mcpdev80/baseharbor-plan.git`), branch `main`.
- Committed my file in one commit (NO `git add -A`): `git add evidence/r28-welle4-2026-11-21/app-edit-core-activation/round-2.md && git commit ...` => `645112b2`.
- Pushed: `645112b203358d3645df7756c15e0ed410c47c2a refs/heads/main`.
- `git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep round-2.md` includes `evidence/r28-welle4-2026-11-21/app-edit-core-activation/round-2.md` (verified present on origin/main before END).
