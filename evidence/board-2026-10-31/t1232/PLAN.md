# t1232-engine-probe: PLAN

## Task-Vertrag
- Repository: baseharbor (remote mcpdev80/baseharbor)
- PR #1232, base develop
- Branch o265 head: 34e60037
- Rebased q1242 candidate head: e4464b68 (b0310d8f is the actual change commit)
- Develop SHA: cb6b7387

## PLAN Step 0: Reality Check
- `git fetch origin` — executed, origin/develop = cb6b7387
- q1242 is already rebased onto origin/develop (merge-base verified)
- o265 is NOT rebased on develop (based on 72ba7a99 from #1224 merge)
- q1242 is the newer/rebased candidate — selected for analysis

## PLAN Step 1: PR File Verification
- PR #1232 touches exactly 3 files:
  1. `internal/providers/runtime/podman/provider_status_test.go`
  2. `internal/runtime/docker_engine.go`
  3. `internal/runtime/docker_engine_test.go`
- Write-set matches mission scope: .go Test/Engine files only
- No service_binding.go included — scope boundary respected

## PLAN Step 2: Engine Probe Code Review
- `docker_engine.go` adds a comment in `dockerEngineOutput()` explaining the regression guard:
  - Docker production path runs exactly the engine the provider selected (`command`)
  - Never derives the binary from `BASEHARBOR_TEST_RUNTIME`
  - That test-ENV switch belongs to the Podman provider boundary, not the Docker engine probe
- The code change is purely documentary — no behavioral change

## PLAN Step 3: Test Review — docker_engine_test.go
- `TestResolveDockerEngineNeverDerivesBinaryFromTestRuntime`: 3 subcases
  - docker-target with BASEHARBOR_TEST_RUNTIME=podman → probes docker, not podman
  - unset runtime → probes docker
  - docker runtime → probes docker
- All pass locally (verified: PASS)

## PLAN Step 4: Test Review — provider_status_test.go
- `TestPodmanProviderResolvesBehindLookPathPodmanBoundary`:
  - Proves podman LookPath resolves to podman binary even when docker exists on PATH
  - Sets DOCKER_CONTEXT, DOCKER_HOST, BASEHARBOR_TEST_RUNTIME but none reach docker probe path
  - Verifies Descriptor.Kind == ProviderPodman (not docker)
  - All pass locally (verified: PASS — podman test package has pre-existing failures in quadlet retirement tests, but those are unrelated to engine probe)

## PLAN Step 5: STOP Condition Evaluation
- STOP (1): "Probe braucht public-contracts/CI-Kette (#1226/#1225) die noch nicht merged"
  - #1225 open (fix-ci-pr-gate: resolver checks) — NOT merged
  - #1226 open (enforce Receipt Approval for contracts/**) — NOT merged
  - **Result: BLOCKED**
- STOP (2): "nur mit Gate-Schwächung grün" — no gate weakening needed; the engine probe is fail-closed
  - The probe correctly distinguishes docker vs podman engine context
  - On podman runner, fail-closed (no false Docker pass-through) is the correct behavior
- STOP (3): Owner-Stop — no owner stop observed

## PLAN Step 6: Evidence Collection
- Local test results: engine probe tests PASS
- CI-hosted run: BLOCKED by dependency on unmerged #1225/#1226
- Cannot push q1242 to origin — blocked by CI chain dependency

## Final Decision
- **END_BLOCKED** — external dependency #1226/#1225 not merged
- Candidate SHA (q1242): e4464b68
- Candidate SHA (o265): 34e60037
- Blocker: #1225 open, #1226 open — CI chain not ready for engine probe integration

## END Lane
END_BLOCKED: t1232-engine-probe — q1242 candidate SHA e4464b68, blocked by unmerged #1225/#1226
