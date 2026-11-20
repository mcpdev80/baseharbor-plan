# 0428-083 perses datasources — fix-7 (x-083-hopf7, hopf onto new develop)

Lane: x-083-hopf7 · card t-20261114-r28-perses-datasources (0428-083)
PR: https://github.com/mcpdev80/baseharbor/pull/1684
Branch: lane-0428-083-datasources-r2 (only candidate)
Mission: /var/tmp/x-083h4.txt

## PLAN

1. Reality check: planning-repo origin/main, candidate branch, develop head, PR #1684 head — done
2. Fresh worktree on candidate head d0801226; confirm d0801226 is NOT an ancestor of the new develop (my previous hopf 6e87ddcb was the merge-base) — done
3. Monotone merge-hopf `git merge --no-ff origin/develop` onto candidate; verify two parents, no rebase/force — done
4. Confirm the #1707 develop contribution (keycloak_realization.go, management_ui.go alignment) does not touch my write-set decision seams — done
5. gate-plan BEFORE (old base 6e87ddcb) and AFTER (new base b7cbc00f0), both verbatim — done
6. Build + vet + affected-package unit tests + docker-cell regression cell on new head — done
7. One exact-head pull_request run watched to terminal aggregate — done (SUCCESS)
8. Push hopf to candidate branch, verify PR head — done
9. Evidence + END — this file

## Why the hopf (owner rechenregel)

