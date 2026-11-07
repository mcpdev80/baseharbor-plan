# CODEX-REVIEW 0427-036 / PR #1405

Role: CODEX-REVIEW. Candidate head: `0f08b877f4152c156b219ff6d13ab05ee6b082de`. Base: `develop` at `934be499b9d2d894f80889fc23cd811884c8aec4` at review time.

## PLAN

1. Confirm mission, task contract, real planning repository, and current remote candidate/base state.
2. Review round-6 behavioral red evidence and verify its remote and exit witnesses plus test-only scope.
3. Inspect the exact candidate diff and required CI results at the candidate SHA.
4. Record the SHA-specific review verdict and actionable correction recipe if rejected.
5. Publish evidence on `origin/main` and post the required END status.

## Review scope and witnesses

- Planning repository verified before evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. This is the real planning checkout, not `workers/baseharbor-plan`.
- Fresh product remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1405/head` returned develop `934be499b9d2d894f80889fc23cd811884c8aec4` and PR head `0f08b877f4152c156b219ff6d13ab05ee6b082de`.
- PR #1405 is OPEN, non-draft, mergeable, targets `develop`, and its head equals the mission SHA.
- `git diff --name-status` and full diff were inspected for `934be499b9d2d894f80889fc23cd811884c8aec4...0f08b877f4152c156b219ff6d13ab05ee6b082de`: 15 changed files, 1,512 insertions and 7 deletions. Scope contains management-host implementation, lifecycle/lock wiring, and Go tests; no `.github/**` changes.
- The candidate history after the fetched base is the management-host task sequence: `a87f83776`, `64d93e945`, `3a80ed040`, `5b8c54222`, then the base-refresh merge `0f08b877f`. `64d93e945` is an ancestor of the candidate (`git merge-base --is-ancestor` returned 0).

## Required red-first evidence

Reviewed `evidence/r27-welle5-folge-2026-11-06/management-host/round-6-redfirst.md` on planning main. Its fresh `ls-remote` witnesses match the PR head and recorded develop SHA. It records the same test and precondition producing a behavioral assertion failure on sick `64d93e94` (exit 1 because `Verify()` returned nil instead of a contended refusal) and passing on candidate `0f08b877` (exit 0). The reported `internal/coreinstallation/management_host_behavioral_red_test.go` is an isolated test-only probe using existing public APIs; it does not change product APIs. The candidate mutation evidence is L0 green, L1 red after the ownership bridge is removed, L2 green after exact restoration, with L0==L2.

## Required CI at exact head

GitHub run `42322027058` (`CI · PR #1405`) is terminal `success` for exact head `0f08b877f4152c156b219ff6d13ab05ee6b082de`. `PR · Validation · go-unit-tests` succeeded, as did build, vet, authority-package, CLI, source-contract and `PR Selected Checks`. `PR Selected Checks` itself succeeded. The skipped jobs (`Targeted HA · docker/podman`, `PR · Exact Candidate`, runtime/interface/public-contract and consumer/demo pin jobs) are gated by workflow conditions not met for this PR; the targeted HA jobs only run on their designated runtime-validation push refs. No required applicable cell is skipped. No rerun or workflow dispatch was performed.

## Blocking finding

`cmd/baha/serve.go:41-43, 97-103` declares `var startup context.Context` and initializes it only when `cfg.RuntimeAppName == ""`. For the supported per-application broker path (`RuntimeAppName != ""`), the candidate leaves `startup == nil` and passes it to `controlplaneruntime.Run`. `Run` forwards that context into server startup and later uses it for connector lifetime/shutdown (`context.WithCancel(ctx)` / `ctx.Done()`), so the per-application serve path can panic on a nil context instead of starting. This violates the task's preservation of the existing per-application runtime broker path and its explicit no-login/service-free ordinary operation.

## Verdict and correction recipe

REJECT for candidate `0f08b877f4152c156b219ff6d13ab05ee6b082de`.

Correction: in `cmd/baha/serve.go`, initialize `startup := ctx` before the `RuntimeAppName` branch, then apply connector target overrides and management-host attachment to that non-nil context. Add a focused regression for `RuntimeAppName != ""` that proves the serve path reaches normal server startup without a nil-context panic, and ensure the GitHub `go-unit-tests` job continues to execute it. Stop criterion: the focused regression and applicable exact-head required CI pass, with a fresh CODEX-REVIEW on the resulting SHA. Do not change `.github/**`; report any CI trigger-selection gap to the Owner.

## Repo-rule compliance

- Review only; no product file changed, no merge, no workflow dispatch/rerun, no runner/VM/container work, and no subagents.
- Evidence is stored only in the real `baseharbor-plan` repository. An unrelated pre-existing untracked file `evidence/r27-welle5-folge-2026-11-06/vm-integration-runs/round-3-docker-podman2.md` was left untouched.
- No markdown checkbox syntax appears in this evidence file.

## END

END_DONE codex-1405-review-b: verdict=REJECT head=0f08b877f4152c156b219ff6d13ab05ee6b082de rotnachweis=ok ci=42322027058-success rezept=cmd/baha/serve.go initialize startup from ctx and add RuntimeAppName regression; stop until focused test and exact-head required CI pass.

## Planning publication witness

Exact output captured immediately before publishing this evidence:

```text
3ee6229b23fb7ec6ec4e6ebcfd363ce72c83844e	refs/heads/main
```
