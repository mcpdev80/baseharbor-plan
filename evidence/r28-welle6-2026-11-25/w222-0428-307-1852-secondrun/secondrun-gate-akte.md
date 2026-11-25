# w222-0428-307-1852run2 — SECONDRUN GATE #1852 + #1819 (content-neutral close/reopen)

Lane: w222-0428-307-1852run2 (session 1e9393b3-d2e1-4503-b130-c302a417c2e7). Mission: coordinator/missions/w222-1852-secondrun.txt
Date: 2026-11-25 (local +01:00)

## PLAN
1. Plan created in all three places (board json + evidence + todo tooling).
   - todowrite note: this harness (opencode on worker-flash) exposes no native todo tool; the execute catalog has no task tools (probed: `Unknown tool 'opencode.task_create'`). Per mission instruction "if unsure, skip leg (0) entirely". Board file `workers/todos/w222-0428-307-1852run2.json` is the live track, ticked as I work; this PLAN list is the second, mandatory track.
2. gh auth OK; exact heads of #1852/#1819 BEFORE witness (gh api pulls/N).
3. Baseline census of existing PR-event runs per PR (per_page=100).
4. #1852: gh pr close + gh pr reopen; head-unchanged AFTER witness.
5. Watch #1852 fresh pull_request run to terminal; Trusted Plan + Selected Checks green; diff develop...HEAD = +27/0 (3 rows).
6. #1819: gh pr close + gh pr reopen; head-unchanged AFTER witness.
7. Watch #1819 fresh PR-event run to terminal; no REQUIRED gate stays skipped (Consumer Pins note).
8. Evidence committed+pushed to baseharbor-plan origin/main via isolated worktree.
9. END post to coordinator with both new run IDs + witnesses.

