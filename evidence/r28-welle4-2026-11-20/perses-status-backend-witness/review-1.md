# Exact-head review — PR #1702 / card 0428-142

ROLLE: CODEX-REVIEW

**VERDICT: REQUEST CHANGES**

## PLAN

1. Verify the exact PR head, base, branch/PR refs, current develop, #1594 ancestry, and the candidate write-set.
2. Read the current 0428-142 contract and cited lane/review evidence; inspect own-run and cleanliness witnesses.
3. Check whether develop's `verify_none_red_test.go` is duplicate, continuation, or unrelated to this candidate.
4. Assess current-base CI risk after #1594 and record the exact supporting job/log evidence.
5. Recheck the candidate identity and record the verdict and actionable recipes; do not merge, push, rerun, dispatch, or edit the PR.

## Candidate identity and write-set

```text
$ gh api repos/mcpdev80/baseharbor/pulls/1702 --jq '[.head.sha,.base.sha,.base.ref,.state,.draft,.mergeable,.mergeable_state,.updated_at]'
["6740299f91c040af7b1357d63be898eac57669f5","28fb427f057499efca705c1b7459e7653bd532a8","develop","open",false,true,"behind","2026-11-20T03:26:59Z"]
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-142-statuswitness refs/pull/1702/head refs/pull/1594/head
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
d8a7b9c30bda10d2f5e0d6d6140a348995169834 refs/pull/1594/head
6740299f91c040af7b1357d63be898eac57669f5 refs/pull/1702/head
$ gh api repos/mcpdev80/baseharbor/pulls/1702 --jq '[.head.ref,.head.sha,.base.ref,.base.sha,.commits,.changed_files,.additions,.deletions]'
["lane-0428-142-statuswitness","6740299f91c040af7b1357d63be898eac57669f5","develop","28fb427f057499efca705c1b7459e7653bd532a8",8,13,378,63]
$ git merge-base --is-ancestor origin/develop origin/pr-1702; echo $?
1
$ git merge-base --is-ancestor origin/pr-1702 origin/pr-1594; echo $?
1
$ git diff --name-status 28fb427f057499efca705c1b7459e7653bd532a8...origin/pr-1702
M cmd/baha/app_perses_access_cli_test.go
M cmd/baha/app_perses_cli_test.go
M cmd/baha/app_status_collect.go
M cmd/baha/app_status_result.go
A cmd/baha/app_status_result_test.go
M cmd/baha/perses_lifecycle.go
M internal/application/management_ui.go
M internal/application/perses_lifecycle.go
M internal/application/perses_lifecycle_test.go
M internal/application/perses_runtime.go
M internal/application/perses_runtime_test.go
M internal/capability/perses.go
M internal/capability/perses_security_test.go
$ git log --oneline 28fb427f057499efca705c1b7459e7653bd532a8..origin/pr-1702
6740299f Merge remote-tracking branch 'origin/develop' into lane-0428-142-statuswitness
56d85ddb hopf onto develop (c988783a): integrate Perses security-policy feature, align enum PersesStatusConfiguredUnverified->configured, gofmt
c988783a Merge remote-tracking branch 'origin/develop' into lane-0428-142-statuswitness
3bdc16d6 ci: re-trigger PR Selected Checks for e679df7a (no content change)
e679df7a Merge remote-tracking branch 'origin/lane-0428-142-statuswitness' into lane-0428-142-statuswitness
def500fb fix(0428-142 r1): migrate Perses public status vocabulary to approved set (configured, not the excluded configured_unverified)
02c97889 fix(0428-142 r1): migrate Perses public status vocabulary to approved set (configured, not the excluded configured_unverified)
e22f6795 feat(0428-142): per-signal perses backend-witness (manifest-only)
```

The current develop tip is `40cb28c758b02960356434b630086a341ebe1738`, and #1594's head `d8a7b9c...` is not an ancestor of #1702. The PR's declared base is `28fb427f...`; therefore its green checks are not current-base currency.

## P1 — backend witness is still manifest-only (BLOCKER)

The task goal/acceptance requires each signal's backend outcome (reached and matched, reached with no match, or unreachable) with a source ID. In the candidate, `cmd/baha/app_status_result.go:76-139` is explicitly `persesBackendSignalWitnessFromManifest`. Its positive branches set `configured` solely from `application.HasMetricsSources`, `HasLogsCollection`, and `HasOTLPTelemetry` (`:92-98`, `:108-114`, `:124-130`). No backend response or stream-match result is read. `persesBackendUnreachable` is declared at `:64-65`, but this function has no branch that emits it. The test `cmd/baha/app_status_result_test.go:60-91` constructs manifest flags and asserts all three backends `configured`; it does not reach a backend witness.

