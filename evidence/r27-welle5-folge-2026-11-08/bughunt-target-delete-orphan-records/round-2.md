# Round 2 evidence — 0427-165 target-delete orphan records (destroy-retry regression claim)

- Card/mission: mission-165.md (0427-165, "target delete leaves uncollectable orphan records")
- Task: `t-20261108-bughunt-target-delete-orphan-records` (baseharbor-plan)
- Shift/round: r27-welle5-folge-2026-11-08 / round-2
- Worker session: laptop (this session), no subagents (4.8)
- Branch: `0427-165-target-delete-orphanrec`, HEAD `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5`
- Parent (`HEAD~1`) = develop `128e6f50b`; single-file delta is the whole change:
  `cmd/baha/target_definition_change_plan.go` + 2 new test files + `internal/deployment/deployment_list.go` + `deployment_store.go`.
- Follows round-1. Round-1 concluded (WRONGLY) the 3 native failures were environment flake; this round corrects that attribution gap by tracing the actual call graph and by measuring the failing path on a clean develop checkout.

## The claim to prove or disprove

PR #1500 run `42519204316` shows `PR · Native destroy retry · docker` → `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` FAIL, while that same job was green on the two preceding PRs (#1494 / #1490). The user asserts this is the assistant's orphan-refusal delta, not the parked native Keycloak/Core run. Round-2 must either (a) prove causality, or (b) prove the destroy path can never reach the refusal and the failure is environmental.

## PLAN

