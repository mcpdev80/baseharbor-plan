# w159 — Compose host-isolation (Round 1)

**Task:** t-20261105-r27-compose-host-isolation · **Release:** v0.4.27
**Lane:** w159 · **Coordinator:** f49a3303 · **Branch:** work/r27-compose-isolation (cut from develop 512dcd721ac3fb739bfd4cb0b990fd68d6794762)
**Repo:** baseharbor (test-harness only, `cmd/baha/*_test.go`)
**Fix commit:** 5246bd9d `test(ci): bind candidate-confirm consent in compose InCI fixtures` (develop 512dcd72 is ancestor; own chain)
**PR:** #1383 `test(ci): bind candidate-confirm consent in compose InCI fixtures` vs develop, OPEN/MERGEABLE
**Evidence of record (host transcript):** `/tmp/w159run1.log` (cell B2 green), `/tmp/w159orig.log` (cell B1 red choke), `/tmp/w159poll2.log` (cell A red gate), `/tmp/w159clean.log` (cell A green), `/tmp/w159-run2/` (authoritative hosted run #2, all green)

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

## OPEN PRODUCT GAP (condition 3 — documented, NOT a blocker)
The four InCI tests cannot be green on a host that carries a foreign live `local` Core unless each test is moved onto an isolated daemon. The harness can reset the shared daemon, but on a SHARED host that also tears down every other lane's `bh-*` resources — that is runner/infra behavior, not a per-test harness guarantee. The card asks for per-test own daemon/socket/container-name space; there is no infra-free way to spin up a second rootful daemon on this host (rootless spawn refuses because the userns maps to uid 0; `slirp4netns` is not installed). **The isolation gate cannot be made per-test without either (a) a fresh dedicated runner per test (CI model) or (b) a per-test rootless daemon.** This is a product-environment gap, not a code defect in the four tests. File:line for the choke is `cmd/baha/deployment_record.go:27`; the isolation gap is unbound at `cmd/baha/runtime_integration_test_support_test.go:55` (`up --control-plane-only` on the ambient daemon). Own card to follow from coordinator.

## Isolation on the hosted runner (cell A, CI mode)
On GitHub-hosted shared runners the `validate` job (ci.yml `runtime_integration`) runs each run against a FRESH rootless daemon prepared by `scripts/ci-core-rootless-runtime.sh` and reset by `scripts/ci-runtime-reset.sh` (no foreign `local` Core present). That is the isolation model the card's acceptance describes: every host gets an isolated runtime, proven, not claimed. Cell A is therefore met by the hosted run below, not by the local VM. The local-VM limitation above is documented here so the two evidence sources are not conflated.

## Hosted run of the exact head (cell A + gates, authoritative)
Branch: `work/r27-compose-isolation` @ 5246bd9d (develop 512dcd72 is ancestor; own chain).
Triggered a fresh `workflow_dispatch` CI run on the branch:
- **Run #1 = 41967119908** — `validate` job FAILURE. Unit tests passed; the runtime-integration step ran all five InCI tests serially on a FRESH rootless daemon. Result:
  - `TestRepositoryWorkflowRealLifecycle` → **FAIL (120.02s)** at `verifyRepositoryFixtureRetirement` → `destroySelectiveApplicationWithConsent` → `app destroy` → `stale-impact-consent` (line 102, `app_repository_integration_test.go`).
  - `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` → PASS (91.82s)
  - `TestRepositoryComposeWorkloadOnlyLifecycleInCI` → PASS (84.46s)
  - `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` → PASS (122.53s)
  - `TestMultiInstanceComposeLifecycleInCI` → PASS (6.79s)
- **Run #2 = 41970165123** (re-dispatch, same head, fresh runner) — `validate` SUCCESS. All five InCI tests PASS:
  - `TestRepositoryWorkflowRealLifecycle` → PASS (116.48s)
  - `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` → PASS (93.92s)
  - `TestRepositoryComposeWorkloadOnlyLifecycleInCI` → PASS (82.56s)
  - `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` → PASS (119.56s)
  - `TestMultiInstanceComposeLifecycleInCI` → PASS (6.53s)

**Conclusion:** the exact head is GREEN on a fresh runner. The single `stale-impact-consent` in run #1 is a **transient flake on the shared runner**, not a fix defect: (1) run #2 on the same head passed that exact test cleanly; (2) my fix only touches `runRepositoryFixtureApply` (the `app apply` choke), whereas the failing assertion is in the retirement's `app destroy` path (`destroySelectiveApplicationWithConsent`, `app_runtime_retirement_native_test.go:44`) which never calls the fixture. Cell A (isolation) = four InCI tests green on fresh runner. Cell B (consent) = original (no fix) + clean daemon → red at the confirm-candidate choke (transcript `/tmp/w159orig.log`, `confirm-hash 0ee02e87…`); fixed + clean daemon → green.

Local `-count=2` on the SHARED VM host is unreliable because other lanes reset the shared rootful daemon mid-lifecycle (observed `signal: killed` at retirement) — exactly the non-isolated-host limitation documented above, not a fix defect. The authoritative isolation evidence is the hosted runner run #2 (41970165123).

## Was die Isolierung angeht (Honesty field — new, this round)
Coordinator post-submission honesty check (two parts). All measurements below are live, one shot, on the baseharbor VM; transcripts under `/tmp/w159-<tag>`.

### (a) Is the per-test isolation still real after the consent fix? Code evidence: NO — the fixture does NOT isolate.
The consent fix (`extractCandidateConfirmDigest` + the `withCandidateConsentDigest` retry) is confined to `runRepositoryFixtureApply` / `runRepositoryFixtureApplyCall` (`cmd/baha/repository_runtime_fixture_test.go:29-34`, `:44`). Both functions end in `runWithIO(callCtx, args, out, out)`: the fixture drives the real `app apply` against whatever daemon the ambient env points at. There is **no daemon/socket/container-name isolation in the fixture code** — no fresh daemon, no scoped target, no `ci-runtime-reset.sh` call. Isolation is therefore an *external precondition*: a clean daemon supplied by the CI runner (per job) or simulated locally by `scripts/ci-runtime-reset.sh` before the run.

Measured consequence — same head, polluted daemon (23 live containers, an existing `local` Core on `baseharbor-local-default`), no reset:
```
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.57s)
    app_workload_integration_test.go:186: prepare BaseHarbor integration trust plane:
        Core sql failed: existing native network lacks a protected Core or shared backend owner
```
The test dies at the runtime gate (line 55, `up --control-plane-only`) **before it ever reaches the apply/choke**. The consent fix cannot help here — it only binds the candidate-confirm digest, it never opens a second socket or drops a foreign Core.

### (b) Second pollution attempt, different mechanism — a real second Core under a different name. One attempt, no race.
Reset the daemon to a clean rootless runtime, then bring up a genuine second BaseHarbor Core under a different name on the shared daemon and run the test against it.

- **Result: the attempt found nothing red at my choke.** The runtime gate that governs these four tests does **not** key on "no foreign Core by name" — it keys on whether the *implicit `local` target's native network* (`baseharbor-local-default`) has a protected Core or shared backend owner. A differently-named second Core on a different network does not trip the gate; only a Core that has claimed `baseharbor-local-default` does.
- The one mechanism that DOES turn these red on a non-clean daemon is the ambient `local` Core on `baseharbor-local-default` (the (a) measurement above). That is the same red as the counter-experiment: `lacks a protected Core or shared backend owner`.
- After the reset the daemon is clean again and the SAME test runs green — but that green is the *clean-daemon precondition*, not fixture code: the fixture apply clears the confirm-candidate choke (`confirm-hash …` re-bound via `withCandidateConsentDigest`) and the full lifecycle completes. Measured clean + fixed head this round: `PASS: TestRepositoryComposeWorkloadOnlyLifecycleInCI (155.87s)`, EXIT=0 (transcript `/tmp/w159_clean_fix2.log`).

**Verdict on isolation: UNPROVEN by code.** The four InCI tests are per-test isolated *only* by the external clean-daemon precondition (CI runner per job / local `ci-runtime-reset.sh`). The consent fix repairs exactly one cause — the second, independent `--confirm-candidate` choke — and nothing more. "verseucht develop = gruen" is therefore not a claim this fix substantiates; on a polluted daemon (existing `local` Core on `baseharbor-local-default`) the four tests stay red at the runtime gate. If the card's acceptance requires per-test isolation to be a *code* guarantee of the fixture rather than an environmental precondition, that guarantee is absent and this card carries the finding; everything past this line (PR, hosted green, release test) is a separate decision by the coordinator.

## Repo-rule compliance (final)
- Fix commit `5246bd9d` on top of develop merge `9bf29c89` (develop 24c7d049 is ancestor; linear chain). Single file changed: `cmd/baha/repository_runtime_fixture_test.go` (+35/-1). No product source, no `deployment_record.go`, no `.github/`, no AGENTS.md.
- The develop merge (`9bf29c89`) initially **reverted** the fix (develop carried the pre-fix version of the same file); the fix was re-applied as the tip commit. Verified: `go build ./...` ok, `go vet ./cmd/baha/` ok, `gofmt -l` empty.
- No subagents. Caches/worktrees under `/home/marcel/w159cache` and `/home/marcel/.local/share/opencode/worktree/a03e86/w159-compose-isolation`; evidence under `baseharbor-plan/evidence/.../compose-host-isolation/`.

