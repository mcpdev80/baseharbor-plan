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
