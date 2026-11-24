# #1812 Docker Light — authoritative per-job ledger (round 1)

Lane: w90-0428-249-1812gateledger (READ-ONLY DESK)
Mission: coordinator/missions/w90-0428-249-1812gateledger.txt
Date: 2026-11-24

## PLAN

1. Fetch origin/develop SHA and record it as current base. — done
2. Paginate `gh api` jobs for run 45398943139 (per_page=100) into /tmp JSON files. — done (45 jobs, single page)
3. Build per-job ledger: id, name, matrix class, status, conclusion, executed vs skipped. — done
4. Pull log tails for each FAILED Docker Light job and quote exact failure line. — done (per-job `actions/jobs/<id>/logs` endpoint; run-level `--log` zip omitted the Light jobs)
5. Reconcile the matrix-skipped claim (podman family vs docker family) and state verdict. — done
6. Write this evidence file with PLAN, table, verdict, cleanliness line. — done
7. Verify baseharbor-plan remote URL, commit+push atomically, show origin/main tree witness. — done
8. Post END line to coordinator. — done

## Base and candidate attestation

- `origin/develop` (real GitHub URL, fetched live):
  `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
  (witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- PR #1812 (`gh pr view`): OPEN, base `develop`, head ref `lane-0428-249-runtime-image-fix`,
  head SHA `47590207518ce9501f1b1bbb115d72d64a206d14`.
  Branch SHA witness: `ls-remote ... refs/heads/lane-0428-249-runtime-image-fix` = same SHA `47590207...`.
- The gate plan in run 45398943139 recorded `DEVELOP_SHA: 46d3dccc...` (same tip this lane fetched — develop
  did not move between the run and this desk) and its own log states
  `Candidate contains the checked develop tip 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2.` — i.e. develop tip
  `46d3dccc` is an ancestor of the tested head `47590207`.
- Run 45398943139: workflow `Pre-Release · v0.4.27`, event `workflow_dispatch`, attempt 1,
  head `47590207518ce9501f1b1bbb115d72d64a206d14`, branch `lane-0428-249-runtime-image-fix`,
  status completed, conclusion failure (run-level: Docker Light gate failures, not a missing job).

## Planning repo remote witness

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Fetch-method note (reproducibility)

- Jobs: `gh api --paginate "repos/mcpdev80/baseharbor/actions/runs/45398943139/jobs?per_page=100"`
  returned 45 jobs in one page; all Light job IDs (138466518597/674/714/757/846/935/939 and the
  placeholder 138466521125) are present. The "GitHub first-page limit hides them" concern is
  disproven for this run.
- `gh run view 45398943139 --log` produced a zip whose text export contains only 17 job namespaces —
  the per-fanout Light/Heavy job logs are NOT in the run-level export. This is the mechanism behind
  the earlier "invisible jobs" confusion: they are visible via the jobs API and their own log
  endpoints, not via the run-log aggregate.
- Per-job logs: the `jobs/<id>` summary endpoint via short path returned 404, but
  `gh api "repos/mcpdev80/baseharbor/actions/jobs/<id>/logs"` (full URL form) returned complete
  logs (policy 217 KB, reconciliation 236 KB, connectivity 221 KB, full-destroy 412 KB).
- The pre-dispatched job-ID set from w81/w85 (138466518597/674/714/757/935/939) is confirmed exact;
  the seventh executed gate (failure) is 138466518846.

## Per-job ledger — run 45398943139, all jobs whose name contains 'Light' or a gate id

Executed? = step 19 "Run runtime gate" ran (not skipped) and gate commands appear in the job log.

| job id | gate | runtime | status | conclusion | executed? | failure line |
| --- | --- | --- | --- | --- | --- | --- |
| 138466518597 | policy | docker | completed | failure | yes | `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state ...` (also: `Error: operator authentication needs interactive setup but input is not a terminal`) |
| 138466518674 | reconciliation | docker | completed | failure | yes | same consent line (`record deployment before mutation: ... --confirm-candidate ...`) |
| 138466518714 | lifecycle | docker | completed | success | yes | — |
| 138466518757 | connectivity | docker | completed | failure | yes | same consent line |
| 138466518846 | failure | docker | completed | success | yes | — |
| 138466518935 | guided | docker | completed | success | yes | — |
| 138466518939 | full-destroy | docker | completed | failure | yes | same consent line |
| 138466521125 | `Light · ${{ matrix.runtime }} · ${{ matrix.gate }}` (unevaluated-name placeholder) | skipped fan-out (podman family; see verdict) | completed | skipped | no | — (never started: started_at == completed_at == 2026-11-24T13:07:38Z, no labels, no step log) |

Cross-checks:
- The aggregate job `runtime light gates · All runtime results` (138471225669) is `success` under the
  one-matrix rule (`DOCKER_RESULT: failure` tolerated only when count==0; docker count was 7, so the
  docker matrix had to execute and it did — its step `Require both runtime matrices` ran).
- The gate-plan artifact (in run log) states `light_docker_count=7, light_docker_execute_count=7,
  light_podman_count=0, light_podman_execute_count=0`, and lists exactly the 7 atomic/docker gate IDs
  (guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy).
- `ONLY_GATES: atomic/docker/guided,atomic/docker/lifecycle,atomic/docker/policy,atomic/docker/connectivity,atomic/docker/reconciliation,atomic/docker/failure,atomic/docker/full-destroy`
  appears verbatim in the plan job's env block — the docker-only selection is explicit, not inferred.
- Evidence artifacts on the run: `pre-release-runtime-evidence-docker-guided` (14922714479),
  `pre-release-runtime-evidence-docker-failure` (14923870709),
  `pre-release-runtime-evidence-docker-lifecycle` (14924375267) — exactly the 3 passing gates uploaded
  passed-gate evidence; the 4 failed gates have no evidence artifact (steps 25/26 skipped in their logs).
- `Pre-Release Checks` (138471278439, failure) terminated on
  `AssertionError: runtime_light_gates_docker: expected success, got failure` — the run's overall failure
  is caused by these 4 Docker Light gate failures.
- Step-level witness (all 4 failed jobs): steps 1–17 success, step 19 `Run runtime gate` = failure,
  step 20 `Preserve demo runtime diagnostics` and steps 22/23 ran (failure path), step 24 cleanup success.

## Verdict

Run 45398943139 DID EXECUTE all seven Docker Light gates on the exact head 475902075 (job IDs
138466518597/674/714/757/846/935/939), with a 3-PASS (guided, lifecycle, failure) / 4-FAIL (policy,
reconciliation, connectivity, full-destroy) outcome that matches the w81/w85 reports — the
"skipped-matrix" claim is wrong for this run: the only skipped Light job (138466521125) is the
unevaluated-name `${{ matrix.runtime }} · ${{ matrix.gate }}` placeholder that GitHub emits when a
matrix fan-out expands to zero children, and here the plan selected ONLY_GATES to the seven
`atomic/docker/*` gates (`light_podman_execute_count=0`), so the entire podman family (Light/Heavy/
Journey/HA/Integration) had no children and correctly skipped. The reason the earlier sessions could
not see the seven executed jobs was tooling-side, not chain-side: the run-level log download
(`gh run view --log`) omits the per-fanout job logs even though the jobs API lists all 45 jobs
(45 ≤ one page of 100) — each job's own `actions/jobs/<id>/logs` endpoint returns its full log. All
four failures carry the same, single root-cause line: the binary at this head enforces operator
consent at deployment recording
(`candidate submission requires an explicit operator/automation consent (--confirm-candidate);
refusing to record deployment state`), and the Docker Light harness only supplies that consent on
its `up --confirm-candidate` step (visible in the operator decision log), not on the earlier
`baha up` deployment-recording call the failing gates make — i.e. this is the consent-gate/runner
contract mismatch tracked for the chain (0428-282 territory), not an infra flake and not a defect
unique to #1812's runtime-image fix; #1812's own target — the missing runtime-image reload before
ORAS publish — is evidenced working (step 14 "Load prebuilt runtime image" and step 15 "Publish exact
candidate image for ORAS verification" succeeded in all 7 executed jobs, and all gates reached real
runtime execution).

## Cleanliness

Read-only desk: created nothing in any product repo; no containers/networks/volumes started on this
host (no docker/podman commands run); no CI actions performed (no cancel/rerun/dispatch — only `gh api`
reads and `gh run view` reads); touched no branch, PR, or file of #1812/#1819/#1820/#1818/#1826/#1650.
Only /tmp working files (w90-*.json/.log/.tsv) and this single evidence file.
`docker ps -a` was never applicable (nothing started); this lane's cleanliness line stands on that.

## END

END_DONE w90-0428-249-1812gateledger: run 45398943139 executed all 7 Docker Light gates on head 47590207 (3 PASS / 4 FAIL, all fails = --confirm-candidate consent refusal); podman family skipped by only_gates=docker selection; candidate SHA for chain unchanged 47590207518ce9501f1b1bbb115d72d64a206d14