The cited prior review `evidence/r28-welle4-2026-11-19/codex-review-wave/1702-0428-142-r4.md`, P2/P4, identifies this same unsatisfied requirement. The lane's `fix-3.md:33-44,61-69` reproduces it and stops rather than fabricating a backend answer. This candidate does not close that blocker.

Recipe: after the contract decision in 0428-143, route authoritative source-ID-bound per-backend evidence into both status output paths (`cmd/baha/app_status_result.go` and `cmd/baha/perses_lifecycle.go`). Add one test per backend outcome (match, no match, error/unreachable), with independent Loki/Tempo/Prometheus ownership, and assert exact source ID plus state in machine and human output. Stop if 0428-143 has not authorized the `Verification=none` treatment or if a backend's own result cannot be obtained inside the card's permitted write-set; do not infer reachability from manifest selection.

## P2 — card scope boundary is crossed (BLOCKER)

The task card scope explicitly marks `internal/capability/perses.go` out of scope and says to stop and ask the coordinator if it is touched. The exact candidate changes that file: `git diff --name-status` lists it, and the candidate diff renames the public status constant and changes `PersesStatusNow`/`PersesConfiguredStatusNow` (`internal/capability/perses.go:206-255`, plus security tests). The PR also changes `internal/application/management_ui.go`, `perses_lifecycle.go`, and `perses_runtime.go`, which are outside the current handoff's stated `cmd/baha` status-result/test files. The lane record acknowledges this history; it is not a documented scope release in the card.

Recipe: the owner/coordinator must resolve the write-set before another acceptance attempt. Either remove the unauthorized capability/runtime edits from this PR and keep the documented status scope, or explicitly amend the card's scope and dependencies before review. Stop while `internal/capability/perses.go` remains touched without that decision. Tests must cover the exact approved status behavior after the scope is settled.

## P3 — existing `verify_none_red_test.go` is not duplicate work

```text
$ git cat-file -e origin/develop:internal/metrics/verify_none_red_test.go; echo $?
0
$ git diff --name-only 28fb427f057499efca705c1b7459e7653bd532a8...origin/pr-1702 -- internal/metrics/verify_none_red_test.go
```

