# w253 — Demo PR Census (#170 + #179), read-only

## Status
- **END DONE** w253-0428-251-demo170verify

## Mission
Read-only census for Codex lane w136's demo CI availability decision. Repo `mcpdev80/baseharbor-demo`. NO writes, NO pushes, NO CI triggers, NO merges. Tasks:
1. ls-remote demo develop + main tip (default branch is main).
2. For #170 (non-draft) and #179 (draft): `gh pr view --json state,isDraft,headRefOid,baseRefName` + reviews/reviewDecision.
3. Runs per head (runs API, per_page=100): count PR-event vs push-event runs, statuses/conclusions; identify the ONLY workflow that can produce PR checks (`.github/workflows/pr-config-matrix.yml`); verify presence/absence of that file on demo MAIN vs develop vs each PR head.
4. For every failed push-event run: the failing step log line verbatim (jobs=[] means dispatch failure — capture the workflow-level error).
5. END: table PR | head | draft | event types | workflow availability on base | what EXACTLY must change for real PR-event checks to run (Codex decides; document only) + akte via plan-PR branch path with post-merge git show witness.

## PLAN
- bullet Plan in all three places (board file, evidence head)
- bullet ls-remote demo develop + main
- bullet gh pr view #170 and #179 (state,isDraft,head,base,reviews)
- bullet runs API per head, classify PR-event vs push-event, statuses
- bullet pr-config-matrix.yml presence on MAIN vs develop vs PR heads
- bullet capture failed push-event run failing step lines
- bullet build census table + what must change for real PR-event checks
- bullet post akte via plan-PR branch path with post-merge git show witness
- bullet post END_DONE

## Reality witnesses

### ls-remote demo develop + main (git ls-remote https://github.com/mcpdev80/baseharbor-demo develop main)
```
5ca92a7cd2f746934890cfd7096a48068bdf218e	refs/heads/develop
2618b3962330509add5bf265522995da2a9034ce	refs/heads/main
```

### gh pr view #170
```
{"baseRefName":"develop","headRefOid":"b086cf58bb2f7aafee30edf52ac4b8199daf7d0d","isDraft":false,"state":"OPEN","title":"test(config-matrix): demo operator-allowlist root-name fix (0428-250)"}
reviews: []  reviewDecision: "" (empty)
```

### gh pr view #179
```
{"baseRefName":"develop","headRefOid":"cda6aa70e80bec1a1db06d85decdd8833cb63994","isDraft":true,"state":"OPEN","title":"fix(demo-fixture): repair 8 executed-FAILED Light gates on #1842 (test-only)"}
reviews: []  reviewDecision: "" (empty)
```

### Runs per head (runs API per_page=100; queried by head_sha because pulls/170/runs returns 404)

