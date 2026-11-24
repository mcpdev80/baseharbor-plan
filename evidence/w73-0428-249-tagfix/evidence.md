# w73-0428-249-tagfix — baha-ci-operator-testonly artifact tag fix (PR #1825)

## PLAN

- Read mission, set up isolated worktree, resolve remotes to the GitHub URL (github.com/mcpdev80 only).
- Fetch develop, record base SHA, attest branch provenance.
- Edit `.github/workflows/pre-release.yml` only: add `-tags=baseharbor_ci_operator_testonly` to the testonly artifact build + a strict `go version -m` build-settings tag proof; normal `baha` build byte-unchanged.
- Commit, push lane branch, open one PR against develop; mark ready so PR CI executes.
- Monitor exact-head Hosted PR CI to terminal and record every job outcome.
- Monitor the owner-dispatched pre-release artifact run on the exact head; capture the `go version -m` tag proof.
- Persist this evidence on baseharbor-plan origin/main and post END.

## Remote resolution (first git action)

Shared checkout shows `origin https://github.com/mcpdev80/baseharbor.git` (plus `lane-origin`/`upstream` same URL). HTTPS push of the workflow file was rejected by GitHub (OAuth App lacks `workflow` scope), so delivery used the SSH form of the same repository: `ssh://git@github.com/mcpdev80/baseharbor.git`. No push/fetch ever went through a non-github.com/mcpdev80 remote.

## Planning repo verification

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)` (verified before first evidence commit).

## Base attestation and provenance

- Base: develop. `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`.
- Branch `lane-0428-249-tagfix` cut from exactly that SHA (worktree creation line: `HEAD is now at 2b9a2c6d1`).
- `git merge-base --is-ancestor 2b9a2c6d1611ea85e11bf81e9650c28165c8293a HEAD` -> OK.
- `git log --oneline origin/develop..HEAD` -> only lane commits:
  - `844987ded fix(ci): replace symbol-table proof with strict go version -m build-settings proof`
  - `dd7fd9056 fix(ci): build baha-ci-operator-testonly artifact with its build tag in pre-release.yml`
- `git diff origin/develop...HEAD --name-only` -> `.github/workflows/pre-release.yml` (only file; `gh pr diff 1825 --name-only` on GitHub agrees). ci.yml untouched; no scripts/pr-gate-coverage.json change.

## Candidate

PR: https://github.com/mcpdev80/baseharbor/pull/1825 (base develop, non-draft). Final head: `844987ded88b1c365f5b660e3f700af69e52bb5a`.
ls-remote witness after push: `844987ded88b1c365f5b660e3f700af69e52bb5a refs/heads/lane-0428-249-tagfix`.

One-usable-line pre-release.yml diff (testonly build):

```
+ CGO_ENABLED=0 go build -trimpath -tags=baseharbor_ci_operator_testonly -ldflags="-s -w -X main.version=... -X main.commit=... -X main.date=unknown" -o "$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly" ./cmd/baha
```

Plus the build-info proof added in the same step (full `go version -m` output logged; strict grep of the `build` settings line for `-tags=baseharbor_ci_operator_testonly`, fails closed). The normal `Build exact candidate binary` step is byte-unchanged (diff shows only the testonly command line and appended proof lines).

## Review round 1 (Codex findings, applied)

- `go tool nm` proof removed: candidate build uses `-ldflags "-s -w"`; `-s` strips the symbol table, so nm can never see symbols (verified from the CI log of run 45391485905's sibling job). Replaced with `go version -m` build-settings proof, which embeds `-tags` regardless of `-s -w`.
- PR flipped from draft to ready so the PR pipeline executes jobs (draft-only matrix was cancelling/skipping the real runs).

## Hosted CI witnesses (exact head 844987ded)

### PR CI run 45391485905 (CI · Source & Quality, pull_request) — completed, success

All executed jobs passed (93 total):

- Workflow policy: success
- PR · Trusted Plan: success
- PR · Native gate plan: success
- PR · Source format: success
- PR · Validation · ci-actionlint: success
- PR · Validation · ci-executor-tests: success
- PR · Validation · ci-policy: success
- PR · Validation · pr-planner-tests: success
- PR · Validation · receipt-execution-tests: success
- PR · Focused Python: success
- PR · Demo Pin: success
- PR · Consumer Pins: skipped (as planned: no consumer pin changes)
- PR · Candidate-added checks (advisory): success
- PR · Exact Candidate: skipped (PR CI does not run the pre-release artifact job)
- PR · Exact full Pre-Release: skipped (requires base main + release/* head)
- PR · Selected Core-less · docker · integration/docker/coreless-lifecycle: success
- PR · Selected Core-less · docker · application / core-capability / foundation / identity-backend: all success
- PR · Selected Core-less · podman · integration/podman/coreless-lifecycle: success
- PR · Selected Core-less · podman · application / core-capability / foundation / identity-backend: all success
- PR Selected Checks (aggregate): success

Stale superseded head runs (45390508094 draft-cancelled, 45390546319 cancelled after owner directive) were terminated; delivery of the cancelled state witnessed via `gh run view 45390546319 -> completed cancelled`.

### Pre-release artifact run 45394505629 (workflow_dispatch, owner-triggered, head 844987ded) — completed, failure

Job `Release · Candidate Artifact` (id 138447102162): **success**.
Step `Produce baha-ci-operator-testonly candidate binary` passed and emitted the tag proof from the artifact's own build info:

```
/home/runner/work/_temp/pre-release-candidate/baha-ci-operator-testonly: go1.26.9
	path	github.com/mcpdev80/baseharbor/cmd/baha
	build	-tags=baseharbor_ci_operator_testonly
	build	-trimpath=true
	build	CGO_ENABLED=0
	build	GOOS=linux
	build	GOARCH=amd64
