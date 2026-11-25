# w185 — podman auth-gap diagnosis, gate-path mapping, fixture option handoff

**Lane:** w185-0428-287-pr1835-podman
**Task:** t-20261116-r28-bug-installation-reset-recovery / card 0428-287 / PR #1835
**Scope of this lane:** reproduce the diagnosis from the hosted job log, map the SAME auth gap across the podman atomic gate path, and hand the test-only login/OIDC-fixture decision to the CODEX/OWNER decision lane (w136). NO product change, NO new candidate, NO `.github/**` edit. No merge.

## Base attestation (ls-remote witnesses)
- PR #1835 head (real github.com/mcpdev80 remote): `72fc60a923b7c9b91b803f469c8c5cf3572e0448` — OPEN, intact card delta.
- develop head: `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`.
- `git merge-base --is-ancestor 2a141387d 72fc60a92` → YES. `2a141387d` (the develop-hopped base from w157) is an ancestor of the PR head.
- PR #1835 head commits vs develop (only card 0428-287, one integration chain):
  - `8cae9c5a8`/`72fc60a92` head identity alignment (additive, no tree change)
  - `38b7ee79e` merge develop, `40f72d101` wire preservation test into native gates, `ce26781f8` remove degenerate Impact assertion, `69953fcce`/`2a4298672` merge develop, `abc390d28` catalog, `e02b8d5e6` add preservation regression, `55d17d437` fix gate incomplete-inventory recovery, `78e572f36` complete failed-apply install reset.
- baseharbor-plan remote (verified before first evidence commit): `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## 1) Diagnosis reproduced from the hosted job log
The failing podman runs (`45611090994`, `45611866489`, both on `72fc60a92`) fail at the podman-quadlet `baha doctor` probe. The exact failed lines from the hosted log:
- `2026-11-25T12:11:12.7977143Z   Managed-environment machine operations require an authenticated BaseHarbor operator.`
- `2026-11-25T12:11:12.8003049Z ##[error]Process completed with exit code 2.`
- Resolution hint in the log: `authenticate the BaseHarbor operator` / `Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.`

Root cause, traced in source (NOT inferred from the error text):
- `podman-acceptance.yml` job "Verify Podman runtime detection" runs `$RUNNER_TEMP/baha doctor` (`line 279`).
- `baha doctor` (outside an application repo) dispatches to `doctorCommand` (`cmd/baha/doctor.go:35`).
- Before any runtime probe it calls `authorizeCurrentMCPContext(ctx, "control-plane.doctor", "", "", "")` (`cmd/baha/doctor.go:79`).
- `authorizeCurrentMCPContext` (`cmd/baha/mcp.go:384`): environment resolves to `dev`; `ManagedEnvironment("dev")` returns `true` (`internal/operatorauth/config.go:89`/`:110`), so it does NOT take the trusted-local short-circuit at `mcp.go:398` and instead reaches the operator-auth boundary.
- The boundary (`internal/operatorauth/authorization.go:287`): no verified principal → `operator_authentication_required` → `machine.NewError(ErrorAuthenticationFailed, ...)` with `Next: "Authenticate the operator for the selected Target and environment, then retry..."`. Exit code 2.
- `podman-acceptance.yml` never authenticates an operator and never builds the `baseharbor_ci_operator_testonly` tagged binary (no `DEMO_ATOMIC_GATE`, no `ciIntegrationOperatorContext`). The synthetic CI operator that authorizes the atomic gate does not exist on this runner. So a fresh podman runner with no provisioned BaseHarbor operator fails the `baha doctor` probe with exactly the observed error.

This is an AUTH/SETUP GAP on the podman runner, NOT a card-0428-287 semantic defect. The card delta (`application_destroy_authorization.go`, `installation_reset_preservation_test.go`, `w287_destroy_after_failed_apply_test.go`) does not touch doctor/operator auth. The same probe PASSED on the SUCCESS podman run `45608237959` on `2a141387d`, which proves the code path is correct and the failure is a runner-provisioning state (missing authenticated operator), not a code regression.

## 2) SAME auth gap across the podman atomic gate path — which gates are affected
There are TWO distinct podman workflows, and this is the decisive distinction:

**A) `podman-acceptance.yml` (the workflow whose log failed) — untagged.**
- Builds the plain binary (`go build -trimpath -o $RUNNER_TEMP/baha ./cmd/baha`, `line 272`).
- Runs `$RUNNER_TEMP/baha doctor` (line 279), then `$RUNNER_TEMP/baha up --control-plane-only --yes` (line 326) and `$RUNNER_TEMP/baha target create podman-ci ...` (line 325) WITHOUT the test-only operator tag.
- Every managed-environment machine operation here (`control-plane.doctor`, `target.create`, `control-plane.up`) hits the same fail-closed operator-auth seam (`authorization.go:287`). **The SAME auth gap blocks every podman step in this workflow** once operator auth is required for managed environments. The `baha doctor` probe is simply the first step to run.
- Note: `ci-core-rootless-runtime.sh` only does `sudo loginctl enable-linger` (line 8) — no operator login/OIDC. No operator is ever provisioned on this runner.

