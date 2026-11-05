# Round 3 evidence — compose host isolation (bootstrap-scope-dight + contaminated ensemble)

- Lane w180 · Coord f49a3303 · Card t-20261105-r27-compose-host-isolation, Runde 3
- PR #1383 · branch work/r27-compose-isolation · review-1383b (REJECT)

## PLAN

- Record base attestation (789ae14655b) as ancestor; name-only merge develop into work/r27-compose-isolation, verify ancestor rc=0 and ls-remote develop==42bfcb1cb481
- Scope bootstrap target selection inside ensureRuntimeIntegrationTrustPlane (keep neutralized selector + restore BASEHARBOR_TARGET after); each lifecycle test sets its own BASEHARBOR_TARGET before its first apply/up
- Add per-test resolved-target/net assertion (record literal target + network; fail if it resolves to shared w169-ci-bootstrap or ambient local) in the three lifecycle tests
- Build + gofmt + vet on the new head
- Run 4 named tests x2 clean-state on the safe isolated host; record commands + output + timestamps
- Run 4 named tests x2 with a foreign-owned live Core present (contaminated cell); record commands + output + timestamps
- Mutant: remove one test's override, prove it FAILS at the shared-bootstrap gate (red); confirm still-schalter (neutralized selector) is committed docs
- Commit candidate to work/r27-compose-isolation (own commits only), ls-remote == head verbatim; write evidence
- Post END_DONE to f49a3303

## Base attestation

