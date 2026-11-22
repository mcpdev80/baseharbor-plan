# 0428-061 source pull — F1/F2/F3 test + zsh-cell fix round (candidate e7df5ab4)

## WHAT

Second fix round on lane-0428-061-sourcepull. The first round (a4adc29a, fix-round-f1-f2-f3.md) had the F3 test premise wrong and left the F1/F2 regression coverage absent. This round:

- F3 test premise corrected to a REAL apply-time failure. The drift-commit approach failed because `git merge --ff-only <ancestor>` returns "Already up to date" (exit 0) when the drift commit is a descendant of the captured target. Rewrote `TestSourcePullApplyTimePartialFailureRunsOnce` (`internal/development/source_pull_test.go`) with a divergence fixture: push `remote2` to peerB so the web-source is strictly behind its upstream at plan time (`UpdateAvailable`, `Applyable`), then commit a `local divergence` on localB so `git merge --ff-only <target>` aborts at apply time. Asserts api-source updated/current, web-source unavailable/blocker, aggregate unsuccessful, and localB HEAD stays at its DIVERGED head — NOT rolled back to base. This documents the truthful partial state: the changed repo is left advanced, the failed repo left exactly as-is (no cross-repository rollback).
- F1 regression test added: `TestEmitSourcePullUpCompositeIsSingleDocument` (`cmd/baha/app_pull_options_test.go`). Drives the exact F1 merge seam `emitSourcePullUpComposite` and asserts ONE valid JSON document (`schema_version`/`pull`/`up` keys only), `up.ran=true`, `up.output` trimmed — proving `baha app pull --up --output json` never emits two concatenated JSON values.
- F2/F4 direct MCP approval regression added: `TestAppPullMCPApprovalRegression` (new file `cmd/baha/app_pull_mcp_approval_regression_test.go`). Drives the typed `baseharbor.app.pull` tool through the real `newMCPServer` in-memory transport (shared CLI/MCP lifecycle pattern): `approval=false` is refused with a classified approval error (fail-closed, exactly like app.stop/perses.remove); `approval=true` passes the approval gate and reaches the shared pull lifecycle (no approval-refusal message). packages/cmd/baha shard.
- Owner-authorized CI fix (exception to the .github/** owner rule): the Coordinator explicitly routed the zsh/fish shell provisioning to this lane. Added an `Install interactive shells for the shell-wrapper path` step (sudo apt-get install -y zsh fish) to the PR Draft Go cell (ci.yml:1672+) so the cmd/baha cli-3 shard runs `TestEndToEndInstalledZshAndFishWrappers` with both shells in PATH, matching the canonical validate cell's install block (ci.yml:343-351).

## WHY

- F3: the drift-commit fixture made the web-source HEAD a descendant of the captured upstream target, so the ff "succeeded" as already-up-to-date and the test premise (a real apply-time failure) never fired. A divergence after plan capture is the only way `merge --ff-only` aborts.
- F1/F2: the independent review (a4adc29a) required durable regression coverage for the single-document JSON property and the direct MCP approval gate, which had code but no CI-routed regression test.
- zsh cell: `TestEndToEndInstalledZshAndFishWrappers` fails on the Draft Go route because no PR cell installs zsh/fish; the test's own comment requires the owning cell to install them.

## GATE

- Exact required hosted run for head e7df5ab4: requested of the Coordinator (post 9142ab1f). No exact hosted run completed yet.
- Local verification (all green): ci-fast-check.sh — 295 tests OK, all gates pass (Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS: 20 approved files). `go vet ./cmd/baha/ ./internal/development/` clean. `go build /tmp/baha` clean. gofmt clean on all changed files.
- Targeted tests PASS: `TestEmitSourcePullUpCompositeIsSingleDocument` (cmd/baha), `TestAppPullMCPApprovalRegression` both sub-cells (cmd/baha), `TestSourcePullApplyTimePartialFailureRunsOnce` (internal/development), all 14 source_pull tests.
- actionlint on .github/workflows/ci.yml: clean (exit 0).
- BLOCKER (resolvable, see below): the exact hosted CI run for head e7df5ab4 has not yet executed. Per CI policy, success is only for the exact tested head with actually executed required jobs; SKIPPED/queued/absent is NOT a pass.

## BRANCH PROVENANCE

- Base: develop 6209874428f08dc3e90d6e29a42b30683ce9932a, ancestor of HEAD (git merge-base --is-ancestor verified).
- `git log --oneline develop..HEAD` lists only lane commits: e7df5ab4 (F1/F2 regression tests), b010dabc (F3 divergence fixture), a4adc29a, 719242df, 9140e0c8, 1c8e19f6, 73a2f084, 449c3f58, 6b9bb242, 403d718c, dab943e6. No foreign commits.
- PR #1752 head refs/pull/1752/head = e7df5ab4a6c3219404de26846198d4f6e1b8fed0 (proven via git ls-remote). Non-force push.
- Changed files vs develop (product/test): cmd/baha/app_pull.go, cmd/baha/mcp.go, cmd/baha/mcp_lifecycle_extra.go, internal/development/source_pull.go, internal/development/source_pull_test.go, cmd/baha/app_pull_options_test.go, cmd/baha/app_pull_mcp_approval_regression_test.go.
- CI change (owner-authorized): .github/workflows/ci.yml — one step added to the PR Draft Go cell (zsh/fish install), validated with actionlint. Not committed to the product repo (owner scope for CI; handed to the Coordinator to land).

## repo-rule compliance

- nolocal respected for the acceptance gate: no bare `go test ./cmd/baha/` (which starts real lifecycle containers); targeted named-form runs with the required skip set used instead. ci-fast-check.sh, go vet, go build, gofmt all run locally and pass.
- .github/** change was made ONLY because the Coordinator explicitly routed the zsh/fish provisioning to this lane (owner exception to the standard scope split). actionlint clean; workflow file count unchanged (20).
- No subagents; no merge; PR kept Draft until gate complete.
- Evidence lives only in baseharbor-plan (evidence/r28-welle5-2026-11-22/sourcepull-0428-061/).

## cleanliness

- No containers, compose projects, or runtime stacks started or left running. `docker ps -a`: no lane-owned images to tear down (only ambient bh-itest stacks, not started by this lane).

## END

- HEAD: e7df5ab4a6c3219404de26846198d4f6e1b8fed0 (lane-0428-061-sourcepull)
- F1/F2/F3 test fixes: PASS locally (14 source_pull tests, F1 + F2 regression, ci-fast-check 295 OK, all gates pass).
- zsh/fish CI provisioning: added to the Draft Go cell (owner-authorized), actionlint clean.
- BLOCKER (open): exact hosted CI run for head e7df5ab4 has not yet executed. awaiting the Coordinator to schedule and report the terminal run + job-ids (packages + MCP surface/coverage gate + cli-3). No .github/** change committed to the product repo; landed via the Coordinator.
- draft = True (kept until gate complete).
- Coordinator notified (post 9142ab1f, END_BLOCKED @ e7df5ab4): exact hosted CI pending.