**B) `pre-release-runtime-suite.yml` (the atomic gated suite) — tagged `baseharbor_ci_operator_testonly`.**
- Builds with `-tags=baseharbor_ci_operator_testonly` (`ci.yml:1145`, `pre-release-runtime-suite.yml:316`, `pre-release.yml:505`).
- `withCIIntegrationOperator` (`cmd/baha/ci_integration_operator_enabled.go:24`) injects `ciIntegrationOperatorContext` — a synthetic verified operator (`operatorauth.WithVerifiedPrincipal`, `ci_integration_operator_enabled.go:601`) scoped EXACTLY to `atomic-<runtime>-<gate>` (`ciIntegrationManagedLocalGateReason`, `ci_integration_operator_enabled.go:105`, env `BASEHARBOR_TARGET=atomic-<runtime>-<gate>`, `GATE`).
- The atomic podman guided/lifecycle/data-capabilities gates run under this tag and so DO NOT hit the unauthenticated boundary: the synthetic operator stamps the exact canonical commands (target create, doctor read-only, app new/edit/footprint show, etc.). The fail-closed OIDC boundary for every other form is preserved (`ci_integration_operator_enabled.go:258` "command-not-in-managed-workload-set").
- Conclusion: the SAME auth gap is NOT a blocker for the atomic suite because that suite carries its own scoped test-only operator. The podman witness that PR #1835 needs therefore lives on the atomic gate path (`pre-release-runtime-suite.yml` dispatch, `runtime=podman`, `gate=guided|lifecycle|data-capabilities`), not on the currently-failing `podman-acceptance.yml`.

Gate-dispatch result / block reason: This lane was diagnostic-only (no dispatch authority). The diagnosis is reproduced from the existing hosted logs (`45611090994`, `45611866489`, `45608237959`) and source trace. The podman witness is obtained by dispatching `pre-release-runtime-suite.yml` (not `podman-acceptance.yml`) with `runtime=podman` and `gate` in {guided, lifecycle, data-capabilities} on the exact head `72fc60a92` — that suite carries the test-only operator and is the path w157's "requested the remaining podman witness" must follow. Docker already MET (`45605189539`, success on `40f72d101`).

## 3) Test-only login/OIDC fixture option table (DECISION = CODEX/OWNER)
The decision to add any test-only `baha login`/OIDC fixture is a consent/auth-boundary change. Per policy it is NOT this lane's write-set and must be decided by CODEX/OWNER. Below are the options with file:line, scope, and consent-neutrality proof.

| Option | file:line | Scope | Consent-neutrality | Decision owner |
| --- | --- | --- | --- | --- |
| (A) Leave as-is; witness on the atomic suite (`pre-release-runtime-suite.yml`) which already carries the scoped synthetic operator | `cmd/baha/ci_integration_operator_enabled.go:24` (`withCIIntegrationOperator`), `:601` (`ciIntegrationOperatorContext`), `:105` (`ciIntegrationManagedLocalGateReason`) | Zero product/CI change; dispatch only on the atomic suite | N/A — no seam touched; fail-closed OIDC boundary (`:258`) intact | w185 can hand off; no CODEX decision if (A) is chosen |
| (B) Add test-only operator bootstrap to `podman-acceptance.yml` (tag the binary + set `DEMO_ATOMIC_GATE=1` for its managed ops) | `.github/workflows/podman-acceptance.yml` (build at `line 272`; `baha doctor` probe `line 279`; `baha up` `line 326`; `baha target create` `line 325`) | Owner-scope `.github/**` + product build tag | Requires the SAME scoped synthetic operator; the atomic suite's admission list (`ci_integration_operator_enabled.go:101-260`) is the template | CODEX/OWNER |
| (C) Provision a real authenticated BaseHarbor operator on the podman CI runner (OIDC config / `baha login` baked into runner image) | `.github/workflows/podman-acceptance.yml` runner env setup; `internal/operatorauth/config.go:89` (managed-env boundary) | External dependency (OIDC issuer) + runner infra | Introduces a real operator secret into CI — highest blast radius | OWNER only (external cert/secret) |
| (D) Make `baha doctor` on a fresh managed environment fail open / warn instead of hard-fail | `cmd/baha/doctor.go:79`, `internal/operatorauth/authorization.go:287` | PRODUCT AUTH/CONSENT BEHAVIOR — must not weaken the managed-environment boundary | FAILS CLOSED by explicit design (`authorization.go:302` "no trusted-local fail-open here"); any change here is a product auth-delta | STOP + escalate (product auth) |

Consent-neutrality proof: the managed-environment operator-auth seam (`authorization.go:287-304`) is an intentional fail-closed boundary with no local-trust arm. Options B/C preserve it; option D weakens it (rejected). Only option A requires no seam change at all and reuses the already-audited scoped test-only operator.

