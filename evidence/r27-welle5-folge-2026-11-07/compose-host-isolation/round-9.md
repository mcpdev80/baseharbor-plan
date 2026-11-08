# Round 9 evidence — w282 compose-host-isolation native acceptance (card t-20261105-r27-compose-host-isolation)

## Summary

Native ECHT acceptance on `baha-docker` (rootless Docker) for the four InCI repository
lifecycle tests. Authoritative CI gate (`ci.yml:306` / `docker-runtime-acceptance.yml:306`)
runs `-count=1`. This round additionally ran `-count=2` on the polluted (contaminated)
scenario, which is now GREEN for all four tests with clean process exit (rc=0).

Two genuine defects fixed this round (both WIP-committet + pushed):

1. **Line 107 `runtime/compose.yaml` missing** — `app apply` writes the workload-runtime
   compose to the deployment-state `Store.Root` (`.../targets/<iso>/deployments/<id>/state/
   repo-e2e/runtime/compose.yaml`), while the read path (`existingTargetRuntimeFiles` →
   `openBaoRuntime`) resolves the compose at the target-runtime root
   (`.../targets/<iso>/runtime/compose.yaml`). For an isolated Target that has no Core of
   its own, that root never exists. Fix: `cmd/baha/target.go` `targetRuntimeFiles` falls back
   to the registered boot Core (`installationLoans.currentBoot()`) when the isolated Target
   runtime is absent; the boot Core's shared project is derived from the boot root so
   `coreFiles.Project` selects the loaned Core's containers exactly. CI-gated on
   `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`; never a production read path.

2. **Bootstrap-network leak (address-pool exhaustion)** — the bootstrap selector
   (`runtime_integration_test_support_test.go:60`, `w169-ci-bootstrap-`) owns its own
   `<bootstrap>-default`/`-internal` native networks and never removed them; repeated
   `count=N` runs exhausted the bridge address pool
   (`all predefined address pools have been fully subnetted`). Fix: `removeBootstrapNetworks`
   deletes the bootstrap Target's own networks immediately after the trust plane is
   established. Best-effort, never mutates Core material (read from the boot runtime root).

## Cell table (`baha-docker`, lane `0427-110-compose-native-acceptance`)

| Test | Scenario | count | Result | Process |
| --- | --- | --- | --- | --- |
| TestRepositoryWorkflowRealLifecycle | contaminated | 2 | PASS | rc=0, 197s |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | contaminated | 2 | PASS | rc=0, 237s |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | contaminated | 2 | PASS | rc=0, 212s |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | contaminated | 2 | PASS | rc=0, 217s |
| TestRepositoryWorkflowRealLifecycle | clean (no ambient Core) | 1 | PASS | rc=0, ~160-210s |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | contaminated | 1 | PASS | rc=0 |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | contaminated | 1 | PASS | rc=0 |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | contaminated | 1 | PASS | rc=0 |

Transcripts on host: `/tmp/c2-matrix.out` (count=2 contaminated), `/tmp/cont-matrix.out`
(count=1 contaminated).

## Host attestation (provenance)

- Branch under verify: `task/r27-compose-host-isolation-wip`.
- Merge head after `origin/develop` merge (`07ae6c3e9`, #1430 access-wizard):
  `e291fba9a458fd1eef10e820c42598a66c2a5efc` (merge commit).
- Before this round: `210b2dbd4c5d5d06baa5a4c0af30b776623b099e`.
- `origin/develop` HEAD: `07ae6c3e9` (access-wizard #1430).
- Drift OK: `06e4b1eaa` is an ancestor of HEAD; delta vs `origin/develop` = exactly 4
  write-set files (`cmd/baha/target.go`, `cmd/baha/deployment_record.go`,
  `cmd/baha/repository_runtime_fixture_test.go`, `cmd/baha/runtime_integration_test_support_test.go`).
- Build + vet clean after merge.

## Open (handed to owner / blocked)

- **Clean `-count=2` deadlock (finding, not fixed):** on a truly clean host (no ambient Core)
  the apply-confirm path at `recordDeploymentBeforeMutation:551` (`consent==nil`) leaks a
  pipe-holding goroutine so the `go test` process never exits; `-count=2` therefore blocks.
  `-count=1` clean passes `TestRepositoryWorkflowRealLifecycle` cleanly (rc=0). Tests 2–4 clean
  also hit the confirm path. The contaminated scenario resolves the confirm via the ambient
  Core, so `-count=2` is green there. CI runs on fresh runners per test (`-count=1`), which is
  the authoritative gate. This is a product/harness finding for the confirm-retry lifecycle.
- **Podman matrix** (clean + contaminated, count=1): `baha-podman` held by mission
  `0427-116-r5`, not releaseable until after the docker lane releases.
- Final: round evidence consolidated, lane release, END_STOPPED at lane `594fd2f5`.
