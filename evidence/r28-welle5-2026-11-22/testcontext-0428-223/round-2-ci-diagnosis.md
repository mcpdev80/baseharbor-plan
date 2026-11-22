# 0428-223 round 2 — CI diagnosis at head 1588ee1b

Card: `t-20261121-develop-full-suite-red` (0428-223). Lane: `0428-223-testctx`.
PR: #1750 (draft, base develop). Branch: `lane-0428-223-testcontext-target`.
Dispatch: coordinator mission files `/var/tmp/w223diag.g.md` + `/var/tmp/w223tail.g.md`
(complete directive, mission sha256 55c70de44f7d step 4). Prior round:
`evidence/r28-welle4-2026-11-21/develop-full-suite-red/round-1-fix.md`.

## PLAN

- Step 1: read both job logs fully at exact head 1588ee1b; record first failed test with file:line.
- Step 2: attribution — compare the failing text on the nearest develop run (run-id + job-id).
- Step 3: if mine, targeted fix + regression in this branch, push, watch new run to terminal.
- Step 4: if pre-existing develop/.github-scope defect, STOP with the finding (file:line, run-id, job-id, verbatim line).
- Step 5: publish this act to origin/main, ls-tree witness, END post.

## 1. Candidate state (remote truth)

Base attestation (ls-remote, this session):
```
6209874428f08dc3e90d6e29a42b30683ce9932a  refs/heads/develop
1588ee1be726a84501f5e513972f31dfad63aa34  refs/heads/lane-0428-223-testcontext-target
1588ee1be726a84501f5e513972f31dfad63aa34  refs/pull/1750/head
```
- `git merge-base --is-ancestor origin/develop HEAD` => OK (0): develop 62098744 IS an ancestor of head 1588ee1b.
- `git log --oneline origin/develop..HEAD` lists exactly ONE commit:
  `1588ee1b test(0428-223): isolate the leaked organization selection in test contexts` (single author `0428-223-testctx`).
- `git diff origin/develop...HEAD --name-only` (the write-set):
  `cmd/baha/app_init_source_neutral_test.go`, `cmd/baha/app_init_wizard_test.go`,
  `cmd/baha/app_perses_host_containers_cli_test.go`, `cmd/baha/app_perses_infra_dashboards_cli_test.go`,
  `cmd/baha/application_lifecycle_lock_test.go`, `cmd/baha/repository_up_init_test.go`,
  `cmd/baha/test_operator_context_test.go`. Test-only files under `cmd/baha/`; no `.github/**`, no `scripts/**`, no product code.

## 2. Mission statement of the fix (round-1 close-out)

Hosted probe runs proved the leak is the disk-persisted organization selection
at the persistent runner's host config root (`/home/runner/.config/baseharbor/organization/active.json`,
`org=acme`, `defaults.target=dev` -> reference `company-dev`), read by
`effectiveTarget` via `orgconfig.LoadActiveOptional()` ahead of the test's own
config. The candidate neutralises it in `testIsolatedSelectionContext` (private
config root only when nothing is activated and a host selection is visible) and
strips the inherited selection environment from the self-executed child of
`TestSharedBackendReconcileRejectsSecondProcess`. No skips, no deleted or
weakened expectations, no enum substitution; all diagnostic probes removed.

Proof it works, from the hosted unit cell at head 1588ee1b (validate job
137044903908): step 14 `Run unit and package tests` =
`ok github.com/mcpdev80/baseharbor/cmd/baha 306.966s` — zero `--- FAIL:` in the
step-14 window, zero `company-dev` occurrences in the whole 129002-byte job
log. The 14 mission names are green hosted.

## 3. Round-2 findings — the two remaining reds at exact head 1588ee1b

### 3a. validate job 137044903908 (run 44969161604) — step 16, NOT step 14

Job log fetched via `gh api /repos/mcpdev80/baseharbor/actions/jobs/137044903908/logs`
(129002 bytes). Steps: 1–14 success, 15 success, **16 `Run runtime integration
tests serially` failure**, 17–19 skipped.

