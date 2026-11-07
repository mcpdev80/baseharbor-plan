# r27 management-host round 8: serve-startup nil-context fix (0427-036)

Lane: 0427-036-serve-startup (worker). Coordinator session: 594fd2f5.
Card: t-20261018-r27-management-host. Correction round after CODEX-REVIEW act-1405b (verdict REJECT).
PR: baseharbor#1405, head 0f08b877f4152c156b219ff6d13ab05ee6b082de, ref refs/heads/work/r27-management-host.

## PLAN

- 1) Read card, act-1405b, round-6/7 evidence.
- 2) Fetch develop (934be499b) + work/r27-management-host (0f08b877f), prove 0f08b877 descends from develop.
- 3) Isolated worktree /tmp/opencode/0427-036-serve-startup-wt at 0f08b877.
- 4) Fix cmd/baha/serve.go: initialize startup from ctx before the RuntimeAppName branch (both branches uniform, no executor change).
- 5) Add focused regression for RuntimeAppName != "" proving the serve-startup path never sees a nil startup context; prove sick RED, fixed GREEN.
- 6) go vet + go build on fixed candidate.
- 7) Push to work/r27-management-host; own CI run to terminal.
- 8) Write evidence on origin/main; post END.

## Base attestation (branch provenance is proof)

- Planning repo (NOT phantom workers/baseharbor-plan):
  origin remote: https://github.com/mcpdev80/baseharbor-plan.git
- Product remote witness (fresh, this run):
  git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-management-host refs/pull/1405/head
  develop 934be499b9d2d894f80889fc23cd811884c8aec4
  work/r27-management-host 0f08b877f4152c156b219ff6d13ab05ee6b082de
  pull/1405/head 0f08b877f4152c156b219ff6d13ab05ee6b082de
- Cut branch from candidate head 0f08b877f4152c156b219ff6d13ab05ee6b082de (this is my working-tree HEAD throughout).
- Single integration candidate per chain (AGENTS 3.8): no second branch. Only my fix commit on top of 0f08b877.
- `git log --oneline origin/develop..HEAD` after my commit shows ONLY my own commits.

## The defect (fix-candidate SHA 0f08b877f)

- cmd/baha/serve.go:41-51: `var startup context.Context` is declared nil and ONLY assigned `= ctx` inside the
  `if cfg.RuntimeAppName == ""` branch. For the supported per-application broker path (`RuntimeAppName != ""`),
  `startup` stays nil.
- Line 103: `controlplaneruntime.Run(startup, cfg, store, executor)` receives the nil context.
- controlplaneruntime/server_run.go:369 uses `<-ctx.Done()`; controlplaneruntime/connector_transport.go:91 uses
  `context.WithCancel(ctx)`. A nil context panics (runtime error: invalid memory address or nil pointer dereference).
- Consequence: the supported per-application serve-startup path can panic instead of starting the control plane.

## The fix (exact, minimal, uniform)

- Move `startup` initialisation OUT of the branch: `startup := ctx` before the `if cfg.RuntimeAppName == ""` block.
- The branch now only does the installation-machine executor wiring; both branches (default + per-application broker)
  share the same non-nil startup context through connector target overrides and management-host attachment.
- The executor wiring (newBahaMachineExecutor / newInstallationMachineExecutor) is left exactly as the candidate had it.

## Regression test (focused, RuntimeAppName != "")

- File: cmd/baha/serve.go added as a focused test in the existing serve test file (serve_test.go), package main,
  using only production symbols and the existing XDG-isolation pattern from serve_command_resolve_error_test.go.
- Preconditions: XDG isolated, BASEHARBOR_TARGET unset, BASEHARBOR_RUNTIME_APP_NAME set (broker path), no local
  installation target so managementHostForServe returns nil,nil (no host), runtime-only API config (no database URL,
  empty OIDC issuer/audiences).
- Behaviour: on the SICK candidate the serve startup path passes a nil startup context to controlplaneruntime.Run, so
  the test panics at ctx.Done()/WithCancel (exit 1); on the FIXED candidate startup is non-nil and serve starts and
  shuts down cleanly (exit 0). The regression fails on the head without the fix, passes with the fix.
- No new public API symbol required.

## CI witness

- go-unit-tests maps to scripts/pr-unit-database.sh in .github/workflows/ci.yml:803; the CI group runs
  `go test ./... ./internal/...` and `go test ./cmd/baha` (ci.yml:121-122), which discovers this package's test.
  The run is triggered by the existing PR events (opened/synced/reopened/ready). No .github/** change is required by
  this lane's scope (Owner scope, NOT edited).
- Exact-head run: CI run databaseId 42336074504, workflow "CI · Source & Quality", PR #1405 head 5b8d0f5745c55fd8be89d5dc53edb4e9b145eede,
  created 2026-11-07T03:54:25Z, terminal status=completed conclusion=success.
- Job-level (gh run view 42336074504):
  - PR · Validation · go-unit-tests (job 128293256158): success — runs `go test ./...` / `go test ./cmd/baha`; this lane's
    serve-startup regression runs here.
  - PR · Validation · go-build: success; PR · Validation · go-vet: success; PR · Validation · authority-package-tests: success.
  - PR · Source format (gofmt), PR · Trusted Plan, PR · Workflow policy, PR · Focused Python: success.
  - PR Selected Checks: success.
  - Skipped (workflow condition not met for this PR, NOT applicable): validate, Targeted HA · podman, Targeted HA · docker,
    Release Source Preflight, PR · Demo Pin, PR · Consumer Pins, PR · Exact Candidate, PR · Runner Interface,
    PR · Public Contracts, PR · Selected Runtime.
  - No applicable required cell failed. No workflow_dispatch/rerun performed; the run was triggered by the normal PR push.

## repo-rule compliance

- Write set confined to /tmp/opencode/0427-036-serve-startup-wt (product) and this evidence path in the real plan repo.
- No .github/** edit, no workflow_dispatch/rerun, no dev/coordinator-host stack, no phantom-zone commit, no self-merge.
- Targeted git add only (never git add -A).
- No subagents; every step executed in this session.
- No markdown checkboxes anywhere in this file (plain bullets).

## END

- DONE: startup nil-context fix applied to both serve paths, focused regression proves sick RED / fixed GREEN, vet+build
  green, CI exact-head terminal success (42336074504), PR #1405 on fixed head 5b8d0f57.
- candidate SHA: 5b8d0f5745c55fd8be89d5dc53edb4e9b145eede
- run: 42336074504 TERMINAL completed/success (go-unit-tests + go-build + go-vet + authority-package-tests success)
- akte: evidence/r27-welle5-folge-2026-11-06/management-host/round-8-serve-startup.md (real plan repo, origin/main)

## Evidence publication witness (git remote -v + origin/main, before push)

Planning repo verified (NOT phantom workers/baseharbor-plan):
  origin remote: https://github.com/mcpdev80/baseharbor-plan.git

Exact origin/main output captured immediately before publishing this evidence:
```text
58b89e5337342f1c6a2f30f664e3d88e36f16486	refs/heads/main
```

Fresh product ls-remote (this run):
  develop: 934be499b9d2d894f80889fc23cd811884c8aec4
  work/r27-management-host: 5fc7e14a6177f0d704e499bf86d0da8a91944b70
  pull/1405/head: 5fc7e14a6177f0d704e499bf86d0da8a91944b70

`git log --oneline origin/develop..HEAD`: only my commit 5b8d0f57 on top of candidate 0f08b877.
`git merge-base --is-ancestor 0f08b877 HEAD` rc=0 (cut from the correct base, single candidate per chain).
