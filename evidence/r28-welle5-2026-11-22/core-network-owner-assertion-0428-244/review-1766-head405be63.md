# PR 1766 independent review

## PLAN

1. Resolve PR 1766 exact head and fetch the current develop base SHA; verify ancestry and the exact changed-file list.
2. Inspect the test assertion to confirm unowned native networks remain rejected and not adopted as external.
3. Verify native Keycloak/Core Docker job 137197826981 and Podman job 137197826980 on the exact candidate.
4. Verify the merge sequence constraint and write the independent review evidence.
5. Publish evidence on baseharbor-plan origin/main, verify its path, and post END.

## Candidate and provenance

- Role: CODEX-REVIEW, read-only and independent.
- PR #1766: https://github.com/mcpdev80/baseharbor/pull/1766; state OPEN; branch `codex/core-network-owner-diagnostic-test`.
- Exact PR head: `405be63ff01061cdb3d5eeb0562ef441d6b89e6e`; base `develop`.
- Product remote `git remote -v` showed `lane-origin` and `origin` both resolve to `https://github.com/mcpdev80/baseharbor.git`; only the resolved GitHub URL was used.
- Fetched remote develop SHA: `8629450ef3c5198bb675331c12f56b2c9377aa1c` from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`; this equals the exact candidate's parent.
- `git merge-base --is-ancestor 8629450ef3c5198bb675331c12f56b2c9377aa1c 405be63ff01061cdb3d5eeb0562ef441d6b89e6e` exited 0.
- `git diff --name-only 8629450ef3c5198bb675331c12f56b2c9377aa1c...405be63ff01061cdb3d5eeb0562ef441d6b89e6e` output: `cmd/baha/operator_core_network_binding_native_test.go`.
- The exact diff changes one test assertion only; it does not touch product implementation, `cmd/baha/app_broker.go`, `.github/**`, or other files under `cmd/baha`.
- `git log --oneline 8629450ef3c5198bb675331c12f56b2c9377aa1c..405be63ff01061cdb3d5eeb0562ef441d6b89e6e` output: `405be63ff test: match protected owner diagnostic after core guard fix`.

## Assertion review

- At `cmd/baha/operator_core_network_binding_native_test.go:78`, the assertion still fails when `err == nil`, and now checks for `no verifiable protected Core or shared backend owner`.
- The exact candidate's production diagnostic at `cmd/baha/core_network_binding.go:71` and `:73` contains that phrase. The changed phrase therefore matches the current valid product diagnostic.
- The follow-up assertion at lines 88-89 remains unchanged: if `bound.DefaultNetworkExternal` is true, the test fails with `unowned native network must not be adopted as external`.
- The rejection requirement is not weakened. Content review passes.

## Exact-head CI evidence

- Exact-head PR run 45019617600 (`CI · Source & Quality`, event `pull_request`) targets `405be63ff01061cdb3d5eeb0562ef441d6b89e6e`. At observation it was `queued`; its native Keycloak/Core Docker job 137199976796 was `queued`, and native Keycloak/Core Podman job 137199976774 was `in_progress`.
- The mission-specified job IDs 137197826981 (Docker) and 137197826980 (Podman) are from run 45018856573 on head `31c6ac1b353a1b26df0dead079ec34e1a85feebe`, not this candidate; both concluded `failure`. They are not valid exact-head evidence for PR #1766.
- No exact-head native Docker or Podman job was terminal green at observation. Queued, in-progress, skipped, or wrong-head results do not pass. Review verdict: PENDING.

## Merge sequence

- PR #1765 remains OPEN at head `31c6ac1b353a1b26df0dead079ec34e1a85feebe`; PR #1766 remains OPEN at the requested head. Neither is merged.
- No merge, close, comment, or rerun was performed. The required sequence remains: merge #1766 first, then rerun and merge #1765, whose native jobs depend on this assertion correction. This sequence has not yet completed and is not represented as completed here.

## Repo-rule compliance

- Read-only review; no product files were edited and no local tests, workflow reruns, or workflow_dispatch were run.
- Planning remote first line observed: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## cleanliness

- Before review, `docker ps -a` under shell PID 4053539 showed only the header and no containers.
- After review, `docker ps -a` under shell PID 4055511 showed only the header and no containers; no containers were started.
- `python3 scripts/plan.py check`: 683 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings.

## Verdict

PENDING — the assertion correction is sound, but exact-head native Docker is queued and native Podman is in progress. The mission-specified failed jobs belong to another head, and the required merge sequence is not complete.

END codex-rev2-1736 DONE: PENDING for exact head 405be63ff01061cdb3d5eeb0562ef441d6b89e6e; merge #1766 before rerunning #1765.