The file exists on develop and is not in the PR write-set. Its `TestRedAllVerificationNoneHasNoCompositionCounter` and `TestVerificationNoneCompositionReportsNullTargetState` test Prometheus scrape-target composition for `Verification=none` (`internal/metrics/verify_none_red_test.go`, candidate base's develop file). This PR's new tests exercise CLI status formatting from manifest fields (`cmd/baha/app_status_result_test.go`). The test is therefore neither continued nor made redundant by #1702; the two tests cover different contracts. No removal/correction of the existing metrics test is warranted.

## P4 — merge-order and current-base CI risk after #1594

`#1594` is now merged: `gh api repos/mcpdev80/baseharbor/pulls/1594` reports `merged=true`, merge commit `40cb28c758b02960356434b630086a341ebe1738`, and develop points at that commit. #1594 changed workload/operator-auth policy (`internal/application/workload_security.go`, `internal/operatorauth/config.go`, `internal/serviceaccess/policy.go` and tests). Its exact-head check-runs show `PR Selected Checks=success` and `PR · Validation · authority-package-tests=success`, while the ordinary CLI Go unit shards are skipped.

A real pull-request run on the current develop base after that merge demonstrates the risk:

```text
$ gh api repos/mcpdev80/baseharbor/actions/runs/44774783515 --jq '[.id,.head_sha,.event,.status,.conclusion]'
[44774783515,"ce5aa9633630b88a017f501da7c2f0bd00e44714","pull_request","completed","failure"]
$ gh api repos/mcpdev80/baseharbor/commits/ce5aa9633630b88a017f501da7c2f0bd00e44714/check-runs --jq '[.check_runs[]|select(.name=="PR Selected Checks" or (.name|startswith("PR · Go unit · cli-")))|{name,status,conclusion}]'
PR Selected Checks: completed/failure
PR · Go unit · cli-0: completed/failure
PR · Go unit · cli-1: completed/failure
PR · Go unit · cli-2: completed/failure
PR · Go unit · cli-3: completed/failure
```

The run's base is the current develop `40cb28c...` plus a test-only PR; its failure output includes:

```text
PR · Go unit · cli-0: main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.
PR · Go unit · cli-1: registration_ci_readiness_test.go:118: ... error:map[code:authentication_failed message:Managed-environment machine operations require an authenticated BaseHarbor operator. ...]
PR · Go unit · cli-2: app_secrets_shared_runtime_test.go:44: ... operator OIDC configuration is required for managed environments
PR Selected Checks: UNIT_SCOPE: cli; UNIT_RESULT: failure
```

Ja, nach dem Merge wäre develop teilweise rot. The exact failing PR was #1718, not #1702, so this is evidence of current-base CLI regression risk rather than a claim that #1702 itself caused those failures. #1702's green run used the older `28fb427f` base. Its required aggregate is not a safe substitute for a new current-base result: the active ruleset `25223521` requires only `PR Selected Checks` and has `strict_required_status_checks_policy=true`; PR #1702 is `behind` and cannot be accepted as current-base green. The merge order should account for the CLI failures and 0428-204 as the owner indicated.

Recipe: do not merge #1702 ahead of the current-base CLI failure resolution. Once the owning work fixes those failures and the merge order is settled, obtain a new exact-current-base run with `PR Selected Checks` success and all required CLI shards executed. Stop if the aggregate remains red, any required shard is skipped, or the PR is still behind the base used by the active strict rule.

## P5 — own-run and cleanliness evidence

```text
$ gh api repos/mcpdev80/baseharbor/actions/runs/44621032956 --jq '[.id,.head_sha,.event,.status,.conclusion,.created_at,.updated_at]'
[44621032956,"6740299f91c040af7b1357d63be898eac57669f5","pull_request","completed","success","2026-11-19T21:39:56Z","2026-11-19T21:44:55Z"]
$ gh api repos/mcpdev80/baseharbor/actions/runs/44621032956/jobs --jq '[.jobs[]|select(.name=="validate" or .name=="PR · Go unit · cli-0" or .name=="PR · Go unit · cli-1" or .name=="PR · Go unit · cli-2" or .name=="PR · Go unit · cli-3")|{name,status,conclusion}]'
validate: completed/skipped
PR · Go unit · cli-0: completed/success
PR · Go unit · cli-1: completed/success
PR · Go unit · cli-2: completed/success
PR · Go unit · cli-3: completed/success
```

The lane's `fix-3.md:25-28` identifies the run at the exact candidate SHA and says it was unchanged this shift; `fix-2.md:45-54` records the push/run-watch procedure. This satisfies the own-run/terminal witness for the unchanged head. However `fix-2.md:35,101-108` incorrectly claims `validate => success` and “no runtime cells skipped”; the run API says `validate=skipped`. `fix-3.md:56-59` does provide the required literal `cleanliness: clean` line and states that no containers/compose/volumes/networks were started.

Recipe: correct `fix-2.md:35,105-108` to the API state, including `validate=skipped` and the relevant skipped optional cells; retain the correct exact-head run and aggregate result. Stop if the run API cannot substantiate an evidence claim. The clean host statement itself is present in fix-3.

## Verdict

REQUEST CHANGES. The candidate still fails the central backend-evidence acceptance, crosses the task's hard capability-file boundary, and has a stale-base CI result while current-base CLI checks are known red. The existing verification-none regression test is unrelated and remains useful. No merge is authorized by this review.

## Review record

- Candidate before review: `6740299f91c040af7b1357d63be898eac57669f5`.
- Candidate after review: pending final `ls-remote` below; expected unchanged.
- Session identifier: not exposed in this API session.
- Model/backend: Codex GPT-6.2 API runtime; backend identifier not exposed.
- Review time: 2026-11-20 22:57 UTC.
- Read: task card, befund-1.md, fix-1.md, fix-2.md, fix-3.md, prior r4 verdict, candidate source/tests/diff, develop test file, PR #1594 metadata/checks, exact candidate run/jobs, current-base run #44774783515/logs, active ruleset.

Final read-only identity recheck:

```text
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-142-statuswitness refs/pull/1702/head
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
6740299f91c040af7b1357d63be898eac57669f5 refs/heads/lane-0428-142-statuswitness
6740299f91c040af7b1357d63be898eac57669f5 refs/pull/1702/head
$ gh api repos/mcpdev80/baseharbor/pulls/1702 --jq '[.head.sha,.base.sha,.state,.draft,.mergeable,.mergeable_state]'
["6740299f91c040af7b1357d63be898eac57669f5","28fb427f057499efca705c1b7459e7653bd532a8","open",false,true,"behind"]
```

PR head before/after review = `6740299f91c040af7b1357d63be898eac57669f5/6740299f91c040af7b1357d63be898eac57669f5`.

Plan clone remote (verified): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Per the mission's explicit read-only rule, this verdict file is local to the plan clone; no commit or push was made.

END_DONE codex-rev-cli2b / PR #1702 review: REQUEST CHANGES; candidate `6740299f91c040af7b1357d63be898eac57669f5`.
