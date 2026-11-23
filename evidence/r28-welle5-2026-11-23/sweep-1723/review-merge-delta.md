# PR #1723 post-merge review delta

Role: REVIEW.

## PLAN

- 385. Read the #1723d mission payload and capture its role, exact candidate, acceptance checks, verdict, and evidence path.
- 386. Verify the authorized GitHub remote, current develop/PR refs, merge state, and exact candidate provenance.
- 387. Inspect the merged diff, card contract, CI/test receipts, and any required historical comparison.
- 388. Decide the post-merge verdict and document only the scope/card changes authorized by the mission.
- 389. Validate and publish evidence in the actual Planning repository with remote and cleanliness witnesses.
- 390. Finish the live board, confirm the published evidence path, and post the required END.

## Post-merge delta review

Mission: `/tmp/opencode/m_rev_1723d.md.g`; role `REVIEW`. The mission's dossier reference `07c423a5e` resolves to Planning commit `07c423a5ef01964756ff6e1216659afe9a657dd8`, which adds the previous #1723 review's final post-merge snapshot to `evidence/r28-welle5-2026-11-23/sweep-1723/review-merge.md`. I reviewed that record and refreshed remote witnesses.

### Live merge and exact-head run

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1723/head` returned:
  `ddddbed16e34638f35968e2dc99921f970ba3720 refs/heads/develop`
  `9627763bd68018e962237b49d05450a7bf1348a9 refs/pull/1723/head`
- PR API returned `state=closed`, `merged=true`, merge time `2026-11-23T11:45:46Z`, merge commit `ddddbed16e34638f35968e2dc99921f970ba3720`, PR head `9627763bd68018e962237b49d05450a7bf1348a9`, and base SHA `b41103867e370f6588a396cb08ab0b3013e209ac` (`develop`). The live develop ref is the merge commit.
- The PR files API lists only `cmd/baha/app_apply.go`, `cmd/baha/app_workload_ports.go`, `cmd/baha/runtime.go`, and `cmd/baha/workload_port_local_regression_test.go` (10/0, 47/0, 45/1, and 119/0 additions/deletions respectively). No workflow file is changed.
- Run `45163965244` is terminal `completed / success`, event `pull_request`, exact head `9627763bd68018e962237b49d05450a7bf1348a9`. `PR Selected Checks` job `137669607778` completed success at `2026-11-23T11:44:57Z`. GitHub identifies the check as Actions integration `15368`. All four CLI Go unit shards completed success; the selected Docker and Podman runtime jobs also completed success. The aggregate reports success.

### Workload-port test receipt classification

The hosted log does not print a per-test PASS line for these cases; it prints each shard's package receipt. The tested source at `9627763bd68018e962237b49d05450a7bf1348a9` contains `TestAppApplyRunAcceptsWorkloadPort`, `TestUpRunAcceptsWorkloadPort`, and `TestExtractLocalWorkloadPorts`. The shard script at that same SHA (`scripts/pr-go-unit-shard.py`) hashes each discovered test name with SHA-256, reads the first eight digest bytes as big-endian, and selects `cli-(value mod 4)`. Applying that exact rule maps:

- `TestAppApplyRunAcceptsWorkloadPort` to `cli-1`, job `137656164098`.
- `TestUpRunAcceptsWorkloadPort` to `cli-3`, job `137656164061`.
- `TestExtractLocalWorkloadPorts` to `cli-3`, job `137656164061`.

The terminal job logs say `PASS cli-1: 445 passed / 10 intentionally skipped / 455 discovered; CLI inventory total=1879` and `PASS cli-3: 440 passed / 16 intentionally skipped / 456 discovered; CLI inventory total=1879`. The shard script emits a PASS summary only after checking its Go JSON events: every selected test must have run, and each must either pass or be intentionally skipped; failures or missing events fail the job. These three test bodies contain no `t.Skip` path. Therefore the summaries plus the exact test-name-to-shard mapping are package-level execution receipts for the workload-port regressions. The logs still lack literal named PASS lines; I do not claim otherwise. This is the package-receipt-with-documented-mapping precedent requested by the mission, consistent with the #1606 receipt approach.

No follow-up test card is needed for this delta: exact source-to-shard mapping is reproducible and both owning shards passed on the exact PR head. This does not revise the earlier historical observation that the hosted logs omit individual test names; it resolves the post-merge acceptance question under the mission's stated precedent.

## Repo-rule compliance

- Read-only review. No product code, workflow, PR, or Planning task status was changed; no merge, rerun, or workflow dispatch was performed.
- No local test was run. GitHub-hosted run `45163965244` was inspected through its API and terminal job logs.
- No Docker/Podman command started a container or compose project. Before-review cleanliness: PID `2138851`, `docker ps -a` printed only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` and listed no containers.
- No subagents were used. Planning remote had been verified as `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push before evidence publication.

## Final verdict

ROLE: REVIEW
VERDICT: APPROVE-delta

END_DONE codex-rev-1747: APPROVE-delta for merged PR #1723 (`ddddbed16e34638f35968e2dc99921f970ba3720`); run `45163965244` passed on exact head `9627763bd68018e962237b49d05450a7bf1348a9`, with workload-port tests mapped to successful `cli-1` and `cli-3` package receipts.

Post-review cleanliness: PID `2145683`; `docker ps -a` printed only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` and listed no containers. No container or compose project was started.