## ANSATZ
- No commits, no pushes to product repos, no merges, no card changes. Pure GitHub-side PR close/reopen toggle (these are `gh pr close`/`gh pr reopen`, NOT workflow_dispatch, NOT reruns, NOT .github/** edits).
- Card frontmatter owner (verbatim from origin/main, fetched at runtime): `owner: ""` — card t-20261125-hunt37-runtime-identity-fallback (card_number "0428-307"), unassigned. This lane makes no card change.
- Identity admission: NO candidate commit is created by this lane, so no `git -c` commit invocation and no pre-push `%an` gate apply to a product branch. The only commit is the planning-repo evidence commit, authored with the lane identity:
  `git -c user.name=w222-0428-307-1852run2 -c user.email=w222-0428-307-1852run2@baseharbor.local commit ...`
  with gate `git show -s --format=%an HEAD` == `w222-0428-307-1852run2` before push.
- Remote resolution: only URLs containing github.com/mcpdev80 are used; gh uses the API directly. `git -C .../baseharbor remote -v` shows 7 lines all resolving to https://github.com/mcpdev80/baseharbor.git (no filesystem-path remote).
- Runner hygiene: no containers, no compose projects, no VM needed → nothing to bring down; no test containers started on this host.

## Witnesses

### gh auth + remote resolution (first git actions)
- `gh auth status`: logged in to github.com as mcpdev80.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v` → 7 remote URL lines, all `https://github.com/mcpdev80/baseharbor.git` (lane-origin/origin/upstream fetch+push).

### Head BEFORE witness (gh api pulls/N)
```
1852 head=d3db4d898414ead953afcda530155fdef8b227cf state=open draft=false base=28296a2e6e920592741c9397486358deac7e95b2
1819 head=b3c5055ad2566b639c2b0d4f4c2848b045221ebf state=open draft=false base=28296a2e6e920592741c9397486358deac7e95b2
```
Both match the mission-mandated heads exactly.

### Baseline run census (event=pull_request, exact head)
```
PR #1852 head d3db4d89: run 45693544910 "CI · PR #1852" completed/success created 2026-11-25T20:17:34Z (ONLY prior PR-event run)
PR #1819 head b3c5055a: run 45694363486 "CI · PR #1819" completed/success created 2026-11-25T20:22:38Z (ONLY prior PR-event run)
```

## Actions

### #1852 close/reopen — DONE

Sequence (one lane, own session, ordinary `gh pr close` then `gh pr reopen`; no workflow_dispatch, no rerun, no .github/** edit):

```
$ gh pr close 1852 --repo mcpdev80/baseharbor
✓ Closed pull request mcpdev80/baseharbor#1852 (fix(0428-307 carrier): catalog runtime-identity workload lifecycle gates)
$ gh pr reopen 1852 --repo mcpdev80/baseharbor
✓ Reopened pull request mcpdev80/baseharbor#1852 (fix(0428-307 carrier): catalog runtime-identity workload lifecycle gates)
$ gh api repos/mcpdev80/baseharbor/pulls/1852 --jq 'head/state/draft'
1852 head=d3db4d898414ead953afcda530155fdef8b227cf state=open draft=false
```

Head-unchanged witness: BEFORE `d3db4d89…227cf` == AFTER `d3db4d89…227cf`.

Fresh run (event=pull_request, exact head):

```
45699226646  CI · PR #1852  pull_request  completed  success  created 2026-11-25T20:53:25Z
45693544910  CI · PR #1852  pull_request  completed  success  created 2026-11-25T20:17:34Z   (prior, baseline)
```

Executed-not-skipped census for 45699226646 (per_page=100 job listing, all `completed`):

- success: Workflow policy, PR · Trusted Plan, PR · Native gate plan, PR · Source format, PR · Focused Python, PR Selected Checks, PR · Validation (receipt-execution-tests, pr-planner-tests, ci-policy, ci-executor-tests), PR · Candidate-added checks (advisory)
- skipped: release/HA/matrix gates outside PR scope (Consumer Pins, Demo Pin, Exact Candidate, Exact full Pre-Release, Go unit shards, Main release checks/Go/source, Native shards, Native Keycloak/Core, Public Contracts, Runner Interface, Draft Go/source-and-routing, Selected Core-less, Selected Runtime, Release Source Preflight, Targeted HA docker/podman, Targeted Workstation onboarding, validate)
- No executed job failed. **PR · Trusted Plan = success** and **PR Selected Checks = success** (the two required aggregates).

Diff invariant re-verified on the exact head (gh PR files API + `gh pr diff`):

```
scripts/pr-gate-coverage.json   +27  -0
```
One file, 27 additions, 0 deletions; the added lines are exactly the 3 runtime-identity catalog rows
(`source.internal_application_runtime_identity_workload_go`,
`…_workload_fallback_test_go`, `…_workload_test_go`).

Two distinct exact-head pull_request run IDs for #1852: **45693544910** (prior) and **45699226646** (new second run), both success on `d3db4d898414ead953afcda530155fdef8b227cf`.

### #1819 close/reopen — DONE

Same content-neutral pattern:

```
$ gh pr close 1819 --repo mcpdev80/baseharbor
✓ Closed pull request mcpdev80/baseharbor#1819 (0428-181 wire Perses identity dashboard into export path)
$ gh pr reopen 1819 --repo mcpdev80/baseharbor
✓ Reopened pull request mcpdev80/baseharbor#1819 (0428-181 wire Perses identity dashboard into export path)
$ gh api repos/mcpdev80/baseharbor/pulls/1819 --jq 'head/state/draft'
1819 head=b3c5055ad2566b639c2b0d4f4c2848b045221ebf state=open draft=false
```

Head-unchanged witness: BEFORE `b3c5055a…21ebf` == AFTER `b3c5055a…21ebf`.

Fresh run (event=pull_request, exact head):

```
45699760220  CI · PR #1819  pull_request  completed  success  created 2026-11-25T20:56:53Z
45694363486  CI · PR #1819  pull_request  completed  success  created 2026-11-25T20:22:38Z   (prior, baseline)
```

Executed-not-skipped census for 45699760220 (job listing, all `completed`; observed to terminal in-session):

- success: Workflow policy, PR · Trusted Plan, PR · Native gate plan, PR · Source format, PR · Focused Python, PR Selected Checks, PR · Exact Candidate, PR · Demo Pin, PR · Runner Interface, PR · Go unit (cli-0..3, owner, packages), PR · Validation (ci-actionlint, ci-executor-tests, ci-policy, go-build, go-vet, pr-planner-tests, receipt-execution-tests), PR · Candidate-added checks (advisory), PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities
- skipped: Consumer Pins, Draft Go shards, Draft source and routing, Exact full Pre-Release, Main release checks/Go/source, Native shards, Native Keycloak/Core, Public Contracts, Selected Core-less, Release Source Preflight, Targeted HA docker/podman, Targeted Workstation onboarding, validate
- **No REQUIRED gate stayed skipped:** PR · Trusted Plan = success and PR Selected Checks = success (both re-confirmable via the check-runs API on BOTH the prior and the new run). No executed job was anything but success.
- `Consumer Pins` skipped — same as the prior run (45694363486). No required-gate skip detected; its planner-route membership is a planning question outside this content-neutral mission (no card/plan edits allowed), so it is flagged as STATE only, not a blocker.

## cleanliness
- No containers, networks, volumes or compose projects were created by this lane: only `gh`/`git` reads and the PR close/reopen commands. Nothing to bring down.
- No scratch files created in /home/marcel/dev/baseharbor-ecosystem (this evidence file lives in workers/, the board json in workers/todos/).

## END STATUS
END_DONE w222-0428-307-1852run2: second Hosted runs delivered for BOTH PRs, heads unchanged, no commits/pushes/merges/cards touched.
- PR #1852: head d3db4d898414ead953afcda530155fdef8b227cf unchanged (before/after witnesses above); new run **45699226646** (pull_request, completed/success) joins prior run **45693544910** = two distinct exact-head IDs; Trusted Plan + PR Selected Checks green; diff develop...HEAD = +27/0, exactly the 3 runtime-identity rows in scripts/pr-gate-coverage.json.
- PR #1819: head b3c5055ad2566b639c2b0d4f4c2848b045221ebf unchanged (before/after witnesses above); new run **45699760220** (pull_request, completed/success) joins prior run **45694363486** = two distinct exact-head IDs; no required gate skipped (Consumer Pins skipped as before, reported as STATE above).

## Publishing proof
```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep w222-0428-307-1852-secondrun
evidence/r28-welle6-2026-11-25/w222-0428-307-1852-secondrun/secondrun-gate-akte.md
$ git ls-remote origin refs/heads/main
43900085d94d449b28e5ec2693ce33690bf54281	refs/heads/main
```
Evidence commit 43900085d94d449b28e5ec2693ce33690bf54281 (author w222-0428-307-1852run2; pre-push gate: git show -s --format=%an HEAD -> w222-0428-307-1852run2). Planning remote: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v -> https://github.com/mcpdev80/baseharbor-plan.git (origin/upstream2).
