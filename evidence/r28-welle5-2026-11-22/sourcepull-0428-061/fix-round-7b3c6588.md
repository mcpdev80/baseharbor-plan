# 0428-061 source pull — F1/F2 interim-review fix round (candidate 7b3c6588)

## WHAT

Interim read-only review of head e7df5ab4 (review-1752-heade7df5ab4.md) returned two provisional findings. This round fixes both. The review noted its findings are provisional and withholds final verdict pending a green exact #1752 run after the #1754 CI repair.

- **F1 (blocking, confirmed real):** On the `--up` SUCCESS path, `cmd/baha/app_pull.go` `runAppPull` wrote the bare pull result to `out` (via `writeJSON`/`writeSourcePullResult`), then `emitSourcePullUpComposite(out, ...)` wrote a SECOND JSON object to the same writer → two concatenated JSON values. The MCP handler unmarshals the combined buffer as ONE JSON value, so `up=true` failed decoding there too. Fixed: when `opts.Up` is set, the JSON path now emits ONLY the composite (`emitSourcePullUpComposite`) and the non-JSON path renders the pull result then the up section via a new `writeSourcePullUpHuman` helper (in `cmd/baha/app_pull_render.go`). The bare-result write no longer happens before the composite on the `--up` path. `runAppPull` still checks `result.Successful` before `opts.Up` and returns `ErrSourcePullBlocked` on partial failure.
- **F2 (test fix):** `TestAppPullMCPApprovalRegression` fixture (`app_pull_mcp_approval_regression_test.go`) wrote `baseharbor.yaml` into the cloned work tree WITHOUT committing it → the git source was dirty → the pull could fail on a dirty-tree blocker instead of the approval gate, making the test a false-positive risk. Fixed: fixture commits `baseharbor.yaml` so the working tree is clean. Assertions strengthened: `approval=false` must be refused with an exact approval-required message and classified code; `approval=true` must NOT receive an approval-refusal (proves the gate passed — the clean fixture then reaches a `source_missing` workspace-resolution error, not an approval error).

## WHY

Direct findings from the interim read-only review of e7df5ab4; both are real defects in the round-4 candidate. The F1 double-write is the original F1 defect resurfacing on the `--up` success path; the F2 dirty-tree is a test-fixture correctness issue.

## GATE

- Local verification (all green): ci-fast-check.sh — 295 tests OK, all gates pass (Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS: 20 approved files). `go vet ./cmd/baha/` clean. `go build /tmp/baha` clean. gofmt clean on all changed files.
- Targeted tests PASS: `TestEmitSourcePullUpCompositeIsSingleDocument`, `TestAppPullMCPApprovalRegression` (approval-required-refuses + approval-granted-proceeds-past-gate), `TestSourcePullApplyTimePartialFailureRunsOnce`, all 14 source_pull tests, plus the full pull/MCP test set.
- actionlint on .github/workflows/ci.yml: clean (zsh/fish install present at Draft Go cell ci.yml:1686, canonical validate cell ci.yml:348, Go unit cell ci.yml:1260).
- BLOCKER (open): exact hosted CI run for head 7b3c6588 has not yet executed. Per CI policy, success is only for the exact tested head with actually executed required jobs (SKIPPED/queued/absent is NOT a pass). Run 44974701796 (head e7df5ab4) was terminal FAILURE on cli-3 (zsh missing) — resolved now at ci.yml:1686.

## BRANCH PROVENANCE

- Base: develop 6209874428f08dc3e90d6e29a42b30683ce9932a, ancestor of HEAD (git merge-base --is-ancestor verified).
- `git log --oneline develop..HEAD` lists only lane commits: 7b3c6588 (F1/F2 interim fixes), e7df5ab4, b010dabc, a4adc29a, 719242df, 9140e0c8, 1c8e19f6, 73a2f084, 449c3f58, 6b9bb242, 403d718c, dab943e6. No foreign commits.
- PR #1752 head refs/pull/1752/head = 7b3c6588 (proven via git ls-remote). Non-force push.
- Changed files this round: cmd/baha/app_pull.go, cmd/baha/app_pull_render.go, cmd/baha/app_pull_options_test.go, cmd/baha/app_pull_mcp_approval_regression_test.go.
- CI: no .github/** change this round (zsh/fish install already landed at ci.yml:1686 in the prior round, validated with actionlint).

## repo-rule compliance

- nolocal respected for acceptance: targeted named-form test runs with the required skip set; ci-fast-check.sh, go vet, go build, gofmt all run locally and pass. No bare `go test ./cmd/baha/` (which starts real lifecycle containers).
- .github/** not edited this round.
- No subagents; no merge; PR kept Draft until gate complete.

## cleanliness

- No containers, compose projects, or runtime stacks started or left running. `docker ps -a`: only ambient bh-itest stacks, not started by this lane.

## END

- HEAD: 7b3c6588 (lane-0428-061-sourcepull)
- F1 double-JSON on --up success: FIXED (composite emitted once; non-JSON path renders result + up section).
- F2 dirty-tree false-positive: FIXED (fixture commits manifest; exact approval assertions).
- zsh/fish CI provisioning: present at Draft Go cell ci.yml:1686, actionlint clean.
- BLOCKER (open): exact hosted CI run for head 7b3c6588 pending — awaiting the Coordinator to schedule and report the terminal run + run-id + job-ids (packages, MCP surface/coverage gate, cli-3) per CI policy.
- draft = True (kept until gate complete).
- Coordinator notified (post 9142ab1f, END_BLOCKED @ 7b3c6588): exact hosted CI pending.
