ROLE: REVIEW

## PLAN

1. Read the rev-1749 mission and measure the live PR head first. Done.
2. Verify current base, exact diff, commit authorship, PR state, and task contract. Done.
3. Inspect pinnedEnv call sites and all six inherited-environment regression cases. Done.
4. Check public-surface diff, exact per-job hosted evidence, and merge readiness. Done.
5. Publish review evidence and handoff note, verify origin/main, and report verdict. In progress.

## Candidate and provenance

- PR #1749, card 0428-222, branch `lane-0428-222-child-env`, exact head `3df3cb8be6372df630b880d369f3806b0a8fe214`.
- `git -C baseharbor ls-remote lane-origin refs/pull/1749/head refs/heads/lane-0428-222-child-env` returned:

  ```
  3df3cb8be6372df630b880d369f3806b0a8fe214 refs/heads/lane-0428-222-child-env
  3df3cb8be6372df630b880d369f3806b0a8fe214 refs/pull/1749/head
  ```

- Exact base `develop` is `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`; `git merge-base --is-ancestor refs/remotes/lane-origin/develop refs/remotes/lane-origin/pr/1749` exited 0.
- `git diff --name-status refs/remotes/lane-origin/develop...refs/remotes/lane-origin/pr/1749`:

  ```
  A internal/corebackup/etcd/child_env_inheritance_0428_222_test.go
  M internal/corebackup/etcd/etcdctl.go
  M internal/corebackup/etcd/etcdutl.go
  A internal/coreupdate/child_env_inheritance_0428_222_test.go
  M internal/coreupdate/dcs_boot_probe.go
  ```

- `git log --format='%h %an <%ae> %s' refs/remotes/lane-origin/develop..refs/remotes/lane-origin/pr/1749` contains three commits, all by identity `0428-222-childenv <0428-222-childenv@baseharbor.local>`; there are no foreign authors. The mission's point 1 says card 0428-224, while its candidate and task path identify 0428-222; the live task is `t-20261121-child-env-inheritance` / 0428-222, and the candidate commits consistently identify that card.
- `git diff --check refs/remotes/lane-origin/develop...refs/remotes/lane-origin/pr/1749` exited 0. The diff does not touch `contracts/machine/v1/control.golden.json` or `docs/de/reference/cli-machine-coverage.md`.
- Planning repository remote verified before evidence commit. Exact line: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- The product checkout had pre-existing tracked and untracked work. Candidate files were read from fetched remote Git objects; no product file was edited.

## Implementation and test review

- In `internal/corebackup/etcd/etcdctl.go`, the `snapshot save`, `snapshot status`, and endpoint-status child commands now use `pinnedEnv`. `internal/corebackup/etcd/etcdutl.go` uses the helper for isolated restore. `pinnedEnv` removes inherited copies of each pinned key, then appends the pin, so Go's last-value-wins environment de-duplication cannot replace the endpoint or TLS paths.
- The new etcd regression sets opposite inherited values for all six keys (`PATH`, `ETCDCTL_API`, `ETCDCTL_ENDPOINTS`, `ETCDCTL_CACERT`, `ETCDCTL_CERT`, `ETCDCTL_KEY`). `TestChildProcessEnvShowsPinNotInherited` executes stub child processes and verifies the actual received pin values for snapshot save and endpoint status; the restore case checks the `PATH` pin. `TestPinnedEnvDropsInheritedKeys` separately has six key cases over the helper output. This tests the direct process-environment contract without a test-only resolver seam.
- Blocking finding: `internal/coreupdate/dcs_boot_probe.go:60-65` still constructs `cmd.Env` as `append([]string{pins...}, os.Environ()...)`. The inherited parent values therefore occur after the pins and can replace `PATH`, `ETCDCTL_API`, `ETCDCTL_CACERT`, `ETCDCTL_CERT`, or `ETCDCTL_KEY` under Go's last-value-wins de-duplication. The same file's `TestDCSBootProbeInheritsParentEnv` (`internal/coreupdate/child_env_inheritance_0428_222_test.go:20-69`) sets and asserts only `BASEHARBOR_0428_222_SENTINEL`; it does not set conflicting pinned values or assert that the child receives the pin values. It passes with the vulnerable ordering.
- Required correction: use the shared safe filtering helper at the boot-probe call site (export it from the etcd package if needed, or centralize it in an allowed shared package) so it removes every pinned key from `os.Environ()` before appending pins. Extend the coreupdate child-process test to set conflicting parent values for each key pinned at this site, capture the child environment, and assert exactly one entry with each intended pin plus the sentinel. Keep the existing probe response assertions. Stop when the boot-probe child cannot be redirected by inherited endpoint/TLS/API/PATH values and the regression fails if the filter is removed.
- Existing `TestRealEtcdMTLSSnapshotRestoreQuorum` is opt-in via `BASEHARBOR_ETCD_TEST_BIN_DIR`; no native runtime gate was selected in this run. I do not treat that skip as a pass, but a separate native etcd runtime is not required to verify this environment-ordering contract because the unit regression executes real child processes at the `exec.Cmd` boundary and captures their environment. The relevant package test route is the normal non-CLI Go package job.
- Mutation-proof evidence is still required by the task contract for the final corrected head: the test must be shown red when inheritance/filtering is removed, with command, output, and exit code. Historical mutation evidence on earlier heads does not prove the new pin-precedence regression at this head.