First (and family-only) failed test, verbatim:
```
app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local installation
--- FAIL: TestRepositoryWorkflowRealLifecycle (0.07s)
```
Same text at `app_workload_integration_test.go:61`, `:193`, `:350`, `:538`
(`TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`,
`TestRepositoryComposeWorkloadOnlyLifecycleInCI`,
`TestRepositoryComposePinnedWorkloadLifecycleInCI`,
`TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`). All five start
2026-11-22T01:05:18.8–19.1Z, each failing at the trust-plane preparation
before any Target resolution — the environment gate
`ci.yml:404-413 (Run runtime integration tests serially)` is reached, but the
validate job has NO step that puts `oras` on PATH: at both develop 22fc68ebc
and develop 62098744 the workflow's `Install verified ORAS for native Core
bootstrap` (`scripts/ci-install-oras.sh`) exists only in the native-gate jobs
(ci.yml:288, :551) — inside the validate job: no match for `oras`.
`.github/workflows/ci.yml` is Owner scope: this is a STATE finding, not my
write-set. My change cannot reach it: the failure text is an exec.LOOKPATH
error, not a target-selection error, and `company-dev` appears zero times in
the log.

The postgres lines the dispatch quotes (`relation "baseharbor_schema_migrations"
does not exist`, `new row violates row-level security policy`, PIDs 547/551)
appear only at 01:05:34 — 15 s AFTER all five ORAS failures, inside the dumped
service-container logs — and belong to tests that had already passed in step 14
(`cmd/baha` was `ok`); PostgreSQL logs expected first-touch errors of the
fail-closed probes (the RLS policy exists precisely to reject unattributed
writes). They are not the first failure and not from my commit.

### 3b. PR · Draft Go · cli-3 job 137044885831 (run 44969156954) — zsh cell

Job log fetched via `gh api` (63741 bytes). Only one failed test in the whole
shard, verbatim:
```
context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH
--- FAIL: TestEndToEndInstalledZshAndFishWrappers (0.00s)
```
Per the dispatch's Praezisierung this is the known #1746 scope question (an
install step `if: matrix.shard == 'cli-3'` installing zsh AND fish in
`.github/workflows/pre-release.yml`). NOT my defect, NOT my fix: report only.
The other draft shards (cli-0/1/2, packages, Draft source and routing) are all
success at this head.

## 4. Attribution rule (step 2 of the dispatch)

- Nearest terminal develop run of this workflow: run 44918870333 (head
  22fc68ebc065, validate job 136890321112, log 124243 bytes). There step 14
  FAILED (the 14 org-selection names), so steps 15–19 were SKIPPED — the ORAS
  message never appears on develop (grep count 0 in that log). The 3a defect
  therefore could not be observed on develop *through that run*: on develop the
  same step 16 fails with the same `ORAS is required before Core setup` as
  soon as step 14 goes green. The workflow's validate job at BOTH develop
  heads lacks any ORAS install (checked at 22fc68ebc and 62098744), and my
  write-set touches no file the integration cell reads before the LookPath
  gate (zero matches for `oras` in my diff). Conclusion: pre-existing
  workflow-environment defect, newly reachable because I fixed the earlier
  blocker.
- 3b is develop/pre-existing by the dispatch's own statement (#1746, Owner).

Eigener defect: NEIN for both runs. Beleg-run-ids: 44918870333 (develop base of
the comparison), 44969161604 + job 137044903908, 44969156954 + job 137044885831.

## 5. STOP declaration (step 4 of the dispatch)

Findings to the coordinator:
- `.github/workflows/ci.yml:404` (validate job, `Run runtime integration tests serially`): the cell has no ORAS provisioning; add an `Install verified ORAS for native Core bootstrap` step (`bash scripts/ci-install-oras.sh`, precedent ci.yml:288) inside the validate job, Owner scope. Failing verbatim line: `app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before Core setup; ...` (run 44969161604, job 137044903908).
- `.github/workflows/pre-release.yml` draft-shard cell for `cli-3` lacks zsh/fish (already Owner-tracked as #1746). Failing verbatim line: `context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH` (run 44969156954, job 137044885831).

The card's own mission gate — the 14 develop-suite names green in the hosted
`validate` cell — is met at head 1588ee1b (section 2).

## repo-rule compliance

- Write-set honored: only `cmd/baha/*_test.go` + the test helper file. No `.github/**`, no `scripts/**`, no product code, no TOML. Verified by `git diff origin/develop...HEAD --name-only` (section 1).
- No skips, no weakened expectations, no enum substitution; probes removed (grep `0428-223-probe` count 0 in the head log).
- Eigenes-Run-Pflicht (AGENTS 4.6): every hosted run cited was started or read by this session to a terminal state, with per-job logs fetched via `gh api` and byte counts recorded.
- Local test policy: no bare `go test` suites; only the compile/vet/audit gates this lane needs (`go build`, `go vet`, `bash scripts/source-readability-audit.sh`, `bash scripts/ci-fast-check.sh`), and the last named-form `-run` isolation probe with an injected selection PASSED before the no-local-tests directive arrived (documented in round-1; not repeated).

## cleanliness

- No containers/networks/volumes were created by this lane on this host in round 2; scratch lives in `/var/tmp/0428-223*` only.
- `docker ps -a` on this host: empty (witness recorded in the END turn).

## witnesses (append at END turn)

- `git -C baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git`
- ls-remote lines: section 1.
- origin/main publication: section 6 (filled at END).

END 0428-223-testctx BLOCKED — first failed test per run: validate/137044903908 = `TestRepositoryWorkflowRealLifecycle` (`app_repository_integration_test.go:27`, ORAS); cli-3/137044885831 = `TestEndToEndInstalledZshAndFishWrappers` (`context_terminal_test.go:467`, zsh). eigener defect: nein (beleg-run 44918870333 + ci.yml inspectie). head 1588ee1b terminal failure, mission names green.
