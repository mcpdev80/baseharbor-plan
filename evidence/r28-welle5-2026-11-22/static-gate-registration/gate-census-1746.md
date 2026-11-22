# PR #1746 gate census

## PLAN

1. Read the mission, required policy, and current Planning context for card 0428-235.
2. Refresh the exact develop and PR #1746 refs, then inspect gate catalogs, workflow definitions, and hosted run records.
3. Compare PR #1746 changes with the current native gate catalog and classify the four directive static gates.
4. Publish this evidence to Planning main, update the live board, and post the coordinator handoff.

Role: CODEX-REVIEW, read-only gate-coverage verdict. No product verdict, workflow edit, rerun, merge, close, comment, local test, or subagent action.

verdict: partly without exact-head execution proof (b): the four named static gates remain registered as hosted release-matrix jobs, but PR #1746 run 44997978036 did not execute them; its native matrix was empty, and the changed pre-release workflow source is missing from native source-component selection.

## Gate registration and triggers

Develop was fetched at `acc343239681feb235a33cf00c8ea754c537291f`; PR #1746 head was `e455302f1a89d17d9fae2f532ebb803f479a0994`. The product remote is `https://github.com/mcpdev80/baseharbor.git`.

In `scripts/release-requirements.json`, the four rows `atomic/static/config-matrix` (lines 13-29), `atomic/static/init` (32-48), `atomic/static/mcp` (51-67), and `atomic/static/shell-ux` (89-105) each name `static_gates` in `jobs` and are required for v0.4.22 through v0.4.27. The release planner maps these IDs to its `static` output (`scripts/pre-release-check-plan.py:9, 34-40`).

The hosted job definition is `static_gates`, displayed as `Static · ${{ matrix.gate }}`, with the matrix generated from the selected static IDs (`.github/workflows/pre-release.yml:663-688`). It calls `.github/workflows/pre-release-runtime-suite.yml` with `runtime: static` and the gate ID. The reusable hosted job is named `Executed static · <gate>` (or `Reused static · <gate>`), runs on `ubuntu-latest`, and dispatches the four corresponding test scripts (`.github/workflows/pre-release-runtime-suite.yml:5-8, 264-271`). The parent workflow is triggered by `workflow_dispatch`, pushes to `release-candidate/**`, `release/v*`, or `validation/pre-release/**`, and `workflow_call` (`.github/workflows/pre-release.yml:2124-2160`). It is not directly a `pull_request` workflow.

Remote execution confirms the matrix expands to separate hosted jobs: run `44987381250` was `workflow_dispatch` on `eb2e471a8fdff3233254043782fd805698d9a798` (not the current PR head). Its job records were `Static · init / Executed static · init` failure, `Static · config-matrix / Executed static · config-matrix` failure, `Static · shell-ux / Executed static · shell-ux` failure, and `Static · mcp / Executed static · mcp` failure. This proves the jobs exist and are named; those failures do not prove successful qualification on PR head `e455302...`.

## Historical static-suite failure state

These are failures from run `44987381250` on `eb2e471a8fdff3233254043782fd805698d9a798`, not failures from PR CI run `44997978036` on `e455302...`:

- STATE `Static · init / Executed static · init` (job `137102052110`): `Error` followed by `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- STATE `Static · config-matrix / Executed static · config-matrix` (job `137102052148`): `workload-only: initialization failed:` followed by `authentication_failed` and `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- STATE `Static · shell-ux / Executed static · shell-ux` (job `137102052189`): `Error` followed by `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- STATE `Static · mcp / Executed static · mcp` (job `137102052168`): `RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.perses.disable', 'baseharbor.app.perses.enable', 'baseharbor.app.perses.remove', 'baseharbor.app.perses.status']`.

## PR #1746 exact diff and native matrix

Command `git diff --name-only acc343239681feb235a33cf00c8ea754c537291f...FETCH_HEAD` (where `FETCH_HEAD` was fetched directly from `refs/pull/1746/head`) returned:

