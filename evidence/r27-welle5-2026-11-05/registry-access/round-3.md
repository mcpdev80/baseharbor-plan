# Round 3 Evidence — registry access (card t-20261018-r27-registry-access, PR #1395)

- Lane: w210-registry-r3 (Worker). Coordinator: 841e7734.
- Date: 2026-11-06.
- Candidate branch: work/r27-registry-access. Base SHA attested below (origin/main develop f01d2fb, ancestor rc=0).
- Scope: review-1395b.md three-point finding; mission w210-registry-r3.txt.

## PLAN

- Step 1: Read mission + review akte; confirm branch HEAD == ls-remote origin (ef0120aa), develop f01d2fb, build baseline. DONE
- Step 2: Ancestry proof develop f01d2fb not ancestor of ef0120aa (rc=1); re-merge latest develop into candidate, ancestor rc=0 after. DONE
- Step 3: Reproduce discriminator gap (review pt 2): mutant removes real production caller (app_broker.go:58 pulls raw tag) => cell stays GREEN. DONE (verified)
- Step 4: Add real caller discriminator cell: drive ensureAndStartRuntimeBroker with mutable dev image, pull digest GREEN; remove real caller body => RED; reverse GREEN. TODO
- Step 5: Scope gate (review pt 3): name-only diff vs develop; new files stay in card write-set (cmd/baha *_test.go); commit name-only. TODO
- Step 6: Local checks: go vet, gofmt, cmd/baha + internal/application + internal/deployment tests green; race-20 on the new cell. TODO
- Step 7: Push one commit onto work/r27-registry-access; launch hosted run; watch to terminal. TODO
- Step 8: Evidence: base ancestor rc=0, name-only, ls-remote==head verbatim, run ID/status; commit akte to origin/main; END. TODO

## Base attestation

- Branch: work/r27-registry-access.
- ls-remote origin work/r27-registry-access: ef0120aa3d738f333dd9bd8fbed385bd1d92fa05 (== mission head ef0120aa).
- ls-remote origin develop: f01d2fbdea6b93af6e06ca6297d04065b6acf701.
- merge-base --is-ancestor f01d2fb ef0120aa BEFORE refresh: rc=1 (NOT ancestor) — reviewer point (1) confirmed.
- After re-merging latest develop, ancestor rc=0 (recorded after step 2 completes).

- After step 2 re-merge: HEAD 4304d828 (Merge branch 'develop' into work/r27-registry-access); merge-base --is-ancestor f01d2fb HEAD: rc=0 (develop IS now ancestor).

## Review point 2 — discriminator gap (verified)

- Existing cell TestPullResolvedRuntimeImagePinsImmutableDigest drives pullResolvedRuntimeImage directly.
- Mutant: real production caller app_broker.go:58 pulls raw mutable tag compose.PullImage(ctx, runtimeImage) instead of pullResolvedRuntimeImage — compiles, cell stays GREEN.
- Conclusion: current cell does not discriminate the real production assembly. Fix = new caller cell.

## Fix: caller-discriminator cell (review point 2)

- New file cmd/baha/app_broker_pull_caller_test.go, cell TestProductionCallerPinsResolvedDigestNotMutableTag.
- Drives the REAL production caller ensureAndStartRuntimeBroker with BASEHARBOR_RUNTIME_IMAGE=ghcr.io/mcpdev80/baseharbor-runtime:edge (mutable dev image). Installs the resolve seam registrySourceExec so resolveRegistrySourceImpl returns digest ghcr.io/mcpdev80/baseharbor-runtime@sha256:aaaa...a.
- Fixture callerPullRecordsCompose records compose.PullImage (single pull) and fails OpenBao readiness after the pull so the caller returns before the workload path.
- Assertion: exactly one pull, and it is the resolved digest identity ghcr.io/...@sha256:aaaa...a.
- Mutant lock (verified):
  - CLEAN caller (pullResolvedRuntimeImage -> resolveRegistrySource -> digest pull): cell GREEN.
  - MUTANT (production caller body replaced with compose.PullImage(ctx, runtimeImage) pulling raw tag): cell RED ("did not drive the artifact resolve invocation").
  - Reverse (clean caller again): cell GREEN.
- Also: existing round-2 cell TestPullResolvedRuntimeImagePinsImmutableDigest stays GREEN on clean caller.
- Set to commit (name-only): cmd/baha/app_broker_pull_caller_test.go only.
- Local: gofmt clean, go vet (cmd/baha + internal/application + internal/deployment) rc=0, race -race on both caller cells ok, internal/application + internal/deployment green.
- Commit 2f073f51 on work/r27-registry-access (child of develop-merge 4304d828); ls-remote origin == 2f073f51; develop f01d2fb ancestor rc=0.

## END

- State: DONE (after step 8). CI run 42152771162 terminal SUCCESS (17 green, 7 skip, 0 red).