## Podman witness — CORRECT dispatch path (owner correction 2026-11-26)
- WRONG TARGET (void): demo-repo dispatch `45616699580` — demo repo, not core card 0428-287/#1835. EXCLUDED from witness.
- CORRECT path: `workflow_dispatch` on `.github/workflows/pre-release.yml` IN THE CORE REPO `mcpdev80/baseharbor`. Inputs:
  - `ref` = PR head `72fc60a923b7c9b91b803f469c8c5cf3572e0448` (branch `lane-0428-287-installation-reset-recovery` tip).
  - `ONLY_GATES` = `atomic/podman/guided,atomic/podman/lifecycle,atomic/podman/data-capabilities`.
  - `demo_ref` pin if input-required = `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` (read from `origin/develop:docs/releases/v0.4.28.demo-ref`; matched).
  - Precedent working input shape on `72fc60a`: run `45375707285` (read its `.run_started_event` inputs + head).
- If podman jobs fail at `baha doctor` auth again: diagnose ONLY from the hosted job log, prepare the option table for w136 (`file:line` per option: docker operator-login step vs podman job, test-only fixture, documented limitation) — NO product auth/consent edit by this lane.
- Red-first baseline FAIL evidence (card contract): same dispatch path with `ref` = the pre-fix baseline commit on develop (pre-fix SHA), expect the named podman gate to FAIL — precedent demo red baseline `45596347301`.
- Receipt = core dispatch run ID (databaseId).

## What the next (witness) lane must do
- Obtain the remaining PODMAN witness on the atomic gate path: dispatch `pre-release-runtime-suite.yml` with `runtime=podman`, `gate` in {guided, lifecycle, data-capabilities} on exact head `72fc60a92`. The suite's `baseharbor_ci_operator_testonly` operator authorizes its canonical commands; the currently-failing `podman-acceptance.yml` path is the one lacking an operator.
- If develop moves past `2a141387d`, hop first (`git merge origin/develop` + normal push, no force), re-qualify on the new exact head (two same-head full-green IDs), retarget PR #1835.
- Full CI (PR event) terminal green on the final exact head + two same-head full greens, then HANDOFF for Codex review/merge.
- The fixture question in §3 is handed to w136 as a QUESTION — no implementation.

## Fleet refresh (owner directive 2026-11-26 — applies to #1835)
- develop moved to `384d857b5` (post #1843 merge). PR #1835 behind develop.
- PRE-MERGE podman dispatch runs are VOID for acceptance; keep only terminal-useful ones.
- Rebased `lane-0428-287-install-reset-recovery` onto `384d857b5`: identities preserved (w105 fix commits + w157 head-identity commits, %an verified; conflict in `scripts/pr-gate-coverage.json` resolved keeping develop's newer gate policy; catalog re-validated PASS; all 3 card files still map to `data.capabilities` gates). Force-with-lease push delivered: remote + PR #1835 head now `736750fb06e4c9a2cff22479756f6421cfb123a8`.
- CONFLICT WITH LATER HOLD: a subsequent owner sequencing-hold (develop `99d9ddebc`, #1842 refreshes FIRST) says DO NOT rebase #1835 again — a second premature refresh burns CI. The one already-pushed refresh (`736750fb0` on `384d857b5`) stands; NO further rebase/push until owner GO after #1842 merges.

## Sequencing hold (owner directive, develop now `99d9ddebc`)
- #1844 merged (develop `99d9ddebc`), #1842 refreshes FIRST. Hold on #1835 rebase until GO after #1842.
- Current duties on present base = DIAGNOSTIC ONLY: finish podman/auth diagnosis to terminal, record. No new rebased candidate, no further push.

## Red-first baseline (contract, from w157)
- Red baseline: base `55d17d437` -> `ok github.com/mcpdev80/baseharbor/cmd/baha 0.008s [no tests to run]`.
- Green candidate: `TestInstallationResetPreservesSharedForeignProvider (1.38s)` PASS on `72fc60a92`.

## Runs and gate proof
| Run | Head / selection | Terminal result | Disposition |
| --- | --- | --- | --- |
| [45605189539](https://github.com/mcpdev80/baseharbor/actions/runs/45605189539) | `40f72d101`; Docker pair | `success`; `atomic/docker/data-capabilities` green | Docker witness MET |
| [45611090994](https://github.com/mcpdev80/baseharbor/actions/runs/45611090994) | `72fc60a92`; podman | `failure`; `baha doctor` operator-unauthenticated | Diagnosed auth/setup gap (runner lacks provisioned operator) |
| [45611866489](https://github.com/mcpdev80/baseharbor/actions/runs/45611866489) | `72fc60a92`; podman | `failure`; same probe | Diagnosed auth/setup gap (runner lacks provisioned operator) |
| [45608237959](https://github.com/mcpdev80/baseharbor/actions/runs/45608237959) | `2a141387d`; podman | `success`; same probe | Same probe PASSES when runner has an operator — proves code path correct, failure is runner state |

## Cleanliness
One rebased candidate branch pushed (fleet refresh): remote + PR #1835 head `736750fb06e4c9a2cff22479756f6421cfb123a8` on branch `lane-0428-287-install-reset-recovery`. No product write by this lane's rebase (only rebase-resolved shared file), no `.github/**` edit, no runner/runner-infra change, no containers/compose started. No `bh-*` stacks touched. No local containers/networks/volumes created. `docker ps -a` shows no lane-owned stack. HOLD active: no further rebase/push until owner GO after #1842.