```text
.github/workflows/pre-release-runtime-suite.yml
.github/workflows/pre-release.yml
CHANGELOG.md
docs/releases/v0.4.28.demo-ref
scripts/ci-fast-check.sh
scripts/pr-gate-plan.py
scripts/pre-release-check-plan.py
scripts/pre-release-runtime-impact.json
scripts/release-requirements.json
scripts/test_ci_v0427_gate_catalog.py
scripts/test_pre_release_check_plan.py
scripts/test_pre_release_runtime_reuse.py
```

The changed paths do not include a source component mapped to any of the four `atomic/static/{init,config-matrix,shell-ux,mcp}` release gates. Their hosted entries are release-suite selections, not PR-native matrix IDs. The run `44997978036` is GitHub Actions `pull_request`, exact head `e455302...`, and concluded success. Its `PR · Native gate plan` job `137133037853` succeeded, but the job log printed `Native gates selected: false` and the matrix `{"include":[]}`. The dependent `PR · Native · ${{ matrix.id }}` job `137133096184` was skipped. Therefore the PR run did not execute any of the four release static gates. The separate hosted `PR · Validation · ci-executor-tests` job `137133097014` succeeded; it does not substitute for the static release gate run.

## Native matrix coverage finding

There is a distinct source-registration gap on the changed `.github/workflows/pre-release.yml` path. At current develop, `scripts/pr-gate-coverage.json:1356-1359` declares source component `source.workflow.pre.release` with that path and the Docker/Podman coreless-lifecycle surfaces. But `scripts/pr-gate-coverage.json:3130-3157` lists the `native/docker/coreless-lifecycle` and `native/podman/coreless-lifecycle` checks without `source.workflow.pre.release` in either `source_components` list. The trusted resolver selects checks by the changed component ID being present in `source_components` (`scripts/validate-pr-gate-coverage.py:66-90`), not by a matching surface alone. Thus the current catalog associates the changed workflow with coreless surfaces but cannot select those native jobs from that path. The observed empty matrix is not evidence that those paths ran.

The PR run also planned from its lagging base SHA `52a3c5446f41a1dd8678d99875e4cb1eee67874c`, while current develop is `acc343239681feb235a33cf00c8ea754c537291f`. The workflow pins the native planner inputs to `github.event.pull_request.base.sha` (`.github/workflows/ci.yml:485-506`; especially `:495, :501-506`). This matches the existing owner-scope finding already documented in Planning task `tasks/t-20261122-native-plan-self-selection.md` for card 0428-235. Required owner/coordinator finding: reconcile native selection for the changed pre-release workflow path and ensure planning uses the intended current trusted catalog; do not edit `.github/**` or rerun here.

## Run and remote witnesses

- Product `git remote -v`: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- Planning `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1746/head` returned:

```text
acc343239681feb235a33cf00c8ea754c537291f	refs/heads/develop
e455302f1a89d17d9fae2f532ebb803f479a0994	refs/pull/1746/head
```

- PR run `44997978036`: `pull_request`, head `e455302f1a89d17d9fae2f532ebb803f479a0994`, base `52a3c5446f41a1dd8678d99875e4cb1eee67874c`, conclusion `success`; native plan succeeded, native matrix skipped.
- Static suite run `44987381250`: `workflow_dispatch`, head `eb2e471a8fdff3233254043782fd805698d9a798`, conclusion `failure`; all four named static jobs were present, with the statuses recorded above. It is not exact-head success evidence for PR #1746.

## Cleanliness

- `docker ps -a` before review recording, shell PID 3280443: header only; no containers listed.
- `docker ps -a` after review recording, shell PID 3287457: header only; no containers listed. No container or compose command was started.

END_DONE codex-rev2-1736: the four named static gates remain in the hosted release static matrix; PR #1746 did not run them, and its empty native matrix exposes the missing `source.workflow.pre.release` native source mapping plus lagging-base finding. Planning remote is origin https://github.com/mcpdev80/baseharbor-plan.git.