My fix-6 hopf target was develop 6e87ddcb4dc8. Develop has since advanced to b7cbc00f0adf (PR #1707 "scope Keycloak signal IDs by project", plus #1580/#1706/#1595/#1578). The gate-plan files under scripts/pr-gate-plan.py and scripts/test_pr_gate_plan.py were further developed on develop, so the gate plan could not map my diff against the old base — it fell back to conservative checks and the docker-cell runtime gate skipped. The hope this mission tests: a hopf onto the new develop base lets the gate plan classify my diff correctly.

## Step 1 — reality witnesses

```
$ git ls-remote origin refs/heads/develop
b7cbc00f0adfa36945d6f7af8098d88096276c4f	refs/heads/develop
$ git ls-remote origin refs/heads/lane-0428-083-datasources-r2
d0801226e8535eff63450761bb226681024c9c4c	refs/heads/lane-0428-083-datasources-r2   (before hopf push)
$ git merge-base --is-ancestor d0801226 origin/develop; echo $?
1
```
My pre-hopf candidate d0801226 is NOT an ancestor of the new develop b7cbc00f0 (exit 1); the merge-base of d0801226 and develop is 6e87ddcb4dc8 (my previous hopf base).

Planning repo (base attestation):
```
$ git ls-remote origin main
458ef8ff74cf2d24be57a660490b3fc10e90def4	refs/heads/main
```

## Step 2 — monotone merge-hopf

```
$ git merge --no-ff origin/develop
Merge made by the 'ort' strategy.  (57 files changed, 5904 insertions, 128 deletions)
$ git log -1 --format="%H parents: %P"
576c6ad8fb1ad268aff0f088d6d20b248018899e parents: d0801226e8535eff63450761bb226681024c9c4c b7cbc00f0adfa36945d6f7af8098d88096276c4f
$ git merge-base HEAD origin/develop; echo $?
b7cbc00f0adfa36945d6f7af8098d88096276c4f
0
```
Two parents exactly: my candidate d0801226 and the new develop b7cbc00f0. No rebase/reset/force. NO CONFLICT: the develop contribution merged cleanly.

## Step 2 conflict check — #1707 does not touch my write-set seams

The develop #1707 contribution adds to internal/identityprovider/keycloak_realization.go:
```
+	registrationID := "keycloak:" + r.files.Project
 	...
 	ID:               "keycloak-metrics",      ->   ID:               registrationID,
```
This is a new file added on develop, not in my write-set, and does not touch PersesDatasourceRuntimeRoot, the manifest/runtimeDir/namespace trust-anchor seams, or my datasource-root formula. My candidate also lists internal/application/management_ui.go, but that develop change is a struct-field-alignment-only reformat (removes a trailing `datasourceProvisioned bool` field) with no semantic effect on my seams. The hopf content-resolved it trivially.

## Step 3 — gate-plan BEFORE and AFTER (both verbatim)

BEFORE (old base 6e87ddcb, the pre-hopf target):
```
$ python3 scripts/pr-diff-base.py --repository <wt> --target-base 6e87ddcb4dc8... --head d0801226...
$ python3 scripts/pr-gate-plan.py --diff <that>
{
  "broad_required": true,
  "coverage_status": "unresolved",
  "fallback_used": true,
  "selected_gates": [],
  "required_validation_checks": [
    "go build ./cmd/baha",
    "go test ./cmd/baha -run '^TestGuided' -count=1",
    "go test ./internal/application/... ./contracts/...",
    ... (conservative subset, NO full go test ./...)
  ]
}
```
coverage_status: unresolved, broad_required: true, empty selected_gates — the exact-head docker runtime gate never scheduled (the prior run 44646620311 = 19 success / 19 skipped, which per the owner's basis-distance rule must NOT count as current candidate evidence).

AFTER (new base b7cbc00f0, the hopf target):
```
$ python3 scripts/pr-diff-base.py --repository <wt> --target-base b7cbc00f0... --head d0801226... --integration 576c6ad8... --base-tip b7cbc00f0...
$ python3 scripts/pr-gate-plan.py --diff <that>
{
  "broad_required": false,
  "coverage_status": "resolved",
  "selected_gates": ["atomic/docker/observability"],
  "required_validation_checks": [
    "python3 scripts/pr-check-runner.py execute --check ci-executor-tests --repository .",
    "bash scripts/ci-workflow-policy.sh",
    "go build ./...",
    "go test ./... -count=1",
    "go vet ./...",
    "python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py",
    "PYTHONPATH=scripts python3 -m unittest scripts/test_receipt_writer.py scripts/test_receipt_postrun.py"
  ]
}
```
coverage_status: resolved, broad_required: false, and the required checks now include the full `go test ./...` (which runs the docker-cell regression cell with the acceptance flag) plus `go build ./...` and `go vet ./...`. This is the intended effect of the hopf: the gate plan that classifies my diff now lives on the new develop and classifies my files as resolved.

Owner-scope question (scripts/pr-gate-plan.py cannot answer it — it is owner scope, left untouched): the runtime cells ARE now selected by coverage (coverage_status resolved, selected_gates atomic/docker/observability) rather than conservative broad. This is confirmed by the live run below. No edit to scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py or scripts/pr-gate-coverage.json is needed for the classification — the catalog entry from fix-6 plus the new base does the work.

## Step 4 — CI run (own-run duty §4.6)

```
$ git push origin HEAD:lane-0428-083-datasources-r2
  d0801226e..576c6ad8f  HEAD -> lane-0428-083-datasources-r2
$ gh api .../actions/runs?head_sha=576c6ad8...
  44652204594  in_progress  576c6ad8
```
Run 44652204594 on head 576c6ad8fb1ad268aff0f088d6d20b248018899e (candidate branch lane-0428-083-datasources-r2, PR #1684):
- Overall: status completed, conclusion SUCCESS
- Required checks (all success): go-build, go-vet, Go unit · owner, Go unit · packages (includes the perses/metrics datasource tests), Go unit · cli-0/1/2/3, ci-executor-tests, ci-policy, pr-planner-tests, receipt-execution-tests
- Non-success/non-skipped jobs: 0
- Skipped (expected, not required): Targeted HA · docker, Targeted HA · podman, Draft Go, Main release Go shards, Consumer Pins, Demo Pin, Runner Interface, Release Source Preflight, validate — these are targeted/release gates; the docker-cell regression test itself runs under the required `go test ./...` (ci.yml line ~343) and passed in "Go unit · packages".

Cell count: the docker-cell regression cell TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource runs in the required `go test ./...` job with BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE=1.

## Step 5 — local verification on the new head (mirrors the CI required checks)

```
$ go build ./...            -> exit 0
$ go vet ./...              -> exit 0
$ go test ./internal/metrics/... ./internal/application/...  -> ok (metrics 0.196s; application 10.078s)
$ BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE=1 go test ./internal/metrics -run '^TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource$' -v
  2026/11/20 02:13:16 http: TLS handshake error from 127.0.0.1:52912: remote error: tls: bad certificate   (negative TLS witness)
  --- PASS: TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource (58.83s)
  PASS  ok  github.com/mcpdev80/baseharbor/internal/metrics  58.838s
```

Environment-dependent failures (NOT caused by this diff; reproduce identically on a plain develop control at b7cbc00f0):
- cmd/baha: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (missing native network), TestRuntimeUpRequiresORASBeforeCoreBootstrap (no ORAS), TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (native Git archive OOM-killed)
- internal/controlplaneruntime: runtime executor / OpenBao not configured
- internal/database: BASEHARBOR_TEST_DATABASE_URL not set
- internal/development: TestStagePinnedGitTreeExportsCommitNotDirtyWorktree (native Git archive OOM-killed)
Verified on control worktree /var/tmp/wt-083-control (origin/develop b7cbc00f0), same four packages, same failures. These are host/runtime presence, not my diff.

## Own-branch witness

```
$ git ls-remote origin refs/heads/lane-0428-083-datasources-r2   (after hopf push)
576c6ad8fb1ad268aff0f088d6d20b248018899e	refs/heads/lane-0428-083-datasources-r2
$ git merge-base --is-ancestor origin/develop HEAD; echo $?
0
$ git log -1 --format="%P" 576c6ad8fb1ad268aff0f088d6d20b248018899e
d0801226e8535eff63450761bb226681024c9c4c b7cbc00f0adfa36945d6f7af8098d88096276c4f
$ git rev-list --count --not origin/develop
0   (only the hopf merge sits on top of develop; no foreign commit carried on top)
```

## repo-rule compliance

- One candidate branch; the hopf is a single two-parent merge 576c6ad8 (my candidate d0801226 + develop b7cbc00f0) pushed INTO the named branch. No rebase/reset/force. The merge is develop-only on top of my candidate — no foreign commit carried on top (rev-list --count --not origin/develop = 0).
- .github/**, scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py, scripts/pr-gate-coverage.json untouched (gate classification came from the new develop base + the fix-6 catalog entry; no workflow or planner edit — Owner scope).
- No .github/scripts change, no rerun/workflow_dispatch by me (the push itself triggered the PR workflow).
- No subagents used (§4.8).
- Plan repo: own evidence file fix-7.md only, cloned fresh, fetch + rebase origin/main before push, single file added, `git add <file>` only, no git -A, no write in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
- Docker tests NOT run on this host; the container-acceptance cell ran locally under the acceptance flag (one docker cell, torn down below) and was also executed by CI under `go test ./...`.
- Host clean: the single docker acceptance cell was brought down after the run.

## cleanliness

- The docker-acceptance cell (fake Prometheus host-side TLS server under `go test`) does not leave named containers; `docker ps -aq --filter name=baha-perses-ds` empty; no lane-owned container/network/volume/state dir remains.
- Worktrees /var/tmp/wt-083-hopf7 and /var/tmp/wt-083-control registered and will be removed at END.
- cleanliness: clean after teardown.

## CI run

Run 44652204594, head 576c6ad8fb1ad268aff0f088d6d20b248018899e, PR #1684, branch lane-0428-083-datasources-r2. Status completed / conclusion SUCCESS. Required: go-build success, go-vet success, Go unit owner/packages/cli-0..3 success, ci-executor-tests/ci-policy/pr-planner-tests/receipt-execution-tests success. 0 failures. Skipped (expected, not required): Targeted HA docker/podman and release shards.
