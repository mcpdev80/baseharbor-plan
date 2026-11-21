# Review 2 — PR #1747

ROLLE: REVIEW

## PLAN

- Read mission, reconcile task and verify live PR/base state. Done.
- Inspect exact candidate diff, route tests, mutation evidence, and hosted checks. Done.
- Write SHA-specific review verdict. Done.
- Publish only this evidence file and verify it on origin/main. In progress.
- Post final lane status with candidate SHA. Pending.

## Candidate and provenance

- Card: `t-20261114-r28-cli2-app-lifecycle` (0428-060); PR: `https://github.com/mcpdev80/baseharbor/pull/1747`.
- Git remote check in product checkout: `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `(push)`; all product remote reads used `lane-origin`.
- Planning remote check: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- PR state: OPEN, draft=false, mergeable=MERGEABLE, baseRefName=develop, headRefName=lane-0428-060-updown.
- Exact PR head from `gh pr view` and `git ls-remote` PR ref: `2d848f4469cfc43130f956f5080e5d33cda15138`.
- Exact fresh remote develop SHA: `ddfa80f7202a0aca3cf68c4542158132c0c2795b` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- `git merge-base --is-ancestor ddfa80f7202a0aca3cf68c4542158132c0c2795b refs/remotes/lane-origin/pr-1747`: exit 0.
- `git rev-list --count develop..head`: 3. `git rev-list --count head..develop`: 0.
- `git log --oneline develop..head`:
  - `2d848f446 0428-060 hop onto develop ddfa80f7202a (measured 2026-11-21)`
  - `663747436 0428-060 r2: put the down/stop consent seam on the registered command route`
  - `8103f0065 0428-060 converge down onto authorized lifecycle consent gate`
  These are the three lane commits carried by the candidate; no unrelated commit was observed.
- `git diff --name-only develop head`:
  - `cmd/baha/app_lifecycle.go`
  - `cmd/baha/app_lifecycle_down_convergence_test.go`
  - `cmd/baha/app_lifecycle_down_route_0428_060_test.go`
- Scope review: all three files are within the card's CLI lifecycle implementation and dedicated test scope. No `.github/**`, `scripts/**`, or listed prohibited paths appear in the diff.

## Review findings

1. The route-level regression addresses review-1 finding 1. In `cmd/baha/app_lifecycle_down_route_0428_060_test.go`, `runRegisteredRoute` at lines 217–226 invokes the `appDownCommand` or `appStopCommand` constructor route. `TestDownRouteWithoutConsentMakesNoChange` at lines 231–262 covers both verbs; it checks the refusal, no retirement banner, zero docker mutation calls, byte-identical deployment record, and byte-identical application store. `TestDownRouteWithConsentRunsRetirement` at lines 264–303 covers both verbs with `--yes` and asserts `runtime-retired` plus persistent runtime.env contents. These are substantive route tests, rather than direct boolean-helper tests.
2. Product code in `cmd/baha/app_lifecycle.go` wraps the shared stop command, adds the down mode before invoking the captured stop route, and places `downRequiresConfirmedConsent` before the stop mutation route. No direct authorization bypass was found in the reviewed diff. The existing retirement consequence-plan consent remains separate from `--yes`.
3. The requested mutation record could not be located. `rg --files evidence` returned no `0428-060` round-2/downroute mutation evidence; it found only review-1, parity evidence, and this review file. Thus the mission's required evidence that mutations in both directions turn the regression red is absent. The test code's assertions are reviewable, but they do not substitute for the requested mutation run record.

## Hosted checks

- Run `44908288698`, workflow `CI · Source & Quality`, event `pull_request`, exact head `2d848f4469cfc43130f956f5080e5d33cda15138`: terminal, conclusion `failure`.
- Required job `PR · Go unit · cli-3`, job `136858546552`: terminal failure. Its failing step is `Execute selected Go tests with isolated PostgreSQL` (step 5). The `gh run view --job 136858546552 --log-failed` and `--log` requests both failed locally with `failed to get run log: zip: not a valid zip file`.
- The check-run annotation for job `136858546552` reports: `Process completed with exit code 1.` This is the available failing log line; detailed per-test output could not be retrieved.
- Aggregate job `PR Selected Checks`, job `136859595083`: terminal failure at `Require complete selected Go shard coverage`; `gh pr checks 1747` reports `PR Selected Checks fail` and `PR · Go unit · cli-3 fail`. Other selected Go shards and validation jobs shown in that run passed; skipped jobs are not counted as passes.
- No rerun was triggered. The candidate has a required red check and cannot be accepted.

## Verdict

**REQUEST CHANGES — candidate `2d848f4469cfc43130f956f5080e5d33cda15138`.** The new command-route tests materially address the earlier coverage finding. Acceptance remains blocked by the terminal required CI failure in `PR · Go unit · cli-3` and the missing round-2 mutation evidence requested by the mission.

### Remediation recipe

- File/action: CI result for PR #1747, `PR · Go unit · cli-3` (job `136858546552`). Obtain the failed test output from the GitHub job log, fix the specific failure on the same candidate branch, and run the required checks under the repository policy. Do not change workflow files or dispatch a rerun from this review lane.
- File/action: Planning evidence `evidence/cli-redesign-20261114/0428-060/round-2-downroute.md` (or identify and link the actual location). Record the exact mutation commands, per-protocol three byte-counts from per-job logs, and results showing the route regression fails when the consent guard is removed in either direction. Keep this as evidence only; do not modify product code from the review lane.
- Stop criterion: exact candidate checks are terminal and required checks pass; the mission's mutation record is present and shows both guard-removal mutations are detected.

END codex-rev-1747 DONE: review result persisted for candidate `2d848f4469cfc43130f956f5080e5d33cda15138`.
