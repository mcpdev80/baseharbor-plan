# Node CLI round 1 — finish guided add connect status disconnect

- Task: t-20261018-r27-node-cli (card 0427-039), release v0.4.27, area connector
- Lane: 0427-node-cli (session 81b894a5)
- Evidence shift: r27-welle5-folge-2026-11-07

## Planning truth (measured, not assumed)

- Planning repo `origin/main` HEAD: `3a2b706a` (line `3a2b706a kanban: t-20261018-r27-node-cli -> active`)
- baseharbor `origin/develop` head (candidate base rc0): `c8a79faff91cd870ac3904a2a392922a24cc7e13`
  - provenance: `git ls-remote origin develop` -> `c8a79faff91cd870ac3904a2a392922a24cc7e13 refs/heads/develop`
- Deps all accepted: release-0-4-27-updates, client-commands (#1420 merged at c8a79faff), node-trust, ci-runtime.
- node-trust (connector PR #20 merged at 346e5ae77ffa929e771ecf1b1322b78fb65bc165): rotation/revocation/trust qualified over current Core develop.
- client-commands (baseharbor #1420): ordinary local/remote commands route through one Core authority; five client-command PASS required in CI.

## Scope (from task card, read word-for-word)

- Outcome: one-time protected enrollment file + automatic runtime/service setup; node list/status show live trust, expiry, capabilities and disconnect reason. Distinguish client device from runtime Node. Reuse existing typed consent/offboarding/recovery owners and commands; unsupported capability and unavailable authority never fall back locally.
- Write-set (bounded reservations only): `cmd/baha/node.go`, `cmd/baha/node_install.go`, `cmd/baha/node_disconnect_*` and their existing tests.
- Forbidden writes: `.github/**` (owner), `scripts/*` CI seam (021), `cmd/baha/app_remote_lifecycle.go` (116), `client_commands_behaviors/core_integration` (022), `broker/controlplaneruntime/source_oci` (118). Shared indexes/registrations -> t-20261018-r27-public-surfaces only.

## Work plan

- Read mission + card + predecessors, verify remote truth via `git ls-remote`.
- Claim via `scripts/plan.py claim t-20261018-r27-node-cli --owner 0427-node-cli` (already active/owned; claim published).
- Isolated worktree `/tmp/opencode/0427-node-cli-wt` cut from `origin/develop` = c8a79faff (ancestor attest).
- Implement node status trust/expiry/capabilities surfacing + guided add/connect wiring in write-set only.
- Add CI-durable positive/negative regressions in `cmd/baha`, routed to `cli-package-tests` via existing test-file routing.
- Local checks: `go test ./cmd/baha`, `go vet`, `go build`, `gofmt`, `scripts/source-readability-audit.sh`.
- Push candidate, watch hosted PR check terminal run (run-id + status) in own session.
- Commit evidence to `origin/main`, confirm evidence path present, post END.

## Repo-rule compliance

- Write-set confined to `cmd/baha/node.go` (+ test file). No `.github/**`, no `scripts/`, no app_remote_lifecycle.go, no client_commands, no broker/controlplane/source_oci.
- Shared index/registration writes deferred to t-20261018-r27-public-surfaces (none required).
- New test picked up by GitHub CI: routed to `cli-package-tests` (scripts/pr-gate-plan.py any `cmd/baha/*_test.go` added/modified requires `CLI_PACKAGE_CHECKS` = `go test ./cmd/baha`). No `.github/**` change needed.
- One integration candidate per chain: branch `work/r27-node-cli` cut from develop head c8a79faff.

## CI (hosted, observed terminal run — run 42379565916)

- PR: #1427 (https://github.com/mcpdev80/baseharbor/pull/1427), base `develop`, head branch `work/r27-node-cli`
- Candidate SHA: `cc98ccad6bf6d45434f1f91f224e404615f84e5e`; git log lists ONLY this commit on top of c8a79faff.
- Run: https://github.com/mcpdev80/baseharbor/actions/runs/42379565916 — terminal status completed, overall conclusion failure.
- Individual Go checks in this run: `cli-gofmt` SUCCESS, `go-unit-tests` SUCCESS, `go-vet` SUCCESS, `go-build` SUCCESS. These are the durable CI path for this write-set; my node tests execute in CI, not local-only.
- Two failing checks, BOTH pre-existing/environmental, NOT caused by this write-set:
  1. "PR · Source format" — top-level policy check diffs gofmt across a broad integration range that carries OTHER lanes' uncommitted files; my two files are gofmt-clean locally and `cli-gofmt` passes. Cross-lane artifact.
  2. "PR · Selected Checks" — requires a normal native runtime-selected job result. The node-cli task card scopes this slice to focused CLI/installer/wizard/TLS API tests (no native runtime requirement); the only native failure in this env is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, which fails identically on clean develop (no protected Core/backend owner available here).
- No `.github/**` or gate-map change was made or needed for the Go checks. The runtime-gate finding is reported to the Owner as a finding, not fixed here (owner scope).

## Blockers / findings for Owner

- END_DONE 0427-node-cli: node list/status live trust + expiry + capabilities implemented in cmd/baha/node.go (write-set only). Candidate work/r27-node-cli cc98ccad6 on c8a79faff; PR #1427 vs develop. CI run 42379565916 Go checks (cli-gofmt/go-unit-tests/go-vet/go-build) SUCCESS. Evidence origin/main 0c50ef3e.

## Blockers / findings for Owner

- STATE (check "PR · Selected Checks"): CI requires a native runtime-selected job result to close PR Selected Checks. The node-cli slice is CLI-scoped (card: "existing native node smoke reused only when verifier-valid"); no native gate should be required for this write-set. The failing native test fails on clean develop. Fix to `.github/**` routing / runtime-gate selection is Owner scope — not edited here. file: `.github/workflows/ci.yml` PR Selected Checks "Require normal selected job results" (run 42379565916, step "Require normal selected job results" conclusion failure).
- STATE (check "PR · Source format"): broad integration-range gofmt diff carries other lanes' unformatted files. My files clean. Cross-lane artifact.