```

The strict gate inside the step (`grep -E '^\s*build\s' ... | grep -q -- '-tags=baseharbor_ci_operator_testonly'`) ran on the real artifact and passed; an untagged binary fails it (logic verified with a fixture in this lane, string-level only).

Run-level failure is NOT from this card's change: job `Static · mcp / Executed static · mcp` (138450101757) failed at "Run static gate" with

```
RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.pull']
```

and `Pre-Release Checks` then asserts source results. The dispatch inputs (tag v0.4.28, demo_ref c23bd9ac, only_gates atomic/static/mcp + atomic/static/ci-fast-check) were outside this lane's write-set; the mismatch concerns the MCP contract surface, not the artifact build. `atomic/static/ci-fast-check` gate: success. Finding reported to coordinator; per CI policy I did not trigger further workflow_dispatch runs (owner action).

## cleanliness

- No containers, compose projects, VMs or networks were started by this lane (host policy: no local builds/tests; CI/artifact scope verified only via Hosted CI). `docker ps -a` untouched ambient stack belongs to other lanes; nothing to tear down for this lane.
- Worktree: workers/0428-249-tagfix-wt (persistent zone), left intact for the correction round until merge.

## repo-rule compliance

- Write-set honored: only `.github/workflows/pre-release.yml` in the product repo; this evidence only in baseharbor-plan.
- One branch, one PR per chain; no second candidate branch.
- No local product tests executed; verification exclusively via exact-head Hosted CI (PR run 45391485905) and the owner-dispatched artifact run 45394505629.
- No subagents used.
- actionlint run on the changed workflow file only (formatting check, not a product test suite) plus `gh pr diff --name-only` scope witness.

END_DONE w73-0428-249-tagfix: candidate 844987ded on PR #1825; PR CI run 45391485905 green; artifact tag proof observed in run 45394505629 job 138447102162 ('build -tags=baseharbor_ci_operator_testonly'); dispatch run's only red is the unrelated MCP static gate (finding).
