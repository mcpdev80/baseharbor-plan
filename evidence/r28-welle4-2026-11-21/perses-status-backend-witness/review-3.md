ROLLE: REVIEW
**Verdict: REQUEST CHANGES**

# PR #1702 — 0428-142: Perses status backend witness

## PLAN

1. Read the mission, task evidence, and prior review; confirm PR identity and exact head from GitHub refs.
2. Inspect the exact candidate diff and production call path for the human Perses status witness.
3. Read hosted checks and logs for the exact head; distinguish observed failures from inaccessible evidence.
4. Check the changed-file set against the explicitly protected PRs and files.
5. Re-read PR head and refs, write this verdict, and publish only this evidence file.

## Candidate and session

- Candidate: `mcpdev80/baseharbor#1702`, branch `lane-0428-142-statuswitness`.
- Head before review: `2b1fdcc06d9e07de583fea5140e020597bd2a18d`.
- Base: `develop` at `40cb28c758b02960356434b630086a341ebe1738`.
- Session: Codex review session; session identifier is not exposed in this interface.
- Model/backend: GPT-6.2, Codex API session.
- Review timestamp: 2026-11-21 04:43 UTC.
- Remote path witness from the initial `git remote -v`:
  `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch/push)`; `origin https://github.com/mcpdev80/baseharbor.git (fetch/push)`; `upstream https://github.com/mcpdev80/baseharbor.git (fetch/push)`; planning `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)`.
- `gh api repos/mcpdev80/baseharbor/pulls/1702 --jq '{head:.head.sha,base:.base.sha,state,draft,merged,updated_at}'`:
  `{"base":"40cb28c758b02960356434b630086a341ebe1738","draft":false,"head":"2b1fdcc06d9e07de583fea5140e020597bd2a18d","merged":false,"state":"open","updated_at":"2026-11-21T04:21:55Z"}`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-142-statuswitness refs/pull/1702/head refs/heads/develop`:
  `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop`
  `2b1fdcc06d9e07de583fea5140e020597bd2a18d refs/heads/lane-0428-142-statuswitness`
  `2b1fdcc06d9e07de583fea5140e020597bd2a18d refs/pull/1702/head`

## P1 — human witness renderer restored and production-reachable, but the CLI proof fails before reaching it

The candidate patch adds `renderPersesBackendWitness(out, result.BackendWitness)` to `cmd/baha/perses_lifecycle.go:92-94`, after `reportPersesSurfaceStatus` returns successfully at `:85-88`. The command registration routes the `status` subcommand to this `Run` function. `reportPersesSurfaceStatus` resolves the application at `:222-225`, enforces `authorizeApplicationOperation` at `:226-228`, then constructs the result and backend witness at `:229-236`. Thus the renderer is on the real human CLI path, but only after authorization succeeds.

The exact-head hosted log shows the new `TestPersesStatusWitnessHumanFaceRendersBackendWitness` was selected and run in `PR · Go unit · cli-1`, then failed at `cmd/baha/app_status_result_test.go:272` with `baha app perses status failed: operator authentication needs interactive setup but input is not a terminal`. The same run shows `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends` failing at `:311` with the same authentication error. Neither test reaches its backend-witness assertion in that run. The direct renderer-only test does not establish the production command result.

Recipe: in `cmd/baha/app_status_result_test.go`, configure the existing test operator authorization fixture/context for these command tests without weakening production authorization. Keep the test invoking `baha app perses status`, and assert the emitted backend witness after the command returns. Required test: the CI-executed human command test must reach and assert the expected backend names/source identities; removing the renderer call must make it fail at that assertion. Stop criterion: the command test passes through the real authorized path and a renderer-removal mutation makes that test fail for missing witness output, not at operator setup.

## P2 — exact-head CI state and log evidence

`gh api repos/mcpdev80/baseharbor/actions/runs/44865751734 --jq '{status,conclusion,head_sha,event,updated_at}'` reports `completed`, `failure`, exact head `2b1fdcc06d9e07de583fea5140e020597bd2a18d`, event `pull_request`, updated `2026-11-21T04:26:29Z`.

`gh run view 44865751734 --repo mcpdev80/baseharbor --json jobs,conclusion,headSha,event,updatedAt` reports `PR Selected Checks` failure; `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` failed. `owner`, `go-build`, `go-vet`, source format, Trusted Plan, native gate plan, focused Python, and cli-gofmt succeeded. Runtime/release-related jobs shown as skipped are not claimed as passes.

The mission expected this run's logs and the comparison run `44850246247` to return zero bytes. This review instead retrieved 1,260,466 bytes from `gh run view ... --log` and 369,072 bytes from `--log-failed` for `44865751734`; the exact-head log contains the two test failures cited in P1. `gh api repos/mcpdev80/baseharbor/actions/runs/44865751734/check-suites` returned `gh: Not Found (HTTP 404)`. Therefore the prior claim that this run's log is unavailable is not true in this review environment. I do not claim byte-identical failure lists against `44850246247`; its prior log retrieval was reported as empty, so that comparison remains unverified. The observed operator-auth error is consistent with the stated inherited failure class, but the new command test's assertion is still unproven because it exits before rendering.

Recipe: after correcting the test setup in P1, obtain a new normal PR run through the configured CI path; do not rerun or dispatch it from this review. Stop criterion: terminal `PR Selected Checks` success on the corrected exact head and the relevant CLI/package tests execute successfully.

## P3 — write-set overlap with owner-held PR work

`gh api repos/mcpdev80/baseharbor/pulls/1702/files --paginate --jq '.[].filename'` lists exactly `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`, and `cmd/baha/perses_lifecycle.go`. Neither `internal/observability/registry.go`, `internal/capability/perses_selection.go`, nor `.github/**` is in this PR diff.

I compared these paths with the file lists of PRs #1615, #1625, #1623, #1650, #1606, #1614, #1731, and #1704. `cmd/baha/app_status_result.go` overlaps PRs #1650, #1606, and #1614, so the stated restriction against files held by those PRs is violated. Comparison with #1615 alone returns no exact path overlap, but that does not remove the overlap with the other explicitly named owner-held PRs.

Recipe: resolve ownership of `cmd/baha/app_status_result.go` with the coordinator before another candidate update; then either remove this card's changes to that file and keep the witness output within its authorized write-set, or obtain an explicit write-set handoff that names the shared file and sequencing. Add/retain a regression for the selected human status path in the resulting authorized location. Stop criterion: the current diff has no owner-held overlap, or an explicit recorded handoff authorizes that exact file and ordering.

## Verdict rationale

The renderer line is restored in a production-reachable command path, but the exact-head CI test reaches an operator-authentication failure before its witness assertion, and the diff overlaps `cmd/baha/app_status_result.go` work in three explicitly named PRs. The exact-head required aggregate is failure. These are actionable blockers; this review does not make a content acceptance claim based on an unreachable assertion or a failed aggregate.

## Head stability

- PR head before review: `2b1fdcc06d9e07de583fea5140e020597bd2a18d`.
- PR head after review: `2b1fdcc06d9e07de583fea5140e020597bd2a18d`.
- `git ls-remote` before/after review had the same branch and PR-head SHA shown above.

END_DONE: review completed; candidate unchanged; verdict and blockers recorded.

## Planning publication witness

Command: `git -C /tmp/opencode/codex-rev-cli2b-plan fetch origin main && git -C /tmp/opencode/codex-rev-cli2b-plan ls-tree -r --name-only origin/main | grep '^evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-3.md$'`

Exact output:
`evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-3.md`
