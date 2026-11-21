ROLLE: REVIEW

Session ID: not exposed by this session interface
Model: GPT-6
Backend: Codex API session with shell and GitHub CLI access
Review time: 2026-11-21 06:41 UTC

**Verdict: REQUEST CHANGES**

## PLAN

1. Read /var/tmp/rev1742.txt and record this numbered plan in the live board and review evidence.
2. Verify GitHub remotes, exact PR head/base, remote branch refs, and before/after freeze.
3. Inspect the card and candidate diff; trace git credential fill through the actual credential path and noninteractive auth controls.
4. Inspect the exact hosted run, all three log byte counts, failure-name comparison, and failure classification.
5. Prove CI selection for internal/credential tests, check write-set exclusions, and review cleanliness evidence.
6. Publish only review-1.md on baseharbor-plan origin/main and verify the evidence path and unchanged candidate head.

## Candidate and read-only freeze

Candidate: mcpdev80/baseharbor#1742, branch `w0428-217credfill`.
PR API before review: head `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`; base `40cb28c758b02960356434b630086a341ebe1738`; open, draft=false, mergeable=true. The head is based on the current develop SHA.

Remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1742/head`:

```text
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
0df7efc00bb3cfd784c988613a9ec5f8fb6215b4 refs/pull/1742/head
```

PR head before review = `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`
PR head after review = `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`

Review was read-only. The review did not alter the candidate or run a push, merge, close, or PR comment.

## Contract and diff

Contract source: `t-20261121-git-credential-fill-bootstrap-hang` (0428-217), plus `evidence/r28-welle4-2026-11-21/git-credential-fill/round-1.md`.

The contract's core acceptance is a noninteractive `git credential fill` path that terminates without hanging when terminal prompts and askpass are unavailable, with a useful host/missing-credential failure. The regression must check the failure content and exercise the production call path. The allowed product scope is `cmd/baha/app_inspect_remote.go` and Git credential/helper files reached from it; `cmd/baha/app_update.go` is outside the named card write-set.

The PR changes five files: `cmd/baha/app_inspect_remote.go`, `cmd/baha/app_update.go`, `internal/credential/native/credfill_noninteractive_test.go`, `internal/credential/native/gitcredential.go`, and `internal/credential/native/host.go`. No `.github/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, or `internal/serviceaccess/**` files are changed. `internal/credential/**` is within scope and is disclosed in the lane evidence.

The credential source's real call chain is `cmd/baha/app_inspect_remote.go:28` → `native.PreInteractiveNoPrompt` → `internal/credential/native/host.go:136-139` → `GitCredentialSource.Resolve` in `internal/credential/native/gitcredential.go:41-60` → `ExecRunner.Invoke` in `host.go:32-40`. Runner errors are wrapped with the host by `gitcredential.go:78-82`. The production runner now installs `GIT_TERMINAL_PROMPT=0`, `GIT_ASKPASS=/bin/false`, and `SSH_ASKPASS=/bin/false` through `host.go:43-61`, so Git's own prompt/askpass paths fail closed.

### Finding 1 — regression does not prove the prompt-hang fix

The new `TestGitCredentialFillIsNonInteractiveProvesTheFix` at `internal/credential/native/credfill_noninteractive_test.go:45-82` does call `GitCredentialSource.Resolve` with the default real runner, which is the correct production seam. However, its helper at lines 57-60 runs `read -r pw < /dev/tty`. That is a direct controlling-TTY read, outside Git's terminal-prompt and askpass machinery; the production change only sets Git/SSH prompt variables and bounded stdin. Thus the test's helper can still block on a host with a controlling TTY, while on a CI process without a controlling TTY that read fails immediately even on the sick implementation. The test has no deadline and does not unset inherited prompt/askpass variables (lines 68-69), so its green result does not establish the card's red-on-baseline, terminates-on-fixed behavior. The test exercises a real source/runner, but its blocking mechanism is not a valid witness of the behavior being fixed.

Recipe: in `internal/credential/native/credfill_noninteractive_test.go`, replace the direct `/dev/tty` helper with a bounded, deterministic reproduction of Git's own prompt/askpass path. Run the real `GitCredentialSource.Resolve`/`ExecRunner` path under an explicit PTY and context deadline; clear inherited `GIT_TERMINAL_PROMPT`, `GIT_ASKPASS`, and `SSH_ASKPASS` before the call so only production code establishes noninteractive behavior. Assert termination within the bound and a host-specific missing-credential error. Record a red-first mutation/reproduction on the sick implementation and green on the fix. Stop when the test hangs/fails on the old implementation and terminates with the expected host-bearing error on the candidate, and when the same test is included in the packages CI cell.