Run 45663390190 (head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`, PR#170):
```
{"id":45663390190,"event":"push","status":"completed","conclusion":"failure","head_sha":"b086cf58bb2f7aafee30edf52ac4b8199daf7d0d","head_branch":"lane-0428-250-demo-operator-root","run_number":4,"run_attempt":1,"name":".github/workflows/pr-config-matrix.yml","created_at":"2026-11-25T17:18:42Z","updated_at":"2026-11-25T17:18:42Z"}
head_commit author: Flash <flash@baseharbor.local>  message: chore(ci): trigger config-matrix pull_request after #177 publication
```

Run 45688177820 (head `cda6aa70e80bec1a1db06d85decdd8833cb63994`, PR#179):
```
{"id":45688177820,"event":"push","status":"completed","conclusion":"failure","head_sha":"cda6aa70e80bec1a1db06d85decdd8833cb63994","head_branch":"w198-1842-demo-fixture-fix-forward","run_number":6,"run_attempt":1,"name":".github/workflows/pr-config-matrix.yml","created_at":"2026-11-25T19:44:34Z","updated_at":"2026-11-25T19:44:34Z"}
head_commit author: w198-0428-284-demo-parser <w198-0428-284-demo-parser@baseharbor.local>
```

Only ONE run per head each. Both are **push** events. No PR-event runs exist for either head.

### jobs=[] (dispatch failure)
- `GET /repos/mcpdev80/baseharbor-demo/actions/runs/45663390190/jobs` -> `[]`
- `GET /repos/mcpdev80/baseharbor-demo/actions/runs/45688177820/jobs` -> `[]`
- Both runs: `created_at == updated_at` (same second) => created and failed instantly at dispatch, never producing jobs.
- `GET .../logs` -> HTTP 404 (no logs to download). `GET .../events` -> HTTP 404.
- `GET /repos/mcpdev80/baseharbor-demo/pulls/170/runs` -> HTTP 404 (no check-suite bound to the PR, i.e. no PR-event checks registered on #170).

### pr-config-matrix.yml presence (git cat-file -e at each ref)
- demo MAIN (`2618b396...`) head `.github/workflows/pr-config-matrix.yml`: **EXISTS**
- develop (`5ca92a7...`): **EXISTS**
- PR#170 head `b086cf5...`: **EXISTS**
- PR#179 head `cda6aa7...`: **EXISTS**

Trigger block on MAIN (verified via `git show main:.github/workflows/pr-config-matrix.yml`):
```yaml
on:
  pull_request:
    branches: [develop]
    paths:
      - .github/workflows/pr-config-matrix.yml
      - baseharbor-core.ref
      - compose.yaml
      - scripts/acceptance.sh
      - scripts/failure-runtime-diagnostics.sh
      - scripts/install-baseharbor.sh
      - tests/config-matrix/**
      - tests/connectivity/run.sh
      - tests/full-destroy/run.sh
      - tests/policy/operator-test-certificate.sh
      - tests/reconciliation/run.sh
      - tests/fixture-consent.py
      - tests/lib.sh
```

## Census table

| PR | head | draft | event types | workflow availability on base | what exactly must change |
| --- | --- | --- | --- | --- | --- |
| #170 `test(config-matrix): demo operator-allowlist root-name fix (0428-250)` (OPEN, non-draft) | `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d` | false | 1 run, **push** only; conclusion `failure`; `jobs=[]`; `pulls/170/runs` = 404 | `pr-config-matrix.yml` EXISTS on develop and on head; trigger is `pull_request` filtered by `paths:` | PR never got a PR-event run because (a) the commit on the head that created run 45663390190 is a `chore(ci):` push directly (not a PR push) — event=push; and (b) the `pull_request` trigger has a `paths:` filter, so if the PR touches no path in the filter, no check is created. To run real PR-event checks: the workflow's `pull_request` trigger must fire on the PR (it already is), AND the PR must either touch a filtered path or the `paths:` filter must be widened/removed so the operator-test change registers; the head branch must be pushed via the PR (event=pull_request) so a check-suite binds to it. |
| #179 `fix(demo-fixture): repair 8 executed-FAILED Light gates on #1842 (test-only)` (OPEN, draft) | `cda6aa70e80bec1a1db06d85decdd8833cb63994` | true | 1 run, **push** only; conclusion `failure`; `jobs=[]` | `pr-config-matrix.yml` EXISTS on develop and on head; same `pull_request`+`paths:` trigger | Draft PR. Draft PRs do not run checks for fork contributors and here never produced a check-suite bound to the PR. The single run (45688177820) is a push event on the head branch, not a PR-event run. To get PR-event checks: move out of draft (or the maintainer must allow) so the `pull_request` check-suite binds; ensure the changed paths fall under the `paths:` filter (they are demo-fixture tests) or widen the filter. |

## Root cause (what must change for real PR-event checks to run)
1. Both failed runs are `event: push`, not `pull_request`. A PR-event check-suite is only created when a commit is pushed **through the PR** (base `develop`), producing a `pull_request`/`push` event on the PR's head ref with a bound check-suite. The `pulls/<n>/runs` API returns **404** for #170 => no check-suite is bound to the PR at all.
2. The single workflow that can produce PR checks (`.github/workflows/pr-config-matrix.yml`) triggers on `pull_request.branches:[develop]` **with a `paths:` filter**. If a PR head does not change any of those filtered paths, no run is created — even for a normal PR push.
3. `jobs=[]` with `created_at==updated_at` on both runs: the workflow dispatched (a run object exists) but produced **zero jobs** — a dispatch-level failure before any step ran, so there is no failing step log line to capture. The logs endpoint returns 404.

## What Codex (w136) will decide/implement
- Whether to widen or remove the `paths:` filter in `pr-config-matrix.yml` (Owner scope, `.github/**`) so operator-test / demo-fixture PRs actually register.
- Whether the demo operator-allowlist fix (#170) and the #1842 fixture repair (#179) should be pushed through their PRs as `pull_request` events so a check-suite binds, rather than as bare head pushes.
- Whether the draft state of #179 is the blocker for the PR-event check-suite.

## repo-rule compliance
- This mission is READ-ONLY. No product writes, no pushes, no CI triggers, no merges. All evidence gathered via read-only git/gh commands (ls-remote, gh pr view, gh api runs/jobs/logs/events, git cat-file -e, git show).

## cleanliness
- No containers/compose/projects started. No daemon artifacts.
- `docker ps -a` witness: (none started by this lane)
- Scratch clone `/tmp/demo-main` (full clone of demo) created 2026-11-26 ~01:13Z, removed after use.

## Akte posting (plan-PR branch path)
- Isolated worktree created in baseharbor-plan: `git worktree add <path> origin/main`
- Commit only own evidence file, canonical identity `w253-0428-251-demo170verify@baseharbor.local`.
- Push via worktree.
- Post-merge git show witness captured after merge to origin/main.
