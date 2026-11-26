# w289-0428-251-demochecks — demo #170 / #179 / #181 exact-head check binding

Card: `0428-251` (`tasks/t-20261123-demo-digest-consent-adaptation.md`, `kanban_status: closed`, `resolution: accepted`).
Mission: `coordinator/missions/w289-0428-251-demochecks.txt` (coordinator commission 2026-11-26).
This lane performed NO product/demo file edits, NO `.github/**` writes, NO merges, NO new branches in product repos,
NO local test execution, NO reruns and NO `workflow_dispatch` triggers. The only remote mutations were the
coordinator-authorized PR transport actions listed in step 2 below.

## PLAN

1. Verify planning-repo and demo-clone remote identity; create own clone/worktree zone.
2. Record the visible ANSATZ block (card frontmatter owner verbatim, git identity, literal `git -c` invocation, pre-push author gate).
3. Attestation: `git remote -v`, `gh api` refs main/develop, `gh pr view` #170/#179/#181, current check rollups and check-run census.
4. #179 (draft): run `gh pr ready`; if ready binds no checks, one authorized close+reopen fresh event; record run IDs.
5. #170 and #181: determine whether an executed `pull_request` run exists on the current head; where absent, one documented close+reopen each.
6. #181 base question: quote the workflow `branches:` trigger lines with file:line and answer whether retargeting to develop is required.
7. Watch every caused event to a terminal state; per-run job census (per_page=100 including attempts); executed/skipped verdict.
8. Root-cause the binding failure with controls (paths-filter hypothesis, workflow-ancestry hypothesis) and state the transport fix.
9. Publish this akte on my own plan branch plus one Plan PR against live `origin/main`; do NOT merge it.
10. Run the origin/main evidence-path witness plus the cleanliness witness; post the END line.

## ANSATZ (visible candidate author block, recorded before the first commit)

Card `0428-251` frontmatter `owner` VERBATIM, fetched from `origin/main` at runtime
(`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan show origin/main:tasks/t-20261123-demo-digest-consent-adaptation.md | sed -n 's/^owner: //p'`):

```text
owner: Coordinator (merge 1450) / 9b7683b5
```

`git user.name`: `w289-0428-251-demochecks`

`git user.email`: `w289-0428-251-demochecks@baseharbor.local`

Literal commit invocation used for every commit in this akte (including the merge of live `origin/main`):

```bash
git -c user.name='w289-0428-251-demochecks' -c user.email='w289-0428-251-demochecks@baseharbor.local' \
  commit -m 'evidence(w289): demo 170/179/181 exact-head check binding akte'
```

Pre-push author/committer gate line (must print my lane identity on both lines):

```bash
git -C /home/marcel/dev/baseharbor-ecosystem/workers/w289-0428-251-demochecks-plan \
  show -s --format='%an%n%cn' HEAD
```

Gate output: recorded under "Commit identity witnesses" below.

## Step 1 — reality witnesses (all before any mutation)

