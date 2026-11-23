# Mission m_rev_1723 evidence

## PLAN

1. Read the mission and confirm its task contract, scope, candidate, and acceptance criteria.
2. Refresh authoritative Planning and product remote state, claims, branch, PR, and CI evidence.
3. Inspect the exact candidate and verify each acceptance requirement without exceeding the authorized write-set.
4. Complete the authorized work or document the blocker and actionable repair recipe.
5. Publish evidence to baseharbor-plan origin/main, update the board, and post the final lane status.

## Mission and scope

Mission: `/tmp/opencode/m_rev_1723.md.g`. Requested role: CODEX-REVIEW, followed by normal squash merge only after every gate passes. The mission-named candidate was `340e66a881e60e20252ef5b284ca95e959732b59` on PR #1723. Its allowed product diff is exactly `cmd/baha/app_apply.go`, `cmd/baha/app_workload_ports.go`, `cmd/baha/runtime.go`, and `cmd/baha/workload_port_local_regression_test.go`.

## Remote and task state

- Product checkout `git remote -v` resolved the GitHub remote to `https://github.com/mcpdev80/baseharbor.git`; all product remote reads used that URL.
- Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1723/head` returned:
  `f6ab22b7dc9793ccd2872cb7717402816561c401 refs/heads/develop`
  `340e66a881e60e20252ef5b284ca95e959732b59 refs/pull/1723/head`
- PR API reports PR #1723 open, non-draft, head `340e66a881e60e20252ef5b284ca95e959732b59`, base ref `develop` at `304b3ad1d88647377ea647d0d94174bfc9298e14`, mergeable true, mergeable state `behind`.
- GitHub compare `f6ab22b7dc9793ccd2872cb7717402816561c401...340e66a881e60e20252ef5b284ca95e959732b59` reports `status=diverged`, `ahead_by=17`, `behind_by=1`, merge base `304b3ad1d88647377ea647d0d94174bfc9298e14`. Candidate is no longer at current develop.
- The only commit after base `304b3ad1d88647377ea647d0d94174bfc9298e14` is `f6ab22b7dc9793ccd2872cb7717402816561c401`, a develop-only catalog ingress (#1799) adding 11 app-access rows. Candidate catalog blob is `087041fdb8d94145b20e0b73dbfcc54708d50570`; current develop catalog blob is `8b07be15eebbb720ec1122ba3215286039dc4c66`. Candidate catalog matches its former base but is not byte-equal to current develop as the mission requires.
- GitHub PR files API lists exactly the four allowed product paths above and zero `.github/**` paths. There are no catalog paths in the PR diff against its old base.
- Planning task `t-20261120-workload-port-flag-ignored-locally` / 0428-199 is `active`, owner `ffe7611b` / Coordinator, PR #1723. `scripts/plan.py show` reports all three dependencies accepted: `t-20261114-r28-cli2-env-delete`, `t-20261121-develop-full-suite-red`, and `t-20261122-footprint-show-not-admitted-in-data-capabilities-gate`.
- GitHub PR review and issue-comment APIs returned no submitted reviews or review comments. This Codex reviewer session performed the requested CODEX-REVIEW against the candidate; it did not post a formal review or attempt a merge.

## Hosted run evidence

- Exact-candidate run `45153328164` is `pull_request`, terminal `completed / success`, head `340e66a881e60e20252ef5b284ca95e959732b59`.
- Its `PR Selected Checks` job `137635355294` completed success; check-run metadata reports app `github-actions`, integration ID `15368`.
- The exact-candidate run executed and passed CLI shards `cli-0` through `cli-3`, and native Docker and Podman `data-capabilities` jobs. The `cli-0` log reports `PASS cli-0: 472 passed / 13 intentionally skipped / 485 discovered; CLI inventory total=1878`.
- Hosted logs for all four CLI shards were searched for `TestAppApplyRunAcceptsWorkloadPort`, `TestUpRunAcceptsWorkloadPort`, and `TestExtractLocalWorkloadPorts`; none of those names appears. The hosted log therefore does not provide the mission-required named regression-test execution receipt. A green shard summary is not a substitute for the requested named log line.
- Mission-cited run `45157306258` is not a run for PR #1723 or its candidate. GitHub reports event `pull_request`, head `ff81c5a17ba0ba6c1f784773302497771ab089d8`, branch `w0428-257-0428-257-edit-toggle`, and status `in_progress` when checked. That head differs from `refs/pull/1723/head` (`340e66a...`), so it cannot serve as exact-head evidence for this review. No rerun or workflow dispatch was initiated.
- Exact-candidate run `45153328164` tested the then-current base `304b3ad1d88647377ea647d0d94174bfc9298e14`; it does not prove checks against current develop tip `f6ab22b7dc9793ccd2872cb7717402816561c401`.

## Source and security review

- At candidate `340e66a...`, the local extractor in `cmd/baha/app_workload_ports.go` accepts both documented flag forms, rejects missing or malformed values, invalid environment names, duplicates, and ports outside 1 through 65535. The workload persistence path verifies the requested variable exists in the selected Compose file and rejects an explicit port if unavailable.
- `cmd/baha/runtime.go` parses the value and routes `WorkloadPorts` into the application context. `portAvailable` attempts `net.Listen("tcp4", "127.0.0.1:<port>")`; a bind failure is treated as unavailable. Explicit conflicts return an error instead of silently replacing the operator's choice. No privilege assumption or privilege escalation is used in this path; unavailable or restricted binds fail closed.
- The regression file defines distinct command-surface tests `TestAppApplyRunAcceptsWorkloadPort` and `TestUpRunAcceptsWorkloadPort`, plus parser and malformed-input cases. Hosted logs do not expose the named PASS evidence required by the mission.
- No local tests were run, per the binding cost policy. No product source or workflow was changed.

## Live rules and repo-rule compliance

- Read-only GitHub rulesets API responses at review time listed ID `23754541` (`develop - integration branch`) with enforcement `disabled`, ID `25223521` (`develop - required checks`) with enforcement `active`, and ID `23754542` (`main - released source`) with enforcement `active`. No bypass or merge was attempted. The required-check run above used integration 15368.
- `python3 coordinator/scripts/basics-check.py` exited successfully without output.
- Planning remote was verified before any evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- No subagents were used. No local tests, containers, compose projects, workflow dispatch, reruns, product branch updates, PR updates, or merge actions were performed.
- A read-only status check in the shared product checkout showed unrelated pre-existing modifications and untracked paths; none were touched.

## Decision

END_BLOCKED codex-rev2-1736: PR #1723 not merged; develop advanced beyond the candidate, cited run 45157306258 belongs to another branch, and exact named regression-test execution is absent from hosted logs. Candidate `340e66a881e60e20252ef5b284ca95e959732b59`.

## Repair recipe

1. On the existing mission branch only, incorporate current develop `f6ab22b7dc9793ccd2872cb7717402816561c401` through the authorized additive update path. Preserve the four-file product write-set, verify no `.github/**` change, and confirm `scripts/pr-gate-coverage.json` is byte-equal to the updated develop base.
2. Obtain a terminal `pull_request` run on the resulting exact PR head and current base. The supplied run 45157306258 cannot be reused because it belongs to branch `w0428-257-0428-257-edit-toggle`.
3. Provide a hosted log line naming and passing `TestAppApplyRunAcceptsWorkloadPort` and `TestUpRunAcceptsWorkloadPort` (or the contract's named regression), rather than only a successful shard count. If the existing CLI CI logger suppresses test names, route an explicit named receipt through the task's authorized test path before handoff.
4. Re-review the new exact head, current base, catalog equality, required CI results, and unresolved review state. Only then consider the authorized squash merge.

## Cleanliness

- Before review probes, shell PID `1910266`: `docker ps -a` returned only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.
- After review, shell PID `1919942`: `docker ps -a` again returned only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.
- No container or compose project was started by this review.

## Review role and verdict

ROLE: REVIEW
VERDICT: BLOCKED
The candidate has a successful exact-head historical run, but it is no longer current-base; the mission-cited run is for another branch; and the required named test receipt is absent from the hosted logs. No merge is authorized on this evidence.

## Required origin/main witness before final publication

Immediately before this evidence update, ran `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1723/review-merge.md$'`. Exact grep output:

evidence/r28-welle5-2026-11-23/sweep-1723/review-merge.md

## Fresh candidate review update — after the additive base hop

This addendum supersedes the earlier `340e66a...` snapshot. PR #1723 advanced during the review via an additive merge of current develop. I re-reviewed the new exact head and its new run; no product changes were made in this reviewer session.

- Current `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1723/head` returned `b41103867e370f6588a396cb08ab0b3013e209ac refs/heads/develop` and `12bf50c4c8dbeadeb5fa9324fdafa4069e267d8d refs/pull/1723/head`.
- Current PR API reports PR #1723 open and non-draft, head `12bf50c4c8dbeadeb5fa9324fdafa4069e267d8d`, base `f6ab22b7dc9793ccd2872cb7717402816561c401`, mergeable true, `mergeable_state=behind`. Compare latest develop `b411038...` to the PR head reports `status=diverged`, `ahead_by=18`, `behind_by=1`, merge base `f6ab22b...`.
- The develop commit after the tested base is `b41103867e370f6588a396cb08ab0b3013e209ac`, `fix(app-edit): acknowledge space-toggle state on screen (#1801)`, touching `cmd/baha/app_edit.go`, `cmd/baha/app_edit_apply_test.go`, and `cmd/baha/app_wizard_controller.go`. It does not touch `.github/**`, the planner, or test-runner scripts, but the mission explicitly requires the candidate base to be current. GitHub also reports the PR behind, so the exact-current-base gate is not satisfied.
- Candidate `12bf50c...` is an additive merge commit with parents `340e66a...` and `f6ab22b...`. GitHub blob SHAs for all four allowed product files are identical between `340e66a...` and `12bf50c...`: `app_apply.go` `f544eac8ed057d5ea2bb7a7d2a001350831f82ce`; `app_workload_ports.go` `fb10ff1fd12b31115f3e501885315c821f40a38e`; `runtime.go` `f74276a169f1858805df9356bb5f51fe08bd7c12`; regression test `6f75ceb39381cf351ba52e3d0112774d14a69adb`. PR files remain exactly the four mission-authorized product paths; `.github/**` remains untouched.
- The catalog blob on candidate and current develop is now equal: `8b07be15eebbb720ec1122ba3215286039dc4c66` on both `12bf50c...` and `b411038...`.

## Exact current-head run 45159172695

- Run `45159172695` is terminal `completed / success`, event `pull_request`, exact head `12bf50c4c8dbeadeb5fa9324fdafa4069e267d8d`. The Trusted Plan job `137639793628` used `BASE_SHA` and `VERIFIED_BASE` `f6ab22b7dc9793ccd2872cb7717402816561c401` and logged `No narrow mapping: conservative checks selected.`
- `PR Selected Checks` job `137654383623` completed success at `2026-11-23T11:15:14Z`; check-run metadata reports app `github-actions`, integration ID `15368`.
- On this exact head, CLI shards `cli-0` through `cli-3` succeeded; native Docker and Podman `data-capabilities` succeeded; selected runtime Docker guided, Docker data-capabilities, and Podman data-capabilities succeeded. No failed jobs were reported.
- The full run log search contains the four shard summaries (for example `PASS cli-0: 472 passed / 13 intentionally skipped / 485 discovered; CLI inventory total=1878`) but no line naming `TestAppApplyRunAcceptsWorkloadPort`, `TestUpRunAcceptsWorkloadPort`, or `TestExtractLocalWorkloadPorts`. The required named hosted-log receipt remains absent; the successful aggregate and shard counts do not prove the named test by name.
- Mission-cited run `45157306258` remains a different pull-request head (`ff81c5a...`, branch `w0428-257-0428-257-edit-toggle`), not PR #1723. The valid exact-head run is `45159172695`, but its base `f6ab22b...` predates current develop `b411038...`.

## Final role and verdict

ROLE: REVIEW
VERDICT: BLOCKED

END_BLOCKED codex-rev2-1736: PR #1723 remains unmerged; head 12bf50c4c8dbeadeb5fa9324fdafa4069e267d8d has a successful exact-head run 45159172695, but the current develop tip b41103867e370f6588a396cb08ab0b3013e209ac is not in that candidate and the hosted logs do not name the required workload-port regression test.

Repair recipe: update the existing candidate against the current develop tip, preserve the four-file product write-set and current catalog bytes, obtain a terminal exact-head run on the current base, and provide an inspectable hosted PASS line for the named workload-port regression test. Then re-review the exact head and only merge if every gate remains satisfied. No workflow rerun or dispatch was initiated by this review.

## Final cleanliness witness

- After the exact-head CI observation, shell PID `2033740`: `docker ps -a` returned only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`; no containers were listed.
- A read-only status check of the shared product checkout still showed unrelated modified and untracked paths; this review left each untouched.
- No container or compose project was started by this review.

## Final origin/main path witness before updated review publication

Immediately before this evidence update, `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1723/review-merge.md$'` returned this exact path:

evidence/r28-welle5-2026-11-23/sweep-1723/review-merge.md
