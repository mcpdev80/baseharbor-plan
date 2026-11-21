ROLE: REVIEW

## PLAN

1. Read the rev-1585 mission and record the numbered review plan. Done.
2. Verify authority, task contract, exact candidate, base, and remote state. Done.
3. Inspect implementation, regression, CI job evidence, and merge readiness. Done.
4. Record findings and verdict in this evidence file and the task handoff. Done.
5. Publish evidence, verify origin/main, update the board, and post END. In progress.

## Candidate and scope

- PR #1585, branch `lane-0428-fix-bf01-v2`, current head `70d39070f4ad2618b120e7a5438fdff7ed94f665`.
- Exact base: `develop` at `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`. `git merge-base --is-ancestor refs/remotes/lane-origin/develop refs/remotes/lane-origin/pr/1585` exited 0.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-fix-bf01-v2 refs/pull/1585/head refs/heads/develop` returned:

  ```
  e6c199e7b7dd7d076a776d11c3ba16f25e59c254 refs/heads/develop
  70d39070f4ad2618b120e7a5438fdff7ed94f665 refs/heads/lane-0428-fix-bf01-v2
  70d39070f4ad2618b120e7a5438fdff7ed94f665 refs/pull/1585/head
  ```

- `git diff --name-status refs/remotes/lane-origin/develop...refs/remotes/lane-origin/pr/1585` lists exactly these six BF-01 files:

  ```
  M cmd/baha/target.go
  M cmd/baha/target_selection.go
  A cmd/baha/target_selection_state_dir_isolation_test.go
  A cmd/baha/target_state_layout.go
  M internal/deployment/target.go
  M internal/orgconfig/store.go
  ```

- The required history command, `git log --oneline refs/remotes/lane-origin/develop..refs/remotes/lane-origin/pr/1585`, includes commit `55a8c0f3550d9cb5638a6223f3c8cbad314c48e6`, authored by `w091-0428-091 <w091@baseharbor.local>`, message `Merge remote-tracking branch 'origin/develop' into sync-indep-bf01v2`. This foreign-authored commit is in the base-to-head history. It violates the own-commits-only provenance requirement even though the final file diff is limited to the six BF-01 files. The PR history must be cleaned before acceptance.
- The planning repository remote was verified before evidence commit. Exact remote line: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- The product checkout had pre-existing tracked and untracked work. It was not edited; candidate content was inspected read-only from fetched remote objects.

## Implementation review

- `cmd/baha/target_selection.go` routes persisted selection through `deployment.TargetSelectionRoot()`. `internal/deployment/target.go` puts the selection under `<BASEHARBOR_STATE_DIR>/config` when the override is set, while preserving XDG and user-home behavior otherwise. The flag surface is unchanged.
- `cmd/baha/target_state_layout.go` implements the production state-root resolver: root-local activation first, then organization state owned by the root, then root-local fallback; stale activation returns a not-found error, and foreign organization defaults cannot select a target outside the root.
- The 239-line `TestStateDirIsolatesTargetSelection` uses real temp directories, writes registrations through `deployment.Config.Save`, stores organization state in the production layout, and calls `effectiveTarget`. It covers A/B isolation, root-local organization selection, and an A activation under B. It does not inject the resolver or replace the production paths with a special test seam.
- Negative direction: the implementation returns `activated target "…" no longer exists` for a persisted target absent from the selected root, rather than falling back. The regression asserts that the missing-target case returns an error, though it does not assert the error text itself.
- The hunt evidence documents the original H-D28 observation and the limitation that the state-root switch could not be validly tested in that hunt. The new regression establishes the behavior contract rather than replaying the original machine-specific symptom. Treat the Owner's stated assumption that this behavior test closes the gap as a merge condition.
- The diff does not touch `contracts/machine/v1/control.golden.json` or `docs/de/reference/cli-machine-coverage.md`; no surface text changed.
- `git diff --check refs/remotes/lane-origin/develop...refs/remotes/lane-origin/pr/1585` completed with exit 0.

## CI and PR state

- Exact-head hosted run `44933797592`, event `pull_request`, head `70d39070f4ad2618b120e7a5438fdff7ed94f665`: completed / success. Required CLI shard job `136936005480` (`PR · Go unit · cli-2`) completed / success. Its per-job log was 44,210 bytes and contained `PASS cli-2: 449 passed / 20 intentionally skipped / 469 discovered; CLI inventory total=1823`.
- The selector in `scripts/pr-go-unit-shard.py:72` uses SHA-256 of the test name and modulo four. `TestStateDirIsolatesTargetSelection` hashes to shard 2, so it is selected in cli-2; the successful per-job summary supplies the passing execution count. This is the per-job evidence, not the aggregate alone.
- Selected Docker lifecycle job `136936377258` completed / success. Terminal `PR Selected Checks` job `136938248298` completed / success. The observed run is exact-head; no skipped job is being represented as a pass.
- Live PR state at review: open, non-draft, base `develop` at `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`, mergeable / CLEAN, no review requests and no existing reviews.

## Verdict

REQUEST CHANGES for candidate provenance. The implementation and behavioral evidence are acceptable subject to the Owner's assumption above, but this exact head cannot be accepted while the base-to-head log contains the foreign-authored merge commit `55a8c0f`. The task owner should rebuild the named candidate from the exact current `develop` head and replay only task-owned BF-01 commits, preserving the six-file product diff; rerun the existing CLI shard and required checks on the resulting exact head. Stop when the base-to-head log contains only task-owned commits and the exact-head selected checks are terminal-success. No product change, push, merge, CI rerun, or approval was performed by this reviewer.

## repo-rule compliance

- Independent review only. No product edits, no local suite tests, no workflow or scripts changes, no PR update, merge, or product push.
- Planning changes are limited to the task's handoff note and this evidence file; no unrelated dirty planning files were staged.

## cleanliness

- No containers or compose projects were started. No Docker state was changed by this review.

END codex-rev-1747 BLOCKED: provenance finding blocks acceptance at candidate `70d39070f4ad2618b120e7a5438fdff7ed94f665`.