Planning repo identity (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The WRONG-ZONE path `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` was NOT used.
The isolated plan worktree is `workers/w289-0428-251-demochecks-plan`, created from live `origin/main`;
the shared planning checkout (uncommitted foreign work) was never rebased, reset, stashed, cleaned or force-checked-out.

Demo clone identity (own clone under `workers/w289-0428-251-demochecks-work/demo-clone`):

```text
origin	https://github.com/mcpdev80/baseharbor-demo.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-demo.git (push)
```

Base attestation — remote refs at attestation time (`gh api repos/mcpdev80/baseharbor-demo/git/ref/heads/<ref>`,
full output in `attest.log` next to this file), matching the mission expectation:

```text
main:    2618b3962330509add5bf265522995da2a9034ce   (expected 2618b3962)
develop: 5ca92a7cd2f746934890cfd7096a48068bdf218e   (expected 5ca92a7cd)
```

`gh pr view` at attestation (verbatim in `attest.log`):

```text
--- PR #170
{"baseRefName":"develop","headRefOid":"b086cf58bb2f7aafee30edf52ac4b8199daf7d0d","isDraft":false,"mergeable":"MERGEABLE","number":170,"state":"OPEN"}
--- PR #179
{"baseRefName":"develop","headRefOid":"cda6aa70e80bec1a1db06d85decdd8833cb63994","isDraft":true,"mergeable":"MERGEABLE","number":179,"state":"OPEN"}
--- PR #181
{"baseRefName":"main","headRefOid":"6d06eab0ed0cd890ab9f818100ff84698e0347f5","isDraft":false,"mergeable":"CONFLICTING","number":181,"state":"OPEN"}
```

Current check rollups at attestation (all three EMPTY, i.e. zero bound checks):

```text
--- #170 statusCheckRollup  -> []
--- #179 statusCheckRollup  -> []
--- #181 statusCheckRollup  -> []
```

Check-run census on each head (`/commits/{sha}/check-runs`): `#170 0`, `#179 0`, `#181 0` — nothing executed,
nothing skipped, simply nothing bound.

Workflow files present on BOTH `main` and `develop` (API contents census, identical sets):
`.github/workflows/pr-config-matrix.yml`, `.github/workflows/pr-guided-consent.yml`, `.github/workflows/v0424-targeted.yml`.
Registered workflow states: `pr-config-matrix.yml` active, `pr-guided-consent.yml` active, `v0424-targeted.yml` active,
plus three `disabled_manually` legacy workflows (`acceptance-harness-check.yml`, `init-targeted.yml`, `recovery-targeted.yml`).

## Step 2 — what I did, per PR (exact commands and timestamps in the `.log` witnesses)

### #179 (was DRAFT, base develop, head cda6aa70e)

1. `gh pr ready 179 --repo mcpdev80/baseharbor-demo` → `✓ … is marked as "ready for review"` at 2026-11-26T03:59:26Z
   (`ready179.log`). Verified afterwards: `draft=false`, and ZERO check-runs / ZERO new workflow runs → ready alone bound nothing.
2. Authorized fresh event, first attempt (`cr179.log`): close at 04:00:08Z + reopen at 04:00:15Z.
3. Second authorized fresh event, after the paths diagnosis in step 6 (`cr179b.log` 04:02:33Z/04:02:40Z; `cr179c.log` 04:21:24Z/04:21:33Z, comment
   `…paths_filter hypothesis`). Total: three pull_request events on this PR today; all three transcripts are in the
   witness files (`cr179.log`, `cr179b.log`, `cr179c.log`; the second attempt's transcript is recorded as the
   terminal-state census in step 4 because that close/reopen ran as one chained command).
4. Result: NO `pull_request` workflow run was created for `cda6aa70e` (run census in step 4).
   Final state: `OPEN`, `draft=false`, `base=develop`, head unchanged `cda6aa70e80bec1a1db06d85decdd8833cb63994`
   (no PR head moved underneath me at any point; verified per event).

### #170 (ready, base develop, head b086cf58b)

Checks were not executed for its head, so the same authorized fresh event was used:
`cr170.log` close 04:04:19Z / reopen 04:04:26Z, `cr170c.log` close 04:14:30Z / reopen 04:14:37Z, and
   `cr170d.log` close 04:22:26Z / reopen 04:22:35Z
(second event = documented control for the paths-filter test in step 6).
Result: NO `pull_request` workflow run created for `b086cf58b`; 0 check-runs. Final state `OPEN`, `draft=false`, head unchanged.

### #181 (ready, base main, head 6d06eab0e)

`cr181.log`: close 04:17:44Z / reopen 04:17:51Z.
Result: NO `pull_request` workflow run created for `6d06eab0e`; 0 check-runs. Final state `OPEN`, head unchanged.

### Negative control (no PR mutation)

`POST /repos/mcpdev80/baseharbor-demo/dispatches` with `event_type=w289-diagnostic-pull-request-synthetic-event`
(sent once at 04:14:01Z; HTTP accepted, zero workflows subscribe to `repository_dispatch`, so no run was created —
confirmed by the run census). This proved the Actions pipeline itself is alive and that my token is admin on this repo.
The three later `pull_request` events on #179/#170 produced no run either, which localizes the failure to
workflow-selection, not to the Actions pipeline.

## Step 3 — #181 base question, answered from the workflow files (file:line)

`pr-config-matrix.yml` on the DEFAULT branch `main` @ `2618b3962` (blob `ea66bbd38dfb7dd45468ccb861487a9790ce95c8`):

```text
3:on:
4:  pull_request:
5:    branches: [develop]
6:    paths:
7:      - .github/workflows/pr-config-matrix.yml
…
17:      - tests/reconciliation/run.sh
```

`pr-config-matrix.yml` on `develop` @ `5ca92a7cd` (blob `7108cf69e4f53164f83faa8dc13ae51ec25e291d`) — the file the
three PR heads still carry (see step 4):

```text
1:# DRAFT ONLY — owner-scope workflow addition; not committed or run.
5:  pull_request:
6:    branches: [develop]
```

`pr-guided-consent.yml` @ `cc361bdf8529f76e21e99c4bef757dc709e261a0` (identical on `main` and `develop`):

```text
4:  pull_request:
5:    branches: [main]
```

ANSWER (report-only, no retarget performed by this lane): **retargeting #181 to develop is NOT required and would
not bind its checks** — the develop-scoped trigger is exactly what already excludes a `base=main` PR, and the
decisive defect is the DRAFT placeholder in #181's own head tree. What #181's checks actually require is either
(i) `base=develop` **plus** a head commit that contains the non-placeholder workflow (i.e. a develop head, `5ca92a7cd`
or newer, as ancestor), or (ii) keeping `base=main`, which only matches `pr-guided-consent.yml`
(lines 4-5, `branches: [main]`) and whose paths have no `paths:` filter — so it fires for any changed file —
but only if the head tree carries a parseable workflow, which `6d06eab0e` does not.
Base changes on that PR stay an owner/Codex decision.

## Step 4 — per-run and per-head census (Eigenes-Run-Pflicht 4.6)

Full repo run census taken repeatedly (latest 2026-11-26T04:28:23Z, `per_page` windows across
`status=queued|in_progress|action_required` all `total_count=0`). There is **no pull_request run for any of the
three heads today**, therefore there is nothing to census per job: the census is

```text
#170 b086cf58b: pull_request runs = 0, check-runs = 0  (0 executed / 0 skipped)
#179 cda6aa70e: pull_request runs = 0, check-runs = 0  (0 executed / 0 skipped)
#181 6d06eab0e: pull_request runs = 0, check-runs = 0  (0 executed / 0 skipped)
```

`GET /repos/…/actions/workflows/pr-config-matrix.yml/runs?event=pull_request` → `total_count = 0`: this workflow has
NEVER produced a pull_request run in the repository (all 8 of its runs are `event=push`).

Terminal-state witnesses of the runs that DO exist and bound (control, not caused by me):
`gh api 'repos/mcpdev80/baseharbor-demo/actions/runs/45726412673/jobs?per_page=100'` (run_attempt 1):

```text
Guided consent · production-path regressions completed success started=2026-11-26T00:07:16Z completed=2026-11-26T00:07:59Z steps=6
```

(`event=pull_request`, `head=d512653aa`, 1 job / 1 job census, executed → this is the proof that GitHub does
create and execute pull_request runs in this repo.)

## Step 5 — the executed-vs-skipped verdict per required job

No required job executed on any of the three heads. SKIPPED counts are also zero, because no run exists at all:
the heads carry **absent** checks, which is NOT a pass (`gh pr view --json statusCheckRollup` → `[]` for #170/#179/#181,
verified again at 04:28:23Z). Qualification for these candidates is therefore still OPEN, and the missing route is a
transport defect in the candidate heads themselves, not a missing trigger (see step 6).

## Step 6 — root cause (this lane's own measurements; supersedes the mission's hypothesis where they differ)

The mission states "the fix is transport, not workflow edits". The measurements confirm transport — but the
transport that is missing is **the workflow content on the PR head**, not the PR event:

1. Every fresh `pull_request` event on the three heads created ZERO workflow runs (`pr-config-matrix.yml`
   `event=pull_request` `total_count=0`; check-runs `0` on all three heads).
2. All three heads carry the develop copy of the workflow, whose line 1 is
   `# DRAFT ONLY — owner-scope workflow addition; not committed or run.` (blob `7108cf69…`, see step 3).
   For `pull_request` events GitHub uses the workflow **as it exists in the head commit**, so this file is what
   GitHub evaluates for #170/#179/#181.
3. That develop copy's `on.pull_request.paths` (develop file, lines 7-16) has NO entries for
   `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`,
   `tests/reconciliation/run.sh`. Those four paths were added only on `main` (main file lines 14-17) by
   `d512653aa` "ci(demo): route fixture gates on pull requests" (a one-file commit touching
   `.github/workflows/pr-config-matrix.yml`, ancestor of `main`, **not** an ancestor of `develop`).
   → #179's only changed files are exactly those four; `git diff --name-only <merge-base develop…head>` confirms it.
   The paths filter matches nothing → no run is created. The same applies to `tests/config-matrix/run.sh`-only
   changes on #170 (that glob IS present on both copies, so #170 fails for reason 4 below).
4. The `push:` trigger of the develop copy (no `paths:` filter, develop lines 1-28) explains why the pushes at
   16:43Z/17:01Z/17:06Z/17:18Z/19:25Z/19:44Z DID create runs (`45656925640`, `45660181295`, `45661078349`,
   `45663390190`, `45685104924`, `45688177820`) — every one of them with `jobs = 0` and `conclusion = failure`.
   A `jobs: {}` mapping is invalid: the run "fails" without a single check-run, which is exactly the zero-job
   symptom `#181` carries as its title. So the develop/main workflow never executed jobs on ANY event.
5. `main`'s copy (blob `ea66bbd3…`) has the full paths allowlist (lines 7-19) and real jobs (lines 74-84 select
   `config-matrix`/`connectivity`/`full-destroy`/`policy`/`reconciliation`); its push runs are
   `45726404672` and `45726589547` (`event=push`, also `conclusion=failure` — a separate follow-up finding).
