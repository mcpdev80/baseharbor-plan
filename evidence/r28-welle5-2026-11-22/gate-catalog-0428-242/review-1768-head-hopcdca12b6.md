# PR 1768 independent review

## PLAN

1. Resolve PR 1768 exact head and develop base SHA; verify ancestry and exact file list.
2. Inspect guardian behavior for uncatalogued product sources versus ci-executor scripts.
3. Verify the catalog routes scripts/ci-native-pr-gate.sh so a later develop candidate runs the 237-native matrix.
4. Verify four required exact-head CI jobs are terminal green and record the verdict.
5. Publish review evidence on baseharbor-plan origin/main, verify its path, and post END.

## Candidate, base, and file scope

- Role: CODEX-REVIEW, read-only and independent.
- PR #1768: https://github.com/mcpdev80/baseharbor/pull/1768; state OPEN, ready (not draft), merge state BEHIND; branch `lane-0428-242-catalog-guardian`.
- Exact remote PR head: `0331ec6f764aba62a293d4f740791bc063155a2d` (`refs/pull/1768/head`).
- Current remote develop SHA: `cdca12b6e87940d50dc1652ee47d01cd0b85c7e1` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- The requested ancestry check `git merge-base --is-ancestor cdca12b6e87940d50dc1652ee47d01cd0b85c7e1 0331ec6f764aba62a293d4f740791bc063155a2d` exited 1. GitHub compare reports base `cdca12b6e87940d50dc1652ee47d01cd0b85c7e1`, merge base `64eab13e23fba8bca07a1d68c687fa36afedb64e`, status `diverged`, ahead_by 3. Thus current develop is not an ancestor of this PR head; the PR is behind the current base.
- GitHub compare file list for exact develop...head:
  - `scripts/pr-gate-coverage.json`
  - `scripts/pr-gate-plan.py`
  - `scripts/test_ci_v0427_gate_catalog.py`
  - `scripts/test_pr_ci_fallback.py`
  - `scripts/test_pr_gate_coverage.py`
  - `scripts/test_pr_gate_plan.py`
  - `scripts/validate-pr-gate-coverage.py`
- The changed paths are all scripts/catalog/planner/guardian tests. No product behavior, `cmd/baha/app_broker.go` implementation, operatorauth guard, or `.github/**` file is changed. The exact PR head's own commits are `41343f638`, `23844ecdb`, and `0331ec6f7` (three commits ahead of the shared base); the `git log` range from current develop cannot be a valid current-base provenance proof because that base is not an ancestor.

## Guardian and catalog review

- `scripts/test_pr_ci_fallback.py:119-128` tests fail-loud behavior: an uncatalogued `internal/newarea/feature.go` raises `ValueError`, includes the path, and does not produce a fallback.
- `scripts/pr-gate-plan.py:1690-1698` classifies `scripts/ci-*` as `ci-executor` and requires `CI_CHECKS`; it does not route these executor scripts through unknown-product abort handling.
- `scripts/pr-gate-coverage.json:165-171` catalogs `cmd/baha/app_broker.go` as `source.cmd.baha.app.broker.go` and maps it to both `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`. `scripts/test_pr_ci_fallback.py:135-145` verifies a cataloged `app_broker.go` source resolves and selects the data-capabilities gate. This is the catalog line that routes the 0428-237 source to Docker and Podman data-capabilities gates on a later develop-based candidate.
- `scripts/test_pr_ci_fallback.py:281-287` verifies the native selected job consumes `pr_native_impact`'s matrix and invokes `scripts/ci-native-pr-gate.sh`. The executor script is covered by the generic `scripts/ci-*` planner branch above; there is no literal `scripts/ci-native-pr-gate.sh` row in the JSON catalog.
- The current catalog's OpenBao entries use `internal/openbao/bootstrap_auth.go` at line 949 and related files; this candidate does not change `internal/openbao/bootstrap.go`.

## Exact-head hosted check states

- Run 45025980169 (`CI · Source & Quality`, `pull_request`) targeted exact head `0331ec6f764aba62a293d4f740791bc063155a2d`; terminal status `completed`, conclusion `success`.
- `PR · Native Keycloak/Core · ${{ matrix.runtime }}` job 137219051753: `completed/skipped`. No Docker or Podman child gate job ran; skipped is not green and fails the mission's explicit native-matrix requirement.
- `PR · Validation · ci-executor-tests` job 137219049781: `completed/success`.
- `PR · Validation · pr-planner-tests` job 137219049736: `completed/success`.
- `PR Selected Checks` job 137219406760: `completed/success`.
- Although the aggregate is green, the required Docker and Podman native checks were skipped, so this is not full exact-head evidence for the specified acceptance.

## Verdict

REQUEST CHANGES — current develop `cdca12b6…` is not an ancestor of the candidate, and the exact-head native Keycloak/Core matrix was skipped rather than running Docker and Podman gates. The guardian behavior and the `app_broker.go` catalog route are present, but they do not clear those blockers.

## Repo-rule compliance

- Read-only review. No product edits, local tests, PR comments, merge/close actions, or workflow reruns/dispatches were performed.
- Planning remote first line observed: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `python3 scripts/plan.py check`: 684 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 11 warnings. Warnings concern existing accepted tasks with unaccepted dependencies and one active task with an unaccepted dependency.

## cleanliness

- Before review, `docker ps -a` under shell PID 128631 showed only the header and no containers.
- After review, `docker ps -a` under shell PID 137380 showed only the header and no containers; no containers were started.

END codex-rev2-1736 DONE: REQUEST CHANGES for PR 1768 head 0331ec6f764aba62a293d4f740791bc063155a2d; current develop is not an ancestor and native Docker/Podman jobs were skipped.
