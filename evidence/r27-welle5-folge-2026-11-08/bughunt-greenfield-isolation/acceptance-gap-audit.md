# 0427-133 – Native Greenfield E2E gap audit (2026-11-08)

## Verified source facts

- Card: `tasks/t-20261108-bughunt-0427-greenfield-isolation.md` remains active. It requires a second isolated target: bootstrap, Core self-install, target activation, status, and proof that no shared-plane object was created/mutated, on BOTH hosted Docker and Podman.
- PR #1460 merged, but its tests check Keycloak-bound issuer resolution with fixture material; they do not prove the whole native path.
- `cmd/baha/target_environment_production_path_test.go` verifies `BASEHARBOR_TARGET` and global override on the production CLI, without starting a Core.
- `cmd/baha/control_plane_single_native_ci_test.go` verifies actual SINGLE topology on an existing package-owned Core; it does not execute `use/activate` on a new independent second target.
- `scripts/ci-native-installation-destroy.sh` runs `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and `TestSecondSameHostCoreNativeConflictInCI`. This is a negative same-engine conflict test, NOT the positive isolated second-Core test.
- `.github/workflows/ci.yml` executes that script on GitHub-hosted Docker (`ubuntu-latest`) and Podman (`ubuntu-26.04`). No new self-hosted runner is required.

## Missing executable acceptance

For each runtime, on the exact PR integration SHA:

1. Provision a fresh, isolated target B with its own native runtime namespace/endpoint. A preexisting A Core must remain owned by A.
2. Run the production CLI's `baha up --control-plane-only --yes` for selected B; assert the new Core belongs to B and reaches READY. A remote Node-Connector target must NOT be substituted: remote bootstrap is currently explicitly unsupported by the safety guard in #1492.
3. Run production `baha use B` and `baha target activate B`, then `baha status --json`. Assert the authoritative identity is B's verified Keycloak issuer and the response names B.
4. Take before/after ownership inventories for A and for all B projects; reject ANY change to A, unknown/foreign resource adoption, or B deployment on A's namespace.
5. Destroy only B in a guaranteed cleanup/teardown path; assert no B resources remain and A is unchanged.
6. Require the named test's exact PASS in the native Docker and Podman jobs. Missing, skipped or failed tests are a failure, not an acceptance.

## Integration constraints and next source change

- Do not use the existing same-host conflict test as a positive witness: it is intentionally fail-closed for a second target on the same native engine.
- Reuse package-level TestMain's durable bootstrap marker and teardown ownership, or a separate process/daemon fixture with equivalent fail-closed cleanup. Do NOT start an unowned second Core on a shared daemon.
- Add one bounded Go native acceptance test in `cmd/baha`; wire it into a hosted-native runner script with exact JSON test-name verification, then inspect the executed jobs on the PR integration SHA.
- `.github/**` is owned by the designated CI owner: coordinate the selector/job addition rather than writing over concurrent CI work.
- **Verdict: NOT ACCEPTED.** The existing green tests cover partial functionality, not the positive native Greenfield lifecycle. Keep 0427-133 active until the two exact native cells PASS.