## Hosted CI and merge readiness

- Exact-head run `44934281616`, event `pull_request`, head `3df3cb8be6372df630b880d369f3806b0a8fe214`: completed / success. Live job tally: 14 success and 21 skipped; the skips are not counted as passes.
- `PR · Go unit · packages`, job `136937468031`, completed / success. The direct Actions job-logs API returned 33,406 bytes (not zero and below the 49,152-byte oversized threshold). Per-job lines: `ok github.com/mcpdev80/baseharbor/internal/corebackup/etcd 0.455s`, `ok github.com/mcpdev80/baseharbor/internal/coreupdate 0.182s`, and `PASS all non-CLI Go package tests`. The log does not provide a numeric test-case count or per-test PASS line; no such count is inferred here.
- `PR · Selected Runtime` and Targeted HA Docker/Podman jobs were skipped. No runtime-specific gate is needed for the child environment-order assertion; the package job executed both affected packages. Terminal `PR Selected Checks` job `136938796575` completed / success on the same head.
- Live PR state: open, non-draft, base `develop` at the exact SHA above, merge state CLEAN, `reviewDecision` empty, no existing reviews or review requests.

## Verdict

REQUEST CHANGES. The exact head still has a security-relevant pin-ordering defect in `internal/coreupdate/dcs_boot_probe.go:60-65`; the changed boot-probe test proves inheritance of an unrelated sentinel but not that its pinned TLS/API/PATH values resist conflicting parent variables. Change that call site to the shared safe filtering helper, add the adversarial child-env assertions described above, and provide current-head mutation proof. Stop when all five child-process sites use the intended ordering, affected package tests pass in `PR · Go unit · packages` on the exact updated head, and the terminal selected-check result is complete. No product edit, product push, PR update, merge, workflow rerun, or local suite test was performed by this reviewer.

## repo-rule compliance

- Independent review only. No product source or workflow changes, no local suite tests, and no merge or product push.
- Review relied on fetched remote objects and GitHub run/job APIs. Planning edits are limited to this review evidence and the assigned task handoff sentence; unrelated dirty planning files remain untouched.

## cleanliness

- No containers or compose projects were started. `docker ps -a` before review, PID 2459391: container IDs `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`; all were already exited and are unrelated ambient entries. They were not changed.
- `docker ps -a` after review, PID 2483081: the same seven exited ambient IDs were present; no review-owned container or compose project exists.

END codex-rev-1747 BLOCKED: remaining unsafe boot-probe environment ordering at candidate `3df3cb8be6372df630b880d369f3806b0a8fe214`.
