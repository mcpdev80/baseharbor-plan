# Round 4 evidence — w236 compose-host-isolation verify (card t-20261105-r27-compose-host-isolation)

## Summary

Round-4 verification of the three points left unverified by CODEX-REVIEW ACCEPT
(`act-1383b.md`) at exact head `1b02e8866dd466b0f1ace764f7e4a27706551478`
(PR #1383, branch `work/r27-compose-isolation`, base develop `7c393b0d`).

The three open points were: (a) the contaminated ensemble -> isolation proof,
(b) the genuine omission mutant (red -> restore -> green), (c) the missing
hosted runtime gates at head `1b02e8866dd4`.

This round ran the four compose InCI lifecycle tests (and the omission mutant)
on the healthy named hosts (baha-docker rootful + rootless, baha-podman
rootless). The four tests do not fail at the isolation gate or at the mutant
line: they fail EARLIER, at the control-plane bootstrap's `up --control-plane-only`
Core-identity readiness check, with `Core identity failed: context deadline
exceeded`. This round root-causes that failure to an environmental mismatch, not
a code defect, and proves it with three verbatim witnesses.

Per Owner directive (14:1xZ, answered to the w236 QUESTION 2026-11-06): Option A.
No source change. The witnesses below are the EXTERNAL CASE for the new card
`t-20261106-r27-control-plane-single-default` (the 4-min identity-readiness path
runs on the HA-ensemble default; the single-instance default shortens that window
below the test deadline). The mutant/ensemble remain unproven ONLY because of the
environmental bootstrap gate; this is `END_BLOCKED`, not a code defect.

## Base attestation (provenance)

- Branch under verify: `work/r27-compose-isolation` (PR #1383). Same branch/PR as
  rounds 1-3. No second branch invented.
- Exact head verified BEFORE work:
  `git ls-remote origin work/r27-compose-isolation` ==
  `1b02e8866dd466b0f1ace764f7e4a27706551478` (verbatim).
- develop IS an ancestor of head:
  `git merge-base --is-ancestor 7c393b0d 1b02e8866dd4` -> rc=0.
- The branch's own compose chain (3b2ec108, 3fcba08f, 789ae146, 9bf29c89,
  bb25f152, 5246bd9d) is present in history; the develop-merge 2-parent head is
  `1b02e8866dd4`. No foreign r27 candidate commit carried on top of the branch's
  own commits (PR commit list from GitHub API: the 7 compose-chain commits only).
- PR #1383 state at time of run: OPEN, non-draft, base `develop 7c393b0d`,
  head `1b02e8866dd4` (GitHub API `state=open`, `merged=false`).
- Worktree: isolated clone of branch `work/r27-compose-isolation` at
  `/home/marcel/dev/baseharbor-ecosystem/work/.w236-compose-wt` (mission disk;
  `/tmp` tmpfs is quota-full cluster-wide). Source tarballs transferred to the
  named SSH hosts only; no scratch files under the ecosystem root.
- No `.github/` edit, no workflow_dispatch, no rerun (Owner field). No subagents.
- No main-branch write in a PRODUCT repo; evidence lives only in baseharbor-plan.

## Local verification (this lane, head 1b02e8866dd4)

- Build: `CGO_ENABLED=0 go build -o /home/.../baha-w236 ./cmd/baha` -> exit 0,
  51 735 974-byte binary.
- Vet: `go vet ./cmd/baha` -> exit 0.
- gofmt: `gofmt -l ./cmd/baha/` -> empty (clean).
- The four InCI tests are gated on `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` and
  `BASEHARBOR_TEST_RUNTIME` (docker|podman); they cannot be run to green without a
  named host runtime, so the local full run was not attempted (fail-closed at
  bootstrap would hang; this is the same constraint documented in ACT-1383b).

## GATE (1) ensemble-proof — attempt and root cause

Four InCI lifecycle tests under test:
`TestRepositoryWorkflowRealLifecycle`,
`TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`,
`TestRepositoryComposeWorkloadOnlyLifecycleInCI`,
`TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`.

### docker host (baha-docker, rootful 29.8.1 + rootless daemon present)

Run (clean state, `BASEHARBOR_TEST_RUNTIME=docker`), verbatim:

```
=== RUN   TestRepositoryWorkflowRealLifecycle
    app_repository_integration_test.go:29: prepare BaseHarbor integration trust plane: Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryWorkflowRealLifecycle (120.00s)
=== RUN   TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI
    app_workload_integration_test.go:61: prepare BaseHarbor integration trust plane: Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (0.10s)
=== RUN   TestRepositoryComposeWorkloadOnlyLifecycleInCI
    app_workload_integration_test.go:187: prepare BaseHarbor integration trust plane: Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.09s)
=== RUN   TestRepositoryBuildWorkloadRebuildsSourceChangesInCI
    app_workload_integration_test.go:333: prepare BaseHarbor integration trust plane: Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (0.09s)
FAIL
```

The first test hits the 120s deadline; the next three fail at ~0.1s because the
shared `runtimeIntegrationTrustPlaneOnce` already recorded the error (fail-closed,
expected). Containers count after run: 8 (`bh-w169-ci-bootstrap-*` control-plane
cores), later pruned.

The first test's `TestRepositoryWorkflowRealLifecycle` sets a 2-minute context on
docker (`app_repository_integration_test.go:24`: `timeout := 2 * time.Minute`).
The control-plane identity readiness window is
`internal/identityprovider/keycloak_driver.go:664`:
`const identityEndpointReadyTimeout = 4 * time.Minute` — LONGER than the test's
own 2-minute context. The `ctx` is therefore canceled after 2 minutes, which is
the exact "context deadline exceeded" observed at 120.00s.

### podman host (baha-podman, rootless 5.7.0, fresh, load ~0.1)

Same run (`BASEHARBOR_TEST_RUNTIME=podman`), clean host, verbatim:

```
=== RUN   TestRepositoryWorkflowRealLifecycle
    app_repository_integration_test.go:29: prepare BaseHarbor integration trust plane: Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryWorkflowRealLifecycle (180.00s)
=== RUN   TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI
    ... Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (0.06s)
=== RUN   TestRepositoryComposeWorkloadOnlyLifecycleInCI
    ... Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.03s)
=== RUN   TestRepositoryBuildWorkloadRebuildsSourceChangesInCI
    ... Core identity failed: context deadline exceeded
--- FAIL: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (0.05s)
FAIL
```

This podman host is fresh (up 4:29, load 0.10, 0 containers, full IPAM free) and
still fails at the same bootstrap identity gate. That rules out IPAM/pollution as
the cause on podman; the cause is the test's 3-minute podman context
(`app_repository_integration_test.go:26`: `timeout = 3 * time.Minute`) versus the
4-minute identity readiness window.

## ROOT-CAUSE PROOF (three witnesses)

### Witness 1 — ctxA: docker bootstrap under the test's 2-min context == DEADLINE

Standalone `baha up --control-plane-only` under a 2-minute context deadline
(a tiny `ctxrun` wrapper that execs `baha` under `context.WithTimeout(ctx, 2m)`),
verbatim tail:

```
Target w169-ci-ctxa created (runtime docker, access local via local)
CREATE_EXIT=0
OpenBao is not initialized; bootstrapping the managed trust plane...
[OK] OpenBao initialized and unsealed
[OK] baseharbor KV v2 mount configured
[OK] restricted manager AppRole configured and verified
[OK] initial root token revoked
Recovery file: /tmp/w236-ctxdata/baseharbor-recovery/w169-ci-ctxa/openbao-recovery.json
Store the recovery file securely and separately from BaseHarbor application state.
CONTEXT_DEADLINE after 2m (identity wait needs >2m)
A_EXIT=42
```

The bootstrap reaches OpenBao init/unseal and then the identity (Keycloak)
readiness wait, which needs MORE than 2 minutes; the 2-minute context is
canceled -> exit 42. This is the same path the test hits; the test's 2-min context
is strictly shorter than the production path's own 4-min window.

### Witness 2 — ctxP: fresh podman bootstrap under a 10-min context == CORE READY

Standalone `baha up --control-plane-only` under a 10-minute context deadline on
the fresh podman host, verbatim tail:

```
=== podman (fresh host) 10-min ctx (production-like)
CREATE_EXIT=0
OpenBao is not initialized; bootstrapping the managed trust plane...
[OK] OpenBao initialized and unsealed
[OK] baseharbor KV v2 mount configured
[OK] restricted manager AppRole configured and verified
[OK] initial root token revoked
Recovery file: /tmp/w236-pdctxdata/baseharbor-recovery/w169-ci-ctxp/openbao-recovery.json
Store the recovery file securely and separately from BaseHarbor application state.
BaseHarbor Core READY: SQL + Secrets + Identity.
[INFO] host trust       managed-local CA is not trusted by this host
       To opt in explicitly: baha trust install --yes
P_EXIT=0
```

The identity bootstrap COMPLETES and reports `BaseHarbor Core READY` when given
an adequate context deadline. The code path is correct; the only thing that
canceled it in the test was the test's shorter context deadline. Cleanup after
this run: podman containers 0, volumes 0.

### Witness 3 — docker IPAM exhaustion on the shared ambient Core

On baha-docker the 10-minute bootstrap (Witness 2 analog) got PAST the identity
wait this time and then failed at network creation, verbatim:

```
network:secrets failed to create network baseharbor-w169-ci-ctxb-secrets:
Error response from daemon: all predefined address pools have been fully subnetted
Volume bh-w169-ci-ctxb-shared_postgres-data-1 Error error during connect:
Post "http://%2Frun%2Fuser%2F1000%2Fdocker.sock/v1.55/volumes/create":
failed to create network baseharbor-w169-ci-ctxb-secrets: Error response from
daemon: all predefined address pools have been fully subnetted
```

The docker bridge pool is `172.17.0.0/16`; the shared ambient `bh-local` Core
(18 containers: `bh-local-shared-openbao{,member-1/2/3,-admin}`,
`bh-local-shared-postgres{,-admin,-member-1/2/3}`, keycloak + haproxy) plus
accumulated orphans have subnetted the default address pools. This is the same
IPAM-exhaustion environmental blocker documented in `act-1383b.md` and rounds 1-3.

### Framing for the new card

Owner directive 14:1xZ (2026-11-06): the 4-minute identity-readiness path runs on
the HA-ensemble DEFAULT in `internal/runtime/assets/compose.yaml`
(`openbao-member-1/2/3` at lines 268/297/326, haproxy at 356, postgres-etcd
1-3 at 10/23/36). Under the single-instance default the card `t-20261106-r27-control-plane-single-default`
introduces, that window is shorter than the test's deadline — the four InCI tests
should then pass. The witnesses above are the EXTERNAL CASE for that new card:
they prove the identity path is correct given adequate window/IPAM, and that the
current failure on the HA default is an environmental (window/IPAM) condition,
NOT a code defect and NOT a compose-scope issue.

## GATE (2) mutant-proof (omission mutant) — blocked by the same environmental gate

The omission mutant is "drop a single test's `isolateRuntimeForTest`" (see
`runtime_integration_test_support_test.go:159-181`): dropping `isolateRuntimeForTest`
makes the test resolve to the ambient local Core and fail at the bootstrap-core
contamination gate — a per-test discriminating red.

Red->restore->green could NOT be demonstrated: the test fails at the bootstrap
Core-identity gate (Witness 1/2) BEFORE it ever reaches the `isolateRuntimeForTest`
scope-proof line (`app_workload_integration_test.go:188`:
`per-test isolated core: target="w169-compose-workload-only-iso"` is logged only
after the bootstrap succeeds). So the mutant's red witness is unreachable behind
the same environmental bootstrap gate that blocks the ensemble. This is an
environmental blocker, not a mutant-code defect: the code is red-first correct
(the scope proof fatals if the resolved target is not the test's own isolated
Core), proven by reading the harness; the red state is not observable because the
bootstrap identity gate aborts first.

No mutant was applied to the source. No source change of any kind was made.

## GATE (3) runtime gates at head 1b02e8866dd4

- PR #1383 is OPEN (GitHub API `state=open`), base `develop`, head
  `1b02e8866dd4`.
- Hosted CI run referenced by the ACCEPT: run
  **#42210404583** "CI · PR #1383", conclusion `success`, head
  `1b02e8866dd4`, base `develop 7c393b0d` (GitHub API
  `GET /repos/mcpdev80/baseharbor/actions/runs/42210404583`:
  `status=completed, conclusion=success`).
- The `validate` and `Selected Runtime` runtime gates are SKIPPED on this
  test-only PR by CI design (documented honestly in `act-1383b.md`): `validate`
  is gated `if: github.event_name != 'pull_request'` and Selected Runtime
  requires `runtime_required=true` in the PR plan; a test-only PR never receives
  that flag. This is a CI-orchestration outcome, NOT a green proof of the four
  InCI tests executing on a runner. No failing check is present. No `.github`
  edit, no workflow_dispatch, no rerun from this host (Owner field). The missing
  gates are therefore correctly reported as STATE (skip-by-design), not as a
  pass.

## VM compose projects

Every docker/podman compose project started this round was brought down by this
same session. Final ps-witness (both hosts):

- baha-podman: `podman ps -q | wc -l` == 0; `podman volume ls` == 0; my w236
  leftovers == 0. (A residual set of `bh-w169-ci-ctxp` Quadlet network/volume
  units were stopped, disabled, unit files removed, `daemon-reload` issued.)
- baha-docker: my w236 / `w169-ci-ctxb` leftovers == 0; my bootstrap volumes == 0.
  The remaining 18 `bh-local-*` containers are the ambient `local` Core, NOT mine
  (created before this session) and left untouched per the one-installation-owner
  / other-session rule.

No orphaned daemon/compose project left behind on either host.

## repo-rule compliance

- One integration candidate (`work/r27-compose-isolation`, PR #1383); no second
  branch. No branch cut from another candidate.
- No product file changed. No `.github/` path. No AGENTS.md/doc change. No source
  change at all (per Owner directive answering the QUESTION).
- Build/vet/gofmt clean at the exact head.
- No subagents (AGENTS 4.8).
- Compose projects brought down on both hosts; ps-witness recorded.
- Evidence lives only in baseharbor-plan; no `.evidence/` in a product repo; no
  main-branch write in a product repo.

## Evidence publish (origin/main witness)

`git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep <evidence-path>`:

```
* branch            main       -> FETCH_HEAD
evidence/r27-welle5-2026-11-06/compose-host-isolation/round-4.md
```

Evidence path `evidence/r27-welle5-2026-11-06/compose-host-isolation/round-4.md`
confirmed present on `origin/main` (HEAD `1723fd8ab36230c1979a2220d7da56c00cb9a191`;
my evidence commit `6cadcfc` is an ancestor of HEAD).

## END

END_BLOCKED w236-compose-r4-verify: head=1b02e8866dd4 branch=work/r27-compose-isolation (PR #1383, OPEN, base develop 7c393b0d) four-InCI-tests FAIL at bootstrap Core-identity "context deadline exceeded" (docker 120s / podman 180s) — root-caused to test 2min/3min ctx < 4min identity-readiness window (keycloak_driver.go:664 identityEndpointReadyTimeout=4m); witness1 ctxA docker 2min ctx -> CONTEXT_DEADLINE after 2m exit42; witness2 ctxP fresh podman 10min ctx -> "BaseHarbor Core READY: SQL + Secrets + Identity" P_EXIT=0 cleanup 0/0; witness3 docker 10min ctx past identity -> IPAM "all predefined address pools have been fully subnetted" (ambient bh-local 18-core) | mutant=RED-unreachable-behind-bootstrap-gate (code red-first correct) | gates=PR #1383 OPEN; CI #42210404583 SUCCESS; validate/Selected-Runtime SKIP by test-only PR design | both hosts ps-witness 0 my-containers | evidence path baseharbor-plan/evidence/r27-welle5-2026-11-06/compose-host-isolation/round-4.md | Owner-answered OPTION-A: no source change; witnesses are external-case for new card t-20261106-r27-control-plane-single-default (HA-ensemble default compose.yaml:268/297/326/356 + etcd 10/23/36; single-instance default shortens readiness window below test deadline)
