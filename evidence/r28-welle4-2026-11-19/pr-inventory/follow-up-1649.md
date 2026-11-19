# PR #1649 follow-up — current develop supersession

Checked 2026-11-19 21:35 UTC. GitHub PR #1649 remained open, non-draft, head `c3840695f4a5551a6474a59781bc130a1c400cf8`, base branch `develop`, attested old base `34c2ede594afc215b1e46eea251a587162224aa0`. Current `origin/develop` was `28fb427f057499efca705c1b7459e7653bd532a8` (includes #1705).

The PR's core claim is to snapshot runtime containers, allow only baseline containers during selective lifecycle assertions, and ensure cleanup preserves pre-existing containers. Current `develop` implements that contract more strictly:

- `cmd/baha/app_backend_selective_runtime_test.go:261-299` stores full runtime-container snapshots; `runtimeContainerBaselineDiff` detects newly created, removed, and changed containers. `TestSelectiveBackendCleanupPreservesRuntimeBaseline` at line 299 covers changed/exited baseline containers as well as created and removed containers.
- Application, HTTPS, and Secrets selective runtime tests snapshot and compare the pre-existing baseline during each phase and cleanup (`cmd/baha/app_application_backend_runtime_test.go:93`, `cmd/baha/app_https_selective_runtime_test.go:54`, `cmd/baha/app_secrets_selective_runtime_test.go:79`).
- The required runtime tests and their native Docker/Podman coreless lifecycle surfaces are already mapped in `scripts/pr-gate-coverage.json` and `scripts/pre-release-runtime-impact.json` on this develop head.

Compared with current develop, the old PR branch removes the full snapshot comparison and state-change check, downgrades the baseline to container IDs only, and removes current ORAS/rootless coverage entries. Its Secrets fixture also expects `coreinstallation.Load(root)` to return `ErrNotExist` after it has explicitly called `seedProviderRuntimeOwner` for that same runtime root. The old head therefore should not be merged over current develop.

The PR's last hosted run `43942855437` failed both Docker and Podman coreless-lifecycle jobs; available run artifacts did not expose a specific assertion. On current develop, the focused Go lifecycle/helper test command passed; those runtime lifecycle tests self-skipped because their acceptance environment variables were not set. `python3 -m unittest scripts.test_pr_gate_coverage scripts.test_pre_release_runtime_reuse` passed all 58 tests. Native Docker and Podman acceptance was not run as part of this local check.

**Disposition:** #1649 was closed on 2026-11-19 21:40 UTC as superseded by stronger current develop content, without merging its stale head: https://github.com/mcpdev80/baseharbor/pull/1649. This does not disposition #1606 or any other PR.
