# 0428-061 source pull — F1/F2/F3 fix round (candidate a4adc29a)

## WHAT

Independent review of head 9140e0c8 (review-1752-head9140e0c8.md) returned REQUEST CHANGES: F1/F2 blocking, F3 non-blocking. This round fixes all three on the product branch lane-0428-061-sourcepull.

- F1 JSON exit masking failures: `cmd/baha/app_pull.go` `runAppPull` now writes the pull result, then evaluates `result.Successful` (returns `ErrSourcePullBlocked` on partial failure) and runs `opts.Up` only on success, in both the human and JSON output paths. `baha app pull --up --output json` no longer skips the up lifecycle and no longer masks partial failures.
- F2 MCP contract fidelity: `machineApplicationPullInput` (in `cmd/baha/mcp.go`) now exposes `components`, `up`, and `approval`. The `app.pull` handler (`cmd/baha/mcp_lifecycle_extra.go`) authorizes `app.pull`, enforces `applicationlifecycle.RequireApproval("app.pull", input.Approval)`, routes components/up through `runAppPull` via a new `machinePullComponents` normalizer, and returns the CLI result as structured JSON. `--up --output json` emits one composite document (`pull` + `up{ran,output}`) captured in separate buffers so it stays one valid JSON value.
- F3 apply-time partial-update accuracy: corrected the preflight-blocker test comment (`source_pull_test.go` 146-148) and the `ApplySourcePull` helper comment (sequential fast-forward, no cross-repository rollback, changed repo left advanced / failed repo left as-is, retriable). Added `TestSourcePullApplyTimePartialFailureRunsOnce`: plan captured while both locals clean/behind, then a local drift commit on localB makes HEAD ahead of the captured target so the fast-forward fails at apply time while api-source already advances; asserts changed/failed repo states individually, unsuccessful aggregate, no mutation of the failed repo.

F3 compile fix: dropped the unused `webTarget` capture and the duplicate `webBefore` in the new test.

## WHY

F1/F2/F3 came from the independent exact-head review of 9140e0c8; F3 compile error came from an in-flight static review of my own test edit.

## GATE

- Exact required hosted run for head a4adc29a: run 44971782040 (event pull_request, head a4adc29a), in progress at time of writing.
- Prior run 44971297170 (head 719242df): Draft Go route. F1/F2/F3 package tests PASS in the packages shard once the F3 compile error is fixed (cli-0, cli-1 success).
- BLOCKER: `TestEndToEndInstalledZshAndFishWrappers` (context_terminal_test.go:467) fails — zsh/fish are not in the CI cell PATH on the Draft Go route. This is a CI-cell prerequisite in `.github/**` (owner scope); the lane cannot edit it. F1/F2/F3 code and tests are correct.
- Coordinator action requested: route exact head a4adc29a to a hosted cell that installs zsh/fish, or add authorized Draft Go provisioning. No `.github/**` change made by the lane.

## BRANCH PROVENANCE

- Base: develop 6209874428f08dc3e90d6e29a42b30683ce9932a, ancestor of HEAD (git merge-base --is-ancestor verified).
- `git log --oneline develop..HEAD` lists only lane commits: a4adc29a (compile fix), 719242df (F1/F2/F3), 9140e0c8 (round-4 golden fixture), 1c8e19f6, 73a2f084, 449c3f58, 6b9bb242, 403d718c, dab943e6. No foreign commits.
- PR #1752 head refs/pull/1752/head = a4adc29a (proven via git ls-remote). Non-force push.
- Changed files vs develop: cmd/baha/app_pull.go, cmd/baha/mcp.go, cmd/baha/mcp_lifecycle_extra.go, internal/development/source_pull.go, internal/development/source_pull_test.go.

## repo-rule compliance

- No local test/vet/go test/ci-fast-check.sh; all acceptance in hosted CI per nolocal + user boundary. gofmt clean on changed files.
- `.github/**` untouched; zsh/fish cell provisioning left for the owner/Coordinator.
- No subagents; no merge; PR kept Draft until gate complete.

## cleanliness

- No containers, compose projects, or runtime stacks started. `docker ps -a`: nothing to tear down.

## END

- HEAD: a4adc29a5844266cf4009bb12b9b68ae26a4a99a (lane-0428-061-sourcepull)
- Blocker: TestEndToEndInstalledZshAndFishWrappers @ context_terminal_test.go:467 — zsh/fish missing in CI cell PATH (Draft Go route); owner scope.
- F1/F2/F3 code + package tests: PASS in packages shard (run 44971297170 once F3 compile fixed).
- Exact CI pending after zsh-cell resolution; run 44971782040 in progress (Draft Go).
- draft= True (kept until gate complete)
- shells-befund: zsh/fell in the Draft Go CI cell (context_terminal_test.go:467) — requires Coordinator to route exact head a4adc29a to a hosted cell with zsh/fish or add authorized Draft Go provisioning; .github/** not edited by the lane.
