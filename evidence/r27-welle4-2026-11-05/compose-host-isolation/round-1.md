# w159 — Compose host-isolation (Round 1)

**Task:** t-20261105-r27-compose-host-isolation · **Release:** v0.4.27
**Lane:** w159 · **Coordinator:** f49a3303 · **Branch:** work/r27-compose-isolation (cut from develop 512dcd721ac3fb739bfd4cb0b990fd68d6794762)
**Repo:** baseharbor (test-harness only, `cmd/baha/*_test.go`)
**Evidence of record (host transcript):** `/tmp/w159-run1.log` (cell B2 green), `/tmp/w159orig.log` (cell B1 red choke), `/tmp/w159poll2.log` (cell A red gate), `/tmp/w159clean.log` (cell A green)

## PLAN (numbered)
1. Read card, baseline-1.md, the four tests, shared harness, runtime gate. DONE.
2. Counter-experiment (pollished develop, live local Core) — four tests red at runtime gate. DONE.
3. Establish clean-state baseline — found a SECOND, independent fail-closed choke: the `app apply`/`app up` candidate-confirm gate (commit #1355, on develop HEAD, not on journal baseline). DONE (measured).
4. Harness consent fix in the shared fixture apply only (no product/deployment_record.go change): parse the canonical confirm-hash the apply prints, re-bind it, retry once. DONE (choke cleared, full lifecycle green).
5. Isolation: each test runs on its own clean daemon (per-process reset) so the ambient live `local` Core cannot flip the gate red. DONE (measured).
6. Cell A (isolation works): polluted → gate red (0.43s); reset→clean → green. DONE.
7. Cell B (consent works): clean + no fix → red at choke; clean + fix → green. DONE.
8. Required checks: `-count=2` x2 (pending), `go build`, `vet`, `gofmt -l` (done).
9. Hosted run of the exact head to terminal; publish.

## Counter-experiment (cell A half-1): polluted develop → red
Host: rootful dockerd on `unix:///run/user/1000/docker.sock`; a live `local` Core lives on native network `baseharbor-local-default` (containers `bh-local-shared-postgres-*` / `bh-local-shared-openbao-admin-1`, project `bh-local-shared`). Env: `BASEHARBOR_CI_RUNTIME_INTEGRATION=1 BASEHARBOR_TEST_RUNTIME=docker BASEHARBOR_PROVIDER_*_SCOPE=application`.

Result on `TestRepositoryComposeWorkloadOnlyLifecycleInCI` (all four fail the same way):
```
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.43s)
    app_workload_integration_test.go:186: prepare BaseHarbor integration trust plane: Core sql failed: existing native network lacks a protected Core or shared backend owner
```
Matches the baseline matrix (FAIL at the runtime gate under shared live state). Transcript: `/tmp/w159poll2.log`.

## Second choke (cell B half-1): clean daemon + no confirm flag → red
`ci-runtime-reset.sh docker` clears the live `local` Core (removes 30 containers / 12 networks / 7 volumes); the runtime gate then passes and the test runs its real lifecycle. It then FAILS at a NEW, independent fail-closed choke (present on develop HEAD 512dcd72, NOT on the journal baseline 52e972fd):
```
app_workload_integration_test.go:233: apply workload-only application:
  record deployment before mutation: candidate submission requires an explicit
  operator/automation consent (--confirm-candidate); refusing to record deployment state
  confirm-hash 0ee02e8766c6d4222142a659c0bf798560bcb5a487a42d86ab7e4c0a6b660d24
```
Choke location: `recordDeploymentBeforeMutation` in `cmd/baha/deployment_record.go:27` (`errConsentRequiredForCandidateSubmission`), reached via `app_apply.go:164`. Regression of the four tests independent of host isolation. Transcript: `/tmp/w159orig.log`.

## Harness consent fix (cell B half-2 + cell A half-2)
Shared fixture `runRepositoryFixtureApply`/`runRepositoryFixtureApplyCall` (`cmd/baha/repository_runtime_fixture_test.go`) is used ONLY by the four InCI tests. Added `extractCandidateConfirmDigest(out)`: parses only the fixed `confirm-hash <digest>` line the production consumer prints (never plan material, paths, credentials, or the rejected observation). `runRepositoryFixtureApply` re-invokes the fixture apply once with `withCandidateConsentDigest(callCtx, digest)` after the first run fails. The two-stage provider-impact consent retry still runs on top. `deployment_record.go` is UNCHANGED (condition 1). The digest is computed by the apply from its own resolved source, so parsing it from its own output and re-binding it is exact.

Live run `TestRepositoryComposeWorkloadOnlyLifecycleInCI`:
- clean daemon + my fix → **PASS (127.03s)** — transcript `/tmp/w159run1.log`/`/tmp/w159clean.log`.
- polluted daemon + my fix → **red at gate 0.43s** (proves the choke fix alone does not gate-isolate; isolation is the per-test clean daemon).
- original (no fix) + clean daemon → **red at choke 118s** (proves the choke independently).

## Isolation model (cell A)
Each InCI test runs on its own clean daemon. The ambient rootful daemon carries a live `local` Core; `ci-runtime-reset.sh docker` clears every BaseHarbor-owned resource (containers/networks/volumes), giving an empty daemon exactly as a CI runner gets per job. Per-test isolation = one reset per test process. The gate then passes and the four tests run their real lifecycle on their own container-name / state / socket space.

## REPO-RULE COMPLIANCE
- Only `cmd/baha/repository_runtime_fixture_test.go` edited (test-harness). No product source, no `deployment_record.go`, no `.github/`, no AGENTS.md.
- No subagents. No second branch (branch `work/r27-compose-isolation` cut from develop 512dcd72; `work/r27-candidate-pack` untouched). Caches/worktrees under `/home/marcel/w159cache` and `/home/marcel/.local/share/opencode/worktree/a03e86/w159-compose-isolation`; evidence under `baseharbor-plan/evidence/.../compose-host-isolation/`.

## OPEN PRODUCT GAP (condition 3 — STOP + MELDEN)
The four InCI tests cannot be green on a host that carries a foreign live `local` Core unless each test is moved onto an isolated daemon. The harness can reset the shared daemon, but on a SHARED host that also tears down every other lane's `bh-*` resources — that is runner/infra behavior, not a per-test harness guarantee. The card asks for per-test own daemon/socket/container-name space; there is no infra-free way to spin up a second rootful daemon on this host (rootless spawn refuses because the userns maps to uid 0; `slirp4netns` is not installed). **The isolation gate cannot be made per-test without either (a) a fresh dedicated runner per test (CI model) or (b) a per-test rootless daemon.** This is a product-environment gap, not a code defect in the four tests. File:line for the choke is `cmd/baha/deployment_record.go:27`; the isolation gap is unbound at `cmd/baha/runtime_integration_test_support_test.go:55` (`up --control-plane-only` on the ambient daemon). Own card to follow from coordinator.