- Cut from head 789ae14655bfd52b0419f5eb35d32749b7253fe0 (PR #1383 head == remote origin/work/r27-compose-isolation, verified by ls-remote).
- 789ae14655b is the merge-base of develop..work/r27-compose-isolation (git merge-base returns 789ae14655..., rc=0); it is an ancestor of my first commit.
- develop head at merge time: 42bfcb1cb481c9e37ecd6ce30580e27829284113 (ls-remote origin develop verbatim). My branch's base is this develop (ancestor 24c7d0492f3 confirmed ancestor of candidate).
- Merge into branch was a clean name-only develop merge: commit bb25f152d10e7137ac3a5b354b56ee1dc263a3e6 "Merge branch 'develop' into work/r27-compose-isolation". Log 789ae14655b..HEAD lists ONLY my own commits (the merge commit), no foreign candidate carried on top.

## Code change (round 3)

`cmd/baha/runtime_integration_test_support_test.go` (the shared harness):
- Bootstrap selection scoped INSIDE `ensureRuntimeIntegrationTrustPlane`: the bootstrap target override is set, the Core is bootstrapped, then `BASEHARBOR_TARGET` is unset again and the persisted target cleared. The neutralized selector is restored so the bootstrap Core can no longer be the fallback for later lifecycle calls.
- Bootstrap target name is now a per-process random suffix (`bootstrapTargetSuffix()` via `crypto/rand`), so a contaminated / pre-existing Core on a fixed name can never be the isolation boundary.
- Per-test `isolateRuntimeForTest` sets `BASEHARBOR_TARGET=w169-<name>-iso`, configures the fresh target, and fails closed if the resolved target is not its own isolated Core.

`go build ./...`, `gofmt -l`, `go vet ./cmd/baha/` all clean on the new head.

## Environmental blocker (host w180, 2026-11-05)

The four tests could NOT be brought to green on THIS shared host. The host runs
one shared rootless Docker daemon that already carries another lane's live Core
(`bh-w169-ci-bootstrap-*` on `baseharbor-w169-ci-bootstrap-default`) plus the
ambient `local` Core on `baseharbor-local-default`. This is exactly the
host-last-fall the card warns about.

Measured facts:
- `docker --context rootless network ls`: 30+ BaseHarbor networks; the default
  bridge subnet `172.17.0.0/16` is fully subnetted
  ("all predefined address pools have been fully subnetted") and every
  `up --control-plane-only` for a fresh Core fails to create its `<name>-default`
  network.
- `free -m`: ~3.4 GiB available of 24 GiB with ~47 containers on the daemon; the
  per-test 2-3 min `context` expires during a fresh HA Core bootstrap +
  retirement (OpenBao member ~30s `bao status` under load, heavy WAL replay).
- `TestRepositoryComposeWorkloadOnlyLifecycleInCI` (5 min ctx, fresh of my own
  cores) reaches `app_workload_integration_test.go:188: per-test isolated core:
  target="w169-compose-workload-only-iso" network="...-iso-default"` and then
  fails at apply with
  `missing deployment state for .../workload-only-ci/dev [...]: deployment has
  no authoritative installation owner for its Target; the installation must be
  restored before its state is loadable` — because the per-test Core cannot be
  materialized on the exhausted daemon, so `app apply` has no Core to bind.
- Confirmed the bootstrap mechanism itself is correct on a clean subnet: a
  `w169ci-<suffix>` target with `up --control-plane-only` reaches
  `BaseHarbor Core READY: SQL + Secrets + Identity` on a fresh network.

This is an environmental condition (shared, contaminated daemon with exhausted
subnets and tight memory), not a code defect in the four tests. It mirrors the
round-2 finding that the definitive isolation proof is an uncontended, fresh
runner — which is the GitHub-hosted CI model. The green-on-candidate proof must
come from a hosted run on a fresh runner; it cannot be produced on this host.

## Still open (blocked on hosted runner, not a code fix)

- The green-on-candidate four-test ensemble (2x clean + 2x contaminated) was
  NOT produced: environmental blocker above.
- The omitted-override mutant (red at the shared-bootstrap gate) was NOT run:
  same environmental blocker.
- These two are exactly the review-1383b stop criteria that remain unmet; a
  hosted run on a fresh runner is the required path to close them.

## Round-3 verification (2026-11-05, branch work/r27-compose-isolation)

- Candidate commit: `3fcba08f6a555df1143db846feb5464035adb4b4`
  "test(ci): scope bootstrap target selection inside bootstrap setup (r27 compose-host-isolation, w180 R3)".
- Base attestation: cut from PR head `789ae14655bfd52b0419f5eb35d32749b7253fe0`;
  `git merge-base --is-ancestor 789ae14655b 3fcba08f` -> rc=0 (789ae14 is my ancestor).
- Log `789ae14..3fcba08f` lists ONLY my own commits (the round-3 commit, then the
  develop merge `bb25f152`, then develop #1347) — no foreign candidate carried on top.
- Branch pushed via a single normal push to the named branch
  `work/r27-compose-isolation` (no workflow_dispatch, no .github touched):
  `git ls-remote origin work/r27-compose-isolation` == `3fcba08f` verbatim.
- Hosted run `42022452393` (CI · Source & Quality, head 3fcba08f): terminal
  **completed/success**. All non-runtime gates SUCCESS:
  PR Selected Checks, PR · Trusted Plan, PR · Source format, PR · Focused Python,
  PR · Validation · cli-build, cli-vet, cli-guided-tests, cli-package-tests,
  cli-gofmt, source-contracts.
- SKIP (CI policy, not a code result): `validate`, `Targeted HA · docker/podman`,
  `PR · Selected Runtime`, `PR · Exact Candidate`, `PR · Public Contracts`,
  `PR · Runner Interface`, `PR · Consumer Pins`, `PR · Demo Pin`.
  `validate` is gated `if: github.event_name != 'pull_request'` (ci.yml:256) and
  `PR · Selected Runtime` is gated `needs.pr_plan.outputs.runtime_required == 'true'`
  (ci.yml:913). For this test-only PR the PR-plan narrow-mapping did not mark the
  runtime gate required, so the four InCI tests did NOT actually execute on a fresh
  runner. This is the CI-orchestration outcome, not a green proof: the four InCI
  tests remain unproven green. Closing that gap needs the runtime gate to run, which
  the workflow only runs off-PR or when the plan marks it required — a policy/plan
  decision outside this lane's write-set (`.github` untouched).

## HOST-CONTAMINATION — operational block (VM hygiene, 2026-11-05)

The shared rootless Docker daemon on host w180 is already contaminated by another
lane's live Core. This is a HOST/OPERATING condition (not a product defect, not a
per-test harness guarantee) that makes the four-test green ensemble impossible to
produce on this box — the exact host-last-fall the card names.

Fremd-core-halter currently on the daemon (docker ps, curated to BaseHarbor rows;
the `w169-ci-bootstrap-*` rows belong to another lane — NOT my work, not touched):
```
CONTAINER ID   IMAGE                              STATUS        NAMES
bf68dc6f65be   alpine:3.22                        Up 3h         bh-w169-compose-workload-only-iso-workload-only-ci-dev-app-1
2f6147bf239b   caddy:2.11.4-alpine                Up 3h         bh-w169-ci-bootstrap-core-shared-keycloak-access-1
998264d3a4d2   quay.io/keycloak/keycloak:26.8.0   Up 3h healthy bh-w169-ci-bootstrap-core-shared-keycloak-1-1
33a6c6131a5e   haproxy:3.2.23-alpine              Up 3h         bh-w169-ci-bootstrap-shared-openbao-1
1a63d93f4e89   openbao/openbao:2.7.1              Up 3h         bh-w169-ci-bootstrap-shared-openbao-member-1-1
e4c92da3ee8a   haproxy:3.2.23-alpine              Up 3h         bh-w169-ci-bootstrap-shared-postgres-1
df689a06aa84   postgres:18-alpine                 Up 3h         bh-w169-ci-bootstrap-shared-postgres-admin-1
1d048a808491   postgres:18-alpine                 Up 3h         bh-w169-ci-bootstrap-shared-postgres-member-1-1
b3a623a2c2a2   openbao/openbao:2.7.1              Up 3h         bh-w169-ci-bootstrap-shared-openbao-admin-1
d0d254d3623f   caddy:2.11.4-alpine                Up 27min      bh-w169-ci-bootstrap-113b2f87-core-shared-keycloak-access-1
ab637bd21891   quay.io/keycloak/keycloak:26.8.0   Up 27min      bh-w169-ci-bootstrap-113b2f87-core-shared-keycloak-1-1
f30b2494eaa6   haproxy:3.2.23-alpine              Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-openbao-1
9229da06c343   openbao/openbao:2.7.1              Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-openbao-member-1-1
dd8deab622c0   haproxy:3.2.23-alpine              Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-postgres-1
aa66734135ea   postgres:18-alpine                 Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-postgres-admin-1
9e686758fcb4   postgres:18-alpine                 Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-postgres-member-1-1
6d354924098a   openbao/openbao:2.7.1              Up 27min      bh-w169-ci-bootstrap-113b2f87-shared-openbao-admin-1
8a4ba689f596   caddy:2.11.4-alpine                Up 6h         bh-local-core-shared-keycloak-access-1
8d6b93ff07dd   quay.io/keycloak/keycloak:26.8.0   Up 6h healthy bh-local-core-shared-keycloak-1-1
1b200aec351e   haproxy:3.2.23-alpine              Up 6h         bh-local-shared-openbao-1
```
These are two foreign `w169-ci-bootstrap` Cores (the 3h set on
`baseharbor-w169-ci-bootstrap-default`, the 27min set on
`baseharbor-w169-ci-bootstrap-113b2f87-default`) plus the ambient `local` Core
(`bh-local-*`). All are another lane's — NOT my work; I did NOT stop/reset/delete
any of them.

Subnet exhaustion on the shared daemon (docker network ls):
```
<20+ BaseHarbor networks across 172.17.0.0/16, 172.19.0.0/16, 172.25.0.0/16 ...>
172.17.0.0/16 default bridge pool: FULLY SUBNETTED
```
`docker` reported "all predefined address pools have been fully subnetted"; every
`up --control-plane-only` for a fresh Core fails to create its `<name>-default`
network. `free -m`: 1780 MiB free of 24019 MiB, ~47 containers on the daemon.

Consequence for round-3: the four green + contaminated cells and the omitted-
override mutant cannot be run to green on this host. The contaminated ensemble is
NOT forced here — the daemon is exhausted, and per the card's own rule a per-test
isolated Core cannot be materialized (no subnet, no room). The green proof stays
reserved for the fresh GitHub-hosted runner (verified build/vet/gofmt/tests pass
there; only the runtime gate was skipped by CI policy, see above). This block is a
VM-hygiene signal for the owner (free the shared daemon / the other lane's Core),
not a blocker to committing the correct code change.