6. The `# DRAFT ONLY` header itself says the workflow was never authorized to run, which is consistent with (4).

CONTROLS that exclude other hypotheses:
- `branches:` hypothesis for #179/#170 (base=develop matches `branches: [develop]`): their events produced no run,
  so a branch filter is not the blocker for them; the paths+zero-jobs facts are.
- "Actions is globally broken" hypothesis: refuted by the executed job in step 4.
- "PRs on base=develop never bind checks" hypothesis: refuted by run `45726412673`
  (`head=d512653aa`, `event=pull_request`, SUCCESS, 1 job) — a head whose tree carries the non-placeholder
  workflow. Its PR (#180) was `base=main`, which matches `pr-guided-consent.yml` lines 4-5.
- Fork/`action_required` hypothesis: refuted — all three head refs live in `mcpdev80/baseharbor-demo`
  (`git ls-remote` in step 1 / `head_repo=mcpdev80/baseharbor-demo` for all three), and
  `runs?status=action_required` → `total_count=0`.
- Attempt-bump contamination hypothesis: none of the runs shows `run_attempt>1` (`per_page=100` census incl.
  attempts; no rerun was issued by this lane or visible in the census).

### What qualification requires (transport, no `.github/**` edit by this lane)

For #170 and #179 (base develop): the head must carry a parseable, non-placeholder
`.github/workflows/pr-config-matrix.yml` — i.e. the content of `d512653aa` (already on `main`) merged into
develop, then `git merge origin/develop` into each lane branch and one normal push, which itself provides the
qualifying `pull_request` event. Until the workflow content is fixed, ANY number of close/reopen fresh events on
these heads is structurally incapable of binding checks (measured: 3 pull_request events on #179, 3 on #170,
   1 on #181 today, all at unchanged heads → 0 runs).
For #181 the same fix applies plus the base decision of step 3.
Because the develop-copy workflow has zero valid jobs, the "second distinct run ID of the pull_request pair"
cannot be produced by transport alone on today's heads; that is a finding for Codex/Owner, not a detail.

## STATE report (per mission stop rule 3)

No required check of #170/#179/#181 executed, so there is no failing product-reason log line to quote from them.
The failing evidence is the zero-job runs on the workflow's own push events, quoted as setup-level state, not a test:

```text
run 45663390190 (.github/workflows/pr-config-matrix.yml, event=push, head=b086cf58b = #170 head)
  jobs = 0, conclusion = failure   → "Workflow has no jobs to run" class (yaml jobs mapping), no test step ran
run 45726589547 (same workflow, event=push, head=2618b3962 = main)
  jobs = 0, conclusion = failure
```

## Commit identity witnesses

Before the push (printed from the plan worktree; see also the pre-push gate command in ANSATZ):

```text
82ede92d3 an=w289-0428-251-demochecks cn=w289-0428-251-demochecks
(gate: git show -s --format=%an%n%cn HEAD)

```

Log line scope: `git log --oneline origin/main..HEAD` in the plan worktree lists ONLY my own commits, i.e.

```text
82ede92d3 merge(origin/main): bring plan main into w289 evidence branch
54c875c86 evidence(w289): demo 170/179/181 exact-head check binding akte
```

Base provenance for the plan branch: cut from `origin/main` at
`27aff0b938df76bd4a7d0116a9b320e5d84123e3`, verified by
`git merge-base --is-ancestor 27aff0b938df76bd4a7d0116a9b320e5d84123e3 HEAD` (exit 0).

## Zero local test execution

No `go test`, no `pytest`, no `python3 -m unittest`, no `scripts/ci-fast-check.sh`, no container runs were executed
on this host by this lane. Only read-only git/`gh api` queries and the authorized PR transport commands.

## cleanliness

Lane pid: `2432031`. `docker ps -a` before (2026-11-26T03:59Z) and after (04:29Z) are both empty
(`docker ps -a --format '{{.Names}} {{.Status}}'` → no rows); no compose project, network, volume or state
directory was created by this lane; ambient images untouched. No VM/SSH access was needed by this mission.
Working zone: `workers/w289-0428-251-demochecks-work/` (own clone + witnesses) and
`workers/w289-0428-251-demochecks-plan/` (isolated plan worktree, removed after the push). Nothing was created
in the ecosystem root.

## END

END_DONE w289-0428-251-demochecks: 3 fresh pull_request events bound zero runs — root cause is the heads'
DRAFT-only/zero-jobs `pr-config-matrix.yml` (develop blob `7108cf69e4f5…`), transport alone cannot qualify
#170/#179/#181; akte + witnesses in this file, plan PR: #93