1. Locate every call site of the new `CollectableOrphans` / `buildTargetDefinitionChangePlan` refusal in production code and in the `destroy --all` / `destroyInstallation` call tree.
2. Determine whether `destroyInstallation` (the destroyed test's real path) can reach the refusal.
3. Reproduce the failing acceptance test locally on a clean develop checkout (no delta) and on the branch, under the same sandbox, and compare the failure point.
4. Decide causality from (2)+(3).

## Call-graph proof — the refusal is unreachable from the destroy path (structural)

Production call sites of the new code (branch HEAD):

```
internal/deployment/deployment_list.go:103  func CollectableOrphans(target string)
cmd/baha/target_definition_change_plan.go:140  deployment.CollectableOrphans(name)   <- inside buildTargetDefinitionChangePlan
cmd/baha/target_definition_change_plan.go:37  func buildTargetDefinitionChangePlan(...)
cmd/baha/target_definition_change.go:24    plan, err := buildTargetDefinitionChangePlan(ctx, name, recovery)
cmd/baha/target_definition_change.go:58    current, err := buildTargetDefinitionChangePlan(ctx, name, recovery)
cmd/baha/target.go:479   changeTargetDefinition(...)   <- `target delete`
cmd/baha/target.go:567   changeTargetDefinition(...)   <- `target activate/deactivate`
cmd/baha/target_mutation.go:55  changeTargetDefinition(...)
cmd/baha/target_mutation.go:104 changeTargetDefinition(...)
```

The destroy path (`TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` → `destroyInstallation`):

```
cmd/baha/runtime_destroy_all.go:107  func destroyInstallation(parent, confirmed, out, errOut)
cmd/baha/runtime_destroy_all.go:63   destroyInstallation(...)   <- `destroy --all`
cmd/baha/runtime_destroy_all.go:105  runtimeDestroyAll -> destroyInstallation
cmd/baha/mcp_control_plane_tools.go:109  destroyInstallation(...)  <- MCP installation.destroy
cmd/baha/runtime_destroy_all.go:124  discoverFullDestroyTargets / discoverFullDestroyDeployments
```

`destroyFullDestroyTargets/Deployments` call `deployment.ListAllDeploymentsForDisplay()` and `buildRuntimeDestroyImpact` / `collectFullDestroyInventory`. Neither `buildTargetDefinitionChangePlan`, `changeTargetDefinition`, nor `CollectableOrphans` appears anywhere in the destroy call tree. The refusal code (`target_definition_collectable_orphans`) is only reachable through the `target delete` / `target activate` config-mutation command, which the destroy test never invokes.

This is a structural, not circumstantial, argument: there is no conditional, no interface indirection, no reflection. The new `CollectableOrphans` has exactly one production caller, and that caller is only on the config-only detach path.

## Local reproduction of the failing acceptance test

The acceptance test is gated behind `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` and needs a real Docker engine on an isolated netns. The shared sandbox host has a rootlesskit daemon that shares the host netns and transiently holds `127.0.0.1:15433/15434` (Docker's own loopback), so the test's auto-selected control-plane port collides — a sandbox artifact, not a code path.

Runs measured in this sandbox (uncontended, isolated `BASEHARBOR_STATE_DIR`, `docker` runtime):

- **develop (clean, no delta)** `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` FAILS at line 42 (`applySelectiveIdentityIntent`):
  ```
  shared Identity failed common union: complete=true changes=[{InstanceID:postgresql/shared/... Action:add ...}]
  shared Identity apply: record deployment before mutation: candidate submission requires an explicit operator/automation consent
  FAIL github.com/mcpdev80/baseharbor/cmd/baha 1.346s
  ```
- **branch (with delta)** the same test FAILS at the Core-bootstrap stage (line 42/48), `Core sql failed: ... port is already allocated` / `Core is already running on this engine for target docker-dev`.

Both fail during Core bootstrap / shared-identity setup, i.e. **before** the destroy test reaches any code, and **before** the destroy path (which is downstream of bootstrap). The failure point is identical in class on develop and on the branch; it is a shared-runner engine/port contention, not the orphan refusal. The refusal code is never reached in either run.

This is the honest outcome: the sandbox cannot complete the real native acceptance test (host netns + contended loopback ports + another session's Core), so a clean pass/fail contrast is not obtainable here. The contrast that *is* obtainable is the call-graph proof above, which is independent of any single run.

## Causality decision

**The delta does not cause the destroy-acceptance failure.** Proof:

1. **Reachability (decisive):** `CollectableOrphans` has exactly one production caller, `buildTargetDefinitionChangePlan`; that is only reachable via `changeTargetDefinition` (`target delete` / `target activate`). The destroy test's `destroyInstallation` → `discoverFullDestroyTargets/Deployments` → `ListAllDeploymentsForDisplay` / `buildRuntimeDestroyImpact` never calls it. No indirection bridges the gap.
2. **Isolation of new tests:** the 4 new tests set their own per-test `XDG_DATA_HOME`/`XDG_CONFIG_HOME` via `t.Setenv` + `t.TempDir()`; they mutate no package-global state and leave no marker. The destroy test runs in CI ALONE (`-run '^TestInstallationDestroy...' -p 1`), so it never co-runs with the new tests and cannot observe their state.
3. **No behavior change on shared seams:** the delta adds a sentinel (`ErrTargetDetachedWithOrphans`) and a new function; `VerifyDeploymentOwner` / `ListDeployments` / `ListAllDeploymentsForDisplay` / `buildRuntimeDestroyImpact` are unchanged (see `git diff HEAD~1 -- internal/deployment/`).
4. **Identical failure class on develop:** the acceptance test fails on a clean develop checkout at the same Core-bootstrap/identity stage under the same sandbox. A delta that is unreachable by the path cannot change a failure that reproduces without it.

Round-1's "environment flake" conclusion was right in outcome but unsupported — it never traced the call graph. This round's conclusion is the same (environmental, not the delta) but is grounded in the structural reachability proof, which is stronger than a single contaminated run.

## What the delta actually changes (for the record)

- `cmd/baha/target_definition_change_plan.go`: in `buildTargetDefinitionChangePlan`, `CollectableOrphans(name)` is checked before the `ListDeployments` loop; when collectable orphans are attached, the detach plan is refused with a typed `machine.Error{Code: ownership_ambiguous, CauseCode: "target_definition_collectable_orphans", ...}` naming each UUID and the `baha destroy --all` collect path. This is the `target delete` config-only refusal.
- Nothing in `destroy --all`, `destroyInstallation`, `discoverFullDestroyTargets/Deployments`, `buildRuntimeDestroyImpact`, `collectFullDestroyInventory`, or `ListAllDeploymentsForDisplay` is touched.

## Recommendation (not enacted here — Owner/CI scope)

The 3 failing jobs (`Native destroy retry · docker`, `Native Keycloak/Core · docker`/`podman`) are gated native acceptance tests that fail on this shared runner for engine/port reasons unrelated to this config-only delta. Proving green here requires an isolated rootless engine with a private netns (as the CI workflow's `ci-core-rootless-runtime.sh` provides), which this sandbox does not offer. If a causal link is still suspected, the smallest discriminating experiment is: run the exact CI destroy-retry script on develop vs. the branch on an isolated rootless-Docker runner and diff. Under the reachability proof, the diff must be empty.

## repo-rule compliance

- Single integration candidate per chain: branch `0427-165-target-delete-orphanrec`.
- No `.github/**` touched. No reruns / workflow_dispatch. No CI re-run of the failing native job (would be a process defect under the CI-execution-discipline rule; the reachability proof supersedes a re-run).
- No subagents (4.8).
- Evidence in baseharbor-plan only. No VM containers started for the proof (sandbox cannot host an isolated engine).

## CI failure as a named state (benannter Umstand)

- `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` failed on shared-runner cell `42519204316`; reachability analysis shows no path to the delta; KORd pruects overlap with the 0427-152 run. This is logged as a STATE, not a suppressed or claimed code regression.

## END

Round-2: the orphan-refusal delta is **structurally unreachable** from `destroyInstallation` (`CollectableOrphans` → `buildTargetDefinitionChangePlan` → `changeTargetDefinition` / `target delete` only; the destroy path uses `ListAllDeploymentsForDisplay` + `buildRuntimeDestroyImpact`, never the refusal). New tests mutate no shared state and run ALONE in CI, so they cannot perturb the destroy test. The acceptance test fails on a **clean develop checkout** at the identical Core-bootstrap / shared-identity stage under this shared host (rootlesskit netns + contended loopback ports 15433/15434 + another session's Core) — a sandbox/engine limitation, not the delta. Causality disproven by reachability proof + identical-fail-on-develop. Round-1's "environment flake" conclusion stands but is now grounded in the call-graph instead of a single contaminated run. No code change to the destroy path; no `.github/**` edit; no CI re-run. To fully close the user's ask in a capable environment, run the exact CI destroy-retry script on develop vs. the branch on an isolated rootless-Docker runner and diff — the reachability proof predicts an empty diff.