### Finding 2 — out-of-card write in app_update.go

The SHA diff adds `cmd.Stdin = strings.NewReader("")` at `cmd/baha/app_update.go:456` and `:515`, in `gitOutput` and `gitIsAncestor`. The task note does not authorize this file, and the lane evidence itself labels it “NOT named in the card.” This remains a scope expansion, even if intended to address the same class of noninteractive behavior.

Recipe: remove the two added stdin assignments from `cmd/baha/app_update.go` and keep this PR to the contract's named inspection/credential path. If the coordinator wants the app-update behavior, first amend the card's write-set and acceptance explicitly, then require focused regression coverage for both `gitOutput` and `gitIsAncestor` through their production callers and prove those tests run in the applicable CLI CI shard. Stop when every changed product file is authorized by 0428-217 or a recorded contract amendment and the focused tests pass.

## Hosted CI and test intake

Exact-head run `44874605168`, event `pull_request`, head `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`, completed with conclusion `failure` (06:14:34Z–06:18:59Z). This is not a passing required-check set.

Log retrieval sizes: `gh run view 44874605168 --log` = 1,209,358 bytes; `--log-failed` = 367,525 bytes; `--job 136756503500 --log` (packages) = 66,913 bytes. The three views were available; no invalid-zip fallback was needed.

The packages job, ID `136756503500`, executed `bash scripts/pr-unit-database.sh "packages"`. Selection is defined in `.github/workflows/ci.yml:1185-1206`; the script routes that cell through `scripts/pr-unit-database.sh:38-40` to `scripts/pr-go-unit-shard.py --mode packages`. The packages mode at `scripts/pr-go-unit-shard.py:118-135` enumerates Go packages excluding only `./cmd/baha`. The log explicitly reports `ok github.com/mcpdev80/baseharbor/internal/credential/native 0.020s`; therefore the new native credential test file was selected and executed in the same PR's packages cell, not skipped. The Native gate plan completed successfully. Native runtime cells that were skipped are not required for this diff: it changes CLI inspection and Go credential helper behavior, not a native runtime target; the successful gate plan selected the Go unit package and CLI cells.

The overall run remains red. Five Go unit shards (`cli-0` through `cli-3` and `packages`) failed. In packages, the exact observed inherited failures include:

```text
--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource
loki_test.go:522: ... stat .../providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability
loki_test.go:586: ... stat .../providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed
```

Failure-name comparison supplied and rechecked: 197 unique first-level `--- FAIL: Test` names in candidate run 44874605168 versus 196 in comparison run 44863102857; 196 names overlap, none are baseline-only, and the one additional name is `TestAppListAllTargetsWorksAfterInstallationDestroy`. Its candidate log says `app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev" ... config.yaml is missing`. It is attributed to card 0428-210 / PR #1739, not to this credential-fill change. The requested “inherited STATE” booking is appropriate for the broad existing failure set and for this separately tracked 0428-210 failure; it is not evidence that run 44874605168 passed. The comparison run is PR #1739, not a successful base-only run, so this classification relies on the supplied #210 provenance and the observed failure-name overlap, not on calling #1739 a clean develop run. The exact failure phrase `requires an authenticated BaseHarbor operator` occurs zero times in candidate run 44874605168.

CI recipe for this review: do not rerun or alter workflow files. Keep run 44874605168 recorded as failed; stop acceptance on that run. The coordinator must resolve the inherited red suite and the 0428-210 failure through their owning work, then obtain a new exact-head required-check run after the review findings are corrected. Stop when the exact candidate SHA has a successful terminal selected-check aggregate and all required jobs executed.

## Cleanliness and repository rules

No containers or compose projects were started during review. `docker ps -a` before review (PID 2968228) returned an empty container list. Planning remote was verified as `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. Only this review evidence file is to be published in the plan repository; no product-repository write was made.

## repo-rule compliance

Review remained read-only on the candidate, did not access the quarantined workers/baseharbor checkout for remote truth, did not run a bare package test, and did not modify workflows, product code, CI, or PR state. No subagents were used. No user-supplied command to post a Codeman END was used.

## END

END codex-rev-cli2b BLOCKED — REQUEST CHANGES for PR #1742 at `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`; findings are the non-deterministic/non-proving prompt regression and unauthorized `cmd/baha/app_update.go` changes. Exact-head CI is also failed, with the inherited/parallel failure state recorded above.

`docker ps -a` after review (PID 2970524) also returned an empty container list. Candidate remote/API after review both still report `0df7efc00bb3cfd784c988613a9ec5f8fb6215b4`.
evidence/r28-welle4-2026-11-21/git-credential-fill/review-1.md
