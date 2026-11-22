# PR 1765 independent review

## PLAN

1. Verify exact PR head, fetched develop base SHA, ancestry, and exact two-file diff.
2. Inspect the selection regression assertion and shared bootstrap-target helper for the registration ordering fix.
3. Verify native Docker and Podman gate runs are terminal green for exact head f4e340eca932ba7bec466bd987e4f1f5235fd305.
4. Write read-only review verdict and required witnesses to this evidence path.
5. Publish evidence on baseharbor-plan origin/main, verify path, and post END.

## Candidate and provenance

- Requested PR: https://github.com/mcpdev80/baseharbor/pull/1765; base `develop`; requested exact candidate `f4e340eca932ba7bec466bd987e4f1f5235fd305`.
- Current PR head observed remotely: `31c6ac1b353a1b26df0dead079ec34e1a85feebe` on branch `codex/0428-209-native-cell-recut`; therefore requested candidate f4e340e is no longer the PR head. This verdict applies only to the requested SHA.
- Product remote `git remote -v` showed `lane-origin` and `origin` both resolve to `https://github.com/mcpdev80/baseharbor.git`; no other remote was used.
- Exact fetched remote develop SHA: `8629450ef3c5198bb675331c12f56b2c9377aa1c` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`). It exactly matches the requested commit's parent.
- `git merge-base --is-ancestor 8629450ef3c5198bb675331c12f56b2c9377aa1c f4e340eca932ba7bec466bd987e4f1f5235fd305` exited 0.
- `git diff --name-only 8629450ef3c5198bb675331c12f56b2c9377aa1c...f4e340eca932ba7bec466bd987e4f1f5235fd305` output:
  - `cmd/baha/control_plane_single_native_ci_test.go`
  - `cmd/baha/runtime_integration_test_support_test.go`
- `git log --oneline 8629450ef3c5198bb675331c12f56b2c9377aa1c..f4e340eca932ba7bec466bd987e4f1f5235fd305` output: `f4e340eca test: register native bootstrap target before selection`.
- The exact diff does not touch `cmd/baha/app_broker.go`, `internal/controlplaneruntime/**`, or `scripts/**`.

## Review findings

- `cmd/baha/runtime_integration_test_support_test.go:945-954` calls `runWithIOAsTestOperator` to create the new Target, then selects it with `os.Setenv` only after registration succeeds.
- However, `TestRuntimeIntegrationBootstrapTargetSelectsAfterCreate` at `cmd/baha/runtime_integration_test_support_test.go:957-973` sets `BASEHARBOR_TARGET` to the not-yet-registered target at line 961 before invoking the helper. In this exact candidate, the helper does not clear that selection before `target create`.
- `runWithIOAsTestOperator` at `cmd/baha/test_operator_context_test.go:18-20` only adds the test operator context and delegates to `runWithIO`; it does not clear `BASEHARBOR_TARGET`. Thus target creation's authorization preflight still resolves the unregistered name. The prior failure mode is not fixed by the requested SHA, and the regression assertion will encounter the same pre-registration selection condition.
- Verdict: REQUEST CHANGES for exact candidate f4e340eca932ba7bec466bd987e4f1f5235fd305.
- PR #1765 is intended to replace stale-base PR #1740. No close or other PR mutation was performed; #1740 remains open.

## Native gate evidence

- Exact-head run 45018784058 (`CI · Source & Quality`, event `pull_request`) targeted `f4e340eca932ba7bec466bd987e4f1f5235fd305` and is terminal `completed`, conclusion `cancelled` (updated 2026-11-22T11:48:08Z).
- `PR · Native · native/docker/guided` job 137196885733: `completed/cancelled`.
- `PR · Native · native/podman/guided` job 137196885744: `completed/cancelled`.
- Other native Docker and Podman jobs in this run (`data-capabilities`, `coreless-lifecycle`) were also cancelled. No required native Docker or Podman gate is terminal green; skipped or cancelled is not a pass.
- The exact requested candidate was superseded as the PR head before this review completed. No other head is approved by this review.

## Repo-rule compliance

- Read-only review; no product edits, test runs, PR comments, merge/close actions, or workflow reruns/dispatches.
- Current product checkout contained unrelated modified files and an untracked worktree. It was not changed or cleaned. Candidate source was read from its exact commit object and GitHub records.
- Planning remote first line observed: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## cleanliness

- Before review, `docker ps -a` under shell PID 4015113 showed only the header and no containers.
- After review, `docker ps -a` under shell PID 4017808 showed only the header and no containers; no containers were started.
- `python3 scripts/plan.py check`: 682 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing warnings.
- `git diff --check` reported trailing whitespace in the unrelated, pre-existing modified `tasks/t-20261122-footprint-show-not-admitted-in-data-capabilities-gate.md` at lines 28 and 38. That task file and other pre-existing Planning changes were left untouched and unstaged.

## Verdict

REQUEST CHANGES — the exact requested candidate still preselects an unregistered target during registration; the native Docker and Podman gates are cancelled, not green. The current PR head is newer and requires a separate exact-head review.

END codex-rev2-1736 DONE: REQUEST CHANGES for requested candidate f4e340eca932ba7bec466bd987e4f1f5235fd305; current PR head 31c6ac1b353a1b26df0dead079ec34e1a85feebe is not approved.

## publication witness

- Exact `git ls-tree -r --name-only origin/main | grep` output after fetching origin/main: `evidence/r28-welle5-2026-11-22/native-cell-operator-0428-209/review-1765-headf4e340e.md`
