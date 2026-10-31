# t1232: Run Records

## Local Test Runs

### Run 1: Engine tests on o265 (34e60037)
- Command: `go test ./internal/runtime/ -run 'Engine' -v`
- Result: PASS — all 11 engine-related tests pass
- Details: TestDockerEngineSelectionPrecedenceAndNoFallback (11 subcases PASS),
  TestResolveDockerEngineNeverDerivesBinaryFromTestRuntime (3 subcases PASS),
  TestMountedVolumeInventoryUsesEngineAnonymityAndAllConsumers PASS

### Run 2: Engine tests on q1242 (e4464b68)
- Command: `go test ./internal/runtime/ -run 'Engine' -v`
- Result: PASS — same all 11 engine tests pass (cached)
- The q1242 candidate is functionally identical to o265 on engine tests
  (q1242 adds a comment annotation but no behavioral change)

### Run 3: Podman provider tests on o265
- Command: `go test ./internal/providers/runtime/podman/ -v`
- Result: FAIL (pre-existing) — 2 of 45 tests fail due to root-UID fixture
  requirements (TestRetiredQuadletDefinitionCannotReappearAtBootAndKeepsSiblingData,
  TestQuadletRetirementRejectsForeignModifiedOrReplacedOwner/replaced)
- These are unrelated to engine probe — quadlet retirement tests require root
- Podman boundary test (TestPodmanProviderResolvesBehindLookPathPodmanBoundary) PASSES

## CI-Hosted Run Status
- **NOT TRIGGERED** — blocked by STOP condition (1)
- Dependency: #1225 (open) and #1226 (open) not merged
- Cannot push q1242 to origin for CI-hosted run until dependencies are resolved
- Per mission STOP: "Probe braucht public-contracts/CI-Kette (#1226/#1225)
  die noch nicht merged ist -> END_BLOCKED mit Abhängigkeit"

## docker-vs-podman Probe Proof
The engine probe code in `docker_engine.go`:
1. `ResolveDockerEngine(ctx, command)` takes an explicit `command` parameter
2. `dockerEngineOutput(ctx, command, args, env)` runs exactly `exec.CommandContext(ctx, command, args...)`
3. The `command` argument comes from the provider's selected binary — not from `BASEHARBOR_TEST_RUNTIME`
4. Test `TestResolveDockerEngineNeverDerivesBinaryFromTestRuntime` proves:
   - When `BASEHARBOR_TEST_RUNTIME=podman` and the target selects docker:
     - All probe commands use "docker" (not "podman")
     - The docker daemon is resolved on its own socket
   - When `BASEHARBOR_TEST_RUNTIME` is unset:
     - The docker engine probe still uses "docker"
5. The podman boundary test `TestPodmanProviderResolvesBehindLookPathPodmanBoundary`:
   - Proves `LookPath("podman")` resolves to podman binary even when docker exists on PATH
   - Sets `BASEHARBOR_TEST_RUNTIME=docker` but the podman provider never calls `ResolveDockerEngine`
   - Verifies `Descriptor.Kind == ProviderPodman` (not docker)
   - Verifies `Descriptor.Realization != "docker-compose"`

**Conclusion: The engine probe is fail-closed. On a podman runner, docker probes
fail (no false pass-through), which is the correct behavior per mission.**

## Branch Selection Rationale
- o265: based on develop-ancestor 72ba7a99 (PR #1224 merge), NOT on current develop cb6b7387
- q1242: rebased onto origin/develop (cb6b7387), includes both engine probe changes + comment annotation
- q1242 is the more recent/rebased candidate — selected for analysis
- q1242 has not been pushed to origin yet
